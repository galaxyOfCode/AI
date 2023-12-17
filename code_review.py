import openai
import pyperclip
from termcolor import colored
import tkinter as tk
from tkinter import filedialog

user_prompt = colored("Select a File: ", "light_blue", attrs=["bold"])
assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])


def code_reviewer(client, model):
    '''
    Reviews a code file.
    
    Allows the user to select a file for openAI to review the code for
    style, performance, readability, and maintainability.  
    '''
    root = tk.Tk()
    root.withdraw()
    print(user_prompt)
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        print(f"Selected file: {file_path}")
        print("Processing...")
        try:
            with open(file_path, "r") as file:
                content = file.read()
                initial_prompt = "You will receive a file's contents as text. Generate a code review for the file.  Indicate what changes should be made to improve its style, performance, readability, and maintainability.  If there are any reputable libraries that could be introduced to improve the code, suggest them.  Be kind and constructive.  For each suggested change, include line numbers to which you are referring."
                messages = [
                    {"role": "system", "content": initial_prompt},
                    {"role": "user", "content": f"Code review the following file: {content}"}
                ]
        except PermissionError:
            print("Error: Permission denied when trying to read the file.")
            return
        except OSError:
            print("Error: An error occurred while reading from the file.")
            return
        try:
            res = client.chat.completions.create(
                model=model,
                messages=messages
            )
            content = res.choices[0].message.content
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)
            return
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
            return
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
            return
        print(f"{assistant_prompt} {content}")
        pyperclip.copy(content)
        root.destroy()
        return
    else:
        print("No file selected or dialog canceled.\n")
        root.destroy()
        return
