# Run: gdb-pwndbg ./chal -x solve_gdb_pwndbg.py

import gdb
import pwndbg
import string

BASE = 0x555555554000

bp = 0x165D

gdb.execute(f"break *0x{hex(BASE+bp)[2:]}")

LEN = 68
flag = 'a'*LEN
flag_ptr = 67

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" + "0123456789" + "_{}!\"#$%&\'()*+,-./:;<=>?@[\\]^`|~ "

while flag_ptr > 0:
    found = 0
    for i in charset:
        inp = flag[:flag_ptr] + i + flag[flag_ptr+1:]
        print(inp)
        with open("inp.txt", 'w') as f:
            f.write(inp)
        gdb.execute("run code < inp.txt")
        
        for i in range(LEN - flag_ptr):
            gdb.execute("c")

        cnt = pwndbg.gdb.breakpoints()[0].hit_count
        print(cnt)
        if cnt == LEN - flag_ptr + 1:
            flag = inp
            found = 1
            print(flag)
            flag_ptr -= 1
            break
    if not found:
        print('skill issue.')
        exit(0)