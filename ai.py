from openai import OpenAI
from chat import chat
from code_review import code_review
from config import Config
from image import vision, image
from voice import tts, whisper
from utilities import print_menu, not_numeric, list_models, settings


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
            code_review(client, config.GPT4_MODEL)
        elif choice == 6:
            image(client, config.IMG_MODEL, config.QUALITY)
        elif choice == 7:
            vision(config.api_key, config.VISION_MODEL, config.MAX_TOKENS)
        elif choice == 8:
            whisper(client, config.WHISPER_MODEL)
        elif choice == 9:
            tts(client, config.TTS_MODEL, config.TTS_VOICE)
        elif choice == 10:
            list_models(client, 0)
        elif choice == 11:
            list_models(client, 1)
        elif choice == 12:
            settings(config)
        elif choice == 13:
            exit()
        else:
            input(
                f"\nPlease Make a Choice Between 1 and {config.STOP} \nPress <Enter> to return to Main Menu ... ")


if __name__ == "__main__":
    main()
