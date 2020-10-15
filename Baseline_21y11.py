
from Custom_Test_NuevaLectura import lectura_datos_excel
#from Custom_Test_NuevaLectura import check_feasibility
import random
import numpy as np
import pandas as pd
from openpyxl import load_workbook


#FUNCIÓN DE CONSTRUCCIÓN DE INDIVIDUOS
def individual_creator(size):
    aux=0
    individual=[]
    #print("IND_SIZE", str(n))
    for i in range(0, size):
        choice=get_choice()
        if choice==1:
            aux+=1
            if aux>(size * 2 / 20):
                choice=0
        individual.append(choice)
    return individual
################################################################################
#FUNCIÓN PARA ESCOGER EL GEN DENTRO DEL INDIVIDUO
def get_choice():
    f=2/20
    if random.random() <=f:
        return 1
    else:
        return 0

#def crear_ind(n):
#    aleatorios = [random.randint(0,1) for _ in range(n)]
 #   return aleatorios

def check_feasibility(individual):
    # Esta función sirve para comprobar si el individuo
    # cumple o no, las restricciones del problema

    #Restricción sobre los solapamientos de las asignaturas
    ind_df = pd.DataFrame(np.reshape(individual, (tam, 20)), index=asignaturas, columns=bloques)
    matrix=np.reshape(individual, (tam, 20))
    #penalty=penalty + abs(sum(row)
           # - dict_horassemanales[ind_row]) if sum(row) != dict_horassemanales[ind_row] for ind_row, row in ind_df.iterrows()
    #print("DESPUÉS DE BUCLE OPTIMIZADO: ",penalty)

    penalty=0
    for ind_row, row in ind_df.iterrows():
        s = sum(row)
        if s != dict_horassemanales[ind_row]:
            penalty += abs(s - dict_horassemanales[ind_row])


    #Se multiplica la matriz del individuo por su transpuesta. De esta forma tendremos
    #una matriz con dimensiones asignaturas x asinaturas donde cada valor refleja el
    #número de veces que cada grupo i coincide con el grupo j
    new_matrix = matrix.dot(np.transpose(matrix))
    #Creamos un dataframe de dicha matriz
    new_df=pd.DataFrame(new_matrix, index=asignaturas, columns=asignaturas)
    #Multiplicamos ambos dataframes porque no es lo mismo multiplicar matrices que dataframes.
    #De esta forma multiplica aquellos que tienen los mismos index. Así, tendremos una matriz
    #resultado en new_df con valores únicamente para los grupos que son incompatibles.
    new_df=new_df*incomp_df
    #Obtenemos dichos valores
    values=new_df.values
    #Sumamos los valores de la diagonal inferior (sin contar la diagonal principal). Este será
    #el valor de penalización que estamos buscando.
    suma_diagonal_inf=sum(values[np.tril_indices(values.shape[0], -1)])
    penalty+=suma_diagonal_inf
    return penalty


def dif_curso(individual, tam_curso, inicio):
    j = inicio
    #print(inicio)
    sum_monday = 0
    sum_tuesday = 0
    sum_wednesday = 0
    sum_thursday = 0
    sum_friday = 0
    #Multiplicamos el tam del curso por 20 (bloques temporales a la semana)
    #print("FINAL BUCLE: ", tam_curso*20+inicio)
    while j < (tam_curso*20+inicio):
        sum_monday+=sum(individual[j:j+4])
        #print("sum monday", sum_monday)
        sum_tuesday += sum(individual[j+4:j + 8])
        sum_wednesday += sum(individual[j + 8:j + 12])
        sum_thursday +=sum(individual[j + 12:j + 16])
        sum_friday +=sum(individual[j + 16:j + 20])
        j+=20
    minimo = min([sum_monday, sum_tuesday, sum_wednesday, sum_thursday, sum_friday])
    maximo = max([sum_monday, sum_tuesday, sum_wednesday, sum_thursday, sum_friday])
    #print("maximo ", maximo)
    #print("minimo ", minimo)
    result = abs(maximo - minimo)
    #print("INICIO ", inicio)
    #print("TAM CURSO:",tam_curso)
    #print("INDIVIDUO: ", individual)
    #print("RESULT: ", result)
    #print("DIFERENCIA CURSO: ", result)
    return result

def evaluator2(individual):

    keys=dict_ev.keys()
    j=0
    result=0
    for k in keys:
        #print("RESULT ANTES: ", result)
        #print("Key: ", k)
        #print("Len: ", len(dict_ev[k]))
        #print("j: ", j)
        result+=dif_curso(individual, len(dict_ev[k]), j)
        #print("RESULT DESPUÉS: ", result)
        j+=(len(dict_ev[k])*20)
    #print("suma resultado: ", result)
    #print("FEASIBILITY: ", check_feasibility(individual))
    restricciones=check_feasibility(individual)
    vector_restricciones.append(restricciones)
    #if restricciones==0:
    #    print(" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% RESTRICCIONES = 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    result =result+ 10*restricciones
    #print("RESULTADO FINAL: ", result)
    return (result, )

vector_result=[]
vector_restricciones=[]
file="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\AsignaturasGruposProfesorado-20200702-Dayana.xlsx"
dict_asignaturas, dict_horassemanales, dict_profes=lectura_datos_excel(file)
dict_ev={}
dict_ev[1, 1, "ES"]=dict_asignaturas[1, 1, "ES"]
dict_ev[1, 1, "EU"]=dict_asignaturas[1, 1, "EU"]
dict_ev[2, 1, "ES"]=dict_asignaturas[2, 1, "ES"]
dict_ev[2, 1, "EU"]=dict_asignaturas[2, 1, "EU"]
dict_ev[2, 1, "IN"]=dict_asignaturas[2, 1, "IN"]
#dict_ev[3, 1, "ES"]=dict_asignaturas[3, 1, "ES"]
#dict_ev[3, 1, "EU"]=dict_asignaturas[3, 1, "EU"]



