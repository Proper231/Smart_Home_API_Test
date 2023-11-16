# # #mkdir tts
# # #pip install pip setuptools wheel -U
# # #pip install TTS
# # #check is install with pip list 
# # #can see all models(voices) with comand -->  tts-server --list_models
# # #code will save the conversion from text to audio in a the output_audio folder 
# # #the function will take the text file and make audio file with the date and time
# from TTS.api import TTS
# import datetime
# import os
from dotenv import load_dotenv
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import time
load_dotenv()
# def tts(textfile):

#     tts = TTS(model_name = "tts_models/de/thorsten/tacotron2-DDC")
#     with open(textfile, 'r') as file:
#         file_contents = file.read()

#     current_datetime = datetime.datetime.now()
#     datetime_string = current_datetime.strftime("%Y%m%d_%H%M%S")
#     audio_filename = f"audio_{datetime_string}.wav"
#     output_folder = os.getenv("PYTHONPATH1")
#     # output_folder = "output_audio"

#     # if not os.path.exists(output_folder):
#     #     os.makedirs(output_folder)

#     audio_path = os.path.join(output_folder, audio_filename)

#     tts.tts_to_file(text =file_contents, file_path= audio_path)

#     return 0 
# def get_file_paths(folder_path):
#     file_paths = []
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith('.wav'):
#             file_path = os.path.join(folder_path, file_name)
#             file_paths.append(file_path)
#     return file_paths

# folder_path = os.getenv("PYTHONPATH3")
# audio_files = get_file_paths(folder_path)


# class AudioFileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         # Check if the created file is a WAV audio file
#         if event.is_directory:
#             return
#         if event.src_path.endswith('.txt'):
#             print(f"New file detected: {event.src_path}")
#             tts(event.src_path)

# def watch_for_new_files(folder_path):
#     event_handler = AudioFileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=folder_path, recursive=False)
#     observer.start()         

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()

#     observer.join()

# folder_path = os.getenv("PYTHONPATH3")
    
#     # Start watching for new files in the folder
# watch_for_new_files(folder_path)

# for file_path in audio_files:
#     tts(file_path)

# # espeakng is trash ans sounds horrible

# # from bark import SAMPLE_RATE, generate_audio, preload_models
# # from scipy.io.wavfile import write as write_wav
# # from IPython.display import Audio

# # # download and load all models
# # preload_models()

# # # generate audio from text
# # text_prompt = """
# #      Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
# #      But I also have other interests such as playing tic tac toe.
# # """
# # audio_array = generate_audio(text_prompt)

# # # save audio to disk
# # write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# # # play text in notebook
# # Audio(audio_array, rate=SAMPLE_RATE)

from gtts import gTTS
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

def tts(textfile):
     # Read the text from the file
     with open(textfile, 'r') as file:
          text_contents = file.read()

    # Create a gTTS object and generate the audio
     tts = gTTS(text=text_contents, lang='en')

    # Define the output folder for audio files
     output_folder = os.getenv("PYTHONPATH1")
     current_datetime = time.strftime("%Y%m%d_%H%M%S")
     audio_filename = f"audio_{current_datetime}.mp3"
     audio_path = os.path.join(output_folder, audio_filename)

     # Save the audio as an MP3 file
     tts.save(audio_path)

     return 0

def get_file_paths(folder_path):
     file_paths = []
     for file_name in os.listdir(folder_path):
          if file_name.endswith('.txt'):
               file_path = os.path.join(folder_path, file_name)
               file_paths.append(file_path)
     return file_paths

class TextFileHandler(FileSystemEventHandler):
     def on_created(self, event):
          if event.is_directory:
               return
          if event.src_path.endswith('.txt'):
               print(f"New file detected: {event.src_path}")
               tts(event.src_path)

def watch_for_new_files(folder_path):
     event_handler = TextFileHandler()
     
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
     folder_path = os.getenv("PYTHONPATH3")

      # Start watching for new text files in the folder
     watch_for_new_files(folder_path)
     # for file_path in audio_files:
     #      tts(file_path)
# ... code to process existing audio files ...
