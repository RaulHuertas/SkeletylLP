print("Starting on RIGHT")

import board
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

testing = False

def initKB():
    from nkbusb import NKB_USB, USBFeedback
    from kmk.modules.splituart import SplitUART, SplitSide
            
    split = SplitUART(
        split_side=SplitSide.RIGHT,
        #split_type=SplitType.UART,
        split_target_left=False,
        data_pin = board.D10,#RX
        data_pin2 = board.IMU_PWR,#TX
        #uart_flip = False,
        debug_enabled = testing
    )

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
    
    fb = USBFeedback(board.D9, 128, 0.01)
    
    from kmk.modules.holdtap import HoldTap
    holdtap = HoldTap()
    #holdtap.tap_time = 600
    keyboard.modules = [
        split, 
        fb,
        holdtap,
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



