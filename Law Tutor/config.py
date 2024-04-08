import os
from configparser import ConfigParser


class Config:
    def __init__(self, config_file="config.ini"):
        self.cfg = ConfigParser()
        self.cfg.read(config_file)

        self.STOP = 10
        self.MAX_TOKENS = self.cfg.getint("OPENAI", "MAX_TOKENS")
        self.GPT3_MODEL = self.cfg["OPENAI"]["GPT3_MODEL"]
        self.GPT4_MODEL = self.cfg["OPENAI"]["GPT4_MODEL"]
        self.FREQ_PENALTY = self.cfg.getfloat("OPENAI", "FREQ_PENALTY")
        self.CHAT_TEMP = self.cfg.getfloat("OPENAI", "CHAT_TEMP")
        self.TUTOR_TEMP = self.cfg.getfloat("OPENAI", "TUTOR_TEMP")
        self.IMG_MODEL = self.cfg["OPENAI"]["IMG_MODEL"]
        self.QUALITY = self.cfg["OPENAI"]["QUALITY"]
        self.WHISPER_MODEL = self.cfg["OPENAI"]["WHISPER_MODEL"]
        self.TTS_MODEL = self.cfg["OPENAI"]["TTS_MODEL"]
        self.TTS_VOICE = self.cfg["OPENAI"]["TTS_VOICE"]
        self.api_key = self.get_api_key()

    def get_api_key(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables.")
        return api_key
