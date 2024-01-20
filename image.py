import openai
import pyperclip
from termcolor import colored
import tkinter as tk
from tkinter import filedialog
from errors import (handle_request_errors,
                    handle_openai_errors, handle_file_errors)


def generate_image(client, model, quality) -> str:
    """
    This will allow the user to input a prompt and openAI will create an image based on the prompt.  IMG_MODEL is the image model that will be used. SIZE is the size of the image.  If IMG_MODEL is not DALL-E-3, then the user can select the number of images, otherwise it will be 1 image.
    """
    
    image_prompt = colored("Image Description: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])
    try:
        prompt = input(image_prompt)
        if (model != "dall-e-3"):
            n = int(input("\nNumber of Images: "))
            result = client.images.generate(
                model=model,
                prompt=prompt,
                n=n,
            )
        else:
            result = client.images.generate(
                model=model,
                prompt=prompt,
                quality=quality,
                n=1
            )
        image_url = result.data[0].url
        print(f"{assistant_prompt} {image_url}")
        pyperclip.copy(image_url)
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        print(content)
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return
    except Exception:
        print("Something went wrong")
        print("Exiting...")
        return


def describe_image(api_key, model, max_tokens) -> str:
    """The user can select an image and ask for a description"""

    import requests
    import base64
    from requests.exceptions import HTTPError, Timeout, RequestException

    user_prompt = colored("Select a File: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])
    root = tk.Tk()
    root.withdraw()
    print(user_prompt)
    image_path = filedialog.askopenfilename(title="Select a File")
    if image_path:
        print(f"Selected file: {image_path}")
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
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }
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
    except:
        error = data["error"]["message"]
        print(f"{assistant_prompt} {error}")
        return
