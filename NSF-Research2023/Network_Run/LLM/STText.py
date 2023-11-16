from faster_whisper import WhisperModel
import datetime
import time
import os 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
#pip install faster-whisper
#requires the NVIDIA libraries cuBLAS 11.x and cuDNN 8.x 
load_dotenv()
#WHISPER AUDIO TO TEXT
#-------------------------
def fasterWhisper(file): 

    model_size = "medium"
    #
    model = WhisperModel(model_size, device="cuda", compute_type="float")
    

    current_datetime = datetime.datetime.now()
    current_date = str(current_datetime.date())

    t = time.localtime()
    current_time = time.strftime("%H-%M-%S", t)
    
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


    # Provide the path to the folder containing the audio files
folder_path = os.getenv('PYTHONPATH2')

print(folder_path)    
    # Start watching for new files in the folder
if folder_path is not None:
    watch_for_new_files(folder_path)
else:
    print("Error: folder_path is None. Please provide a valid folder path.")
       


# Process each audio file
for file_path in audio_files:
    fasterWhisper(file_path)






