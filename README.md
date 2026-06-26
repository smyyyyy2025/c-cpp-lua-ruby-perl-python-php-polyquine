# c-cpp-lua-ruby-perl-python-php-polyquine

A **562-byte, 7-line** polyglot quine ([6-line variant →](6-line/)) that prints its own source code, valid in:

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
| Python | 3.0 | 3.10.12 |
| Lua | 5.2 | 5.4.4 |
| Ruby | 2.0 | 3.0.2 |
| Perl | 5.6 | 5.34.0 |
| PHP | — | — |

## Run it

```bash
gcc -std=c99 polyquine.c -o polyquine && ./polyquine     # C
g++ -std=c++11 -w polyquine.c -o polyquine && ./polyquine # C++
python3 polyquine.py     # Python
lua polyquine.lua        # Lua
ruby polyquine.rb        # Ruby
perl polyquine.pl        # Perl
php polyquine.php        # PHP (trivial: no <?php needed)
```

## Verify it

The quine outputs its own source code, so `diff` shows nothing when correct:

```bash
gcc -std=c99 polyquine.c -o polyquine && ./polyquine | diff - polyquine.c && echo "[OK] C"
g++ -std=c++11 -w polyquine.c -o polyquine && ./polyquine | diff - polyquine.c && echo "[OK] C++"
python3 polyquine.py | diff - polyquine.c && echo "[OK] Python"
lua polyquine.lua | diff - polyquine.c && echo "[OK] Lua"
ruby polyquine.rb | diff - polyquine.c && echo "[OK] Ruby"
perl polyquine.pl | diff - polyquine.c && echo "[OK] Perl"
php polyquine.php | diff - polyquine.c && echo "[OK] PHP"
```

> The `-w` flag disables all C++ compilation warnings. C and C++ compile to the same binary. Each `.py` `.lua` `.rb` `.pl` `.php` file is byte-for-byte identical to `polyquine.c`. PHP works trivially — without `<?php` tags, it outputs any file verbatim.

