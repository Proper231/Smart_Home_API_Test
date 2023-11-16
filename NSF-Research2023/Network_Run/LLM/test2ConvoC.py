# import socket
# import os

# def send_file(file_path, server_address, server_port):
#     host = server_address
#     port = server_port

#     # Connect to the server
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((host, port))
#     print("Connected to the server.")

#     # Send the request to the server to send the file
#     client_socket.send("send_file".encode('utf-8','ignore'))

#     # Send the audio file to the server
#     with open(file_path, 'rb') as file:
#         # Send the filename first
#         filename = os.path.basename(file_path)
#         client_socket.send(filename.encode('utf-8','ignore'))
#         print("Sending file:", filename)
        
#         # Send the file data
#         while True:
#             data = file.read(1024)
#             if not data:
#                 break
#             client_socket.send(data)

#         # Send the delimiter to indicate the end of data transmission
#         client_socket.send(b"\n")

#     print("File transmission complete.")

#     # Close the connection
#     client_socket.close()
#     print("Client closed.")

# def request_file(server_address, server_port):
#     host = server_address
#     port = server_port

#     # Connect to the server
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((host, port))
#     print("Connected to the server.")

#     while True:
#         request = input("Enter your request (send_file, request_file, or no_more_questions): ")

#         if request == "send_file":
#             client_socket.send("send_file".encode('utf-8','ignore'))

#             # Send the audio file to the server
#             audio_file_path = 'recording_20230724_131327.wav'
#             with open(audio_file_path, 'rb') as file:
#                 # Send the filename first
#                 filename = os.path.basename(audio_file_path)
#                 client_socket.send(filename.encode('utf-8','ignore'))
#                 print("Sending file:", filename)

#                 # Send the file data
#                 while True:
#                     data = file.read(1024)
#                     if not data:
#                         break
#                     client_socket.send(data)

#                 # Send the delimiter to indicate the end of data transmission
#                 client_socket.send(b"\n")

#             print("File transmission complete.")

#         elif request == "request_file":
#             client_socket.send("request_file".encode('utf-8','ignore'))

#             # Receive the confirmation audio from the server
#             confirmation_filename = "confirmation_audio_received.wav"
#             with open(confirmation_filename, 'wb') as file:
#                 while True:
#                     data = client_socket.recv(1024)
#                     if not data or data.endswith(b'\n'):
#                         break
#                     file.write(data)

#             print("Received confirmation audio from the server.")

#         elif request == "no_more_questions":
#             client_socket.send("no_more_questions".encode('utf-8','ignore'))
#             break

#         else:
#             print("Invalid request. Please try again.")

#     # Close the connection
#     client_socket.close()
#     print("Client closed.")

# if __name__ == "__main__":
#     server_address = socket.gethostname()  # Server's hostname
#     server_port = 3000  # Server's port number

#     request_file(server_address, server_port)
###################################################################################
import socket
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

def send_file(file_path, server_address, server_port):
    host = server_address
    port = server_port

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server.")

    # Send the request to the server to send the file
    client_socket.send("send_file".encode('utf-8','ignore'))

    # Send the audio file to the server
    with open(file_path, 'rb') as file:
        # Send the filename first
        filename = os.path.basename(file_path)
        client_socket.send(filename.encode('utf-8','ignore'))
        print("Sending file:", filename)
        
        # Send the file data
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)

        # Send the delimiter to indicate the end of data transmission
        client_socket.send(b"\n")

    print("File transmission complete.")

    # Close the connection
    client_socket.close()
    print("Client closed.")

def watch_for_new_files(directory_to_watch, server_address, server_port):
    event_handler = MyHandler(directory_to_watch, server_address, server_port)
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

class MyHandler(FileSystemEventHandler):
    def __init__(self, directory_to_watch, server_address, server_port):
        self.directory_to_watch = directory_to_watch
        self.server_address = server_address
        self.server_port = server_port
        self.most_recent_audio_file = None

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if file_path.endswith('.wav'):
            print(f"New audio file detected: {file_path}")
            self.send_most_recent_audio()

    def send_most_recent_audio(self):
        audio_files = [f for f in os.listdir(self.directory_to_watch) if f.endswith('.wav')]
        if not audio_files:
            print("No audio files found in the directory.")
            return

        most_recent_audio_file = max(audio_files, key=os.path.getctime)
        print(f"Sending the most recent audio file: {most_recent_audio_file}")

        send_file(os.path.join(self.directory_to_watch, most_recent_audio_file), self.server_address, self.server_port)

if __name__ == "__main__":
    server_address = socket.gethostname()  # Server's hostname
    server_port = 3000  # Server's port number
    directory_to_watch = os.getenv('PYTHONPATH2') #"."  # Directory to monitor for new audio files
    print("this is good")
    print("file name" + directory_to_watch)
    watch_for_new_files(directory_to_watch, server_address, server_port)
    print("this is great")