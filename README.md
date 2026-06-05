# c-cpp-lua-ruby-perl-python-polyquine

A polyglot quine that prints its own source code, valid in:

- C
- C++
- Lua
- Ruby
- Perl
- Python

## Run it

```bash
# C
gcc polyquine.c -o polyquine && ./polyquine

# C++
g++ polyquine.c -o polyquine && ./polyquine

# Python
python polyquine.c

# Lua
lua polyquine.c

# Ruby
ruby polyquine.c

# Perl
perl polyquine.c
```
## Verify it

```bash
# C
gcc polyquine.c -o polyquine && ./polyquine | diff - polyquine.c

# C++
g++ -Wno-write-strings polyquine.c -o polyquine && ./polyquine | diff - polyquine.c

# Python
python polyquine.c | diff - polyquine.c

# Lua
lua polyquine.c | diff - polyquine.c

# Ruby
ruby polyquine.c | diff - polyquine.c

# Perl
perl polyquine.c | diff - polyquine.c
```
> Note: No output means the quine is correct.
