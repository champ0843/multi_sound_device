import logging
import threading
import time
import sounddevice as sd
import soundfile as sf 
import os

#sound_folder = "D:\\sound_work\\sounds" #for office
sound_folder = "C:\\Users\\HP\\Documents\\GitHub\\multi_sound_device\\Sound file"   #For home

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

long_sound,fs = dict_n['rain'][0],dict_n['rain'][1]
short_sound = dict_n['thunder'][0]

def play_long_sound(long_sound,fs,snd):
    print('its_playing')
    snd.play(long_sound,fs,device = snd.query_devices(2)['name'],loop = True)

def play_short_sound(short_sound,interval,fs,snd):
    while True:
        print("Played after",interval,":secs")
        snd.OutputStream(fs,device=snd.query_devices(7)['name'])
        
        time.sleep(interval)

def get_device_number_if_usb_soundcard(index_info):
    index, info = index_info
    print(index_info,index,info)
    if "USB Audio Device" in info["name"]:
        return index
    return False


usb_sound_card_indices = list(filter(lambda x: x is not False,
                                     map(get_device_number_if_usb_soundcard,
                                         [index_info for index_info in enumerate(sd.query_devices())])))

if __name__ == "__main__":
    long_t = threading.Thread(target = play_long_sound,args=(long_sound,fs,sd))
    short_t = threading.Thread(target = play_short_sound,args=(short_sound,9,fs,sd))
    long_t.start()
    short_t.start()
    long_t.join()
    short_t.join()
    print("exiting")



import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,),daemon = False)
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    x.join()
    logging.info("Main    : all done")