from openai import OpenAI

from chat import chat
from reviewer import doc_review
from config import Config
from image import (describe_image, generate_image)
from voice import text_to_speech, speech_to_text
from utilities import (print_menu, not_numeric,
                       list_models, list_settings,
                       update, clear_screen)


def main():
    config = Config()
    client = OpenAI()
    while True:
        clear_screen()
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
            chat(client, config.FASTER_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1)
        elif choice == 2:
            chat(client, config.BETTER_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1)
        elif choice == 3:
            chat(client, config.ASST_MODEL,
                 config.ASST_TEMP, config.FREQ_PENALTY, 0)
        elif choice == 4:
            doc_review(client, config.BETTER_MODEL)
        elif choice == 5:
            generate_image(client, config.IMG_MODEL, config.QUALITY)
        elif choice == 6:
            describe_image(config.api_key, config.VISION_MODEL,
                           config.MAX_TOKENS)
        elif choice == 7:
            speech_to_text(client, config.WHISPER_MODEL)
        elif choice == 8:
            text_to_speech(client, config.TTS_MODEL, config.TTS_VOICE)
        elif choice == 9:
            list_models(client, 0)
        elif choice == 10:
            list_models(client, 1)
        elif choice == 11:
            list_settings(config)
        elif choice == 12:
            update()
        elif choice == 13:
            exit()
        else:
            input(
                f"\nPlease Make a Choice Between 1 and {config.MENU_MAX}\n Hit <Enter> to return to Main Menu..."
            )


if __name__ == "__main__":
    main()
