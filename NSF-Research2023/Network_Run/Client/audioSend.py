import socket
import os

def send_recent_audio():
    audio_dir = '.'  # Directory where the audio files are stored

    audio_files = []
    for file in os.listdir(audio_dir):
        if file.endswith(".wav"):
            audio_files.append(file)

    if not audio_files:
        print("No audio files found.")
        return

    most_recent_file = max(audio_files, key=os.path.getmtime)
    file_path = os.path.join(audio_dir, most_recent_file)

    print("Audio file selected:", most_recent_file)

    host = socket.gethostname()  # Server's hostname
    port = 3000  # Server's port number

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print("Connected to the server.")

    # Send the most recent audio file to the server
    with open(file_path, 'rb') as file:
        # Send the filename first
        s.send(most_recent_file.encode())
        print("Sending file:", most_recent_file)
        
        # Send the file data
        while True:
            data = file.read(1024)
            if not data:
                break
            s.send(data)

    # Close the connection
    s.close()

    print("File transmission complete.")

send_recent_audio()
