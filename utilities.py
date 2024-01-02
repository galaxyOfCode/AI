import os
import configparser
from termcolor import colored

class Config:
    def __init__(self, config_file='config.ini'):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_file)
        self.load_settings()

    def load_settings(self):
        self.STOP = self.cfg.getint('PARAM', 'STOP')
        self.MAX_TOKENS = self.cfg.getint('PARAM', 'MAX_TOKENS')
        self.GPT3_MODEL = self.cfg['PARAM']['GPT3_MODEL']
        self.GPT4_MODEL = self.cfg['PARAM']['GPT4_MODEL']
        self.FREQ_PENALTY = self.cfg.getfloat('PARAM', 'FREQ_PENALTY')
        self.CHAT_TEMP = self.cfg.getfloat('PARAM', 'CHAT_TEMP')
        self.TUTOR_TEMP = self.cfg.getfloat('PARAM', 'TUTOR_TEMP')
        self.IMG_MODEL = self.cfg['PARAM']['IMG_MODEL']
        self.QUALITY = self.cfg['PARAM']['QUALITY']
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


def print_menu():
    '''Prints the main menu'''
    print("\n")
    print(f"AI Assistant (J. Hall, 2023)\n")
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

    
def not_numeric():
    '''Error message if menu choice is not numeric'''

    input("\nYou Entered a non-numeric value or wrong format.\nPress <Enter> to continue ... ")
    return


def list_models(client, option):
    '''List only the GPT models available through the API'''    
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    if option == 0:
        model_ids = [
            model_id for model_id in model_ids if model_id.startswith("gpt")]
        print("Current GPT Models\n")
    else:
        print("Current openAI Models:\n")
    model_ids.sort()
    print("\n".join(model_ids))
    input("\nHit Enter to continue . . .")


def settings():
    '''Prints off the hardcoded "Magic Numbers" '''
    config = Config()
    print("\nCurrent Settings:\n")
    print(colored("GPT3_MODEL: \t", "blue", attrs=["bold"]), config.GPT3_MODEL)
    print(colored("GPT4_MODEL: \t", "blue", attrs=["bold"]), config.GPT4_MODEL)
    print(colored("IMG_MODEL: \t", "blue", attrs=["bold"]), config.IMG_MODEL)
    print(colored("QUALITY: \t", "blue", attrs=["bold"]), config.QUALITY)
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