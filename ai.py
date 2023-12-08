# Dec 2023 - Jeff Hall

import os
import sys
from openai import OpenAI
import configparser
from termcolor import colored
from chat import chat, tutor
from image import vision, image
from code_review import code_reviewer
from voice import tts, whisper
from siu import asst

config = configparser.ConfigParser()
config.read('config.ini')
STOP = config.getint('PARAM', 'STOP')  # maximum value for choice in the main menu
MAX_TOKENS = config.getint('PARAM', 'MAX_TOKENS')
GPT3_MODEL = config['PARAM']['GPT3_MODEL']  # latest chatGPT 3.5 model
GPT4_MODEL = config['PARAM']['GPT4_MODEL']  # latest chatGPT 4 model
FREQ_PENALTY = config.getfloat ('PARAM', 'FREQ_PENALTY')
CHAT_TEMP = config.getfloat ('PARAM', 'CHAT_TEMP')
TUTOR_TEMP = config.getfloat ('PARAM', 'TUTOR_TEMP') 
IMG_MODEL = config['PARAM']['IMG_MODEL']
SIZE = config['PARAM']['SIZE']
QUALITY = config['PARAM']['QUALITY']
VISION_MODEL = config['PARAM']['VISION_MODEL']
WHISPER_MODEL = config['PARAM']['WHISPER_MODEL']
TTS_MODEL = config['PARAM']['TTS_MODEL']
TTS_VOICE = config['PARAM']['TTS_VOICE']

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


def list_gpt_models():
    '''
    List only the GPT models available through the API
    '''
    print("Current GPT Models")
    print("------------------")
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    gpt_model_ids = [
        model_id for model_id in model_ids if model_id.startswith("gpt")]
    gpt_model_ids.sort()
    for id in gpt_model_ids:
        print(id)
    input("\nHit Enter to continue . . .")


def list_models():
    '''
    List ALL openAI models available through the API
    '''
    print("Current openAI Models")
    print("---------------------")
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    model_ids.sort()
    for id in model_ids:
        print(id)
    input("\nHit Enter to continue . . .")


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
    print(colored("VISION_MODEL:\t", "blue", attrs=["bold"]), VISION_MODEL)
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
    print(" 1 = 3.5 Chat")
    print(" 2 = 4.0 Chat")
    print(" 3 = 3.5 Tutor")
    print(" 4 = 4.0 Tutor")
    print(" 5 = Code Reviewer")
    print(" 6 = Image Generator")
    print(" 7 = Vision")
    print(" 8 = Speech-to-Text")
    print(" 9 = Text-to-Speech")
    print("10 = List GPT Models")
    print("11 = List All Models")
    print("12 = List Current Settings")
    print("13 = SIU Assistant")
    print("14 = Quit")


# Main Loop
while True:
    print_menu()
    try:
        choice = int(input("\nEnter Choice: "))
    except ValueError:
        not_numeric()
        continue
    if choice == 1:
        chat(GPT3_MODEL, client)
    elif choice == 2:
        chat(GPT4_MODEL, client)
    elif choice == 3:
        tutor(GPT3_MODEL, client)
    elif choice == 4:
        tutor(GPT4_MODEL, client)
    elif choice == 5:
        code_reviewer()
    elif choice == 6:
        image(client)
    elif choice == 7:
        vision(api_key)
    elif choice == 8:
        whisper(client)
    elif choice == 9:
        tts(client)
    elif choice == 10:
        list_gpt_models()
    elif choice == 11:
        list_models()
    elif choice == 12:
        settings()
    elif choice == 13:
        asst(client)
    elif choice == 14:
        quit()
    else:
        input(
            f"\nPlease Make a Choice Between 1 and {STOP} \nPress <Enter> to return to Main Menu ... ")
