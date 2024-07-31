import random
random.seed("He's a FAN, he's a FAN, he's a FAN")

FLAG = b"BKISC{No_problem!_Here's_the_information_about_the_Mercedes_CLR_GTR}"
# print(len(FLAG))

flag_enc = list(FLAG)
# Opcodes
OUT = b">"
INP = b"?"
SUB = b"|"
ADD = b"!"
XOR = b"@"
LOAD_INP = b"$"
LOAD_VAL = b","
LOAD_MEM = b"."
CMP = b"="
RET = b'\r'

# Messages
MSG1 = b"Flag:"

MEM = [0] * 8

OPCODES = b""
for c in MSG1:
    OPCODES += OUT + chr(c).encode()
for _ in range(len(FLAG)):
    OPCODES += INP

for idx in reversed(range(len(FLAG))):
    OPCODES += LOAD_INP
    MEM[0] = flag_enc[idx]
    vals = [random.randrange(21, 127) for i in range(3)]
    for i, v in enumerate(vals):
        # print(chr(v).encode())
        OPCODES += LOAD_VAL + chr(i+1).encode() + chr(v).encode()
        MEM[i+1] = v
    calc_list = [ADD, SUB, XOR]
    for i, op in enumerate(random.choices(calc_list, k=4)):
        # print(op)
        a1 = 0
        a2 = 0
        a3 = 0
        match i:
            case 0:
                a1 = 4
                a2 = 0
                a3 = 1
                OPCODES += op + chr(4).encode() + b'\x00' + chr(1).encode()
            case 1:
                a1 = 5
                a2 = 4
                a3 = 2
                OPCODES += op + chr(5).encode() + b'\x04' + chr(2).encode()
            case 2:
                a1 = 6
                a2 = 5
                a3 = 3
                OPCODES += op + chr(6).encode() + b'\x05' + chr(3).encode()
            case 3:
                a1 = 7
                a2 = 6
                a3 = 1
                OPCODES += op + chr(7).encode() + b'\x06' + chr(1).encode()
            case _:
                print("how the fuck")   
                
        if op == ADD:
            # flag_enc[idx] |= MEM[i+1]
            MEM[a1] = (MEM[a2] + MEM[a3]) & 0xff
        elif op == SUB:
            # flag_enc[idx] &= MEM[a3]
            MEM[a1] = (MEM[a2] - MEM[a3]) & 0xff
        elif op == XOR:
            # flag_enc[idx] ^= MEM[a3]
            MEM[a1] = MEM[a2] ^ MEM[a3]
    # op = list(random.choices(calc_list, k=4))
    # OPCODES += op[0] + chr(4).encode() + chr(0).encode() + chr(1).encode()
    # OPCODES += op[1] + chr(4).encode() + chr(0).encode() + chr(1).encode()
    # OPCODES += op[2] + chr(4).encode() + chr(0).encode() + chr(1).encode()
    # OPCODES += op[3] + chr(4).encode() + chr(0).encode() + chr(1).encode()
    
    # Check flag:
    print(hex(MEM[7]))
    if len(hex(MEM[7])) == 4:
        OPCODES += CMP + bytes.fromhex(hex(MEM[7])[2:])
    else:
        OPCODES += CMP + chr(MEM[7]).encode()
    
# Return
OPCODES += RET
    
# print(OPCODES)
# for i in range(256):
#     if chr(i).encode() not in OPCODES:
#         print(chr(i).encode())
#         break
print(len(OPCODES))
# print(bytes(flag_enc))

with open("code", 'wb') as f:
    f.write(OPCODES)