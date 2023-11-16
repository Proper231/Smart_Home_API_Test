import socket
import os
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import time

load_dotenv()

def save_file(file_data, filename, save_directory):
    with open(os.path.join(save_directory, filename), 'wb') as file:
        file.write(file_data)

def start_server(input_file):
    host = socket.gethostname()  # Server's IP address
    port = 3000  # Server's port number
    save_directory = os.getenv('PYTHONPATH2')  # Directory to save received audio files
    output_directory = os.getenv('PYTHONPATH1') # Directory to send output audio files
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for incoming connections

    print("Server is ready to receive audio.")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print('Connection from:', client_address)

        while True:
            # Receive the request from the client
            request = client_socket.recv(1024).decode('utf-8','ignore')
            if not request:
                break

            print("Received request:", request)

            if request == "request_file":
                confirmation_filename = input_file
                with open(os.path.join(output_directory, confirmation_filename), 'rb') as file:
                    file_data = file.read()
                    client_socket.sendall(file_data + b"\n")  # Sending the delimiter to indicate the end of data transmission
                    print("Confirmation audio sent to client.")

            elif request == "send_file":
                filename = client_socket.recv(1024).decode('utf-8','ignore')
                print("Receiving file:", filename)

                # Save the received audio file
                file_path = os.path.join(save_directory, "received_audio.wav")
                with open(file_path, 'wb') as file:
                    while True:
                        data = client_socket.recv(1024)
                        if not data or data.endswith(b"\n"):
                            break
                        file.write(data)

                print("File transmission complete.")

            elif request == "no_more_questions":
                break

            else:
                print("Invalid request. Please try again.")

        # Close the client connection
        client_socket.close()

    # Close the server socket
    server_socket.close()
    print("Server closed.")


'''def get_file_paths(folder_path):
    file_paths = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.wav'):
            file_path = os.path.join(folder_path, file_name)
            file_paths.append(file_path)
    return file_paths

# Provide the path to the folder containing the audio files
folder_path = os.getenv('PYTHONPATH1')
audio_files = get_file_paths(folder_path)



class AudioFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the created file is a WAV audio file
        if event.is_directory:
            return
        if event.src_path.endswith('.wav'):
            print(f"New file detected: {event.src_path}")
            start_server(event.src_path)

def watch_for_new_files(folder_path):
    event_handler = AudioFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


    # Provide the path to the folder containing the audio files
folder_path = os.getenv('PYTHONPATH1')

print(folder_path)    
    # Start watching for new files in the folder
if folder_path is not None:
    watch_for_new_files(folder_path)
else:
    print("Error: folder_path is None. Please provide a valid folder path.")
       
'''

# Process each audio file
if __name__ == "__main__":
    start_server('./')
