import openai
import pyperclip
from termcolor import colored
import tkinter as tk
from tkinter import filedialog

user_prompt = colored("Select a File: ", "light_blue", attrs=["bold"])
image_prompt = colored("Image Description: ", "light_blue", attrs=["bold"])
assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])


def image(client, model, size):
    '''
    This will allow the user to input a prompt and openAI will create an image based on the prompt.  IMG_MODEL is the image model that will be used. SIZE is the size of the image.  If IMG_MODEL is not DALL-E-3, then the user can select the number of images, otherwise it will be 1 image.
    '''
    try:
        prompt = input(image_prompt)
        if (model != "dall-e-3"):
            n = int(input("\nNumber of Images: "))
            res = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                n=n,
            )
        else:
            res = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                n=1
            )
        image_url = res.data[0].url
        print(f"{assistant_prompt} {image_url}")
        pyperclip.copy(image_url)
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
    except KeyboardInterrupt:
        print("Exiting...")
        return
    except Exception:
        print("Something went wrong")
        print("Exiting...")
        return


def encode_image(image_path):
    '''
    Helper function for vision()
    '''
    import base64
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except OSError as e:
        print(e)
        return ""


def vision(api_key, model, max_tokens):
    '''
    The user can select an image and ask for a description
    '''
    import requests
    from requests.exceptions import HTTPError, Timeout, RequestException
    root = tk.Tk()
    root.withdraw()
    print(user_prompt)
    image_path = filedialog.askopenfilename(title="Select a File")
    if image_path:
        print(f"Selected file: {image_path}")
    else:
        print("No file selected or dialog canceled.\n")
        return
    base64_image = encode_image(image_path)
    if (base64_image == ""):
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
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return
    except Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")
        return
    except RequestException as req_err:
        print(f"Error during request: {req_err}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
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
