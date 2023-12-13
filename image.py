import tkinter as tk
from tkinter import filedialog
from termcolor import colored
import configparser
import pyperclip

cfg = configparser.ConfigParser()
cfg.read("config.ini")
IMG_MODEL = cfg['PARAM']['IMG_MODEL']
SIZE = cfg['PARAM']['SIZE']
QUALITY = cfg['PARAM']['QUALITY']
VISION_MODEL = cfg['PARAM']['VISION_MODEL']
MAX_TOKENS = cfg.getint('PARAM', 'MAX_TOKENS')

blue1 = colored("Select a File: ", "light_blue", attrs=["bold"])
blue2 = colored("Image Description: ", "light_blue", attrs=["bold"])
red = colored("Assistant: ", "light_red", attrs=["bold"])


def image(client):
    '''
    This will allow the user to input a prompt and openAI will create an image based on the prompt.  IMG_MODEL is the image model that will be used. SIZE is the size of the image.  If IMG_MODEL is not DALL-E-3, then the user can select the number of images, otherwise it will be 1 image.
    '''
    try:
        prompt = input(blue2)
        if (IMG_MODEL != "dall-e-3"):
            n = int(input("\nNumber of Images: "))
            res = client.images.generate(
                model=IMG_MODEL,
                prompt=prompt,
                size=SIZE,
                n=n,
            )
        else:
            res = client.images.generate(
                model=IMG_MODEL,
                prompt=prompt,
                size=SIZE,
                quality=QUALITY,
                n=1
            )
        image_url = res.data[0].url
        print(red, image_url)
        pyperclip.copy(image_url)
    except:
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


def vision(api_key):
    '''
    The user can select an image and ask for a description
    '''
    config = configparser.ConfigParser()
    import requests
    from requests.exceptions import HTTPError, Timeout, RequestException
    root = tk.Tk()
    root.withdraw()
    print(blue1)
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
        "model": VISION_MODEL,
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
        "max_tokens": MAX_TOKENS
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
    try:
        assistant_content = data["choices"][0]["message"]["content"]
        print(red, assistant_content)
        pyperclip.copy(assistant_content)
    except:
        error = data["error"]["message"]
        print(red, error)
        return
