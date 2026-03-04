"""
This module provides functions for speech-to-text and text-to-speech functionalities using OpenAI's API. It includes error handling for file-related and OpenAI API errors, and uses the Rich library for terminal styling and user interaction. The speech-to-text function allows users to transcribe audio files, while the text-to-speech function converts user input text into an audio file saved on the user's desktop."""

from pathlib import Path
import pyperclip
import openai
from rich.console import Console
from rich.prompt import Prompt

from errors import handle_file_errors, handle_openai_errors


def speech_to_text(client: openai.OpenAI, model: str, console: Console) -> None:
    """ Transcribes a voice file to text using Rich for terminal styling. """

    user_style = "bold bright_blue"
    assistant_style = "bold bright_red"

    console.print("Select a File", style=user_style)
    choice = Prompt.ask("[bold bright_blue]Enter the path to your audio file[/bold bright_blue]")

    if not choice or not Path(choice).exists():
        console.print("[yellow]No valid file selected or file does not exist.\n[/yellow]")
        return

    try:
        with open(choice, "rb") as audio_file:
            content = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )
            console.print("Assistant: ", style=assistant_style, end="")
            console.print(content)
            pyperclip.copy(content)

            console.input("\nPress [magenta]<Enter>[/magenta] to return to menu...")

    except (PermissionError, OSError, FileNotFoundError) as e:
        content = handle_file_errors(e)
        console.print(f"Assistant: {content}", style=assistant_style)

    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/]")


def text_to_speech(client: openai.OpenAI, model: str, voice: str, console: Console) -> None:
    """ Converts text to speech using Rich for input and output styling. """

    assistant_style = "bold bright_red"

    try:
        user_input = Prompt.ask("[bold bright_blue]Enter the text[/bold bright_blue]")

        if not user_input:
            return

        speech_file_path = Path.home().joinpath("Desktop") / "speech.mp3"

        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=user_input
        )

        response.write_to_file(speech_file_path)

        console.print(
            "Assistant: 'speech.mp3' successfully created. Check your Desktop\n", 
            style=assistant_style
        )
        console.input("\nPress [magenta]<Enter>[/magenta] to return to menu...")

    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        console.print(f"Assistant: {content}", style=assistant_style)

    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/yellow]")
        