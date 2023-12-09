import tkinter as tk
from tkinter import filedialog
from termcolor import colored
import configparser

cfg = configparser.ConfigParser()
cfg.read("config.ini")
IMG_MODEL = cfg['PARAM']['IMG_MODEL']
SIZE = cfg['PARAM']['SIZE']
QUALITY = cfg['PARAM']['QUALITY']
MAX_TOKENS = cfg.getint('PARAM', 'MAX_TOKENS')

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
    except:
        print("Something went wrong")
        print("Exiting...")
        return
