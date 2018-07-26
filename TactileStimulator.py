import serial
import time


class Stimulator:
    def __init__(self, com_port, max_amplitude=4095, debug=False):
        self._stim = serial.Serial(com_port, baudrate=256000)
        self.debug = debug
        self._max_amplitude = float(max_amplitude)

    def __del__(self):
        self.write_all_channels_equal(0)
        self._stim.close()

    def _scale_to_max_amplitude(self, value):
        return int(float(value)*self._max_amplitude/4095.0)

    def write_single(self, channel, input_int):
        # type: (int, int) -> None
        string = "S{:01x}{:03x}\n".format(channel, self._scale_to_max_amplitude(input_int))
        if self.debug:
            print(repr(string))
        self._stim.write(bytearray(string, "UTF-8"))

    def write_all_channels_equal(self, input_int):
        # type: (int) -> None
        self.write_array_master([input_int] * 8)
        time.sleep(0.05)
        self.write_array_slave([input_int] * 8)

    def write_array_master(self, input_list):
        # type: (list) -> None
        self._write_array("M", input_list)

    def write_array_slave(self, input_list):
        # type: (list) -> None
        self._write_array("m", input_list)

    def _write_array(self, char, input_list):
        # type: (str, list) -> None
        out = str(char)
        if len(input_list) == 8:
            for element in input_list:
                element &= 0xFFF
                out += "{:03x}".format(self._scale_to_max_amplitude(element))
            out += "\n"
            if self.debug:
                print(repr(out))
            self._stim.write(bytearray(out, "UTF-8"))
