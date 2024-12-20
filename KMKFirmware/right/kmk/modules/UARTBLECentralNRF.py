from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from micropython import const
import time;
CONNECTING = 0
CONNECTED = 1

class UARTBLECentralNRF:
    ble = None
    name = ""
    uart = None
    advertisement = None
    #enums for connection status
    #trackin how many time connection has failed
    connectionState = CONNECTING
    connectionFails = 0
    readTimeout = 0.1

    def __init__(self, name):
        self.name = name
        self.ble = BLERadio()
        self.ble.name = self.name
        self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)
        self.advertisement.short_name = self.name
        self.connectionState = CONNECTING
        self.connectionFails = 0

    def longDisconnected(self):
        return self.connectionFails > 5
    
    def connected(self):
        return self.connectionState == CONNECTED
    
    def evaluate(self):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()

    def evaluateConnecting(self):
        #since this side won't connect to the host, 
        #the central can block
        advertisingTimeUnit = 0.625
        timeout_s = 5
        if self.longDisconnected():
            timeout_s = 5
        print("Advertising...")
        self.ble.start_advertising(self.advertisement, interval=advertisingTimeUnit*4, timeout=timeout_s)
        accumWaitingTime = 0
        
        while not self.ble.connected and accumWaitingTime<timeout_s:
            time.sleep(1)
            accumWaitingTime += 1
        
        
        if self.ble.connected:
            self.connectionState = CONNECTED
            self.connectionFails = 0
            print("Connected")
            return
        else:
            self.connectionFails += 1

        self.ble.stop_advertising()
        if self.longDisconnected():
            time.sleep(5)
        else:
            time.sleep(2)
        

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
            self.connectionState = CONNECTING

    def readline(self) -> bytes | None:
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return None
        #connected
        connOK = False
        try:
            s = self.uart.readline()
            connOK = True
        except:
            pass
        if not connOK or not self.ble.connected :
            self.connectionState = CONNECTING
            return b""
        return s
    
    def read(self, nbytes: int | None = None ):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return
        #connected
        connOK = False
        try:
            self.uart.read(nbytes)
            connOK = True
        except:
            pass
        if not connOK or not self.ble.connected:
            self.connectionState = CONNECTING

         