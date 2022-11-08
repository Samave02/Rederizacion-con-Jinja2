import requests
import pandas as pn
from jinja2 import Environment, FileSystemLoader
# url de Cat Fact API
url = 'https://catfact.ninja/facts'
res = requests.get(url).json()
i = 1
# Lista que almacenara cada paquete de objetos de cada una de las paginas
listaDatos = []
# recorrido sobre las 34 paginas 
while i < 35:
    i += 1
    # de las claves principales de json se ingresa a links con la finalidad de tierar sobre las paginas que pueden tener información
    links = res['links']
    # Acumula la informacion contenida en data del json
    listaDatos = listaDatos + res['data']
    for item in links:
        # Se itera sobre aca elemento de los links evaluando si existe o no un proximo link, si existe
        # accede al proximo link asigando este como la nueva URL
        if item['label'] == 'Next':
           if item['url'] != None:
                url = item['url']
                # genera el nuevo res de la nueva paguina
                res = requests.get(url).json()
    #Convierto la lista que almaceno la información en un DataFramer            
    datosGatos = pn.DataFrame(listaDatos)

fileLoader = FileSystemLoader('templates')
env = Environment(loader=fileLoader)

# renderizado del template de jinja2
render = env.get_template('datosGatos.html').render(datosGatos=datosGatos)
documentoHtml = 'index.html'
# se establece el metodo de escritura y la ruta de acceso
with open(f"./site/{documentoHtml}","w") as doc:
    doc.write(render)