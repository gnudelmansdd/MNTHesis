
##
## Subject Class
## mantiene la estructura de cada subject
##

from config import config

from category import catTypes,  CategoryItem, CategoryType

from correctedText import CorrectedText

class Subject(object): 
    
    # Constructor method: initializes the object
    def __init__(self, name, age=None):
        self.name = name  
        self.age = age    
        self.txt_fname   = os.path.join(config.default_path, f"{name+config.default_txt_ext}")
        self.audio_fname = os.path.join(config.default_path, f"{name+config.default_audio_ext}")
        self.text = find_and_process(self.txt_fname, self.audio_fname) 
        self.corrected_text = CorrectedText(self.text)

        
    ## Transcribe the audio file to TXT
    def transcribe_audio(self, audio_file):
        """Transcribes audio using le Cloud Speech API."""
      
        return self.text
    
    def setCorrectedText(self, text):
        ## alguien deberia generar el corrected Text     esta y la de abajo es medio lo mismo... ver con cual llamo a la API....
        self.corrected_text = CorrectedText(text)
        self.corrected_text.update()
        print(text)
    
    ## correct the text . using the API should create a prompt and call the api....
    def correct_text(self, profile = None):
        #self.corrected_text = CorrectedText("this a (text) I need {this text red} because <is> enclosed by and [this text green] because is <enclosed> by the secnod is {nada} veremos..")
        ## llamar a la API y corregir
        self.corrected_text = CorrectedText(self.text)
        print("Correcting text using gpt API") ## profile es para definir quien lo esta corrigiendo...
        
    def show(self):
        print("Name:"+self.name)
        print("Original Text:")
        print(self.text)
        if self.corrected_text is None:
            print("NO corrected Text")
        else:
            print("Corrected Text:")
            #self.corrected_text.update()
            self.corrected_text.show()

    def update(self):
        self.corrected_text.update()
        
              

        
    
import os
import glob

##
## aux functions.... should be in another file maybe
##
##
def find_and_process(txt_fname, audio_fname):
        # Search for .txt and .m4a files
    
    txt_file   = glob.glob(txt_fname) 
    audio_file = glob.glob(audio_fname) 

    content = ""
    if txt_file:
        print(f"Found text file: {txt_file[0]}")
        with open(txt_file[0], 'r') as file:
            content = file.read()
            print("Loading text content:")
            #print(content)
    elif audio_file:
        print(f"Found audio file: {audio_file[0]}")
        #transcribe_audio(m4a_file[0])
    else:
        print("Subject File not found."+txt_fname)

    return content


## resolve el load *
def process_files_by_name(name):
    data_folder = './data'
    found = False  # Track if any files were found with the given name

    for filename in os.listdir(data_folder):
        if not os.path.isfile(filename):    # skip subfolders
            continue

        if filename.startswith(name) and filename.endswith(('.txt', '.mp3')):
            file_path = os.path.join(data_folder, filename)
            found = True

            if filename.endswith('.txt'):
                manage_txt(file_path)
            elif filename.endswith('.mp3'):
                transcribed_text = transcribe(file_path)
                manage_txt(transcribed_text)  # Call manage_txt with the transcribed text
    
    if not found:
        print(f"No files found with the name '{name}' in {data_folder}")

            

            
            

        
    



