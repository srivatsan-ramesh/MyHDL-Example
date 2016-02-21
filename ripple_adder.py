from myhdl import Signal, delay, instance, always, Simulation, concat, always_comb, intbv, traceSignals

def ClkDriver(clk, period=20):
    @always(delay(period/2))
    def driveClk():
        clk.next = not clk
    return driveClk

def shift_reg(inp, out, clk, parallelin):
    @always(clk.posedge)
    def shift_right():
        out.next = concat(inp,out[8:1])
    @always_comb
    def load():
        out.next = parallelin
    return load,shift_right

def full_adder(a, b, cin, sum, cout, clk):
    @always_comb
    def add():
        sum.next = a ^ b ^ cin
        print a,b,cin,sum
        cout.next = (a and b) or (cin and (a ^ b))
    @always(clk.posedge)
    def carry():
        cin.next = cout
    return add, carry

def test():
    clk = Signal(intbv(1))
    out1 = Signal(intbv(0)[8:])
    parallelin1 = Signal(intbv(0)[8:])
    out2 = Signal(intbv(0)[8:])
    parallelin2 = Signal(intbv(0)[8:])
    sum, cin, cout, inp1, inp2, a, b = [Signal(intbv(0)) for i in range(7)]

    clkdriver = ClkDriver(clk)
    shift1 = shift_reg(inp1, out1, clk, parallelin1)    #contains first number
    shift2 = shift_reg(inp2,out2,clk,parallelin2)       #contains second number initially and final result at the end of simulation
    adder = full_adder(a, b, cin, sum, cout, clk)
    @always_comb
    def connect():
        inp1.next = intbv(out1[0])[1:]
        inp2.next = sum
        a.next = intbv(out1[0])[1:]
        b.next = intbv(out2[0])[1:]
    @instance
    def tb():
        yield clk.negedge
        parallelin1.next = Signal(intbv(35)[8:])    #load first number
        parallelin2.next = Signal(intbv(39)[8:])    #load second number
    return connect, clkdriver, shift1, shift2, adder, tb

Simulation(traceSignals(test)).run(180)
