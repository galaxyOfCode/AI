"""
This module contains utility functions for the AI Assistant, including menu display, error handling, model listing, and date calculations.
"""

import os
import platform
import subprocess
from datetime import datetime, timedelta

import openai
from openai import OpenAIError
from rich.console import Console
from rich.table import Table

from config import Config


def print_menu() -> None:
    """Prints the Main Menu"""

    menu = """
AI Assistant (J. Hall, 2023-2026)

 1 = Faster Chat
 2 = Better Chat
 3 = Legal Assistant
 4 = Date Calculator
 5 = Document Review
 6 = Generate an Image
 7 = Descibe an Image
 8 = Speech-to-Text
 9 = Text-to-Speech
10 = Speech-to-Speech 
11 = List All Models
12 = List Current Settings
13 = Update API packages
 Q = Quit
"""
    print(menu)


def not_numeric(console: Console) -> None:
    """Error message if menu choice is not numeric"""

    console.input("\nYou Entered a [bold red]non-numeric value[/bold red] or wrong format.\nHit [magenta]<Enter>[/magenta] to continue...")


def list_models(client: openai.OpenAI, console: Console) -> None:
    """List the GPT models available through the API using a Rich Table."""

    with console.status("[bold green]Fetching models from OpenAI..."):
        try:
            model_list = client.models.list()
            model_ids = sorted([model.id for model in model_list.data])
        except OpenAIError as e:
            console.print(f"[bold red]Error fetching models:[/bold red] {e}")
            console.input("[yellow]Hit <Enter> to acknowledge the error...[/yellow]")
            return

    table = Table(
        title="[bold cyan]Available OpenAI Models[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue"
    )

    table.add_column("Model ID", justify="left")

    for m_id in model_ids:
        style = "green" if "gpt" in m_id.lower() else "white"
        table.add_row(f"[{style}]{m_id}[/{style}]")

    console.print("\n")
    console.print(table)

    console.input("\nHit [magenta]<Enter>[/magenta] to continue...")


def list_settings(config: Config, console: Console) -> None:
    """Prints off the hardcoded "Magic Numbers" """

    table = Table(title="Current Settings", show_header=True, header_style="bold blue")

    # Add columns
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    # Add rows with settings and their corresponding values
    table.add_row("faster_model", str(config.faster_model))
    table.add_row("better_model", str(config.better_model))
    table.add_row("asst_model", str(config.asst_model))
    table.add_row("doc_review_model", str(config.doc_review_model))
    table.add_row("img_model", str(config.img_model))
    table.add_row("quality", str(config.quality))
    table.add_row("vision_model", str(config.vision_model))
    table.add_row("transcribe_model", str(config.transcribe_model))
    table.add_row("tts_model", str(config.tts_model))
    table.add_row("tts_voice", str(config.tts_voice))
    table.add_row("sts_model", str(config.sts_model))
    table.add_row("asst_temp", str(config.asst_temp))
    table.add_row("chat_temp", str(config.chat_temp))
    table.add_row("freq_penalty", str(config.freq_penalty))
    table.add_row("max_tokens", str(config.max_tokens))

    # Print the table
    console.print(table)

    console.input("\nHit [magenta]<Enter>[/magenta] to continue...")


def update(console: Console) -> None:
    """Updates the 'openai' package"""

    package = "openai"
    original_version = check_package_version(package)
    subprocess.check_call(["pip", "install", "--upgrade",
                          "openai"], stdout=subprocess.DEVNULL)
    updated_version = check_package_version(package)
    if original_version == "error" or updated_version == "error":
        return
    if original_version != updated_version:
        console.print(f"\n{package} has been updated to version {updated_version}\n")
    else:
        console.print(
            f"\nYou already have the latest version of {package} - ({original_version})\n")
    console.input("Hit [magenta]<Enter>[/magenta] to continue...")


def check_package_version(package_name: str) -> str:
    """
    Returns the version number of a Python package using pip.
    Returns:
        - version string if found
        - 'Error' if package is not found or another exception occurs
    """
    try:
        result = subprocess.check_output(
            ["pip", "show", package_name],
            stderr=subprocess.DEVNULL,
            text=True  # automatically decodes output
        )
        for line in result.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
        return "Version not found"

    except subprocess.CalledProcessError:
        console = Console()
        console.print(f"\n'{package_name}' package not found.\n")
        return "Error"
    except (OSError, ValueError) as e:
        console = Console()
        console.print(f"\nUnexpected error while checking '{package_name}': {e}\n")
        return "Error"


def clear_screen() -> None:
    """Clears the terminal screen in a cross-platform way."""

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def date_calculator(console: Console) -> None:
    """Simple Date Calculator"""

    console.print("\nDate Calculator")
    console.print("1. Add days to a date")
    console.print("2. Subtract days from a date")
    console.print("3. Calculate difference between two dates")
    choice = input("Choose an option (1-3): ")

    if choice not in {"1", "2", "3"}:
        console.input("[bold red]Invalid choice.[/] Hit [magenta]<Enter>[/] to return to Main Menu...")
        return

    try:
        if choice in {"1", "2"}:
            date_str = input("Enter the date (MM-DD-YYYY): ")
            base_date = datetime.strptime(date_str, "%m-%d-%Y")
            days = int(input("Enter number of days: "))
            if choice == "1":
                new_date = base_date + timedelta(days=days)
                console.print(f"New date after adding {days} days: {new_date.date()}")
            else:
                new_date = base_date - timedelta(days=days)
                console.print(f"New date after subtracting {days} days: {new_date.date()}")
        else:
            date_str1 = input("Enter the first date (MM-DD-YYYY): ")
            date_str2 = input("Enter the second date (MM-DD-YYYY): ")
            date1 = datetime.strptime(date_str1, "%m-%d-%Y")
            date2 = datetime.strptime(date_str2, "%m-%d-%Y")
            delta = abs((date2 - date1).days)
            console.print(f"Difference between {date_str1} and {date_str2}: {delta} days")

    except ValueError as ve:
        console.print(f"Invalid input: {ve}")

    console.input("Hit [magenta]<Enter>[/magenta] to return to Main Menu...")
    