##
## dependencies:
## pip install openai google-cloud-speech
## pip install json
## pip install colorama
##
# -*- coding: latin-1 -*-

#from cmd import Cmd
import os
import json 
import re
import json
from google.cloud import speech

from subject import Subject
#from google.cloud.speech import enums, types
#from google.cloud.speech import types

from colorama import Fore, Style, init
## init colorama
init(autoreset=True)

from cmdProcessor import CmdProcessor

# Initialize Google Speech Client
#client = speech.SpeechClient()


def main():
    # Get subject name from the user
    
    shell = CmdProcessor()
    
    shell.clear_console()
    shell.run()


if __name__ == "__main__":
    main()
