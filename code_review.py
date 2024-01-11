import openai
import pyperclip
from termcolor import colored
import tkinter as tk
from tkinter import filedialog
from errors import handle_openai_errors, handle_file_errors


def code_review(client, model) -> str:
    """
    Reviews a code file.
    
    Allows the user to select a file for openAI to review the code for
    style, performance, readability, and maintainability.  
    """
    
    user_prompt = colored("Select a File: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])
    root = tk.Tk()
    root.withdraw()
    print(user_prompt)
    try:
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            print(f"Selected file: {file_path}")
            print("Processing...")
        else:
             print("No file selected")
             return
        with open(file_path, "r") as file:
            content = file.read()
            initial_prompt = "You will receive a file's contents as text. Generate a code review for the file.  Indicate what changes should be made to improve its style, performance, readability, and maintainability.  If there are any reputable libraries that could be introduced to improve the code, suggest them.  Be kind and constructive.  For each suggested change, include line numbers to which you are referring."
            messages = [
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": f"Code review the following file: {content}"}
            ]
        try:
            res = client.chat.completions.create(
                model=model,
                messages=messages
            )
            content = res.choices[0].message.content
        except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
                content = handle_openai_errors(e)
                print(f"{assistant_prompt} {content}")
        print(f"{assistant_prompt} {content}")
        pyperclip.copy(content)
        root.destroy()
        return
    except (PermissionError, OSError, FileNotFoundError) as e:
            content = handle_file_errors(e)
            print(f"{assistant_prompt} {content}")
