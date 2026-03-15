import pyaudio

p = pyaudio.PyAudio()
default_input = p.get_default_input_device_info()
print(f"Default Input: {default_input['name']} (Index: {default_input['index']})")
p.terminate()
