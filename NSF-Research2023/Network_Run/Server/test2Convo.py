import socket
import os

def save_file(file_data, filename, save_directory):
    with open(os.path.join(save_directory, filename), 'wb') as file:
        file.write(file_data)

def start_server():
    host = '149.61.16.80'  # Server's IP address
    port = 3000  # Server's port number
    save_directory = '.'  # Directory to save received audio files

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
                confirmation_filename = "confirmation_audio.wav"
                with open(os.path.join(save_directory, confirmation_filename), 'rb') as file:
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

if __name__ == "__main__":
    start_server()
