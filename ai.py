import os
import configparser
from openai import OpenAI
from termcolor import colored
from chat import chat
from code_review import code_reviewer
from image import vision, image
from voice import tts, whisper


class Config:
    def __init__(self, config_file='config.ini'):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_file)
        self.load_settings()

    def load_settings(self):
        self.VERSION = self.cfg['PARAM']['VERSION']
        self.STOP = self.cfg.getint('PARAM', 'STOP')
        self.MAX_TOKENS = self.cfg.getint('PARAM', 'MAX_TOKENS')
        self.GPT3_MODEL = self.cfg['PARAM']['GPT3_MODEL']
        self.GPT4_MODEL = self.cfg['PARAM']['GPT4_MODEL']
        self.FREQ_PENALTY = self.cfg.getfloat('PARAM', 'FREQ_PENALTY')
        self.CHAT_TEMP = self.cfg.getfloat('PARAM', 'CHAT_TEMP')
        self.TUTOR_TEMP = self.cfg.getfloat('PARAM', 'TUTOR_TEMP')
        self.IMG_MODEL = self.cfg['PARAM']['IMG_MODEL']
        self.SIZE = self.cfg['PARAM']['SIZE']
        self.VISION_MODEL = self.cfg['PARAM']['VISION_MODEL']
        self.WHISPER_MODEL = self.cfg['PARAM']['WHISPER_MODEL']
        self.TTS_MODEL = self.cfg['PARAM']['TTS_MODEL']
        self.TTS_VOICE = self.cfg['PARAM']['TTS_VOICE']
        self.api_key = self.get_api_key()

    def get_api_key(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables.")
        return api_key


def not_numeric():
    '''Error message if menu choice is not numeric'''

    input("\nYou Entered a non-numeric value or wrong format.\nPress <Enter> to continue ... ")
    return


def list_gpt_models(client):
    '''List only the GPT models available through the API'''

    print("Current GPT Models")
    print("------------------")
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    gpt_model_ids = [
        model_id for model_id in model_ids if model_id.startswith("gpt")]
    gpt_model_ids.sort()
    print("\n".join(gpt_model_ids))
    input("\nHit Enter to continue . . .")


def list_models(client):
    ''' List ALL openAI models available through the API '''

    print("Current openAI Models")
    print("---------------------")
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    model_ids.sort()
    print("\n".join(model_ids))
    input("\nHit Enter to continue . . .")


def settings():
    '''Prints off the hardcoded "Magic Numbers" '''

    config = Config()
    print("\nCurrent Settings:")
    print("-----------------------------------")
    print(colored("GPT3_MODEL: \t", "blue", attrs=["bold"]), config.GPT3_MODEL)
    print(colored("GPT4_MODEL: \t", "blue", attrs=["bold"]), config.GPT4_MODEL)
    print(colored("IMG_MODEL: \t", "blue", attrs=["bold"]), config.IMG_MODEL)
    print(colored("SIZE: \t\t", "blue", attrs=["bold"]), config.SIZE)
    print(colored("VISION_MODEL:\t", "blue",
          attrs=["bold"]), config.VISION_MODEL)
    print(colored("WHISPER_MODEL: \t", "blue",
          attrs=["bold"]), config.WHISPER_MODEL)
    print(colored("TTS_MODEL: \t", "blue", attrs=["bold"]), config.TTS_MODEL)
    print(colored("TTS_VOICE: \t", "blue", attrs=["bold"]), config.TTS_VOICE)
    print(colored("TUTOR_TEMP: \t", "blue", attrs=["bold"]), config.TUTOR_TEMP)
    print(colored("CHAT_TEMP: \t", "blue", attrs=["bold"]), config.CHAT_TEMP)
    print(colored("FREQ_PENALTY: \t", "blue",
          attrs=["bold"]), config.FREQ_PENALTY)
    print(colored("MAX_TOKENS: \t", "blue", attrs=["bold"]), config.MAX_TOKENS)
    input("\nHit Enter to continue . . .")


def print_menu():
    '''Prints the main menu'''

    config = Config()
    print("\n")
    print(f"AI Assistant v{config.VERSION} (J. Hall, 2023)")
    print("-----------------------------------")
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
    print("13 = Quit")


# Main Loop
def main():
    config = Config()
    client = OpenAI()
    while True:
        print_menu()
        try:
            choice = int(input("\nEnter Choice: "))
        except ValueError:
            not_numeric()
            continue
        if choice == 1:
            chat(client, config.GPT3_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1)
        elif choice == 2:
            chat(client, config.GPT4_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1)
        elif choice == 3:
            chat(client, config.GPT3_MODEL,
                 config.TUTOR_TEMP, config.FREQ_PENALTY, 0)
        elif choice == 4:
            chat(client, config.GPT4_MODEL,
                 config.TUTOR_TEMP, config.FREQ_PENALTY, 0)
        elif choice == 5:
            code_reviewer(client, config.GPT4_MODEL)
        elif choice == 6:
            image(client, config.IMG_MODEL, config.SIZE)
        elif choice == 7:
            vision(config.api_key, config.VISION_MODEL, config.MAX_TOKENS)
        elif choice == 8:
            whisper(client, config.WHISPER_MODEL)
        elif choice == 9:
            tts(client, config.TTS_MODEL, config.TTS_VOICE)
        elif choice == 10:
            list_gpt_models(client)
        elif choice == 11:
            list_models(client)
        elif choice == 12:
            settings()
        elif choice == 13:
            exit()
        else:
            input(
                f"\nPlease Make a Choice Between 1 and {config.STOP} \nPress <Enter> to return to Main Menu ... ")


if __name__ == "__main__":
    main()
