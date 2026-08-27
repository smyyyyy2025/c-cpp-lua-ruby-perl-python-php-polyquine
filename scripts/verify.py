#!/usr/bin/env python3
"""Verify source formatting, synchronized copies, and exact quine output."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BYTES = 415
MAIN_FILES = tuple("polyquine." + ext for ext in ("c", "lua", "php", "pl", "py", "rb"))
VARIANT_FILES = tuple("variants/quine_415_%d.c" % i for i in range(4))
ALIASES = {"Lua": "lua", "PHP": "php", "Perl": "pl", "Python": "py", "Ruby": "rb"}


def format_errors(label, source):
    errors = []
    if len(source) != SOURCE_BYTES:
        errors.append("%s: expected %d bytes, got %d" % (label, SOURCE_BYTES, len(source)))
    if not source.isascii():
        errors.append("%s: source must be ASCII" % label)
    if b"\r" in source:
        errors.append("%s: CR/CRLF found; use LF only" % label)
    if source.count(b"\n") != 3 or source.endswith(b"\n"):
        errors.append("%s: expected four lines with no trailing newline" % label)
    return errors


def check_sources(root):
    sources, errors = {}, []
    for name in MAIN_FILES + VARIANT_FILES:
        try:
            sources[name] = (root / name).read_bytes()
        except OSError as exc:
            errors.append("%s: %s" % (name, exc))
            continue
        errors.extend(format_errors(name, sources[name]))
    actual = {p.relative_to(root).as_posix() for p in (root / "variants").glob("*.c")}
    if actual != set(VARIANT_FILES):
        errors.append("variants/: expected exactly quine_415_0.c through quine_415_3.c")
    if "polyquine.c" in sources:
        for name in MAIN_FILES[1:] + (VARIANT_FILES[0],):
            if name in sources and sources[name] != sources["polyquine.c"]:
                errors.append("%s: differs from polyquine.c; run scripts/sync.py" % name)
    return sources, errors


def run_command(command, timeout=20):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return b"", str(exc)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        return result.stdout, "exit %d%s" % (result.returncode, ": " + detail if detail else "")
    return result.stdout, None


def check_output(command, expected):
    stdout, error = run_command(command)
    if error:
        return error
    if stdout == expected:
        return None
    offset = next((i for i, (a, b) in enumerate(zip(expected, stdout)) if a != b),
                  min(len(expected), len(stdout)))
    return "output differs at byte %d (source=%d bytes, stdout=%d bytes)" % (
        offset, len(expected), len(stdout))


def toolchains():
    requested = {
        "C": ("CC", "gcc", ["--version"]),
        "C++": ("CXX", "g++", ["--version"]),
        "Python": ("PYTHON", sys.executable, ["--version"]),
        "Lua": ("LUA", "lua", ["-v"]),
        "Ruby": ("RUBY", "ruby", ["--version"]),
        "Perl": ("PERL", "perl", ["-e", 'print "$^V\n"']),
        "PHP": ("PHP", "php", ["--version"]),
    }
    found, errors = {}, []
    for language, (variable, default, flags) in requested.items():
        executable = os.environ.get(variable, default)
        path = shutil.which(executable)
        if not path:
            errors.append("%s: missing executable %r (override with %s)" % (language, executable, variable))
            continue
        found[language] = path
        try:
            version = subprocess.run([path] + flags, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, timeout=10, check=True)
        except (OSError, subprocess.SubprocessError) as exc:
            errors.append("%s: version check failed: %s" % (language, exc))
            continue
        lines = version.stdout.decode("utf-8", errors="replace").splitlines()
        print("%s: %s" % (language, lines[0] if lines else path))
    return found, errors


def main():
    sources, errors = check_sources(ROOT)
    if errors:
        print("\n".join("FAIL " + error for error in errors), file=sys.stderr)
        return 1
    print("Source checks: 10 files, 415 bytes / 4 lines / LF / no trailing newline.")
    print("All six main files and variant 0 are byte-for-byte identical.")
    tools, errors = toolchains()
    if errors:
        print("\n".join("FAIL " + error for error in errors), file=sys.stderr)
        return 1
    jobs = [(name, language) for name in ("polyquine.c",) + VARIANT_FILES for language in tools]
    jobs += [("polyquine." + ext, language) for language, ext in ALIASES.items()]
    passed = 0
    with tempfile.TemporaryDirectory(prefix="polyquine-") as directory:
        for index, (name, language) in enumerate(jobs):
            source_path = str(ROOT / name)
            error = None
            if language in ("C", "C++"):
                executable = str(Path(directory) / ("quine_%d" % index))
                standard = "-std=c99" if language == "C" else "-std=c++11"
                command = [tools[language], standard]
                if language == "C++":
                    command.append("-w")  # Same permissive GCC mode documented in README.
                _, error = run_command(command + [source_path, "-o", executable])
                command = [executable]
            else:
                command = [tools[language], source_path]
            if error is None:
                error = check_output(command, sources[name])
            if error:
                errors.append("%s / %s: %s" % (name, language, error))
                print("FAIL %s / %s: %s" % (name, language, error))
            else:
                passed += 1
                print("PASS %s / %s" % (name, language))
    print("%d/%d passed; exit codes and raw output bytes checked." % (passed, len(jobs)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
