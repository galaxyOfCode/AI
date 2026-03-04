"""
This module defines the Config class, which is responsible for loading and managing configuration settings
"""

import os
from configparser import ConfigParser


class Config:
    """Loads configuration settings from a file and environment variables."""

    def __init__(self, config_file="config.ini"):
        self.cfg = ConfigParser()
        self.cfg.read(config_file)

        self.max_tokens = self.cfg.getint("OPENAI", "max_tokens")
        self.faster_model = self.cfg["OPENAI"]["faster_model"]
        self.better_model = self.cfg["OPENAI"]["better_model"]
        self.asst_model = self.cfg["OPENAI"]["asst_model"]
        self.freq_penalty = self.cfg.getfloat("OPENAI", "freq_penalty")
        self.chat_temp = self.cfg.getfloat("OPENAI", "chat_temp")
        self.asst_temp = self.cfg.getfloat("OPENAI", "asst_temp")
        self.img_model = self.cfg["OPENAI"]["img_model"]
        self.quality = self.cfg["OPENAI"]["quality"]
        self.vision_model = self.cfg["OPENAI"]["vision_model"]
        self.transcribe_model = self.cfg["OPENAI"]["transcribe_model"]
        self.tts_model = self.cfg["OPENAI"]["tts_model"]
        self.tts_voice = self.cfg["OPENAI"]["tts_voice"]
        self.api_key = self.get_api_key()

    def get_api_key(self) -> str:
        """Retrieves the OpenAI API key from environment variables."""

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables.")
        return api_key
