import pyvisa as visa
from typing import Optional
class SpectrumAnalyzer:
    def __init__(self, instrument_address):
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(instrument_address)

    def reset(self):
        self.instrument.write("*RST")
        self.check_status_byte()

    def clear_status(self):
        self.instrument.write("*CLS")
        self.check_status_byte()

    def set_frequency_range(self, start_freq, stop_freq):
        """Sets the start & stop Frequencies in MHz"""
        self.instrument.write(f":SENS:FREQ:STAR {start_freq} MHZ")
        self.instrument.write(f":SENS:FREQ:STOP {stop_freq} MHZ")
        self.check_status_byte()

    def set_center_frequency(self,center_frequency:float):
        """Sets the Center Frequencies in MHz"""
        self.instrument.write(f":SENS:FREQ:CENTER {center_frequency} MHZ")
        self.check_status_byte()

    def set_span(self, span: float):
        """Sets the span Frequencies in MHz"""
        self.instrument.write(f":SENS:FREQ:SPAN {span} MHZ")
        self.check_status_byte()

    def set_resolution_bandwidth(self, bandwidth):
        self.instrument.write(f":SENS:BAND:RES {bandwidth} HZ")
        self.check_status_byte()

    def set_detector_mode(self, mode):
        self.instrument.write(f":DETECTOR {mode}")
        self.check_status_byte()

    def set_offset_level(self, offset):
        self.instrument.write(f":DISP:WIND:TRAC:Y:SCAL:RLEV:OFFS {offset} dB")
        self.check_status_byte()


    def set_reference_level(self, level):
        self.instrument.write(f":DISP:WIND:TRAC:Y:SCAL:RLEV {level} dBm")
        self.check_status_byte()



    def set_continuous_mode(self, state):
        if state:
            self.instrument.write(":INIT:CONT ON")
        else:
            self.instrument.write(":INIT:CONT OFF")
        self.check_status_byte()

    def initiate_measurement(self):
        self.instrument.write(":INIT:RESTart")
        self.check_status_byte()

    def find_peak(self):
        self.instrument.write(":CALC:MARK1:MAX")
        self.check_status_byte()

    def get_marker_amplitude(self):
        return float(self.instrument.query(":CALC:MARK1:Y?"))

    def get_marker_frequency(self):
        return float(self.instrument.query(":CALC:MARK1:X?"))

    def get_trace_data(self):
        return self.instrument.query(":TRACE:DATA TRACE1?")

    def check_status_byte(self):
        status_byte = int(self.instrument.read_stb())
        return status_byte

    def set_trigger_source(self,trigger): # trigger EST,IMM,IF,VID
        self.instrument.write(f"TRIGger:SOURce {trigger}")
        self.check_status_byte()

    def configure_spectrum(self,sa_object: str,
                           cf_freq: int,
                           span: int,
                           rbw: int,
                           ref_level: int ,
                           detector: Optional[str] = None,
                           trigger_source: Optional[str]=None,
                           offset_level: Optional[int] = None,
                           ):
        """ Configures the basic of a spectrum anlayzer
         inputs:
         a_object : is the visa instrumenet handle object received from SpectrumAnalyzer()
         cf_freq : Center frequency in [MHz]
         span: in [Mhz]
         rbw: in [kHz]
         detector: 'NORMal' if not chosen ('POSitive', 'NEGative', 'SAMple', 'AVERage)
         trigger_source: Free Run if not chosen, ('EXTernal', 'IF')
         offset_level, zero if not chosen
         """

        self.reset()
        self.set_center_frequency(cf_freq)
        self.set_span(span)
        self.set_resolution_bandwidth(rbw)
        if detector is not None:
            self.set_detector_mode(detector)
        if offset_level is not None:
            self.set_offset_level(0)
        if ref_level is not None:
            self.set_reference_level(ref_level)
        if trigger_source is not None:
            self.set_trigger_source('EXT')





if __name__ == "__main__":
    device_address = 'GPIB0::10::INSTR' #TCPIP0::10.100.102.31::5025::SOCKET
    vsa = SpectrumAnalyzer(device_address)


    # rm = pyvisa.ResourceManager()
    # vsa = rm.open_resource(device_address)  # R&S

    vsa.read_termination = '\n'
    vsa.write_termination = '\n'
    vsa.timeout = 30000

    # Example usage
    # vsa.reset()
    # vsa.set_trigger_source('EXT')
    # vsa.set_center_frequency(2450)
    # vsa.set_frequency_range(2449.31, 2450.310)
    # vsa.set_resolution_bandwidth(1)
    # vsa.set_detector_mode('POS')
    # vsa.set_offset_level(0)
    # vsa.set_reference_level(-40)

    vsa.configure_spectrum(vsa,2400,1,1e3,-40)
    vsa.set_continuous_mode(False)
    vsa.initiate_measurement()
    vsa.find_peak()
    amplitude = vsa.get_marker_amplitude()
    frequency = vsa.get_marker_frequency()
    trace_data = vsa.get_trace_data()

    rm.close()