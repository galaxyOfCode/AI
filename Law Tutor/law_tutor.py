from openai import OpenAI

from chat import chat
from config import Config
from image import generate_image
from voice import text_to_speech, speech_to_text
from utilities import (print_menu, not_numeric,
                       list_settings)


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
            chat(client, config.GPT4_MODEL,
                 config.TUTOR_TEMP, config.FREQ_PENALTY, 0)
        elif choice == 2:
            chat(client, config.GPT3_MODEL,
                 config.TUTOR_TEMP, config.FREQ_PENALTY, 0)
        elif choice == 3:
            chat(client, config.GPT4_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1)
        elif choice == 4:
            chat(client, config.GPT3_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1)
        elif choice == 5:
            generate_image(client, config.IMG_MODEL, config.QUALITY)
        elif choice == 6:
            speech_to_text(client, config.WHISPER_MODEL)
        elif choice == 7:
            text_to_speech(client, config.TTS_MODEL, config.TTS_VOICE)
        elif choice == 8:
            list_settings(config)
        elif choice == 9:
            exit()
        else:
            input(
                f"\nPlease Make a Choice Between 1 and {config.STOP}\n Press <Enter> to return to Main Menu ... "
            )


if __name__ == "__main__":
    main()
