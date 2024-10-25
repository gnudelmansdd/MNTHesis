##
## CmdProcessor
## 
##

import os
import platform
from subject import Subject

from promptGen import PromptGenerator 

from config import config       ## for api key
import openai                   ## for use the api

## para copiar el prompt al clipboard
import pyperclip  

class CmdProcessor(object):
    
    def __init__(self):
        # Map commands to the methods that handle them
        self.commands = {
            'load'      : (self.load,        "Load a new subject. Use load [fileName] will look for a audio file or a text file for the subject"),
            'change'    : (self.changeSub,   "Change Subject" ),
            'process'   : (self.process,     "Procesa algo..."),
            'transcribe': (self.transcribe,  "Transcribe un audio file"),
            'ls'        : (self.listSubjects,"List several things. [s] subjects in memory [t] texts ... ver"),
            'show'      : (self.show ,       "Show the subject and the corrected Text "),
            'setText'   : (self.setCText,    "Set Corrected Text - manually or cpy & pasting from chatgpt"), 
            'text'      : (self.setText,     "Set text original"), 
            'gen [n]'   : (self.genPrompt,   "Generate Prompt on the current subject [n] if n include n samples of each categories"), 
            'askgpt [n]': (self.askgpt,      "Ask gpt to correct the current subject with n samples"),
            'cls'       : (self.clear_console, "clear the screen console"),
            'help'      : (self.help,        "Show this help."), 
            'exit'      : (self.exit,        "Exit"),
            'quit'      : (self.exit,        "Quit")
            
        }
        self.subjectName = ""
        self.quit = False
        self.args = ""
        self.cmdLine = ""
        self.subject = None         ## current subject
        self.subjectList = []
        self.pomptGen = PromptGenerator()
        

    def run(self):
        while not self.quit:                                                                                                  
            # Get user input
            ## command = input("Enter a command (or 'exit' to quit): ").strip().lower()
            self.cmdLine = input(self.prompt()).strip().lower()

            if len(self.cmdLine) == 0:
                continue

            parse   = self.cmdLine.split()
            command = parse[0]
            self.args = parse[1:]
            # Find matching commands based on partial input
            matched_commands = [cmd for cmd in self.commands if cmd.startswith(command)]

            #print(matched_commands)

            if len(matched_commands) == 1:
                # If only one match, execute the corresponding method                                                
                self.commands[matched_commands[0]][0]()
            elif len(matched_commands) > 1:
                # If multiple matches, ask for clarification
                print(f"Ambiguous command: '{command}'. Possible matches: {', '.join(matched_commands)}")
            else:
                print(f"Unknown command: {command}")



    # Command handlers
    # ====================
    def load(self):
        if len(self.args) <= 0:
            print("Must specify filename")    
            return 
        
        names = []
        if self.args[0] == '*':
            names = loadMultipleSubject()
        else:
            names.append(self.args[0])

        for name in names:    
            s = self.subjectByName(name) 
            # new subject
            if s is None:
                self.subjectName = name                
                self.subject = Subject(name)
                self.subjectList.append(self.subject)
                #self.subject.correct_text()
                print(f"Added subject: {name}")
            else:
                self.subject = s                    
                 
        
    # Process
    def process(self):
        print("Executing process command...")

    # Transcribe
    def transcribe(self):
        print("Executing transcribe command...")
        # Function to transcribe audio
        openai.api_key = config.openAi_key
        try:
            with open(self.subject.audio_fname, 'rb') as audio_file:
                # Send the request to OpenAI's Whisper API
                response = openai.Audio.transcribe(
                    model="whisper-1",  # Specify the model
                    file=audio_file,
                    language="en"  # Specify the language if needed
                )
        
            # Print the transcribed text
            print("Transcription:", response['text'])
            self.subject.text = response['text']

        except Exception as e:
            print("Error during transcription:", str(e))


    ## set the corrected Text
    def setCText(self):
        if not self.subject:
            return self.invalidSubject()        
        
        spc = self.cmdLine.find(' ')   ## the rest of the line....
        self.subject.setCorrectedText(self.cmdLine[spc+1:] if spc != -1 else "")
         
    ## set the Original Text
    def setText(self):
        if not self.subject:
            return self.invalidSubject()        
        
        spc = self.cmdLine.find(' ')   ## the rest of the line....
        self.subject.text = self.cmdLine[spc+1:] if spc != -1 else ""
        self.subject.setCorrectedText("")


    ## ask chat gpt
    def askgpt(self):    
        if not self.subject:
            return self.invalidSubject()        
        
        if not config.openAi_key:
            print("Need a open Ai API KEY")
            return
        
        try:
            openai.api_key = config.openAi_key
            prompt = self.getPromptText(int(self.args[0]) if len(self.args) > 0 else 0) 
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}],
            
            temperature=0.3,  # Controls randomness of responses,
            max_tokens=300,
            frequency_penalty=2
            )
            cText = response.choices[0].message['content']
            print(response)
            cText = self.subject.setCorrectedText(cText)
            return cText
        except Exception as e:
            print(f"Error calling ChatGPT API: {e}")
            return None


    def exit(self):
        print("Thanks for your time. Bye.")
        self.quit = True

        
    def prompt(self):
        return (self.subject.name if self.subject is not None else "None")+": >"
            
    def listSubjects(self):
        for i, subject in enumerate(self.subjectList):
            print(f"{i + 1}. {subject.name}, Age: {subject.age}, Audio File: {subject.audio_fname}\t {subject.corrected_text.getTotalStr()}" )

    def subjectByName(self,name):
        for subject in self.subjectList:
            if subject.name == name:
                return subject
                
        return None # Exit the function if the subject exists

    ## genera Prompt using different Profiles
    def genPrompt(self):
        if not self.subject:
            return self.invalidSubject()
        
        ## x ahora gen con parameto incluye samples
        prompt = self.getPromptText(int(self.args[0]) if len(self.args) > 0 else 0)
        
        pyperclip.copy(prompt)
        print(prompt)

    def getPromptText(self, samples):
        ## x ahora gen con parameto incluye samples
        return self.pomptGen.getPrompt(self.subject.text, samples)
        
    ## ch subject    
    def changeSub(self):
        if len(self.args) <= 0:
            print("Must specify subject name. Subject loaded are: ")
            self.listSubjects()
            return        

        name = self.args[0]

        for subject in self.subjectList:
            if subject.name == name:
                self.subject = subject
                return  # Exit the function if the subject exists
            
        print(f"Subject: {name} not Loaded. Use Load subjectName to work on this subject")            
        
    # actualiza la cantidad de cItems    
    def show(self):
        if not self.subject:
            return self.invalidSubject()
        self.subject.update()
        self.subject.show()

    def clear_console(self):
        # Detect the operating system
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        
    def help(self):
        for cmd, (func,desc) in self.commands.items():
            print(f"{cmd}: {desc}")


    ## mensaje de err comun de todos los cmds    
    def invalidSubject(self):
        print("Must Select a Subject using Load")
        return        



