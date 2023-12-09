import os
import sys
from openai import OpenAI
import configparser
from termcolor import colored
from chat_law import chat, tutor
from image import image
from voice import tts, whisper

cfg = configparser.ConfigParser()
cfg.read('config.ini')
STOP = cfg.getint('PARAM', 'STOP')
MAX_TOKENS = cfg.getint('PARAM', 'MAX_TOKENS')
GPT3_MODEL = cfg['PARAM']['GPT3_MODEL']
GPT4_MODEL = cfg['PARAM']['GPT4_MODEL']
FREQ_PENALTY = cfg.getfloat('PARAM', 'FREQ_PENALTY')
CHAT_TEMP = cfg.getfloat('PARAM', 'CHAT_TEMP')
TUTOR_TEMP = cfg.getfloat('PARAM', 'TUTOR_TEMP')
IMG_MODEL = cfg['PARAM']['IMG_MODEL']
SIZE = cfg['PARAM']['SIZE']
QUALITY = cfg['PARAM']['QUALITY']
WHISPER_MODEL = cfg['PARAM']['WHISPER_MODEL']
TTS_MODEL = cfg['PARAM']['TTS_MODEL']
TTS_VOICE = cfg['PARAM']['TTS_VOICE']

# get api_key from user's shell config file#
try:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
except ValueError as e:
    print(f"Error: {e}")
    print("Please ensure that the 'OPENAI_API_KEY' environment variable is set.")
    sys.exit(1)

client = OpenAI()


def not_numeric():
    '''
    Error message if menu choice is not numeric
    '''
    input("\nYou Entered a non-numeric value or wrong format.\nPress <Enter> to continue ... ")
    return


def settings():
    '''
    Prints off the hardcoded "Magic Numbers"
    '''
    print("\nCurrent Settings:")
    print("-----------------------------------")
    print(colored("GPT3_MODEL: \t", "blue", attrs=["bold"]), GPT3_MODEL)
    print(colored("GPT4_MODEL: \t", "blue", attrs=["bold"]), GPT4_MODEL)
    print(colored("IMG_MODEL: \t", "blue", attrs=["bold"]), IMG_MODEL)
    print(colored("SIZE: \t\t", "blue", attrs=["bold"]), SIZE)
    print(colored("QUALITY: \t", "blue", attrs=["bold"]), QUALITY)
    print(colored("WHISPER_MODEL: \t", "blue",
          attrs=["bold"]), WHISPER_MODEL)
    print(colored("TTS_MODEL: \t", "blue", attrs=["bold"]), TTS_MODEL)
    print(colored("TTS_VOICE: \t", "blue", attrs=["bold"]), TTS_VOICE)
    print(colored("TUTOR_TEMP: \t", "blue", attrs=["bold"]), TUTOR_TEMP)
    print(colored("CHAT_TEMP: \t", "blue", attrs=["bold"]), CHAT_TEMP)
    print(colored("FREQ_PENALTY: \t", "blue", attrs=["bold"]), FREQ_PENALTY)
    print(colored("MAX_TOKENS: \t", "blue", attrs=["bold"]), MAX_TOKENS)
    input("\nHit Enter to continue . . .")


def print_menu():
    '''
    Prints the main menu
    '''
    print("\n")
    print("AI Assistant v3.5 (J. Hall, 2023)")
    print("---------------------------------")
    print(" 1 = 4.0 Law Tutor")
    print(" 2 = 3.5 Law Tutor")
    print(" 3 = 4.0 Chat")
    print(" 4 = 3.5 Chat")
    print(" 5 = Image Generator")
    print(" 6 = Speech-to-Text")
    print(" 7 = Text-to-Speech")
    print(" 8 = List Current Settings")
    print(" 9 = Quit")


# Main Loop
while True:
    print_menu()
    try:
        choice = int(input("\nEnter Choice: "))
    except ValueError:
        not_numeric()
        continue
    if choice == 1:
        tutor(GPT4_MODEL, client)
    elif choice == 2:
        tutor(GPT3_MODEL, client)
    elif choice == 3:
        chat(GPT4_MODEL, client)
    elif choice == 4:
        chat(GPT3_MODEL, client)
    elif choice == 5:
        image(client)
    elif choice == 6:
        whisper(client)
    elif choice == 7:
        tts(client)
    elif choice == 8:
        settings()
    elif choice == 9:
        quit()
    else:
        input(
            f"\nPlease Make a Choice Between 1 and {STOP} \nPress <Enter> to return to Main Menu ... ")
