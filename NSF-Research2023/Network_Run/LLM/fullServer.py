import socket
import os
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()

def save_file(file_data, filename, save_directory):
    with open(os.path.join(save_directory, filename), 'wb') as file:
        file.write(file_data)

def start_server(input_file):
    host = socket.gethostname()
    port = 3000
    save_directory = os.getenv('PYTHONPATH2')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server is ready to receive audio.")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print('Connection from:', client_address)

            event_handler = AudioFileHandler(client_socket)
            observer = Observer()
            observer.schedule(event_handler, path=save_directory, recursive=False)
            observer.start()

            while True:
                request = client_socket.recv(1024).decode('utf-8','ignore')
                if not request:
                    break

                print("Received request:", request)

                if request == "request_file":
                    confirmation_filename = '.'
                    most_recent_audio_file = get_most_recent_audio_file(save_directory)
                    if most_recent_audio_file:
                        with open(most_recent_audio_file, 'rb') as file:
                            file_data = file.read()
                            client_socket.sendall(file_data + b"\n")
                            print("Audio sent to client.")
                    else:
                        client_socket.sendall(b"\n")

                elif request == "send_file":
                    filename = client_socket.recv(1024).decode('utf-8','ignore')
                    print("Receiving file:", filename)
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

            client_socket.close()

            observer.stop()
            observer.join()

    except KeyboardInterrupt:
        pass

    server_socket.close()
    print("Server closed.")

def get_most_recent_audio_file(directory):
    audio_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
    if audio_files:
        return os.path.join(directory, max(audio_files, key=os.path.getctime))
    return None

def send_audio_to_client(client_socket, file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        client_socket.sendall(file_data + b"\n")
        print("Audio sent to client.")

class AudioFileHandler(FileSystemEventHandler):
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.wav'):
            print(f"New file detected: {event.src_path}")
            send_audio_to_client(self.client_socket, event.src_path)

if __name__ == "__main__":
    start_server('.')
