import pyvisa as visa
import time

cmd_output_on = 'OUTP ON'
cmd_output_off = 'OUTP OFF'
cmd_get_id = '*IDN?'
query = '?'

class DG1022A:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.dmm = self.find_dmm()
        print('Instrument ID (IDN:) = ', self.query(cmd_get_id)) 

    def query(self, cmd):
        self.dmm.write(cmd)
        time.sleep(.5)
        rawStr = self.dmm.read()
        print(rawStr)

    def find_dmm(self):
        devices_id = self.rm.list_resources()
        dmm_resources=''
        for string in devices_id:
            if 'DG1' in string:
                dmm_resources = string
                print(f"DG1022A address: {dmm_resources}")
                dmm = self.rm.open_resource(dmm_resources)  
        if(dmm_resources==''):
            print("DG1022A not found, list found devices:")
            print("\n".join(devices_id))
            dmm = TestDM()
        return dmm


    def send(self, cmd):
        self.dmm.write(cmd)
        time.sleep(0.1)

    def set_freq(self,freq):
        self.send('FREQ '+str(freq))
        

    def set_sin(self,freq,amp,offset,phase):
        self.send('VOLT:UNIT VPP')
        self.send('FUNC SIN')
        self.set_freq(freq)
        self.send('VOLT '+str(amp))
        self.send('VOLT:OFFS '+str(offset))
        self.send('PHAS '+str(phase))
        
    def set_pulse(self,freq,amp,offset,phase):
        self.send('VOLT:UNIT VPP')
        self.send('FUNC SQU')
        self.set_freq(freq)
        self.send('VOLT '+str(amp))
        self.send('VOLT:OFFS '+str(offset))
        self.send('PHAS '+str(phase))
        
    def set_ext_clk(self):
        self.send('SYST:CLKSRC EXT')

    def output(self, onoff):
        if (onoff): self.send('OUTP ON')
        else: self.send('OUTP OFF')



dg1022a = DG1022A()
dg1022a.set_ext_clk()
dg1022a.set_pulse(1e6/46.4, 1, 0, 0)
dg1022a.output(1)

class TestDM:
    def query(self, command: str) -> str:
        match command:
            case "*IDN?":
                return "TestDM"
            case _:
                return "?"
