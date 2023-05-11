import os
import time
import wave
import audioop
from control import RECCONTROL
from log import LOGGER

def Datahandler_worker():   
    try:
        N = 5 
        intensity_history = [] 
        mic_sensitivity = RECCONTROL.micsensiticity 
        while RECCONTROL.continue_rec:
            if os.path.exists(RECCONTROL.directory):
                wav_files = [f for f in os.listdir(RECCONTROL.directory) if f.endswith('.wav')]
            else:
                wav_files = []
                       
            for wav_file_name in wav_files:
                wav_file_path = os.path.join(RECCONTROL.directory, wav_file_name)
                with wave.open(wav_file_path, 'rb') as wav_file:
                    sample_width = wav_file.getsampwidth()
                    channels = wav_file.getnchannels()

                    audio_data = wav_file.readframes(-1)

                    audio_string = audioop.tomono(audio_data, sample_width, 1, 0)
                    
                    rms = audioop.rms(audio_string, sample_width)

                    scaling_factor = 2 ** (8 * sample_width) * channels

                    avg_intensity = rms / scaling_factor


                    intensity_history.append(avg_intensity)


                    if len(intensity_history) > N:
                        intensity_history.pop(0)


                    moving_avg = sum(intensity_history) / len(intensity_history)


                    if avg_intensity > moving_avg:
                        mic_sensitivity -= 10
                        os.system("amixer -D pulse sset 'Capture' {}%".format(mic_sensitivity))
                        
                        LOGGER('gain',"amixer -D pulse sset 'Capture {}%".format(mic_sensitivity))
                    elif avg_intensity < moving_avg:
                        mic_sensitivity += 10
                        os.system("amixer -D pulse sset 'Capture' {}%".format(mic_sensitivity))
                        
                        LOGGER('gain',"amixer -D pulse sset 'Capture {}%".format(mic_sensitivity))

                    LOGGER('rms',f'{wav_file_name}: {round(avg_intensity,3)}')
                    os.remove(wav_file_path)

            time.sleep(2)

    except Exception as e:
        LOGGER('exception','handldata: {}'.format(e))
