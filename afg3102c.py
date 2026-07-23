import pyvisa as visa
import time

cmd_output_on = 'OUTP ON'
cmd_output_off = 'OUTP OFF'
cmd_get_id = '*IDN?'
query = '?'

class AFG3102C:
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
            if 'AFG3' in string:
                dmm_resources = string
                print(f"AFG3102C address: {dmm_resources}")
                dmm = self.rm.open_resource(dmm_resources)  
        if(dmm_resources==''):
            print("AFG3102C not found, list found devices:")
            print("\n".join(devices_id))
            dmm = TestDM()
        return dmm


    def send(self, cmd):
        self.dmm.write(cmd)
        time.sleep(0.1)

    def set_freq(self,freq,chan = 1):
        self.send(':SOUR'+str(chan) +':FREQ '+str(freq) +'MHZ')

    def set_sin(self,freq,amp,offset,phase,chan = 1):
        self.send(':SOUR' + str(chan) +':VOLT:UNIT VPP')
        self.send(':SOUR' + str(chan) +'FUNC:SHAP SIN')
        self.set_freq(freq)
        self.send(':SOUR' + str(chan) +'VOLT:LEV:IMM:AMP '+ str(amp) + 'VPP')
        self.send(':SOUR' + str(chan) +'VOLT:OFFS '+str(offset) + 'V')
        self.send(':SOUR' + str(chan) +'PHAS '+ str(phase) +'DEG')
        self.send('AFGCONTROL:CSCOPYCH1,CH2')
        self.send(':PHAS:INIT')
        
        
    def set_ext_clk(self):
        self.send('SOUR:ROSC:SOUR EXT')

    def output(self, onoff):
        if (onoff): 
            self.send('OUTPUT1:STATE ON')
            self.send('OUTPUT2:STATE ON')
        else: 
            self.send('OUTPUT1:STATE OFF')
            self.send('OUTPUT2:STATE OFF')




gen_40mhz = AFG3102C()
gen_40mhz.set_sin(40, 3, 0, 0)
gen_40mhz.output(1)

class TestDM:
    def query(self, command: str) -> str:
        match command:
            case "*IDN?":
                return "TestDM"
            case _:
                return "?"
