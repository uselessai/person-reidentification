import bibtexparser

# Abre el archivo .bib y lo lee
with open(r'path\Tesis-Seminario-Articulo-00Reviews-GAN-ReID.bib', 'r', encoding='utf8') as bibtex_file:
    bib_database_reviews = bibtexparser.load(bibtex_file)
with open(r'path\Tesis-Seminario-Articulo-01Articulaciones.bib', 'r', encoding='utf8') as bibtex_file:
    bib_database_articulaciones = bibtexparser.load(bibtex_file)

with open(r'path\Tesis-Seminario-Articulo-01TransferStyle.bib', 'r', encoding='utf8') as bibtex_file:
    bib_database_transfer = bibtexparser.load(bibtex_file)

with open(r'path\Tesis-Seminario-Articulo-01Aleatorios.bib', 'r', encoding='utf8') as bibtex_file:
    bib_database_random = bibtexparser.load(bibtex_file)

 




def escribir_archivo(entries, backgroundColor, data, textColor):
   

    with open(r'path\dataset.txt', "a") as text_file:
        # Extrae la información de los campos que quieres
      


        if (len(entries) == 0):
            text_file.write("{" + "\n")
            text_file.write("label:''," + "\n")
            text_file.write("backgroundColor: ['"+ backgroundColor +"']," + "\n")
            text_file.write("abstract: ['']," + "\n")
            text_file.write("  URL: ['']," + "\n")
            text_file.write("  textColor: ''," + "\n")
            text_file.write("  data: [25]," + "\n")
            text_file.write("  year: ''," + "\n")
            text_file.write("},"  + "\n")
            


        for entry in entries:
            text_file.write("{" + "\n")
            text_file.write("label:'" + entry['title'] + "'," + "\n")
            text_file.write("backgroundColor: ['"+ backgroundColor +"']," + "\n")
            if entry.get('abstract') is not None and entry.get('abstract').strip() != '':
                text_file.write("abstract: ['"+  entry['abstract'].replace("'", "") +"']," + "\n")
            else:
                text_file.write("abstract: ['"+  entry['title'] +"']," + "\n")
            
            if entry.get('url') is not None and entry.get('url').strip() != '':
                text_file.write("  URL: ['" + entry['url'] + "']," + "\n")
            elif entry.get('doi') is not None and entry.get('doi').strip() != '':
                text_file.write("  URL: ['https://www.google.com/search?q=" + entry['doi'] + "']," + "\n")
            else :
                text_file.write("  URL: ['https://www.google.com/search?q=" + entry['title'] + "']," + "\n")
            
            text_file.write("  year: '" +  entry['year'] + "'," + "\n")
            text_file.write("  textColor: '" +  textColor+ "'," + "\n")
            # valor que se le da para que se muestren todos iguales
            # en total son 5 por cabeza en total son 100 
            data = 25 / len(entries)
            text_file.write("  data: [" + str(data) + "]," + "\n")
            text_file.write("},"  + "\n")

        
def entries_anios(anio):
# Filtra las entradas por el año 2021
    entries_reviews_anio = [entry for entry in bib_database_reviews.entries if entry.get('year') == anio]
    
    entries_articulaciones_anio = [entry for entry in bib_database_articulaciones.entries if entry.get('year') == anio]
    entries_transfer_anio = [entry for entry in bib_database_transfer.entries if entry.get('year') == anio]
    entries_random_anio = [entry for entry in bib_database_random.entries if entry.get('year') == anio]

    
    color_reviews = "#3a2bff" 
    color_articulaciones = "#fc9303"
    color_transfer = "#FF0000"
    color_random = "#008000"

    if (int(anio) % 2 == 0):
        background = "#F5F5F5"
    else:
        background = "#CDCDCD"

    if (int(anio) == 2021):
        background = "#898989"
    elif (int(anio) == 2020):
        background = "#A4A4A4"
    elif (int(anio) == 2019):
        background = "#BFBFBF"
    elif (int(anio) == 2018):
        background = "#DBDBDB"
    elif (int(anio) == 2017):
        background = "#F7F7F7"
        
        
        


    with open(r'path\dataset.txt', "a") as text_file:
        text_file.write("[" + "\n")

    escribir_archivo(entries_transfer_anio , background , "5", color_transfer)
    escribir_archivo(entries_random_anio , background , "5", color_random)
    escribir_archivo(entries_articulaciones_anio , background , "5", color_articulaciones)
    escribir_archivo(entries_reviews_anio , background , "5", color_reviews)
    
   
    with open(r'path\dataset.txt', "a") as text_file:
        text_file.write("]," + "\n")




with open(r'path\dataset.txt', "w") as text_file:
    text_file.write("datasets: [" + "\n")

entries_anios('2021')

entries_anios('2020')

entries_anios('2019')

entries_anios('2018')

entries_anios('2017')

with open(r'path\dataset.txt', "a") as text_file:
    text_file.write("]" + "\n")
