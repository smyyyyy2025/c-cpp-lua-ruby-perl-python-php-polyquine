# c-cpp-lua-ruby-perl-python-polyquine

A polyglot quine that prints its own source code, valid in:

- C
- C++
- Lua
- Ruby
- Perl
- Python

## Requirements

| Language | Minimum Version | Tested Version |
| :--- | :--- | :--- |
| C (gcc) | C99 | 11.4.0 |
| C++ (g++) | C++11 | 11.4.0 |
| Python | 3.6 | 3.10.12 |
| Lua | 5.1 | 5.4.4 |
| Ruby | 2.0 | 3.0.2 |
| Perl | 5.0 | 5.34.0 |

## Run it

```bash
# C
gcc -std=c99 polyquine.c -o polyquine && ./polyquine

# C++ (suppress -Wwrite-strings warning)
g++ -std=c++11 -Wno-write-strings polyquine.c -o polyquine && ./polyquine

# Python
python3 polyquine.c

# Lua
lua polyquine.c

# Ruby
ruby polyquine.c

# Perl
perl polyquine.c
```
# Verify it

```bash
# C
gcc -std=c99 polyquine.c -o polyquine && ./polyquine | diff - polyquine.c

# C++ (no warnings)
g++ -std=c++11 -Wno-write-strings polyquine.c -o polyquine && ./polyquine | diff - polyquine.c

# Python
python3 polyquine.c | diff - polyquine.c

# Lua
lua polyquine.c | diff - polyquine.c

# Ruby
ruby polyquine.c | diff - polyquine.c

# Perl
perl polyquine.c | diff - polyquine.c
```
> Note: No output means the quine is correct. The -Wno-write-strings flag suppresses the C++ warning about assigning a string constant to char*.
