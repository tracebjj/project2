import os
import socket
import json
import time
from platform import system
import PySimpleGUI as sg

def Get_Pi_Data():
    """Function to retrieve the pi data each iteration or whenever called"""
    core_temp = os.popen('vcgencmd measure_temp').readline().strip()  # Get the core temperature
    gpu_core_speed = os.popen('vcgencmd measure_clock core').readline().strip()  # Get the GPU core speed
    hdmi_clock = os.popen('vcgencmd measure_clock hdmi').readline().strip()  # Get the HDMI clock
    ram_io_voltage = os.popen('vcgencmd measure_volts sdram_i').readline().strip()  # Get the RAM I/O Voltage
    sd_card_speed = os.popen('vcgencmd measure_clock emmc').readline().strip()  # Get the SD card interface speed
    pixel_values = os.popen('vcgencmd measure_clock pixel').readline().strip()  # Get the 'pixel values'
    

    # Format the values to just get numerical values and any periods for decimal numbers
    core_temp_value = round(float(''.join(keep for keep in core_temp if keep.isdigit() or keep == '.')), 1)
    gpu_core_speed_value = round(float(''.join(keep for keep in gpu_core_speed if keep.isdigit() or keep == '.')), 1)
    hdmi_clock_value = round(float(''.join(keep for keep in hdmi_clock if keep.isdigit() or keep == '.')), 1)
    ram_io_voltage_value = round(float(''.join(keep for keep in ram_io_voltage if keep.isdigit() or keep == '.')), 1)
    sd_card_speed_value = round(float(''.join(keep for keep in sd_card_speed if keep.isdigit() or keep == '.')), 1)
    pixel_values_value = round(float(''.join(keep for keep in pixel_values if keep.isdigit() or keep == '.')),1)
    # values_value because grammar suffers for the sake of consistency
    
    return {
        'core_temp': core_temp_value,
        'gpu_core_speed': gpu_core_speed_value,
        'hdmi_clock': hdmi_clock_value,
        'ram_io_voltage': ram_io_voltage_value,
        'sd_card_speed': sd_card_speed_value,
        'pixel_values': pixel_values_value
    }

def Collate_Data(iteration_count):
    """Collates and arranges the pi data, in function form to be called each iteration"""
    pi_data = Get_Pi_Data()
    pi_data['iteration_count'] = iteration_count
    return json.dumps(list(pi_data.values()))

if __name__ == "__main__":
    if system() != "Linux": # Used the platform library to import system, if it isn't Linux it exits
        print("Not on Raspberry Pi, goodbye.")
    else:
        host = '127.0.0.1' # Loopback ip
        port = 8000
        
        try:
            s = socket.socket()
            s.connect((host, port))

            sg.theme('DarkGreen')
            layout = [
                [sg.Text('LED:'), sg.Text('◌', key='-LED-', font=('Arial', 16))],  # Unicode LED stand-in (U+25CC), LED off
                # opposite of Server so they alternate
                [sg.Button('Exit')]
            ]

            window = sg.Window('Client GUI', layout, finalize=True)

            try:
                for iteration in range(1, 51):
                    data = Collate_Data(iteration)
                    s.send(data.encode())

                    event, values = window.read(timeout=2000)  # Used timeout to check GUI every 2 seconds
                    window['-LED-'].update('🟢' if window['-LED-'].get() == '◌' else '◌')  # Toggles between led modes, '🟢' and '◌'

                s.close()
                print("Data sent successfully. Exiting.")

            except socket.error as err: # Catches and exits without ugly messages
                print(f"Error: {err}")
                print("Goodbye.")

            finally:
                window.close()

        except Exception as err:
            print(f"Error: {err}")
            print("Goodbye.")
