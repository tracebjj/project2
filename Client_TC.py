# Add 5th vcgencmd
import os
import socket
import json
import time
from platform import system
import PySimpleGUI as sg


def get_pi_data():

    core_temp = os.popen('vcgencmd measure_temp').readline().strip()  # Get the core temperature
    gpu_core_speed = os.popen('vcgencmd measure_clock core').readline().strip()  # Get the GPU core speed
    hdmi_clock = os.popen('vcgencmd measure_clock hdmi').readline().strip()  # Get the HDMI clock
    ram_io_voltage = os.popen('vcgencmd measure_volts sdram_i').readline().strip()  # Get the RAM I/O Voltage
    sd_card_speed = os.popen('vcgencmd measure_clock emmc').readline().strip()  # Get the SD card interface speed

    # Format the values to just get numerical values and any periods for decimal numbers
    core_temp_value = round(float(''.join(keep for keep in core_temp if keep.isdigit() or keep == '.')), 1)
    gpu_core_speed_value = round(float(''.join(keep for keep in gpu_core_speed if keep.isdigit() or keep == '.')), 1)
    hdmi_clock_value = round(float(''.join(keep for keep in hdmi_clock if keep.isdigit() or keep == '.')), 1)
    ram_io_voltage_value = round(float(''.join(keep for keep in ram_io_voltage if keep.isdigit() or keep == '.')), 1)
    sd_card_speed_value = round(float(''.join(keep for keep in sd_card_speed if keep.isdigit() or keep == '.')), 1)
    return {
        'core_temp': core_temp_value,
        'gpu_core_speed': gpu_core_speed_value,
        'hdmi_clock': hdmi_clock_value,
        'ram_io_voltage': ram_io_voltage_value,
        'sd_card_speed': sd_card_speed_value
    }

def collate_data(iteration_count):
    pi_data = get_pi_data()
    pi_data['iteration_count'] = iteration_count
    return json.dumps(list(pi_data.values()))

def main():
    host = '127.0.0.1'
    port = 8000
    max_iterations = 50

    try:
        s = socket.socket()
        s.connect((host, port))

        sg.theme('DarkGreen')
        layout = [
            [sg.Text('LED:'), sg.Text('◌', key='-LED-', font=('Arial', 16))],  # Unicode LED stand-in (U+25CC), LED off
            [sg.Button('Exit')]
        ]

        window = sg.Window('Client GUI', layout, finalize=True)

        try:
            for iteration in range(1, max_iterations + 1):
                data = collate_data(iteration)
                s.send(data.encode())

                event, values = window.read(timeout=2000)  # Used timeout to check GUI every 2 seconds
                window['-LED-'].update('🟢' if window['-LED-'].get() == '◌' else '◌')  # Toggles between led modes, '🟢' and '◌'

            s.close()
            print("Data sent successfully. Exiting.")

        except socket.error as e:
            print(f"Error: {e}")
            print("Exiting gracefully.")

        finally:
            window.close()

    except Exception as e:
        print(f"Error: {e}")
        print("Goodbye.")

if __name__ == "__main__":
    if system() != "Linux": # Used the platform library to import system, if it isn't Linux it exits
        print("Not on Raspberry Pi, goodbye.")
    else:
        main()
