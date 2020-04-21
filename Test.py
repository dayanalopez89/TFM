import random
import xlrd
import numpy as np
import pandas as pd
from deap import base
from deap import creator
from deap import tools


################################################################################
#FUNCIÓN DE EVALUACIÓN
def evaluator(individual):
    #Aquí se debe calcular la diferencia entre el día que más horas lectivas posee
    #y el día que menos
    l=len(individual)
    result=0
    j=0
    sum_monday=0
    sum_tuesday=0
    sum_wednesday=0
    sum_thursday=0
    sum_friday=0
    #Se recorre el vector total.
    #individual es un vector que contiene la info de los grupo-asignatura por bloques
    #de forma consecutiva. Es decir, de 0-19 toda la info del Grupo-Asign1, de 20-30 Grupo-Asing2, etc
    #Además, el vector correspondiente al grupo-asign está la info de todos los bloques horarios.
    #Sabemos que cada día tiene 4 bloques posibles, luego para saber las horas por cada día serían los
    #bloques 0-3 para el lunes, 4-7 para el martes, 8-11 para el miércoles, etc.
    while j < len:
        for i in range(j, j+3):
            sum_monday=sum_monday+individual[i]
        for i in range(j+4, j+7):
            sum_tuesday=sum_tuesday+individual[i]
        for i in range(j + 8, j + 11):
            sum_wednesday = sum_wednesday + individual[i]
        for i in range(j + 12, j + 15):
            sum_thursday = sum_thursday + individual[i]
        for i in range(j + 16, j + 19):
            sum_friday = sum_friday + individual[i]
        j+=20
    minimo=min([sum_monday, sum_tuesday, sum_wednesday, sum_thursday, sum_friday])
    maximo = max([sum_monday, sum_tuesday, sum_wednesday, sum_thursday, sum_friday])
    result=abs(maximo-minimo)
    return result

###################################################################################
#LEER ARCHIVOS CON DATOS DE ENTRADA
#Leemos el archivo excel
file="C:\\Users\\tr5568\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\AsignaturasYGrupos-Dayana.xlsx"
#We want the sheet called Data
read_file=xlrd.open_workbook(file)
sheet=read_file.sheet_by_name("Asignaturas y Grupos")
dict_asignaturas={}
vector_es=[]
vector_eu=[]
vector_en=[]

