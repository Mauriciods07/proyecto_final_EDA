import requests
import nltk
import numpy

valores = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
T = "Textos/"
t = ".txt"
    
def abrir_archivos():
    print("Introduzca el nombre de los textos a analizar")
    print("Los archivos deben estar en archivos de extensión .txt")
    print("No es necesario anotar la extensión en este espacio")
    documento01 = input("¿Cuál es su primer documento?: ")
    documento02 = input("¿Cuál es su segundo documento?: ")

    with open(T + documento01 + t, "r", encoding = 'utf8') as doc:
        texto1 = doc.read()
    with open(T + documento02 + t, "r", encoding = 'utf8') as doc:
        texto2 = doc.read()
    return documento01, documento02, texto1, texto2

print("Bienvenido al SAE (Sistema de Análisis Estilómetrico)")
print("En este programa podrás encontrar varias opciones para analizar y comparar dos textos distintos")
print("")
documento01, documento02, texto1, texto2 = abrir_archivos()
promedio = lambda numero1, numero2 : numero1 / numero2
            
#Declarar funciones

#Imprime las opciones del programa, ayuda a no saturar el cuerpo principal del código
def opciones(num):
    if num == 1:
        print("Seleccione una opción:")
        print("1. Riqueza léxica")
        print("2. Dice Smilarity")
        print("3. Análisis POS")
        print("4. Análisis de datos")
        print("5. Ayuda")
    elif num == 2:
        print("Seleccione una categoría gramatical")
        print("1. Adjetivo")
        print("2. Sustantivo")
        print("3. Verbo")
        print("4. Adverbio")
        print("5. Determinante")
        
#Imprime la ayuda por si no se conocen las herramientas de análisis
def imprimir_ayuda():
    with open("help.txt", "r", encoding = "utf8") as doc1:
        ayuda = doc1.read()
        print(ayuda)
        print("")
    
#Conseguir el etiquetado de las categorías gramaticales de ambos textos
def Etiquetado_POS():
    #Código copiado del servicio Freeling http://www.corpus.unam.mx/servicio-freeling/
    files = {'file': open(T + documento01 + t, 'rb')}
    params = {'outf': 'tagged', 'format': 'json'}
    url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
    r = requests.post(url, files=files, params=params)
    obj1 = r.json()
    
    files = {'file': open(T + documento02 + t, 'rb')}
    params = {'outf': 'tagged', 'format': 'json'}
    url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
    r = requests.post(url, files=files, params=params)
    obj2 = r.json()
    
    return obj1, obj2

POS_TEXTO1, POS_TEXTO2 = Etiquetado_POS()

#Riqueza_lexica se encarga de contar el número de palabras de cada texto. Con el número que salga de la razón, se puede hacer una estimación
#Si el número es mayor a 1, los textos, posiblemente, pertenecen al mismo autor. Si el número es menor a 1, los textos no tienen una similitud muy amplia
def Riqueza_lexica():
    print("Riqueza léxica")
    dato1 = len(texto1) / len(set(texto1))
    dato2 = len(texto2) / len(set(texto2))
    
    prom = promedio(dato1, dato2)
    if prom > 1:
        print("Los textos tienen una riqueza léxica similar, por lo tanto, ambas muestras son similares")
    else:
        print("Los textos tienen una riqueza léxica distante, por lo tanto, las muestras no son similares")
    return prom
        
#Esta función obtiene las palabras en común que tienen ambos textos y las divide entre la suma de las palabras totales de ambos textos
def Dice_similarity():
    print("Dice Similarity")
    cont = 0
    WORDS1 = []
    WORDS2 = []
    COMMON_WORDS = []
    token = 'token'
    lemma = 'lemma'
    i = 50
    
    for oracion in POS_TEXTO1:
        for palabra in oracion:
            WORDS1.append(palabra[lemma])
                
    for oracion in POS_TEXTO2:
        for palabra in oracion:
            WORDS2.append(palabra[lemma])
    
    for palabra in WORDS1:
        if palabra in WORDS2:
            if palabra not in COMMON_WORDS:
                cont = cont + 1
                COMMON_WORDS.append(palabra)

    print("Palabras comunes |", len(COMMON_WORDS))
    print("Palabras texto 1 |", len(WORDS1))
    print("Palabras texto 2 |", len(WORDS2))
    print("Acercamiento     | "+str((len(COMMON_WORDS))/(len(WORDS1) + len(WORDS2) - len(COMMON_WORDS))))
    return (2*len(COMMON_WORDS))/(len(WORDS1) + len(WORDS2))
 
