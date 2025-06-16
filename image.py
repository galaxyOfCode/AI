import base64
import openai
import pyperclip
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from termcolor import colored
import tkinter as tk
from tkinter import filedialog

from errors import (handle_request_errors,
                    handle_openai_errors,
                    handle_file_errors)


def generate_image(client, model, quality) -> None:
    """
    This will allow the user to input a prompt and openAI will create an image based
    on the prompt.  MODEL is the image model that will be used. QUALITY is the quality of the image
    that will be generated (Low, Medium, High).  The image will be copied to the clipboard.
    """

    image_prompt = colored("Image Description: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])
    try:
        prompt = input(image_prompt)
        response = client.images.generate(
            model=model,
            prompt=prompt,
            quality=quality)
        image_url = response.data[0].url
        print(f"{assistant_prompt} {image_url}")
        pyperclip.copy(image_url)
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        print(content)
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return
    except Exception as e:
        print(f"Something went wrong: {e}")
        print("Exiting...")


def describe_image(api_key, model, max_tokens) -> None:
    """The user can select an image and ask for a description"""

    user_prompt = colored("You: ", "light_blue", attrs=["bold"])
    file_prompt = colored("Select a File: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])
    prompt = input(user_prompt)
    root = tk.Tk()
    root.withdraw()
    print(file_prompt)
    image_path = filedialog.askopenfilename(title="Select a File")
    root.destroy()
    if image_path:
        print("Working...")
    else:
        print("No file selected or dialog canceled.\n")
        return
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except (PermissionError, OSError, FileNotFoundError) as e:
        content = handle_file_errors(e)
        print(content)
        return
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [{"type": "text",
                         "text": prompt},
                        {"type": "image_url",
                         "image_url": {
                                 "url": f"data:image/png;base64,{base64_image}"}}]}], "max_tokens": max_tokens}
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
    except (HTTPError, Timeout, RequestException, Exception) as e:
        content = handle_request_errors(e)
        print(f"{assistant_prompt} {content}")
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return
    try:
        content = data["choices"][0]["message"]["content"]
        print(f"{assistant_prompt} {content}")
        pyperclip.copy(content)
    except Exception as e:
        print(f"Something went wrong: {e}")
        error = data["error"]["message"]
        print(f"{assistant_prompt} {error}")
