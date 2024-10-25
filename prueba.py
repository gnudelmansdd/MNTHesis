
from config import config       ## for api key
import openai


openai.api_key = config.openAi_key 

messages = [
    {"role": "system", "content": "sos un especialista en lenguaje. Clasifica textos categorias y las marca usando marcadores"},
    {"role": "assistant", "content": "Entidades (EP): son las declaraciones que menciona entidades distintas. Pueden ser objetos, personas, animales, entre otros. En general son sustantivos marcar con:[] Referencia espacial (SPA): son las declaraciones donde se hace referencia a la posicion relativa de las entidades (personas, objetos, animales, etc) dentro del entorno. Tambien incluye direcciones relativas al punto de vista del participante o medidas explicitas marcar con:{} Descripcion de entidades (SD): consiste en cualquier declaracion que describa las propiedades de una entidad. asi como descripciones generales del estado del tiempo marcar con:() Pensamiento/emocion/accion (TEA): son las declaraciones donde aparece cualquier pensamiento introspectivo o sentimiento emocional. asi como los pensamientos, intenciones y acciones de otras entidades en la escena. Esta ultima categoria no incluye ACCIONES en primera persona marcar con:<>"},
    {"role": "assistant", "content": "marcar texto es poner las categorias en cada separador las entidades entre [] y las demas con sus marcadores "},
    {"role": "user", "content" : "marcar bueno ahi me trae como olor a viejo, pero no olor a viejo malo, de nada de historia, es como un libro viejo que lo oles el mismo papel tiene ese olor caracteristico "}  
 # pero que es lindo como que mucha historia mucho pasado ahi y te trae un monton de recuerdos vivos. Por ejemplo dice muchas exhibiciones yo lo que me estoy imaginando es el museo de ciencia que esta en el parque centenario que ahi esqueletos figuras asi que esta buenisimo te llama mucho la atencion me imagino mucho lo visual como para todos lados que hay muchos estimulos, una cosa y la otra, mucha carteleria, pero me viene a la cabeza ese olor a antiguo a viejo que no es negativo, olor a historia, que mas? tambien muchas luces porque muchos museos de exhibiciones hay tambien, en mi museo que me estoy imaginando en este momento hay muchas luces, hay mucho estimulo porque me encantan los museos que son asi como para poner en practica todos los sentidos como el museo de prohebido no tocar que esta en recoleta que es para niÃ±os o niÃ±os grandes encontces me imagino eso, pero ahi me imagino el silencio, sola, probablemente sola, no estoy acompaÃ±ada como en la playa, sola leyendo mucho, mucho el tema del olfato como dije y viendo para todos lados, como que no terminas de leer una cosa que vas a otra y caminas y hay mucho eco en el piso porque suelen ser salas donde no hay mucha gente, entonces caminas, te vas encontrando y vas pasando de cosas y de paso te vas nutriendo, eso me encanta de los museos de historia, en esta cabeza para mi es un museo de historia natural, me imagino con los animalitos con los cuerpos de los animalitos y luces muy tenues bajas, porque si bien como que yo dije quera en una parte que era luminoso pero me imagino como cositas interactivas, como jueguitos que siempre hay en los museos como el de recoleta pero en si como la iluminacion central es baja siempre enfocada en las cosas que te estan mostrando pero me lo re imagino eso, un lugar calmo, eco y olor como a anatiguo a historia, creo que hasta ahi"}


]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

print(response.choices[0].message["content"])