# c-cpp-lua-ruby-perl-python-php-polyquine

[![Verify quines](https://github.com/smyyyyy2025/c-cpp-lua-ruby-perl-python-php-polyquine/actions/workflows/verify.yml/badge.svg)](https://github.com/smyyyyy2025/c-cpp-lua-ruby-perl-python-php-polyquine/actions/workflows/verify.yml)

A **415-byte, 4-line** polyglot quine for **C, C++, Lua, Ruby, Perl, Python, and PHP**.

The same source prints itself byte-for-byte in every listed language. PHP is a
trivial case: without a `<?php` opening tag, it outputs the source verbatim.

The main version is **54 bytes shorter** than the previous 469-byte, 5-line
version. The [469-byte source](https://github.com/smyyyyy2025/c-cpp-lua-ruby-perl-python-php-polyquine/blob/4f2443db89f25d0b2b18b979cb6142b8e133afb6/polyquine.c)
remains available in Git history.

## Files and variants

The six root files (`polyquine.c`, `.lua`, `.php`, `.pl`, `.py`, and `.rb`)
are byte-for-byte identical to [variant 0](variants/quine_415_0.c).
C and C++ both compile `polyquine.c`; a separate C++ copy is unnecessary.

All four variants are **415 bytes and 4 lines**:

| File | Difference |
| :--- | :--- |
| [quine_415_0.c](variants/quine_415_0.c) | Main version. The initial comment precedes the macro; the final `printf` macro invocation generates the whole `main` function. |
| [quine_415_1.c](variants/quine_415_1.c) | Moves the macro definition before the opening block comment. |
| [quine_415_2.c](variants/quine_415_2.c) | Opens `main` explicitly before the local `char*` declaration; the macro emits the print call and closing brace. |
| [quine_415_3.c](variants/quine_415_3.c) | Uses an alternative quote/comment arrangement on the shared third line. |

The size reduction uses `__builtin_printf` instead of a header and ordinary
`printf`, a shorter Perl helper, and Lua's `load` instead of an explicit
function wrapper. The four alternatives have the same verified behavior; their
numbering does not rank compatibility.

## Tested environments

The following versions were verified locally on Ubuntu 22.04 under WSL.
These are **tested versions, not minimum-version claims**.

| Language | Compiler / interpreter | Mode |
| :--- | :--- | :--- |
| C | GCC 11.4.0 | `-std=c99` |
| C++ | G++ 11.4.0 | `-std=c++11` |
| Python | 3.10.12 | `python3` |
| Lua | 5.3.6 | `lua` |
| Ruby | 3.0.2 | `ruby` |
| Perl | 5.34.0 | `perl` |
| PHP | 8.1.2 | `php` CLI |

CI also runs on Ubuntu 22.04 and 24.04 and prints the actual tool versions
in each run. Verification targets Linux/WSL; native Windows runtimes may
translate output newlines.

C and C++ depend on GCC-style named variadic macros (`_...`) and
`__builtin_printf`. The selected standard modes do **not** imply strict ISO
portability. G++ accepts the string-literal-to-`char*` conversion with a
warning in the tested configuration. Strict or warnings-as-errors builds
are not claimed to work. `-w` in the commands below suppresses warnings.

## Run

Run these commands from the repository root on Linux or WSL:

```bash
gcc -std=c99 polyquine.c -o polyquine && ./polyquine
g++ -std=c++11 -w polyquine.c -o polyquine && ./polyquine
python3 polyquine.c
lua polyquine.c
ruby polyquine.c
perl polyquine.c
php polyquine.c
```

A corresponding extension may be used for the interpreters, for example
`python3 polyquine.py` or `lua polyquine.lua`.

On Ubuntu, install the tools with:

```bash
sudo apt-get update
sudo apt-get install -y gcc g++ python3 lua5.3 ruby perl php-cli
```

## Verify

```bash
python3 -m unittest discover -s tests -v
LUA=lua5.3 python3 scripts/verify.py
```

The verifier uses only Python's standard library. It checks:

- All ten source files are 415-byte ASCII, with three LF separators and no
  trailing newline.
- The six root copies and variant 0 are identical.
- The main source and all four variants each work in seven languages
  (35 checks), plus five extension-specific interpreter checks.
- Every compile and execution exits successfully, and every runtime's raw
  stdout matches its source bytes exactly. No whitespace or newline
  normalization is applied.

A missing tool, timeout, compilation failure, nonzero exit code, or byte
mismatch makes verification fail. Compiled executables are kept in a temporary
directory and cleaned up afterward.

If necessary, override individual executable paths with `CC`, `CXX`,
`PYTHON`, `LUA`, `RUBY`, `PERL`, or `PHP`. Each value must name a single
executable, without extra shell arguments.

The [GitHub Actions workflow](.github/workflows/verify.yml) runs the regression
tests and all **40** execution checks on both Ubuntu versions for pushes to
`main`, pull requests, and manual runs.

## Editing and synchronization

Edit [variants/quine_415_0.c](variants/quine_415_0.c) to change the main version,
then synchronize the six root copies:

```bash
python3 scripts/sync.py
LUA=lua5.3 python3 scripts/verify.py
```

Other variants remain independent. The sync helper validates the source format
before writing and copies bytes without adding a newline.

Keep **LF line endings and no final newline** in every quine source.
`.gitattributes` enforces LF checkout, and `.editorconfig` disables automatic
final-newline insertion for these files. Avoid formatters on the quines;
CI checks the exact byte count and output.

## License

[MIT](LICENSE).
