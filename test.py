"""This script tests the PyAudio library by retrieving and printing the default input audio device information. It serves as a basic check to ensure that PyAudio is installed correctly and can access the system's audio input devices."""

import pyaudio

p = pyaudio.PyAudio()
default_input = p.get_default_input_device_info()
print(f"Default Input: {default_input['name']} (Index: {default_input['index']})")
p.terminate()
