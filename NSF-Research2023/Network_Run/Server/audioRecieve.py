import socket
import os

host = '155.210.158.143'  # Server's hostname
port = 3000  # Server's port number

# Create a server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)  # Listen for incoming connections

print("Server is ready to receive audio.")

# Accept a client connection
client_socket, client_address = s.accept()
print('Connection from:', client_address)

# Receive the filename from the client
filename = client_socket.recv(1024).decode()
print("Receiving file:", filename)

# Determine the directory where the audio files will be stored
audio_dir = 'server_audio_directory'
os.makedirs(audio_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Save the received audio file
file_path = os.path.join(audio_dir, filename)
with open(file_path, 'wb') as file:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file.write(data)

print("File transmission complete.")

# Close the client connection
client_socket.close()

# Close the server socket
s.close()
