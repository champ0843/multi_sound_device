import sounddevice as sd
import soundfile as sf
import threading
import os
import argparse
import queue
import sys

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', metavar='FILENAME',
    help='audio file to be played back')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
args = parser.parse_args(remaining)


DATA_TYPE = "float32"
def load_sound_file_into_memory(path):
    audio_data = soundfile.read(path,dtype=DATA_TYPE)
    return audio_data

def play_sound_file(audio_data,stream_object):
    stream_object.write(audio_data)

def create_outstream(index):
    output = sounddevice.OutputStream(
        device=index,
        dtype=DATA_TYPE
    )
    output.start()
    return output


----
def good_filepath(path):
    return str(path).endswith(".wav") and (not str(path).startswith("."))

cwd = "C:\\Users\\HP\\Documents\\GitHub\\multi_sound_device\\Sound file"
sound_file_paths = [
    os.path.join(cwd, path) for path in sorted(filter(lambda path: good_filepath(path), os.listdir(cwd)))
]


print("Discovered the following .wav files:", sound_file_paths)

files = [load_sound_file_into_memory(path) for path in sound_file_paths]

print("Files loaded into memory, Looking for USB devices.")

usb_sound_card_indices = list(filter(lambda x: x is not False,
                                     map(get_device_number_if_usb_soundcard,
                                         [index_info for index_info in enumerate(sounddevice.query_devices())])))

print("Discovered the following usb sound devices", usb_sound_card_indices)

streams = [create_running_output_stream(index) for index in usb_sound_card_indices]

running = True

if not len(streams) > 0:
    running = False
    print("No audio devices found, stopping")

if not len(files) > 0:
    running = False
    print("No sound files found, stopping")

while running:

    print("Playing files")

    threads = [threading.Thread(target=play_wav_on_index, args=[file_path, stream])
               for file_path, stream in zip(files, streams)]

    try:

        for thread in threads:
            thread.start()

        for thread, device_index in zip(threads, usb_sound_card_indices):
            print("Waiting for device", device_index, "to finish")
            thread.join()

    except KeyboardInterrupt:
        running = False
        print("Stopping stream")
        for stream in streams:
            stream.abort(ignore_errors=True)
            stream.close()
        print("Streams stopped")

print("Bye.")