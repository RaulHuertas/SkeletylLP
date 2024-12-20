'''Enables splitting keyboards wirelessly or wired'''

import busio
from micropython import const
from supervisor import runtime, ticks_ms

from keypad import Event as KeyEvent
from storage import getmount

from kmk.kmktime import check_deadline
from kmk.modules import Module

class SplitSide:
    LEFT = const(1)
    RIGHT = const(2)

class SplitRole:
    Secondary = const(1)
    Primary = const(2)


class SplitBL(Module):

    def __init__(
        self,
        split_side=None,
        split_role=None,
        uart_interval=20,
        common_name="nutymini",
        debug_enabled=False,
    ):
        self._is_target = True
        self._uart_buffer = []
        self.split_side = split_side
        self.split_role = split_role
        self.split_offset = None
        self.common_name = common_name
        self._uart = None
        self._uart_interval = uart_interval
        self._debug_enabled = debug_enabled
        self.uart_header = bytearray([0xB2])  # Any non-zero byte should work

        
    def during_bootup(self, keyboard):
    
        self._is_target = self.split_role==SplitRole.Primary
            

        if not self._is_target:
            keyboard._hid_send_enabled = False

        if self.split_offset is None:
            self.split_offset = keyboard.matrix[-1].coord_mapping[-1] + 1

        if not self._is_target:   
            print("Creating central BLE") 
            from  kmk.modules.UARTBLECentralNRF import UARTBLECentralNRF     
            self._uart = UARTBLECentralNRF(self.common_name)
            self._uart.evaluate()
        else:
            print("Creating peripheral BLE") 
            from  kmk.modules.UARTBLEPeripheralNRF import UARTBLEPeripheralNRF  
            self._uart = UARTBLEPeripheralNRF(self.common_name)
            self._uart.evaluate()

        if self.split_side == SplitSide.RIGHT:
            offset = self.split_offset
            for matrix in keyboard.matrix:
                matrix.offset = offset
                offset += matrix.key_count

    def before_matrix_scan(self, keyboard):
        if self._uart is None:
            return
        self._uart.evaluate()
        self._receive_uart(keyboard)
        return

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update:
            if not self._is_target :
                self._send_uart(keyboard.matrix_update)
            else:
                pass  # explicit pass just for dev sanity..
            

        return

    def before_hid_send(self, keyboard):
        if not self._is_target:
            keyboard.hid_pending = False

        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass


    def _serialize_update(self, update):
        buffer = bytearray(2)
        buffer[0] = update.key_number
        buffer[1] = update.pressed
        return buffer

    def _deserialize_update(self, update):
        kevent = KeyEvent(key_number=update[0], pressed=update[1])
        return kevent

    def _checksum(self, update):
        checksum = bytes([sum(update) & 0xFF])

        return checksum

    def _send_uart(self, update):
        # Change offsets depending on where the data is going to match the correct
        # matrix location of the receiever
        if self._uart is not None:
            update = self._serialize_update(update)
            self._uart.write(self.uart_header)
            self._uart.write(update)
            self._uart.write(self._checksum(update))

    def _receive_uart(self, keyboard):
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            if self._uart.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self._uart.in_waiting >= 4:
                # Check the header
                if self._uart.read(1) == self.uart_header:
                    update = self._uart.read(2)

                    # check the checksum
                    if self._checksum(update) == self._uart.read(1):
                        self._uart_buffer.append(self._deserialize_update(update))
            if self._uart_buffer:
                keyboard.secondary_matrix_update = self._uart_buffer.pop(0)