curso_aux=int(1)
cuatri_aux="Primer cuatrimestre"
for row in range(2,sheet.nrows):
    #Código de asignatura posición 0
    curso=sheet.cell(row,2).value
    cuatri=sheet.cell(row,3).value
    #Si coinciden curso y cuatri de la fila, seguimos metiendo valores en el vector
    if curso==curso_aux and cuatri==cuatri_aux:
        #Columna 5: idioma ES y magistral. Columna 6: idioma ES y laboratorio.
        if int(sheet.cell(row, 5).value)>0:
            for i in range(1, int(sheet.cell(row, 5).value)+1):
                codigo=str(int(sheet.cell(row,0).value))+"-M"+str(i).zfill(2)+"ES"
                vector_es.append(codigo)
        if int(sheet.cell(row, 6).value)>0:
            for i in range(1, int(sheet.cell(row, 6).value)+1):
                codigo=str(int(sheet.cell(row,0).value))+"-GL"+str(i).zfill(2)+"ES"
                vector_es.append(codigo)
        # Columna 7: idioma EU y magistral. Columna 8: idioma EU y laboratorio.
        if int(sheet.cell(row, 7).value) > 0:
            for i in range(1, int(sheet.cell(row, 7).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
        if int(sheet.cell(row, 8).value) > 0:
            for i in range(1, int(sheet.cell(row, 8).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
        # Columna 9: idioma EN y magistral. Columna 10: idioma EN y laboratorio.
        if int(sheet.cell(row, 9).value) > 0:
            for i in range(1, int(sheet.cell(row, 9).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)
        if int(sheet.cell(row, 10).value) > 0:
            for i in range(1, int(sheet.cell(row, 10).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)
    else:
        #Cuando deja de coincidir, significa que estamos en una fila que tiene alguno de los parámetros diferentes.
        #Guardamos la info en el diccionario correspondiente, vaciamos los vectores y metemos
        #el valor de dicha fila. Será el primer valor de la siguiente entrada del diccionario.
        if(curso_aux!="X"): curso_aux=int(curso_aux)
        dict_asignaturas[curso_aux, cuatri_aux, "ES"]=vector_es
        dict_asignaturas[curso_aux, cuatri_aux, "EU"] = vector_eu
        dict_asignaturas[curso_aux, cuatri_aux, "EN"] = vector_en
        curso_aux=curso
        cuatri_aux=cuatri
        vector_es=[]
        vector_eu = []
        vector_en = []
        if int(sheet.cell(row, 5).value)>0:
            for i in range(1, int(sheet.cell(row, 5).value)+1):
                codigo=str(int(sheet.cell(row,0).value))+"-M"+str(i).zfill(2)+"ES"
                vector_es.append(codigo)
        if int(sheet.cell(row, 6).value)>0:
            for i in range(1, int(sheet.cell(row, 6).value)+1):
                codigo=str(int(sheet.cell(row,0).value))+"-GL"+str(i).zfill(2)+"ES"
                vector_es.append(codigo)
        if int(sheet.cell(row, 7).value) > 0:
            for i in range(1, int(sheet.cell(row, 7).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
        if int(sheet.cell(row, 8).value) > 0:
            for i in range(1, int(sheet.cell(row, 8).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
        if int(sheet.cell(row, 9).value) > 0:
            for i in range(1, int(sheet.cell(row, 9).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)
        if int(sheet.cell(row, 10).value) > 0:
            for i in range(1, int(sheet.cell(row, 10).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)

#print(dict_asignaturas)

###################################################################################
#MATRIZ DE INCOMPATIBILIDADES
#Creamos la matriz de incompatibilidades
#Podrán solaparse aquellos grupos que compartiendo curso, cuatri e idioma, sean de tipo laboratorio.
tam=len(dict_asignaturas[1, "Primer cuatrimestre", "ES"])
matrix=np.ones([tam, tam])
incomp_df=pd.DataFrame(matrix, index=dict_asignaturas[1, "Primer cuatrimestre", "ES"], columns=dict_asignaturas[1, "Primer cuatrimestre", "ES"])
#print(incomp_df)

#Creamos un dataframe para tener en indice_fila y col los códigos únicos de cada asignatura.
#Primero lo creamos con 1.0 y después, lo cambiamos por un 0 en los casos en los que
#se trate de dos grupos de laboratorio de diferente asignatura:
for col in incomp_df:
    #print(col)
    if "GL" in col:
        for indice_fila, fila in incomp_df.iterrows():
            #print(indice_fila)
            #print(fila)
            if "GL" in indice_fila and indice_fila!=col:
                incomp_df.at[indice_fila, col]=0

#print(incomp_df)

################################################################################
#INFORMACIÓN SOBRE LABORATORIOS
#Leemos la información de la hoja Laboratorios
laboratorios_df=pd.read_excel(file, sheet_name="Laboratorios", header=0, index_col=False)
#print(laboratorios_df)

################################################################################
#ALGORITMO GENÉTICO
#creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
#creator.create("Individual", list, fitness=creator.FitnessMin)


#Ejemplo cuatrimestre 2, 1º curso
# Existen 34 grupos y 20 módulos a la semana.
# En total, el tamaño del array sería 34x20=680 posiciones
# Necesario crear una función que pase una matriz ixj a un vector
# Y viceversa. Creo que simplificaría el tema.


#De esta forma, creamos los individuos, estarán formados
# por 1 o 0, en función de si se imparte clase durante ese bloque o no.
#IND_SIZE=680
#toolbox = base.Toolbox()
#toolbox.register("attr_bool", random.randint, 0, 1)
#toolbox.register("individual", tools.initRepeat, creator.Individual,
 #                toolbox.attr_bool, n=IND_SIZE)

#Ahora creamos una población de individuos. Empezamos con 100
#toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#toolbox.population(n=100)