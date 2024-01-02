import openai
from pathlib import Path
import pyperclip
from termcolor import colored
import tkinter as tk
from tkinter import filedialog
from errors import handle_file_errors, handle_openai_errors

user_prompt = colored("Select a File: ", "light_blue", attrs=["bold"])
text_prompt = colored("Enter the text: ", "light_blue", attrs=["bold"])
assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])


def whisper(client, model):
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
    except (PermissionError, OSError, FileNotFoundError) as e:
        content = handle_file_errors(e)
        return content
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
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        return content
    except KeyboardInterrupt:
        print("Exiting...")
        return
