import tkinter as tk
from tkinter import filedialog
from termcolor import colored
from pathlib import Path
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')
WHISPER_MODEL = cfg['PARAM']['WHISPER_MODEL']
TTS_MODEL = cfg['PARAM']['TTS_MODEL']
TTS_VOICE = cfg['PARAM']['TTS_VOICE']

blue1 = colored("Select a File: ", "light_blue", attrs=["bold"])
blue2 = colored("Enter the text: ", "light_blue", attrs=["bold"])
red = colored("Assistant: ", "light_red", attrs=["bold"])


def whisper(client):
    '''
    This will take an audio file and create and transcribe a text file from the audio source.
    '''
    root = tk.Tk()
    root.withdraw()
    print(blue1)
    choice = filedialog.askopenfilename(title="Select a File")
    if choice:
        print(f"Selected file: {choice}")
    else:
        print("No file selected or dialog canceled.\n")
        return
    try:
        with open(choice, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
                response_format="text"
            )
            print(red, transcript)
    except FileNotFoundError:
        print(f"Error: The file {choice} was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read {choice}.")
    except OSError:
        print(
            f"Error: An error occurred while reading from the file {choice}.")


def tts(client):
    '''
    This will take text from a prompt and create an audio file using a specified voice (TTS_VOICE)
    '''
    user_input = input(blue2)
    speech_file_path = Path.home().joinpath("Desktop") / "speech.mp3"
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=user_input
    )
    response.stream_to_file(speech_file_path)
    print(red,
          "'speech.mp3' succesfully created, Check your Desktop\n")
