##
## Categories...
##
##

# -*- coding: latin-1 -*-

from enum import Enum

class CategoryType(Enum):
    EP  = "EP"
    SPA = "SPA"
    SD  = "SD"
    TEA = "TEA"

class CategoryItem:
    # Constructor method: initializes the object
    def __init__(self, ctype, text):
        self.cType = ctype
        self.text  = text
    

class CategoryType(object):
    # Constructor method: initializes the object
    def __init__(self, name, sigla, desc, samples, sep):
        self.name  = name
        self.sigla = sigla
        self.desc  = desc
        self.examples = samples
        self.sep   = sep
            
    # ver si la uso 
    def add_example(self, text):
        self.examples.append(text)
            


## define categories
catTypes = {}

catTypes["EP"]  = CategoryType("Entidades", "EP", "son las declaraciones que menciona entidades distintas. Pueden ser objetos, personas, animales, entre otros. En general son sustantivos", ["pajaros","Gente","senora","adultos mayores"],"[]")    
catTypes["SPA"] = CategoryType("Referencia espacial","SPA","son las declaraciones donde se hace referencia a la posicion relativa de las entidades (personas, objetos, animales, etc) dentro del entorno. Tambien incluye direcciones relativas al punto de vista del participante o medidas explicitas",["detras de la barra","a mi izquierda puedo ver"],"{}")
catTypes["SD"]  = CategoryType("Descripcion de entidades", "SD","consiste en cualquier declaracion que describa las propiedades de una entidad. asi como descripciones generales del estado del tiempo",["la silla en la que estoy sentado esta hecha de madera","la sombrilla es roja","mayor de 70 anos","hace mucho calor"],"()")
catTypes["TEA"] = CategoryType("Pensamiento/emocion/accion","TEA","son las declaraciones donde aparece cualquier pensamiento introspectivo o sentimiento emocional. asi como los pensamientos, intenciones y acciones de otras entidades en la escena. Esta ultima categoria no incluye ACCIONES en primera persona",["Tengo la sensacion de estar solo","parece tener prisa","el barman esta preparando un trago","fui caminando"],"<>")



