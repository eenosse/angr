import angr
import claripy
import logging
import IPython

p = angr.Project("./chal")

flag_char = [claripy.BVS(f"flag_{i}", 8) for i in range(68)]
flag = claripy.Concat(*flag_char)

with open("code", 'rb') as f:
    filename = "code"
    data = claripy.BVV(f.read())
    
    simfile = angr.SimFile(filename, content=data)

init_state : angr.SimState= p.factory.full_init_state(
    args = ["./chal", "code"],
    stdin = flag,
    fs = {filename: simfile},
    add_options={angr.options.LAZY_SOLVES}
)
    
for c in flag_char:
    init_state.add_constraints(c >= ord('!'), c <= ord('~'))
# init_state.add_constraints(flag_char[-1] == ord('}'))

BASE = 0x400000
FIND = 0x1722
AVOID = 0x1678

cnt = 0

# Debugging purpose :v
def debug_ready(state):
    print("Shit is ready")
    logging.getLogger('angr.sim_manager').setLevel(logging.DEBUG)

p.hook(BASE + 0x1703, debug_ready)

sim = p.factory.simgr(init_state)

sim.explore(find=BASE+FIND, avoid=BASE+AVOID)

if sim.found:
    sol_state = sim.found[0]
    print(sol_state.solver.eval(flag, cast_to=bytes))
    # In case I want to do something more
    IPython.embed()