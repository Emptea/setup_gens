from dg1022a import *
from afg3102c import *

gen_46u4 = DG1022A()
gen_46u4.set_ext_clk()
gen_46u4.set_pulse(1e6/46.4, 1, 0, 0)
gen_46u4.output(1)

gen_40mhz = AFG3102C()
gen_40mhz.set_sin(40, 3, 0, 0)
gen_40mhz.output(1)