##
## aux functions.... should be in another file maybe
##
##
import os
import glob

# busca el *.txt no la uso x ahora
def subjetctFromFile(name):
    txt_fname   = os.path.join(config.default_path, f"{name+config.default_txt_ext}")
    audio_fname = os.path.join(config.default_path, f"{name+config.default_audio_ext}")

    txt_file   = glob.glob(txt_fname) 
    audio_file = glob.glob(audio_fname) 


    content = ""
    if txt_file:
        print(f"Found text file: {txt_file[0]}")
        with open(txt_file[0], 'r') as file:
            content = file.read()
            print("Loading text content:")
            return Subject(name,content)
    elif audio_file:
        print(f"Found audio file: {audio_file[0]}")
        print("Transcribe Audio File and create the txt File:")

        #transcribe_audio(m4a_file[0])
    else:
        print("Subject File not found."+name)

    return content


## resolve el load *
def loadMultipleSubject():
    data_folder = config.default_path
    found = False  # Track if any files were found with the given name

    subjectNames = []
    print (data_folder)
    for filename in os.listdir(data_folder):
        #if not os.path.isfile(filename):    # skip subfolders
        #    continue

        if filename.endswith((config.default_txt_ext, config.default_audio_ext)):
            subjectNames.append( os.path.splitext(os.path.basename(filename))[0] )
            found = True
            
    
    if not found:
        print(f"No subject files found with the name in {data_folder}")

    return subjectNames

            
