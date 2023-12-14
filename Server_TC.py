import socket
import json
import PySimpleGUI as sg

def parse_data(data): # Function to be run during iterations, parses incoming data
    return json.loads(data)

def Update_GUI(window, data): # Updates the GUI sections when needed, a function so it happens every iteration
    window['-CORE_TEMP-'].update(f"Core Temperature: {data[0]}°C")
    window['-GPU_CORE_SPEED-'].update(f"GPU Core Speed: {data[1]}Hz")
    window['-HDMI_CLOCK-'].update(f"HDMI Clock: {data[2]}Hz")
    window['-RAM_IO_VOLTAGE-'].update(f"RAM I/O Voltage: {data[3]}V")
    window['-SD_CARD_SPEED-'].update(f"SD Card Interface Speed: {data[4]}Hz")
    window['-LED-'].update('🟢' if window['-LED-'].get() == '◌' else '◌')  # Toggle between '🟢' and '◌'
    sg.popup_quick_message("Data Received!", auto_close_duration=1)

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8000

    listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listensocket.bind((host, port))
    listensocket.listen(1)

    print(f"Server listening on {host}:{port}")

    sg.theme('DarkRed') # Dark Red to go with the other green GUI
    #Sets up the GUI layout
    layout = [
        [sg.Text('', key='-CORE_TEMP-', size=(40, 1))],
        [sg.Text('', key='-GPU_CORE_SPEED-', size=(40, 1))],
        [sg.Text('', key='-HDMI_CLOCK-', size=(40, 1))],
        [sg.Text('', key='-RAM_IO_VOLTAGE-', size=(40, 1))],
        [sg.Text('', key='-SD_CARD_SPEED-', size=(40, 1))],
        [sg.Text('LED:'), sg.Text('◌', key='-LED-', font=('Arial', 16))],
        [sg.Button('Exit')]
    ]



    window = sg.Window('Server GUI', layout, finalize=True)

    try:
        clientsocket, addr = listensocket.accept()
        print('Got connection from', addr)

        for _ in range(50):  # Assuming 50 iterations from the client
            message = clientsocket.recv(1024).decode()
            
            if not message:
                break

            data = parse_data(message)
            Update_GUI(window, data)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if clientsocket:
            clientsocket.close()

        listensocket.close()
        window.close()