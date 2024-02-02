from termcolor import colored


def print_menu():
    '''
    Prints the main menu
    '''
    print("\n")
    print("AI Assistant (J. Hall, 2024)")
    print("---------------------------------")
    print(" 1 = 4.0 Law Tutor")
    print(" 2 = 3.5 Law Tutor")
    print(" 3 = 4.0 Chat")
    print(" 4 = 3.5 Chat")
    print(" 5 = Image Generator")
    print(" 6 = Speech-to-Text")
    print(" 7 = Text-to-Speech")
    print(" 8 = List Current Settings")
    print(" 9 = Quit")


def not_numeric() -> None:
    """Error message if menu choice is not numeric"""

    input("\nYou Entered a non-numeric value or wrong format.\nPress <Enter> to continue ... ")


def list_settings(config) -> None:
    """Prints off the hardcoded "Magic Numbers" """

    print("\nCurrent Settings:\n")
    print(colored("GPT3_MODEL: \t", "blue", attrs=["bold"]), config.GPT3_MODEL)
    print(colored("GPT4_MODEL: \t", "blue", attrs=["bold"]), config.GPT4_MODEL)
    print(colored("IMG_MODEL: \t", "blue", attrs=["bold"]), config.IMG_MODEL)
    print(colored("QUALITY: \t", "blue", attrs=["bold"]), config.QUALITY)
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
