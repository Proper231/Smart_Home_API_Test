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
import queue

# Global variables
is_recording = False
frames = []
received_audio_data = queue.Queue()

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

    # Process the most recent audio recording
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
    parent_directory = 'server_audio_directory'

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

    # Step 11: Send the processed audio to the server
    send_audio_to_server(output_file, socket.gethostname, 3000)

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

# New function to receive audio from the server
def receive_audio(client_socket):
    global received_audio_data

    audio_file_name = client_socket.recv(1024).decode()
    print("Receiving audio file:", audio_file_name)

    received_audio_data.queue.clear()  # Clear any previous audio data

    audio_data = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        audio_data += data

    received_audio_data.put(audio_data)  # Put received audio data into the queue

    print("Audio file received.")

# New thread function to monitor socket for audio data
def socket_listener(client_socket):
    while True:
        if not is_recording:  # Only listen to the socket when not recording
            receive_audio(client_socket)
        time.sleep(1)  # Adjust the sleep interval as needed

# New function to play received audio
def play_received_audio():
    global received_audio_data

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    print("* Playing received audio")

    audio_data = received_audio_data.get()  # Get audio data from the queue
    stream.write(audio_data)

    print("* Audio playback complete")

    stream.stop_stream()
    stream.close()
    p.terminate()

# Start the socket listener thread
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('149.61.16.80', 3000))
socket_listener_thread = threading.Thread(target=socket_listener, args=(client_socket,))
socket_listener_thread.daemon = True  # Thread Swill exit when the main program exits
socket_listener_thread.start()

# Main loop (Simulated GPIO Input)
while True:
    if keyboard.is_pressed('r'):
        button_pressed()
        while keyboard.is_pressed('r'):
            pass
        button_released()

    if not received_audio_data.empty():
        play_received_audio()

    time.sleep(0.1)
