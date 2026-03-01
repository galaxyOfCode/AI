from openai import OpenAI
from rich.console import Console

from chat import chat
from reviewer import doc_review
from config import Config
from image import (describe_image, generate_image)
from voice import text_to_speech, speech_to_text
from utilities import (print_menu, not_numeric,
                       list_models, list_settings,
                       update, clear_screen, date_calculator)

FASTER_MODEL = 1
BETTER_MODEL = 2
ASST_MODEL = 3
DATE_CALCULATOR = 4
DOC_REVIEW = 5
IMG_GEN = 6
IMG_DESC = 7
SPEECH_TO_TEXT = 8
TEXT_TO_SPEECH = 9
LIST_MODELS = 10
LIST_SETTINGS = 11
UPDATE_PACKAGES = 12
MENU_MAX = 13

def main():
    console = Console()
    config = Config()
    client = OpenAI()
    while True:
        clear_screen()
        print_menu()
        choice = console.input("[bold cyan]Enter Choice:[/bold cyan] ")
        if choice == "q" or choice == "Q":
            choice = MENU_MAX
        else:
            try:
                choice = int(choice)
            except ValueError:
                not_numeric()
                continue
        if choice == FASTER_MODEL:
            chat(client, config.FASTER_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1, console)
        elif choice == BETTER_MODEL:
            chat(client, config.BETTER_MODEL,
                 config.CHAT_TEMP, config.FREQ_PENALTY, 1, console)
        elif choice == ASST_MODEL:
            chat(client, config.ASST_MODEL,
                 config.ASST_TEMP, config.FREQ_PENALTY, 0, console)
        elif choice == DATE_CALCULATOR:
            date_calculator()
        elif choice == DOC_REVIEW:
            doc_review(client, config.BETTER_MODEL)
        elif choice == IMG_GEN:
            generate_image(client, config.IMG_MODEL, config.QUALITY, console)
        elif choice == IMG_DESC:
            describe_image(config.api_key, config.VISION_MODEL,
                           config.MAX_TOKENS, console)
        elif choice == SPEECH_TO_TEXT:
            speech_to_text(client, config.TRANSCRIBE_MODEL, console)
        elif choice == TEXT_TO_SPEECH:
            text_to_speech(client, config.TTS_MODEL, config.TTS_VOICE, console)
        elif choice == LIST_MODELS:
            list_models(client, console)
        elif choice == LIST_SETTINGS:
            list_settings(config, console)
        elif choice == UPDATE_PACKAGES:
            update()
        elif choice == MENU_MAX:
            exit()
        else:
            console.input(
                f"\nPlease Make a Choice Between [bold red]1 and {MENU_MAX}[/bold red]\n Hit [magenta]<Enter>[/magenta] to return to Main Menu..."
            )


if __name__ == "__main__":
    main()
