
print("Starting on LEFT")
GREEN = (0, 255, 0)
OFF = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (234,133,51)
RED = (255, 0, 0)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (128, 128, 0)
import time
import board
testing  = False
def isItOn(cols, rows, keyIndex):
    nCol = len(cols)
    nRow = len(rows)
    colPins = [None]*nCol 
    rowPins = [None]*nRow 
    import digitalio
    for i in range(nCol):
        colPin = colPins[i] = digitalio.DigitalInOut(cols[i])
        colPin.direction = digitalio.Direction.OUTPUT
        colPin.value = False
    for i in range(nRow):
        rowPin = rowPins[i] = digitalio.DigitalInOut(rows[i])
        rowPin.direction = digitalio.Direction.INPUT
        rowPin.pull = digitalio.Pull.UP

    colIndex = keyIndex % nCol
    rowIndex = keyIndex // nCol
    #Setup the columns. The one active must be low, the rest high
    for c in range(nCol):
        if c == colIndex:
            colPins[c].value = False
        else:
            colPins[c].value = True
    #Final read of the switch
    import time
    time.sleep(0.01)
    returnVal = rowPins[rowIndex].value

    for i in range(nRow):
        rowPins[i].direction = digitalio.Direction.INPUT
        rowPins[i].deinit()
    

    for i in range(nCol):
        colPins[i].direction = digitalio.Direction.INPUT
        colPins[i].deinit()

    return not returnVal
row_pins = (board.D8, board.D7, board.D0, board.D1,)
col_pins = ( board.D2, board.D3,board.D4, board.D5,board.D6,)
def initKB():
    from nkbusb import NKB_USB, USBFeedback
    from kmk.modules.splituart import SplitUART, SplitSide
    keyboard = NKB_USB(col_pins, row_pins)
    keyboard.coord_mapping =  [
        0,  1,  2,  3,  4,   
        20,21,22,23,24,
        5,6,7,8,9,
        25,26,27,28,29,
        10,11,12,13,14,
        30,31,32,33,34,
        15,16,17,18,19,
        35,36,37,38,39,
    ]
    split = SplitUART(
            split_side=SplitSide.LEFT,
            split_target_left=True,
            data_pin = board.IMU_PWR,#RX
            data_pin2 = board.D10,#TX
            debug_enabled = False
        )
    keyboard.modules = [
        split, 
    ]

    
    return keyboard

def assignKeymap(kb):
    from keyAssignations import assignKeys
    kb.keymap = assignKeys()
    
if __name__ == '__main__':
    keyboard = initKB()
    assignKeymap(keyboard)
    keyboard.debug_enabled = testing
    keyboard.go()
