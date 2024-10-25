##
## config.py - Singleton to manage global configuration
##
##

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # Initialize configuration values here
            cls._instance.default_path = ".\\data"
            cls._instance.default_audio_ext = ".mp4"  #  ".m4a"
            cls._instance.default_txt_ext = ".txt"
            cls._instance.api_key = "your-api-key"
            cls._instance.openAi_key =  "api-key"
        return cls._instance


config = Config()
