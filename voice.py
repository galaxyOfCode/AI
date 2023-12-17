import openai
from pathlib import Path
import pyperclip
from termcolor import colored
import tkinter as tk
from tkinter import filedialog

user_prompt = colored("Select a File: ", "light_blue", attrs=["bold"])
text_prompt = colored("Enter the text: ", "light_blue", attrs=["bold"])
assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])


def whisper(model, client):
    '''
    Transcribes a voice file to text
    
    This will take an audio file and create and transcribe a text file from the audio source. The transcription will appear as a text response from the assistant.  It will be copied to the clipboard.
    '''
    root = tk.Tk()
    root.withdraw()
    print(user_prompt)
    choice = filedialog.askopenfilename(title="Select a File")
    if choice:
        print(f"Selected file: {choice}")
    else:
        print("No file selected or dialog canceled.\n")
        return
    try:
        with open(choice, "rb") as audio_file:
            content = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )
            print(f"{assistant_prompt} {content}")
            pyperclip.copy(content)
    except FileNotFoundError:
        print(f"Error: The file {choice} was not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied when trying to read {choice}.")
        return
    except OSError:
        print(
            f"Error: An error occurred while reading from the file {choice}.")
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return


def tts(client, model, voice):
    '''
    Text to speech
    
    This will take text from a user prompt and create an audio file using a specified voice (TTS_VOICE). The new file will default to 'speech.mp3' and will be saved to the Desktop.
    '''
    try:
        user_input = input(text_prompt)
        speech_file_path = Path.home().joinpath("Desktop") / "speech.mp3"
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=user_input
        )
        response.stream_to_file(speech_file_path)
        print(
            f"{assistant_prompt} 'speech.mp3' succesfully created, Check your Desktop\n")
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)
        return
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        return
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return
