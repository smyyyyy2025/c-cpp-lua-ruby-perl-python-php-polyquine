#!/bin/bash
BASE="polyquine"          # 改这里切换目标文件
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
