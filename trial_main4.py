import matplotlib.pyplot as plt
import numpy as np
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
# Import StepMotor and Spectrum_Analyzer classes
from StepMotor import StepMotor
from Spectrum_Advantests import SpectrumAnalyzer


def init_stepmotor(STEP_MOTOR_PORT:str,STEP_MOTOR_BAUD_RATE:int):
    """ Initialize StepMotor and and return its object"""
# STEP_MOTOR_PORT = 'com10'
# STEP_MOTOR_BAUD_RATE = 9600
    return StepMotor(STEP_MOTOR_PORT, STEP_MOTOR_BAUD_RATE)

def init_spectrum_analyzer(device_address:str,visa_timeout:int):
    """ Initialize spectrum ANalyzer and and return its object"""
    # device_address = 'GPIB0::10::INSTR' #TCPIP0::10.100.102.31::5025::SOCKET
    vsa = SpectrumAnalyzer(device_address)
    vsa.read_termination = '\n'
    vsa.write_termination = '\n'
    vsa.timeout = visa_timeout
    return vsa

def get_marker_peak(vsa):
    # Perform Spectrum Analysis and get the peak marker value
    vsa.initiate_measurement()

    vsa.find_peak()
    peak_marker = vsa.get_marker_amplitude()
    return peak_marker




if __name__ == "__main__":

    # Initialize the Spectrum Analyzer
    cf = 2400 # in MHz
    span = 1 # in MHz
    rbw = 30e3 #in Hz
    vsa = init_spectrum_analyzer('GPIB0::10::INSTR', 30000)
    vsa.configure_spectrum(vsa,cf,1,30e3,-40,'POS','EXT')


    # vsa.reset()
    # vsa.set_center_frequency(cf)
    # vsa.set_span(span)
    # vsa.set_resolution_bandwidth(rbw)
    # vsa.set_detector_mode('POS')
    # # vsa.set_offset_level(0)
    # vsa.set_reference_level(-40)
    # vsa.set_trigger_source('EXT')



    # Initialize the Step Motor
    m = init_stepmotor('com10',9600)
    # Initialize the Step Motor
    tic= time.time()
    m.flush_serial_buffer()
    toe = time.time() - tic
    print(m.set_echo(True))
    m.flush_serial_buffer()
    print(m.set_step_delay(100))
    print('time passed',time.time() - tic)
    # Initialize the polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    # Initialize the line to be updated during animation
    line, = ax.plot([], [], lw=2)


    plt.figure(1)
    ax = plt.subplot(111, polar=True)

    max_radius = 10  # Define the maximum radius for the polar plot

    prev_r = None
    prev_theta = None
    stop_degree =360
    step_degree = 2
    print(m.set_step_delay(10))
    theta_dbm_pairs = []

    dbm_ticks = [-100, -90, -80, -70, -60, -50]

    for i in range(0, stop_degree,step_degree):
        # Generate random dBm value from the sample list
        dbm = get_marker_peak(vsa)
        # Normalize dBm value to be within a range that corresponds to positive radii
        normalized_r = (dbm + 100) / 100 * max_radius
        # normalized_r = 10 ** (dbm / 10) # Convert dBm values to linear scale
        tic = time.time()
        ans = m.turn_left(step_degree)
        print('time passed', time.time() - tic)

        theta = 2 * np.pi * i / 360

        # Customize the radial ticks to reflect the original dBm values
        # ax.set_rticks(np.linspace(0, max_radius, num=len(dbm_values)))


        if prev_r is not None and prev_theta is not None:
            # Reflect points with negative radii across the origin
            if prev_r < 0:
                prev_theta += np.pi
                prev_r = abs(prev_r)
            if normalized_r < 0:
                theta += np.pi
                normalized_r = abs(normalized_r)

            ax.plot([prev_theta, theta], [prev_r, normalized_r], color='blue', linestyle='-', linewidth=1)

        ax.plot(theta, normalized_r, '-xr')
        plt.pause(0.01)  # Pause for a short while to update the plot

        # Append theta and dBm pair to the list of tuples
        theta_dbm_pairs.append((theta, dbm))
        # Convert list of tuples to numpy array for easy manipulation if needed
        theta_dbm_array = np.array(theta_dbm_pairs)

        prev_r = normalized_r
        prev_theta = theta

    # Customize the radial ticks to reflect the original dBm values
    #   ax.set_rticks(normalized_r, labels=dbm_ticks)  # Set radii ticks with dBm values

# ax.set_rticklabels(dbm_values)
comments = f'Frequency= {cf} MHz, Cantenna\n'
np.savetxt('CantennaTheta_dbm_data.csv', theta_dbm_array, delimiter=',', header='Theta (radians), dBm', comments=comments)
plt.show()
