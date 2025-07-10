import openai
import os
import pyperclip
from termcolor import colored
import tkinter as tk
from tkinter import filedialog

from errors import handle_openai_errors, handle_file_errors
from PyPDF2 import PdfReader


def extract_text_from_file(file_path) -> str:
    """
    Extracts text from a file. Supports both text files and PDFs.
    """
    _, ext = os.path.splitext(file_path)  # Get file extension
    ext = ext.lower()

    if ext == ".txt":
        with open(file_path, "r") as file:
            return file.read()
    elif ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {e}")
    else:
        raise ValueError("Unsupported file type. Please select a .txt or .pdf file.")

def doc_review(client, model) -> None:
    """
    Reviews a document (text file or PDF).

    Allows the user to select a file and ask a question about its contents.
    """
    def colored_prompt(text, color):
        return f"\033[{color}m{text}\033[0m"

    file_prompt = colored("Select a File: ", "light_green", attrs=["bold"])
    user_prompt = colored("You: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])

    root = tk.Tk()
    root.withdraw()

    print(file_prompt)
    try:
        # File selection dialog
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")]
        )
        if not file_path:
            print("No file selected")
            return

        # User input
        user_input = input(user_prompt)

        # Extract text content
        try:
            file_content = extract_text_from_file(file_path)
        except ValueError as e:
            print(f"{assistant_prompt} {e}")
            return

        # Prepare initial prompt and messages
        initial_prompt = (
            "You will receive a document. Please review the document and provide "
            "answers to the user's prompt based on the contents of the document. "
            "If it will help the user, please provide references to page numbers."
        )
        messages = [
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": f"{user_input}\n\nDocument Content:\n{file_content}"}
        ]

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            content = response.choices[0].message.content
        except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
            content = handle_openai_errors(e)
            print(f"{assistant_prompt} {content}")
            return

        # Output response
        print(f"{assistant_prompt} {content}")
        pyperclip.copy(content)
        
    except (PermissionError, OSError, FileNotFoundError) as e:
        content = handle_file_errors(e)
        print(content)
        return
    except Exception as e:
        print(f"{assistant_prompt} An unexpected error occurred: {e}")
    finally:
        root.destroy()
        