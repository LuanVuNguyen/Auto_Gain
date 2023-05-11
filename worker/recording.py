import pyaudio
import wave
import datetime
import os
from control import RECCONTROL
from log import LOGGER
from worker.clean_file import delete_old_files

def recording_worker():
    try:
        delete_old_files()
        mic_sensitivity = RECCONTROL.micsensiticity
        
        os.system("amixer -D pulse sset 'Capture' {}%".format(mic_sensitivity))
        
        # Set audio parameters
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024

        # Initialize PyAudio
        audio = pyaudio.PyAudio()

        # Initialize recording variables
        frames = []
        file_number = 1
        start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


        # Check if "record" directory exists, create it if it doesn't
        if not os.path.exists(RECCONTROL.directory):
            os.makedirs(RECCONTROL.directory)

        # Start recording loop
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        while RECCONTROL.continue_rec:
            data = stream.read(CHUNK)
            frames.append(data)            
            if len(frames) == int(RATE / CHUNK * RECCONTROL.record_seconds):
                # Save WAV file to "record" directory
                file_path = os.path.join(RECCONTROL.directory, f"{start_time}.wav")
                wf = wave.open(file_path, "wb")
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(frames))
                wf.close()
                LOGGER('save_record',f"Saved recording to {file_path}")
                
                # Reset recording variables for next file
                frames = []
                file_number += 1
                start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
        # Stop audio stream
        stream.stop_stream()
        stream.close()

        # Terminate PyAudio
        audio.terminate()
    except Exception as e:
        LOGGER('exeption','recording: {}'.format(e))
