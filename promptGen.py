
##
## prompt generator using the categories
## 
##

from category import catTypes,  CategoryItem, CategoryType
       

class PromptGenerator:
    def __init__(self):
        self.rol = 1                ## x si queremos definir prompt segun roles...
        self.text = None
    
    def getPrompt(self,text,samples=0):
        self.text = text
        prompt = self.getBasicPrompt() if not samples else self.getPromptWithSamples(samples)
        
        # Add the text to categorize
        #prompt += f"\ngive me this Text marking categories:\n{text}\n"
        prompt += f"\nmarcar este texto y devolver solo el texto marcadoset:\n{text}\n"

        return prompt
        

    # deberia recibir un subject como parametro... x ahora va asi... pero text deberia ser subject
    def getBasicPrompt(self):
        #prompt = "Please categorize the following text according to these categories and give the text marked using the separators for each category as following:\n\n"
        #prompt = "Having these categories:\n\n"
        prompt = "Definimos las siguientes categorias:\n\n"
        
        # Loop through the category types and their descriptions
        for sigla, category in catTypes.items():
            prompt += f"{category.name} ({sigla}): {category.desc}\n"
            prompt += f"marcar con:{category.sep}\n"
                        
        prompt += "Ejemplo\n"                
        prompt += "texto: Si me imagino que estoy sentada en una playa de arena blanca en una hermosa bahia tropical minimamente estoy tomando algun trago acompanada de una amiga se me ocurre vacaciones todo pago o pagado a futuro, dios proveera"
        prompt += "texto marcado: Si me imagino que estoy sentada en una [playa] de (arena blanca) en una [hermosa bahia tropical], minimamente estoy tomando algun trago <acompañada de una [amiga], se me ocurre <vacaciones todo pago o pagado a futuro>, <dios proveera>" 

        return prompt
    
    def getPromptWithSamples(self, samples):
        prompt = self.getBasicPrompt()
                
        # Loop through the category types and their descriptions
        for sigla, category in catTypes.items():
            prompt += f"({sigla}): {category.examples}\n"
            samples -=1
            if samples == 0: break
                
        return prompt
    
    
    def getPromptWithCorrected(self, ctext):
        prompt = self.getBasicPrompt()

        prompt += "\n the corrected text is as following: \n" + ctext

        return prompt
    

    
    

