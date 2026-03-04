"""
This is the main entry point for the AI application. It provides a menu-driven interface for users to interact with various AI functionalities, including chat, document review, image generation, and speech processing."""

import sys
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
    """Main function to run the AI Assistant application."""

    console = Console()
    config = Config()
    client = OpenAI()
    while True:
        clear_screen()
        print_menu()
        choice = console.input("[bold cyan]Enter Choice:[/bold cyan] ")
        if choice in ["Q", "q"]:
            choice = MENU_MAX
        else:
            try:
                choice = int(choice)
            except ValueError:
                not_numeric(console)
                continue
        if choice == FASTER_MODEL:
            chat(client, config.faster_model,
                 config.chat_temp, config.freq_penalty, 1, console)
        elif choice == BETTER_MODEL:
            chat(client, config.better_model,
                 config.chat_temp, config.freq_penalty, 1, console)
        elif choice == ASST_MODEL:
            chat(client, config.asst_model,
                 config.asst_temp, config.freq_penalty, 0, console)
        elif choice == DATE_CALCULATOR:
            date_calculator(console)
        elif choice == DOC_REVIEW:
            doc_review(client, config.better_model, console)
        elif choice == IMG_GEN:
            generate_image(client, config.img_model, console)
        elif choice == IMG_DESC:
            describe_image(config.api_key, config.vision_model,
                           config.max_tokens, console)
        elif choice == SPEECH_TO_TEXT:
            speech_to_text(client, config.transcribe_model, console)
        elif choice == TEXT_TO_SPEECH:
            text_to_speech(client, config.tts_model, config.tts_voice, console)
        elif choice == LIST_MODELS:
            list_models(client, console)
        elif choice == LIST_SETTINGS:
            list_settings(config, console)
        elif choice == UPDATE_PACKAGES:
            update(console)
        elif choice == MENU_MAX:
            sys.exit()
        else:
            console.input(
                f"\nPlease Make a Choice Between [bold red]1 and {MENU_MAX}[/bold red]\n Hit [magenta]<Enter>[/magenta] to return to Main Menu..."
            )


if __name__ == "__main__":
    main()
