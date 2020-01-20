import logging
import threading
import time
import sounddevice as sd
import soundfile as sf 
import os

sound_folder = "D:\\sound_work\\sounds"

def good_filepath(path):
    print(path,str(path).endswith(".wav") and (not str(path).startswith(".")))
    return str(path).endswith(".wav") and (not str(path).startswith("."))

sound_file_paths = [
    os.path.join(sound_folder, path) for path in sorted(filter(lambda path: good_filepath(path), os.listdir(sound_folder)))
]

DATA_TYPE = "float32"
def load_sound_file_into_memory(path,dict_n):
    audio_data = sf.read(path,dtype=DATA_TYPE)
    file_name = path.split("\\")[-1].split('.')[0]
    dict_n[file_name] = audio_data
    return audio_data

dict_n = {}
file = [load_sound_file_into_memory(path,dict_n) for path in sound_file_paths]

long_sound,fs = dict_n['casio'][0],dict_n['casio'][1]
short_sound = dict_n['drum'][0]

def play_long_sound(long_sound,fs,snd):
	print('its_playing')
	snd.play(long_sound,fs,device = snd.query_devices(14)['hostapi'],loop = True)

def play_short_sound(short_sound,interval,fs,snd):
	print("Played after",interval,":secs")
	snd.play(short_sound,fs,device=snd.query_devices(14)['hostapi'])	
	time.sleep(interval)
	play_short_sound(short_sound,interval,fs,snd)


if __name__ == "__main__":
	long_t = threading.Thread(target = play_long_sound,args=(long_sound,fs,sd))
	short_t = threading.Thread(target = play_short_sound,args=(short_sound,5,fs,sd))
	long_t.start()
	play_short_sound(short_sound,5,fs,sd)
	short_t.start()
	long_t.join()
	short_t.join()