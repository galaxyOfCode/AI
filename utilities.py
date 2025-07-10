import os
import platform
from rich import print
from rich.table import Table
import subprocess


def print_menu() -> None:
    """Prints the Main Menu"""

    menu = """
AI Assistant (J. Hall, 2023-2024)

 1 = Faster Chat
 2 = Better Chat
 3 = Legal Assistant
 4 = Document Review
 5 = Image Generation
 6 = Vision
 7 = Speech-to-Text
 8 = Text-to-Speech
 9 = List GPT Models
10 = List All Models
11 = List Current Settings
12 = Update API packages
 Q = Quit
"""
    print(menu)


def not_numeric() -> None:
    """Error message if menu choice is not numeric"""

    input("\nYou Entered a non-numeric value or wrong format.\nHit <Enter> to continue...")


def list_models(client, option) -> None:
    """List only the GPT models available through the API"""

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
    input("\nHit <Enter> to continue...")


def list_settings(config) -> None:
    """Prints off the hardcoded "Magic Numbers" """

    table = Table(title="Current Settings", show_header=True, header_style="bold blue")
    
    # Add columns
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    # Add rows with settings and their corresponding values
    table.add_row("FASTER_MODEL", str(config.FASTER_MODEL))
    table.add_row("BETTER_MODEL", str(config.BETTER_MODEL))
    table.add_row("ASST_MODEL", str(config.ASST_MODEL))
    table.add_row("DOC_REVIEW_MODEL", str(config.BETTER_MODEL))
    table.add_row("IMG_MODEL", str(config.IMG_MODEL))
    table.add_row("QUALITY", str(config.QUALITY))
    table.add_row("VISION_MODEL", str(config.VISION_MODEL))
    table.add_row("WHISPER_MODEL", str(config.WHISPER_MODEL))
    table.add_row("TTS_MODEL", str(config.TTS_MODEL))
    table.add_row("TTS_VOICE", str(config.TTS_VOICE))
    table.add_row("ASST_TEMP", str(config.ASST_TEMP))
    table.add_row("CHAT_TEMP", str(config.CHAT_TEMP))
    table.add_row("FREQ_PENALTY", str(config.FREQ_PENALTY))
    table.add_row("MAX_TOKENS", str(config.MAX_TOKENS))

    # Print the table
    print(table)

    input("\nHit <Enter> to continue...")


def update() -> None:
    """Updates the 'openai' package"""

    package = "openai"
    original_version = check_package_version(package)
    subprocess.check_call(["pip", "install", "--upgrade",
                          "openai"], stdout=subprocess.DEVNULL)
    updated_version = check_package_version(package)
    if original_version == "error" or updated_version == "error":
        return
    if original_version != updated_version:
        print(f"\n{package} has been updated to version {updated_version}\n")
    else:
        print(
            f"\nYou already have the latest version of {package} - ({original_version})\n")
    input("Hit <Enter> to continue...")


def check_package_version(package_name: str) -> str | None:
    """
    Returns the version number of a Python package using pip.
    Returns:
        - version string if found
        - None if package is not found
        - 'error' string if another exception occurs
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
        return None  # pip show succeeded, but no version found (very rare)
    except subprocess.CalledProcessError:
        print(f"\n'{package_name}' package not found.\n")
        return None
    except Exception as e:
        print(f"\nUnexpected error while checking '{package_name}': {e}\n")
        return "error"
    
def clear_screen() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
