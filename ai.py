from openai import OpenAI

from chat import chat
from reviewer import code_review
from config import Config
from image import (describe_image, generate_image)
from voice import text_to_speech, speech_to_text
from utilities import (print_menu, not_numeric,
                       list_models, list_settings,
                       update)


def main():
    config = Config()
    client = OpenAI()
    while True:
        print_menu()
        choice = input("Enter Choice: ")
        if choice == "q" or choice == "Q":
            choice = config.MENU_MAX
        else:
            try:
                choice = int(choice)
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
            generate_image(client, config.IMG_MODEL, config.QUALITY)
        elif choice == 7:
            describe_image(config.api_key, config.VISION_MODEL,
                           config.MAX_TOKENS)
        elif choice == 8:
            speech_to_text(client, config.WHISPER_MODEL)
        elif choice == 9:
            text_to_speech(client, config.TTS_MODEL, config.TTS_VOICE)
        elif choice == 10:
            list_models(client, 0)
        elif choice == 11:
            list_models(client, 1)
        elif choice == 12:
            list_settings(config)
        elif choice == 13:
            update()
        elif choice == 14:
            exit()
        else:
            input(
                f"\nPlease Make a Choice Between 1 and {config.MENU_MAX}\n Hit <Enter> to return to Main Menu..."
            )


if __name__ == "__main__":
    main()
