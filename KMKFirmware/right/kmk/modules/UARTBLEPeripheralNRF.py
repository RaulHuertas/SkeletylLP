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
    uartConn = None
    connectionFails = 0
    readTimeout = 0.1
    restingForScan = False
    restingStartTime = 0
    checkLinkCounter = 0

    def __init__(self, name):
        
        self.name = name
        self.ble = BLERadio()
        self.connectionState = CONNECTING
        self.connectionFails = 0
        self.restingStartTime = time.monotonic()-5
    @property
    def in_waiting(self):
        if self.uart is  None:
            return 0
        return self.uart.in_waiting
    
    def longDisconnected(self):
        return self.connectionFails > 5
    
    def connected(self):
        return self.connectionState == CONNECTED
    
    def linkOk(self):
        if self.uartConn is None:
            return False
        return self.uartConn.connected
    def checkLink(self):
        self.checkLinkCounter += 1
        if self.checkLinkCounter > 20:
            self.checkLinkCounter = 0
            if not self.linkOk():
                self.disconnect()

    def evaluate(self):
        if self.connectionState == CONNECTED:
            if not self.linkOk() :
                self.disconnect()
        else:
            self.evaluateConnecting()

    def evaluateConnecting(self):
        now = time.monotonic()
        if((now-self.restingStartTime) < 1):
            return
        if self.ble.advertising:
            return#avoiding error 0011
        #since this side won't connect to the host, 
        #the central can block
        print("scanning split pair...")
        devicesFound =  self.ble.start_scan(ProvideServicesAdvertisement,timeout = 5, interval = 0.8)
        for adv in devicesFound:
            print("Candidate pair: ", (adv.short_name))
            if adv.short_name != self.name:
                continue;
            if UARTService in adv.services:
                print("other side found!") 
                serviceOk = False
                try:
                    self.uartConn = self.ble.connect(adv)
                    self.uart = self.uartConn[UARTService]
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
        self.uartConn  = None
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
        
        if not connOK:
            self.disconnect()    
        self.checkLink()

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
            #print("x4")
            pass
        
        self.checkLink()
        return s
    
    def read(self, nbytes: int | None = None ):
        if nbytes is None:
            return None
        if nbytes == 0:
            return None
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return None
        #connected
        retValue = None
        connOK = False
        try:
            retValue = self.uart.read(nbytes)
            connOK = True
        except:
            pass
        
        if  not connOK :
            self.disconnect()
        self.checkLink()

        return retValue
         