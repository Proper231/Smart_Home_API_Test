import socket
import os

def send_file(file_path, server_address, server_port):
    host = server_address
    port = server_port

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server.")

    # Send the request to the server to send the file
    client_socket.send("send_file".encode())

    # Send the audio file to the server
    with open(file_path, 'rb') as file:
        # Send the filename first
        filename = os.path.basename(file_path)
        client_socket.send(filename.encode())
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

def request_file(server_address, server_port):
    host = server_address
    port = server_port

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server.")

    while True:
        request = input("Enter your request (send_file, request_file, or no_more_questions): ")

        if request == "send_file":
            client_socket.send("send_file".encode())

            # Send the audio file to the server
            audio_file_path = 'recording_20230724_131844.wav'
            with open(audio_file_path, 'rb') as file:
                # Send the filename first
                filename = os.path.basename(audio_file_path)
                client_socket.send(filename.encode())
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

        elif request == "request_file":
            client_socket.send("request_file".encode())

            # Receive the confirmation audio from the server
            confirmation_filename = "confirmation_audio_received.wav"
            with open(confirmation_filename, 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data or data.endswith(b'\n'):
                        break
                    file.write(data)

            print("Received confirmation audio from the server.")

        elif request == "no_more_questions":
            client_socket.send("no_more_questions".encode())
            break

        else:
            print("Invalid request. Please try again.")

    # Close the connection
    client_socket.close()
    print("Client closed.")

if __name__ == "__main__":
    server_address = socket.gethostname()  # Server's hostname
    server_port = 3000  # Server's port number

    request_file(server_address, server_port)
