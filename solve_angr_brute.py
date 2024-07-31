import angr
import claripy

LEN = 68
flag = 'a'*LEN
flag_ptr = 67

charset = [chr(i) for i in range(ord('!'), ord('~')+1)]

while flag_ptr > 0:
    found = 0
    for i in charset:
        inp = flag[:flag_ptr] + i + flag[flag_ptr+1:]
        print(inp)
        proj = angr.Project('./chal', auto_load_libs=False)

        k = claripy.BVV(inp)
        data = claripy.BVV(open('code', 'rb').read())

        filename = 'code'
        simfile = angr.SimFile(filename, content=data)

        bp = 0x40165D

        cnt = 0

        def hook(state):
            global cnt
            cnt += 1

        proj.hook(bp, hook)
        state = proj.factory.full_init_state(
            args=['./chal', 'code'], 
            fs={filename: simfile}, 
            stdin=k,
            add_options={angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
                    angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS,
                    angr.options.LAZY_SOLVES}
        )
        state.options |= angr.options.unicorn

        sm = proj.factory.simulation_manager(state)
        sm.run()

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

