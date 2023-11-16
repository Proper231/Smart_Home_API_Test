import socket
import os
import random
from faster_whisper import WhisperModel
import datetime
import time
import os 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

host = socket.gethostname()  # Server's hostname
port = 3000  # Server's port number

# Create a server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)  # Listen for incoming connections

print("Server is ready to receive audio.")

def select_specific_audio_file(audio_dir, audio_name):
    audio_file_path = os.path.join(audio_dir, audio_name)
    if os.path.exists(audio_file_path):
        return audio_file_path
    else:
        return None

# Accept a client connection
client_socket, client_address = s.accept()
print('Connection from:', client_address)

# Receive the filename from the client
filename = client_socket.recv(1024).decode()
print("Receiving file:", filename)

# Determine the directory where the audio files will be stored
audio_dir = os.getenv('PYTHONPATH2')
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


#WHISPER AUDIO TO TEXT
#-------------------------
def fasterWhisper(file): 

    model_size = "medium"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    

    current_datetime = datetime.datetime.now()
    current_date = str(current_datetime.date())

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    #fileout the file that will have the text of the audio file
    fileout= current_date + "_"+ current_time +'.txt'
    output_dir = os.getenv('PYTHONPATH4')

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, fileout)
    #audio go through whisper and extract the text from audio
    segments, info = model.transcribe( file, beam_size=5)
    for segment in segments:
        print(segment.text)
        with open(file_path, "a") as file:
    #            # Write the new text to the file
            file.write(segment.text.strip())
            

    return 0

def get_file_paths(folder_path):
    file_paths = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.wav'):
            file_path = os.path.join(folder_path, file_name)
            file_paths.append(file_path)
    return file_paths

# Provide the path to the folder containing the audio files
folder_path = os.getenv('PYTHONPATH2')
audio_files = get_file_paths(folder_path)



class AudioFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the created file is a WAV audio file
        if event.is_directory:
            return
        if event.src_path.endswith('.wav'):
            print(f"New file detected: {event.src_path}")
            fasterWhisper(event.src_path)

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

if __name__ == "__main__":
    # Provide the path to the folder containing the audio files
    folder_path = os.getenv('PYTHONPATH2')
    
    # Start watching for new files in the folder
    watch_for_new_files(folder_path)
       


# Process each audio file
for file_path in audio_files:
    fasterWhisper(file_path)


#--------------------------------------------------------------
#END




# Select a specific audio file from the server's directory
selected_audio_file = select_specific_audio_file(audio_dir, "specific_audio.wav")

# Send the selected audio file back to the client
if selected_audio_file:
    with open(selected_audio_file, 'rb') as file:
        client_socket.sendall(os.path.basename(selected_audio_file).encode())
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)
    print("Selected audio file sent to the client.")
else:
    client_socket.sendall(b"No audio file available on the server.")

# Close the client connection
client_socket.close()

# Close the server socket
s.close()
