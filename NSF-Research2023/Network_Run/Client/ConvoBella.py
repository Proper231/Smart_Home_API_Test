import threading
import pyaudio
import wave
import datetime
import time
import os
import struct
import numpy as np
import sys
import webrtcvad
import socket
import utils
import re
import keyboard

# Global variables
is_recording = False
frames = []

# Button press event handler
def button_pressed():
    global is_recording
    global frames

    if not is_recording:
        is_recording = True
        frames = []
        t1 = threading.Thread(target=start_recording)
        t1.start()
    print("Button pressed.")

# Button release event handler
def button_released():
    global is_recording

    if is_recording:
        is_recording = False
    print("Button released.")

# Start recording audio
def start_recording():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("* Recording started")

    frames = []
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Recording stopped")

    stream.stop_stream()
    stream.close()
    p.terminate()

    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("* Recording saved as " + filename)

    # Process the audio locally (if desired)
    process_audio(filename)

# Process the audio using VAD
def process_audio(wav_file, aggressiveness=3):
    audio, sample_rate = utils.read_wave(wav_file)
    vad = webrtcvad.Vad(int(aggressiveness))

    frames = utils.frame_generator(30, audio, sample_rate)
    frames = list(frames)

    voiced_frames = []
    for i, frame in enumerate(frames):
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        voiced_frames.append(1 if is_speech else '0')

    vad_decisions = np.array(voiced_frames).astype(int)
    vad_mask = np.kron(vad_decisions, np.ones(int(0.03 * sample_rate)))

    base_file_name = os.path.splitext(os.path.basename(wav_file))[0]
    parent_directory = '.'

    if not os.path.exists(parent_directory):
        os.mkdir(parent_directory)

    directory_path = os.path.join(parent_directory, base_file_name)

    if not os.path.exists(directory_path):
        os.mkdir(directory_path)

    segments = utils.vad_collector(sample_rate, 30, 300, vad, frames)

    for i, segment in enumerate(segments):
        path = os.path.join(directory_path, f'chunk-{i:02d}.wav')
        utils.write_wave(path, segment, sample_rate)

    print("VAD applied and segmented speech chunks saved.")

    # Combine the speech chunks into a single audio file
    combine_audio(directory_path, parent_directory)

# Combine audio chunks into a single file
def combine_audio(directory_path, parent_directory):
    file_pattern = re.compile(r'chunk-\d{2}\.wav')
    file_names = [f for f in os.listdir(directory_path) if re.match(file_pattern, f)]
    sorted_files = sorted(file_names, key=lambda f: int(re.search(r'\d{2}', f).group()))

    combined_audio = wave.open(os.path.join(directory_path, 'combined_audio.wav'), 'wb')

    first_audio_file = wave.open(os.path.join(directory_path, sorted_files[0]), 'rb')
    sample_width = first_audio_file.getsampwidth()
    sample_rate = first_audio_file.getframerate()
    num_channels = first_audio_file.getnchannels()

    combined_audio.setnchannels(num_channels)
    combined_audio.setsampwidth(sample_width)
    combined_audio.setframerate(sample_rate)

    for file in sorted_files:
        audio_file = wave.open(os.path.join(directory_path, file), 'rb')
        frames = audio_file.readframes(audio_file.getnframes())
        combined_audio.writeframes(frames)

        audio_file.close()

    combined_audio.close()

    # Slow down the combined audio by reducing the sample rate
    slow_factor = 1  # Adjust this value to control the slowdown (e.g., 0.5 for half speed)

    output_file = os.path.join(parent_directory, f'processed_audio_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.wav')
    output_audio = wave.open(output_file, 'wb')

    output_audio.setnchannels(num_channels)
    output_audio.setsampwidth(sample_width)
    output_audio.setframerate(int(sample_rate * slow_factor))

    combined_audio = wave.open(os.path.join(directory_path, 'combined_audio.wav'), 'rb')
    frames = combined_audio.readframes(combined_audio.getnframes())
    output_audio.writeframes(frames)

    combined_audio.close()
    output_audio.close()

    os.remove(os.path.join(directory_path, 'combined_audio.wav'))

    print("Audio chunks combined and processed.")

    # Step 10: Send the processed audio to the server
    send_audio_to_server(output_file, socket.gethostname(), 3000)

# Step 12: Send the processed audio to the server
def send_audio_to_server(audio_file, server_host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_host, port))

    print("Connected to the server.")

    with open(audio_file, 'rb') as file:
        # Send the filename first
        s.sendall(os.path.basename(audio_file).encode())

        # Send the file data
        while True:
            data = file.read(1024)
            if not data:
                break
            s.sendall(data)

    s.close()

    print("File transmission complete.")

    


    # Step 14: Receive and play the audio file from the server
    receive_and_play_audio(server_host, port)

# Step 14: Receive and play the audio file from the server
def receive_and_play_audio(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print("Connected to the server.")

    received_filename = s.recv(1024).decode()

    if received_filename == "No audio file available on the server.":
        print(received_filename)
        s.close()
        return

    received_audio_file = os.path.join('.', received_filename)

    with open(received_audio_file, 'wb') as file:
        while True:
            data = s.recv(1024)
            if not data:
                break
            file.write(data)

    s.close()

    print("File received from the server.")

    # Play the received audio
    play_audio(received_audio_file)

# Step 15: Play the audio file
def play_audio(audio_file):
    CHUNK = 1024
    wf = wave.open(audio_file, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    print("* Playing audio")

    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("* Audio playback complete.")

# Step 13: Main loop (Simulated GPIO Input)
while True:
    if keyboard.is_pressed('r'):
        button_pressed()
        while keyboard.is_pressed('r'):
            pass
        button_released()

    time.sleep(0.1)