#Esta función busca una categoría gramatical en específico por medio de la etiqueta obtenida con Freeling. Divide el total de veces que se repite dicha categoría y la divide entre el total de palabtas en el texto. Esto lo hace con cada archivo.
#Finalmente, divide el promedio, nuevamente, entre sí. Si el número es cercano a 1, significa que los textos son similares.
#Las cinco categorías gramaticales disponibles son adjetivos, sustantivos, verbos, adbverbios y determinantes.
def Contar_pos(categoria):
    print("Análisis POS")
    #Selecciona la etiqueta que se va a analizar
    if categoria == 1:
        letra = 'A'
        pos = 'adjetivo'
    elif categoria == 2:
        letra = 'N'
        pos = 'sustantivo'
    elif categoria == 3:
        letra = 'V'
        pos = 'verbo'
    elif categoria == 4:
        letra = 'R'
        pos = 'adverbio'
    elif categoria == 5:
        letra = 'D'
        pos = 'determinante'
        
    categoria = 0
    for oracion in POS_TEXTO1:
        for palabra in oracion:
            if palabra['tag'].startswith(letra):
                categoria += 1
    print("Hay {} {}s en el texto {}.txt".format(categoria, pos, documento01))
    categoria2 = 0
    for oracion in POS_TEXTO2:
        for palabra in oracion:
            if palabra['tag'].startswith(letra):
                categoria2 += 1
    print("Hay {} {}s en el texto {}.txt".format(categoria2, pos, documento02))
    aprox = promedio(categoria, categoria2)
    aprox = round(aprox, 1)
    print("Aproximación: ", aprox)
    if aprox in valores:
        print("Parece que los textos son similares")
    else:
        print("Parece que los textos no son similares")
    cadena = 'Categoría gramatical: ' + pos
    return cadena, aprox

POS_TEXTO1, POS_TEXTO2 = Etiquetado_POS()
lista = {}

while True:
    
    print("")
    opciones(1)
    opcion = int(input("¿Qué desea hacer?: "))
    print("")
    
    if opcion is 1:
        lista["Riqueza léxica"] = Riqueza_lexica()
    elif opcion is 2:
        lista["Dice similarity"] = Dice_similarity()
    elif opcion is 3:
        opciones(2)
        POS = int(input("¿Qué categoría gramatical necesitas?: "))
        print("")
        texto, a = Contar_pos(POS)
        lista[texto] = a
    elif opcion is 4:
        print("Conteo general")
        datos = 0
        if len(list(lista)) <= 1:
            print("Se necesitan más datos para continuar")
            print("Por favor, haga otra prueba.")
        else:
            datos = sum(lista.values())
            resultado = promedio(datos, len(list(lista)))
            for elemento in list(lista):
                print("En {}, se obtuvo un resultado de {}".format(elemento, lista.get(elemento)))
            print("")
            print("El promedio de información analizada hasta el momento es igual a {}".format(resultado))
            print("Mientras más próximo esté el resultado a 1, más similitud existe entre los textos")
    elif opcion is 5:
        imprimir_ayuda()
    elif opcion is 6:
        break
    else:
        print("Opción no válida")
    
    print("")
    print("¿Desea hacer otra prueba?")
    print("1. Sí")
    print("2. No")
    opcion = int(input())
    if opcion == 2:
        break

print("")
print("Gracias por usar el servicio de SAE")
print("¡Esperamos que vuelva pronto!")