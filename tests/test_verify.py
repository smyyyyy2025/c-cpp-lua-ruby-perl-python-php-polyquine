"""Regression tests for the checks that protect byte-exact quines."""
from pathlib import Path
import io
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verify
import sync


class SourceChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = b"a\nb\nc\n" + b"x" * 409
        for name in verify.MAIN_FILES + verify.VARIANT_FILES:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(self.source)

    def test_valid_structure(self):
        sources, errors = verify.check_sources(self.root)
        self.assertEqual(len(sources), 10)
        self.assertEqual(errors, [])

    def test_crlf_is_rejected(self):
        errors = verify.format_errors("source", self.source.replace(b"\n", b"\r\n"))
        self.assertTrue(any("CR/CRLF" in error for error in errors))

    def test_trailing_newline_is_rejected(self):
        errors = verify.format_errors("source", self.source + b"\n")
        self.assertTrue(any("no trailing newline" in error for error in errors))

    def test_wrong_size_is_rejected(self):
        self.assertTrue(any("expected 415 bytes" in error
                            for error in verify.format_errors("source", self.source[:-1])))

    def test_non_ascii_is_rejected(self):
        self.assertTrue(any("ASCII" in error
                            for error in verify.format_errors("source", b"\xff" + self.source[1:])))

    def test_alias_and_variant_zero_must_match_main(self):
        for name in ("polyquine.py", "variants/quine_415_0.c"):
            with self.subTest(name=name):
                (self.root / name).write_bytes(b"z" + self.source[1:])
                _, errors = verify.check_sources(self.root)
                self.assertTrue(any(name + ": differs" in error for error in errors))
                (self.root / name).write_bytes(self.source)

    def test_missing_or_extra_variants_are_rejected(self):
        (self.root / "variants/quine_415_3.c").unlink()
        (self.root / "variants/unexpected.c").write_bytes(self.source)
        _, errors = verify.check_sources(self.root)
        self.assertTrue(any("expected exactly" in error for error in errors))
        self.assertTrue(any("variants/quine_415_3.c:" in error for error in errors))

    def test_sync_restores_copies_without_adding_newline(self):
        (self.root / "polyquine.lua").write_bytes(b"broken\n")
        with mock.patch.object(sync, "ROOT", self.root), mock.patch.object(sys, "stdout", io.StringIO()):
            self.assertEqual(sync.main(), 0)
        for name in verify.MAIN_FILES:
            self.assertEqual((self.root / name).read_bytes(), self.source)

    def test_sync_rejects_invalid_source_before_writing(self):
        (self.root / verify.VARIANT_FILES[0]).write_bytes(self.source + b"\n")
        (self.root / "polyquine.c").write_bytes(b"preserve this")
        with mock.patch.object(sync, "ROOT", self.root), mock.patch.object(sys, "stderr", io.StringIO()):
            self.assertEqual(sync.main(), 1)
        self.assertEqual((self.root / "polyquine.c").read_bytes(), b"preserve this")


class ProcessChecks(unittest.TestCase):
    def test_exact_output_passes(self):
        command = [sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'abc')"]
        self.assertIsNone(verify.check_output(command, b"abc"))

    def test_nonzero_exit_fails_even_when_output_matches(self):
        command = [sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'abc'); sys.exit(7)"]
        self.assertIn("exit 7", verify.check_output(command, b"abc"))

    def test_output_is_not_newline_normalized(self):
        command = [sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'a\\r\\nb')"]
        self.assertIn("differs at byte 1", verify.check_output(command, b"a\nb"))

    def test_extra_trailing_byte_fails(self):
        command = [sys.executable, "-c", "print('abc')"]
        self.assertIn("differs at byte 3", verify.check_output(command, b"abc"))

    def test_timeout_and_missing_executable_fail(self):
        for exception in (subprocess.TimeoutExpired(["tool"], 20), FileNotFoundError("tool")):
            with self.subTest(exception=type(exception).__name__):
                with mock.patch.object(verify.subprocess, "run", side_effect=exception):
                    self.assertIsNotNone(verify.check_output(["tool"], b""))


if __name__ == "__main__":
    unittest.main()
