import os
import sys
from openai import OpenAI
from termcolor import colored
import tkinter as tk
from tkinter import filedialog
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')
GPT4_MODEL = cfg['PARAM']['GPT4_MODEL']

blue1 = colored("Select a File: ", "light_blue", attrs=["bold"])
red = colored("Assistant: ", "light_red", attrs=["bold"])

# get api_key from user's shell config file#
try:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
except ValueError as e:
    print(f"Error: {e}")
    print("Please ensure that the 'OPENAI_API_KEY' environment variable is set.")
    sys.exit(1)

client = OpenAI()


def code_review(file_path):
    '''
    Selects the file for code reviewer
    '''
    try:
        with open(file_path, "r") as file:
            content = file.read()
        generated_code_review = make_code_review_request(content)
        print(red, generated_code_review)
    except PermissionError:
        print("Error: Permission denied when trying to read the file.")
    except OSError:
        print("Error: An error occurred while reading from the file.")


def make_code_review_request(filecontent):
    '''
    Helper function for code reviewer
    '''
    initial_prompt = "You will receive a file's contents as text. Generate a code review for the file.  Indicate what changes should be made to improve its style, performance, readability, and maintainability.  If there are any reputable libraries that could be introduced to improve the code, suggest them.  Be kind and constructive.  For each suggested change, include line numbers to which you are referring."
    messages = [
        {"role": "system", "content": initial_prompt},
        {"role": "user", "content": f"Code review the following file: {filecontent}"}
    ]
    res = client.chat.completions.create(
        model=GPT4_MODEL,
        messages=messages
    )
    content = res.choices[0].message.content
    return content


def code_reviewer():
    '''
    Allows the user to select a file for openAI to perform code review
    '''
    root = tk.Tk()
    root.withdraw()
    print(blue1)
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        print(f"Selected file: {file_path}")
        code_review(file_path)
    else:
        print("No file selected or dialog canceled.\n")
        return
