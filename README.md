# c-cpp-lua-ruby-perl-python-php-polyquine

A **469-byte, 5-line** polyglot quine that prints its own source code, valid in:

- C
- C++
- Lua
- Ruby
- Perl
- Python
- PHP (trivial: outputs source verbatim without `<?php`)

## Requirements

| Language | Minimum Version | Tested Version |
| :--- | :--- | :--- |
| C (gcc) | C99 | 11.4.0 |
| C++ (g++) | C++11 | 11.4.0 |
| Python | 3.0 | 3.13.11 |
| Lua | 5.2 | 5.3.6 |
| Ruby | 2.0 | 3.0.2 |
| Perl | 5.6 | 5.34.0 |
| PHP | — | 8.1.2 |

## Run it

```bash
BASE="polyquine"
TARGET="${BASE}.c"
EXEC="${BASE}"

gcc -std=c99   "$TARGET" -o "$EXEC" && ./"$EXEC"     # C
g++ -std=c++11 -w "$TARGET" -o "$EXEC" && ./"$EXEC"  # C++
python3 "$TARGET"     # Python
lua "$TARGET"         # Lua
ruby "$TARGET"        # Ruby
perl "$TARGET"        # Perl
php "$TARGET"         # PHP
```

## Verify it

```bash
BASE="polyquine"
TARGET="${BASE}.c"
EXEC="${BASE}"

check() { "$2" "$TARGET" | diff - "$TARGET" && echo "[OK] $1"; }

gcc -std=c99   "$TARGET" -o "$EXEC" && ./"$EXEC" | diff - "$TARGET" && echo "[OK] C"
g++ -std=c++11 -w "$TARGET" -o "$EXEC" && ./"$EXEC" | diff - "$TARGET" && echo "[OK] C++"
check Python python3
check Lua    lua
check Ruby   ruby
check Perl   perl
check PHP    php
```

> `-w` disables C++ warnings. C uses GCC variadic macro extension (`_...` named varargs). C and C++ minimum versions remain C99/C++11. Each `.py` `.lua` `.rb` `.pl` `.php` file is byte-for-byte identical to `polyquine.c`. PHP works trivially — without `<?php` tags, it outputs any file verbatim.