tam=len(dict_asignaturas[1, 1, "ES"])+len(dict_asignaturas[1, 1, "EU"])+len(dict_asignaturas[2, 1, "ES"])+len(dict_asignaturas[2, 1, "EU"])+len(dict_asignaturas[2, 1, "IN"])
    #+len(dict_asignaturas[3, 1, "ES"])+len(dict_asignaturas[3, 1, "EU"])
ind_tam=tam*20
asignaturas = dict_asignaturas[1, 1, "ES"]+dict_asignaturas[1, 1, "EU"]+dict_asignaturas[2, 1, "ES"]+dict_asignaturas[2, 1, "EU"]+dict_asignaturas[2, 1, "IN"]
              #+dict_asignaturas[3, 1, "ES"]+dict_asignaturas[3, 1, "EU"]
bloques=['Lunes1', "Lunes2", "Lunes3", "Lunes4", "Martes1", "Martes2", "Martes3", "Martes4",
         "Miércoles1", "Miércoles2", "Miércoles3", "Miércoles4", "Jueves1", "Jueves2", "Jueves3",
         "Jueves4", "Viernes1", "Viernes2", "Viernes3", "Viernes4"]
matrix=np.ones([tam, tam], dtype=np.int)
incomp_df=pd.DataFrame(matrix, index=asignaturas, columns=asignaturas)
pop_tam=ind_tam*30*75
print("IND_TAM: ",ind_tam)
print("POP_TAM: ", pop_tam)
for col in incomp_df:
    #print(col)
    curso_cuatri=int(col.split("-")[2])
    grupo_idioma=col.split("-")[1]
    idioma=grupo_idioma[len(grupo_idioma)-2]+grupo_idioma[len(grupo_idioma)-1]
    #print(curso_cuatri)
    if "GL" in col:
        for indice_fila, fila in incomp_df.iterrows():
            #print(indice_fila)
            #print(fila)
            if ("GL" in indice_fila and indice_fila!=col) or ("GA" in indice_fila and indice_fila!=col):
                incomp_df.at[indice_fila, col]=0

    #Versión nueva lectura (tipo GA existe)
    if "GA" in col:
        for indice_fila, fila in incomp_df.iterrows():
            #print(indice_fila)
            #print(fila)
            if ("GA" in indice_fila and indice_fila!=col) or ("GL" in indice_fila and indice_fila!=col) :
                incomp_df.at[indice_fila, col]=0

    #Versión nueva lectura
    if ("3C" or "IC" or "SI") in col:
         #print("COL: ", col)
         opt = col.split("-")[3]
         #print("OPT: ", opt)
         for indice_fila, fila in incomp_df.iterrows():
             if ("3C" in indice_fila and indice_fila!=col and indice_fila.split("-")[3]!=opt) or ("IC" in indice_fila and indice_fila!=col and indice_fila.split("-")[3]!=opt) or("SI" in indice_fila and indice_fila != col and indice_fila.split("-")[3] != opt):
                incomp_df.at[indice_fila, col]=0
                #print(indice_fila)

    for indice_fila, fila in incomp_df.iterrows():
        curso_cuatri_aux=int(indice_fila.split("-")[2])
        if curso_cuatri_aux!=curso_cuatri:
            incomp_df.at[indice_fila, col] = 0

    for indice_fila, fila in incomp_df.iterrows():
        grupo_idioma_aux=indice_fila.split("-")[1]
        idioma_aux = grupo_idioma_aux[len(grupo_idioma_aux)-2] + grupo_idioma_aux[len(grupo_idioma_aux)-1]
        if idioma_aux!=idioma:
            incomp_df.at[indice_fila, col] = 0

for i in range(0, pop_tam):
    print("Individuo: ", i)
    ind=individual_creator(ind_tam)
    result=evaluator2(ind)
    print("FUNCIÓN OBJETIVO: ", result)
    vector_result.append(result[0])

#print(vector_result)
df_result= pd.DataFrame({"Valor fitness":vector_result[0:1000000]})
#df_result= pd.DataFrame({"Valor fitness":vector_result[0:2]})
df_result_2= pd.DataFrame({"Valor fitness_2":vector_result[1000000:2000000]})
#df_result_2= pd.DataFrame({"Valor fitness_2":vector_result[2:4]})
df_result_3= pd.DataFrame({"Valor fitness_3":vector_result[2000000:3000000]})
#df_result_3= pd.DataFrame({"Valor fitness_3":vector_result[4:6]})
df_result_4= pd.DataFrame({"Valor fitness_4":vector_result[3000000:4000000]})
#df_result_4= pd.DataFrame({"Valor fitness_4":vector_result[6:8]})
df_result_5= pd.DataFrame({"Valor fitness_5":vector_result[4000000:pop_tam]})
#df_result_5= pd.DataFrame({"Valor fitness_5":vector_result[8:10]})
filename="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
                        "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\RESULTADOS\\Resultados_baseline_11y21_test.xlsx"
#df_result= pd.DataFrame(data=vector_result[1:2], columns=["Valor fitness_2"])
df_result.to_excel(filename,sheet_name="Resultados", index=False)

book = load_workbook(filename)
writer = pd.ExcelWriter(filename, engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

df_result_2.to_excel(writer,sheet_name="Resultados_2", index=False)
writer.save()

df_result_3.to_excel(writer,sheet_name="Resultados_3", index=False)
writer.save()

df_result_4.to_excel(writer,sheet_name="Resultados_4", index=False)
writer.save()

df_result_5.to_excel(writer,sheet_name="Resultados_5", index=False)
writer.save()