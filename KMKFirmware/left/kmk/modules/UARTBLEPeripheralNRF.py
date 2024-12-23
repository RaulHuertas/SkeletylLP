from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from micropython import const
import time;
CONNECTING = 0
CONNECTED = 1

class UARTBLEPeripheralNRF:
    ble = None
    name = ""
    uart = None
    connectionFails = 0
    readTimeout = 0.1
    restingForScan = False
    restingStartTime = 0
    def __init__(self, name):
        self.name = name
        self.ble = BLERadio()
        self.connectionState = CONNECTING
        self.connectionFails = 0
        self.restingStartTime = time.monotonic()

    def longDisconnected(self):
        return self.connectionFails > 5
    
    def connected(self):
        return self.connectionState == CONNECTED
    
    def evaluate(self):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()

    def evaluateConnecting(self):
        now = time.monotonic()
        if((now-self.restingStartTime) < 3):
            return
    #since this side won't connect to the host, 
        #the central can block
        print("z0")
        devicesFound =  self.ble.start_scan(ProvideServicesAdvertisement,timeout = 1)
        for adv in devicesFound:
            print((adv))
            print((adv.short_name))
            if adv.short_name != self.name:
                continue;
            if UARTService in adv.services:
                print("expected device found!") 
                serviceOk = False
                try:
                    self.uart = self.ble.connect(adv)
                    self.uart = self.uart[UARTService]
                    serviceOk = True
                except:
                    pass
                if serviceOk:
                    self.connectionState = CONNECTED
                    self.connectionFails = 0
                    print("Connected")
                    break
                    
        if not self.connected():
            self.connectionFails += 1
        self.restingStartTime = time.monotonic()
        #time.sleep(3)
        self.ble.stop_scan()


       
    def disconnect(self):
        self.connectionState = CONNECTING
        self.connectionFails = 0
        self.uart  = None
        self.restingStartTime = time.monotonic()-3

    def write(self,buf: circuitpython_typing.ReadableBuffer):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return

        #connected
        connOK = False
        try:
            self.uart.write(buf)
            connOK = True
        except:
            pass
        if not connOK or not self.ble.connected:
            self.disconnect()    

    def readline(self) -> bytes | None:
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            print("x1")
            return None
        #connected
        #print("x2")
        s = None
        try:
            s = self.uart.readline()
            #print("x3")
        except:
            print("x4")
            pass
        if not self.ble.connected :
            self.disconnect()
            print("x5")
        
        #print("x6")
        return s
    
    def read(self, nbytes: int | None = None ):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return
        #connected
        retValue = None
        try:
            retValue = self.uart.read(nbytes)
        except:
            pass
        if  not self.ble.connected:
            self.disconnect()

        return retValue
         