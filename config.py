import os
from configparser import ConfigParser


class Config:
    def __init__(self, config_file="config.ini"):
        self.cfg = ConfigParser()
        self.cfg.read(config_file)

        self.MENU_MAX = 13
        self.MAX_TOKENS = self.cfg.getint("OPENAI", "MAX_TOKENS")
        self.FASTER_MODEL = self.cfg["OPENAI"]["FASTER_MODEL"]
        self.BETTER_MODEL = self.cfg["OPENAI"]["BETTER_MODEL"]
        self.ASST_MODEL = self.cfg["OPENAI"]["ASST_MODEL"]
        self.FREQ_PENALTY = self.cfg.getfloat("OPENAI", "FREQ_PENALTY")
        self.CHAT_TEMP = self.cfg.getfloat("OPENAI", "CHAT_TEMP")
        self.ASST_TEMP = self.cfg.getfloat("OPENAI", "ASST_TEMP")
        self.IMG_MODEL = self.cfg["OPENAI"]["IMG_MODEL"]
        self.QUALITY = self.cfg["OPENAI"]["QUALITY"]
        self.VISION_MODEL = self.cfg["OPENAI"]["VISION_MODEL"]
        self.WHISPER_MODEL = self.cfg["OPENAI"]["WHISPER_MODEL"]
        self.TTS_MODEL = self.cfg["OPENAI"]["TTS_MODEL"]
        self.TTS_VOICE = self.cfg["OPENAI"]["TTS_VOICE"]
        self.api_key = self.get_api_key()

    def get_api_key(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables.")
        return api_key
