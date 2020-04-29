import random
import xlrd
import numpy as np
import pandas as pd
from deap import algorithms, base, creator, tools
import multiprocessing

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
    while j < l:
        #for i in range(j, j+4):
        #    sum_monday=sum_monday+individual[i]
        sum_monday+=sum(individual[j:j+4])

        #for i in range(j+4, j+8):
         #   sum_tuesday=sum_tuesday+individual[i]
        sum_tuesday += sum(individual[j+4:j + 8])
        #for i in range(j + 8, j + 12):
         #   sum_wednesday = sum_wednesday + individual[i]
        sum_wednesday += sum(individual[j + 8:j + 12])
        #for i in range(j + 12, j + 16):
            #sum_thursday = sum_thursday + individual[i]
        sum_thursday +=sum(individual[j + 12:j + 16])
        #for i in range(j + 16, j + 20):
            #sum_friday = sum_friday + individual[i]
        sum_friday +=sum(individual[j + 16:j + 20])
        j+=20
    #print("Monday: ", sum_monday)
    #print("Tuesday: ", sum_tuesday)
    #print("Wednesday: ", sum_wednesday)
    #print("Thursday: ", sum_thursday)
    #print("Friday: ", sum_friday)

    minimo=min([sum_monday, sum_tuesday, sum_wednesday, sum_thursday, sum_friday])
    maximo = max([sum_monday, sum_tuesday, sum_wednesday, sum_thursday, sum_friday])
    result=abs(maximo-minimo)
    if not check_feasibility(individual):
        result+=2000
    #print("Result: ", result)
    return (result, )

#print("FUNCIÓN EVAL: ", evaluator(list([1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0])))

##################################################################################

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
dict_horassemanales={}
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
                dict_horassemanales[codigo]=int(sheet.cell(row,14).value)
        if int(sheet.cell(row, 6).value)>0:
            for i in range(1, int(sheet.cell(row, 6).value)+1):
                codigo=str(int(sheet.cell(row,0).value))+"-GL"+str(i).zfill(2)+"ES"
                vector_es.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 15).value)
        # Columna 7: idioma EU y magistral. Columna 8: idioma EU y laboratorio.
        if int(sheet.cell(row, 7).value) > 0:
            for i in range(1, int(sheet.cell(row, 7).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 14).value)
        if int(sheet.cell(row, 8).value) > 0:
            for i in range(1, int(sheet.cell(row, 8).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 15).value)
        # Columna 9: idioma EN y magistral. Columna 10: idioma EN y laboratorio.
        if int(sheet.cell(row, 9).value) > 0:
            for i in range(1, int(sheet.cell(row, 9).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 14).value)
        if int(sheet.cell(row, 10).value) > 0:
            for i in range(1, int(sheet.cell(row, 10).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 15).value)
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
                dict_horassemanales[codigo] = int(sheet.cell(row, 14).value)
        if int(sheet.cell(row, 6).value)>0:
            for i in range(1, int(sheet.cell(row, 6).value)+1):
                codigo=str(int(sheet.cell(row,0).value))+"-GL"+str(i).zfill(2)+"ES"
                vector_es.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 15).value)
        if int(sheet.cell(row, 7).value) > 0:
            for i in range(1, int(sheet.cell(row, 7).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 14).value)
        if int(sheet.cell(row, 8).value) > 0:
            for i in range(1, int(sheet.cell(row, 8).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EU"
                vector_eu.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 15).value)
        if int(sheet.cell(row, 9).value) > 0:
            for i in range(1, int(sheet.cell(row, 9).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-M" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 14).value)
        if int(sheet.cell(row, 10).value) > 0:
            for i in range(1, int(sheet.cell(row, 10).value) + 1):
                codigo = str(int(sheet.cell(row, 0).value)) + "-GL" + str(i).zfill(2) + "EN"
                vector_en.append(codigo)
                dict_horassemanales[codigo] = int(sheet.cell(row, 15).value)

#print(dict_asignaturas)
#print(dict_horassemanales)
#print(len(dict_horassemanales))
###################################################################################
#MATRIZ DE INCOMPATIBILIDADES
#Creamos la matriz de incompatibilidades
#Podrán solaparse aquellos grupos que compartiendo curso, cuatri e idioma, sean de tipo laboratorio.
tam=len(dict_asignaturas[1, "Primer cuatrimestre", "ES"])
matrix=np.ones([tam, tam], dtype=np.int)
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


##################################################################################
#FUNCIÓN DE COMPROBACIÓN DE RESTRICCIONES
def check_feasibility(individual):
    # Esta función sirve para comprobar si el individuo
    # cumple o no, las restricciones del problema

    #Restricción sobre los solapamientos de las asignaturas
    ind_df = pd.DataFrame(np.reshape(individual, (tam, 20)), index=asignaturas, columns=bloques)
    feasibility = True

    for ind_row, row in ind_df.iterrows():
        s = sum(row)
        #print(s)
        #print(dict_horassemanales[ind_row])
        if s != dict_horassemanales[ind_row]:
            feasibility = False
            #print("False")
            return feasibility
    for col in ind_df:
        # print(col)
        # aux_df=incomp_df.loc[:, col]
        # Recorremos el DF por columnas y nos quedamos con aquellas filas cuyo valor es 1.
        condicion = ind_df[col] >= 1
        # print(df[condicion][col])
        aux_df = ind_df[condicion][col]
        # print(aux_df.index)
        # print(incomp_df)
        for ind in list(aux_df.index):
            #print(ind)
            list_aux = list(aux_df.index)
            list_aux.remove(ind)
            #print(list_aux)
            for ind_aux in list_aux:
                #print(ind_aux)
                # Buscamos en la matriz de incompatibilidades, para ver si dichos grupos se pueden solapar
                if incomp_df[ind_aux][ind] == 1:
                    feasibility = False
                    return feasibility

    return feasibility

#################################################################################
#VARIABLES GLOBALES
#Ejemplo cuatrimestre , 1º curso
tam=len(dict_asignaturas[1, "Primer cuatrimestre", "ES"])
asignaturas=dict_asignaturas[1, "Primer cuatrimestre", "ES"]
bloques=['Lunes1', "Lunes2", "Lunes3", "Lunes4", "Martes1", "Martes2", "Martes3", "Martes4",
         "Miércoles1", "Miércoles2", "Miércoles3", "Miércoles4", "Jueves1", "Jueves2", "Jueves3",
         "Jueves4", "Viernes1", "Viernes2", "Viernes3", "Viernes4"]

################################################################################
#ALGORITMO GENÉTICO

def main():

    if __name__ == "__main__":
        #Consideramos la función de fitness como FitnessMin y creamos los individuales como listas
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        #Existen 21 grupos en el primer curso del primer cuatrimestre, en español.

        #De esta forma, creamos los individuos, estarán formados
        # por 1 o 0, en función de si se imparte clase durante ese bloque o no.
        #El tamaño del vector será de 21grupos *5 días*4 bloques/día.
        #Sería una matriz de 21x20
        IND_SIZE=tam*20

        #Ahora, necesitamos un toolbox.
        #Se generarán de forma aleatoria las posibles individuos que tendrán
        #un total de 21x20 elementos y estarán formados por enteros 0 o 1.
        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, n=IND_SIZE)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        #Para varios procesadores
        pool=multiprocessing.Pool(processes=3)
        toolbox.register("map", pool.map)
        #Utilizamos la función evaluator que creamos como función de evaluación
        toolbox.register("evaluate", evaluator)
        #Añadimos la función para penalizar en caso de no cumplir las restricciones
        #toolbox.decorate("evaluate", tools.DeltaPenalty(check_feasibility, 20000))
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Creamos la población
        pop = toolbox.population(n=4000)
        hof = tools.HallOfFame(1, similar=np.array_equal)
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
            # print("FIT: ", fit)

        # CXPB = probabilidad con las que dos invidividuos se cruzan
        # MUTPB = probabilidad de mutar un individuo
        CXPB, MUTPB = 0.5, 0.2

        # Se almacenan en fits los valores de fitness de los individuos
        fits = [ind.fitness.values[0] for ind in pop]

        # g=variable que cuenta el número de iteraciones realizadas
        g = 0
        # Comienza la evolución
        while min(fits) > 0 and g < 500:
            # A new generation
            g = g + 1
            print("-- Generation %i --" % g)
            # Seleccionamos la población
            offspring = toolbox.select(pop, len(pop))
            # Se clonan los individuos
            offspring = list(map(toolbox.clone, offspring))
            # Se aplican crossover y mutación
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Se evalúa el fitness de los nuevos individuos
            # Se reevalúan aquellos casos donde se consideró inválido el valor de fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Se reemplaza la población por la nueva generada
            # después del crossover y la mutación
            pop[:] = offspring

            #Se hace un update del HallOfFame donde se almacenará la mejor solución
            hof.update(pop)
            # Se evalúa la solución
            fits = [ind.fitness.values[0] for ind in pop]

            # length = len(pop)
            # mean = sum(fits) / length
            # sum2 = sum(x * x for x in fits)
            # std = abs(sum2 / length - mean ** 2) ** 0.5

            print("  Min %s" % min(fits))
            # print("  Max %s" % max(fits))
            # print("  Avg %s" % mean)
            # print("  Std %s" % std)


        if list(hof[0])!=None:
            # Almacenamos la mejor solución en un excel para realizar comprobaciones
            print(list(hof[0]))
            df = pd.DataFrame(data=np.reshape(list(hof[0]), (tam, 20)),
                              columns=bloques, index=asignaturas)
            out_file = "solucion.xlsx"
            df.to_excel(out_file, index=False)

        return hof


#Ejecutamos el algoritmo genético
main()




# comp=True
# for col in df:
#     #print(col)
#     #aux_df=incomp_df.loc[:, col]
#     #Recorremos el DF por columnas y nos quedamos con aquellas filas cuyo valor es 1.
#     condicion=df[col]>=1
#     #print(df[condicion][col])
#     aux_df=df[condicion][col]
#     #print(aux_df.index)
#     #print(incomp_df)
#     for ind in list(aux_df.index):
#         #print(ind)
#         list_aux=list(aux_df.index)
#         list_aux.remove(ind)
#         #print(list_aux)
#         while comp:
#             for ind_aux in list_aux:
#                 #print(ind_aux)
#                 # Buscamos en la matriz de incompatibilidades, para ver si dichos grupos se pueden solapar
#                 if incomp_df[ind_aux][ind]==1:
#                     comp=False

















##############################################################################
# #VERSIÓN CORTA DEL ALGORITMO GENÉTICO
# stats = tools.Statistics(lambda ind: ind.fitness.values)
# stats.register("avg", np.mean)
# stats.register("std", np.std)
# stats.register("min", np.min)
# stats.register("max", np.max)
#
# #Necesitamos HallOfFame para poder obtener la permutación con mejor valor
# hof = tools.HallOfFame(1, similar=np.array_equal)
# #Utilizando verbose=False, no se muestran por pantalla los resultados de las estadísticas
# ngen=1
# pop, logbook=algorithms.eaSimple(pop, toolbox, stats=stats, cxpb=0.5, mutpb=0.2, ngen=ngen, verbose=False, halloffame=hof)
#
# #Nos quedamos solo con el mínimo ya que se trata de un problema de minimización
# evals=logbook.select("min")
# best_sol=list(hof[0])
# print(evaluator(hof[0]))
#
# print("EVALS: ", evals)
# print("BEST SOL: ", np.reshape(best_sol, (tam, 20)))
#
# print(len(best_sol))
# #solucion=np.matrix(best_sol)
# #solucion.reshape(tam, 20)
# #print(solucion)
#
# df = pd.DataFrame(data=np.reshape(best_sol, (tam, 20)), columns=['Lunes1', "Lunes2", "Lunes3", "Lunes4", "Martes1", "Martes2", "Martes3", "Martes4",
#                                       "Miércoles1", "Miércoles2", "Miércoles3", "Miércoles4", "Jueves1", "Jueves2", "Jueves3",
#                                       "Jueves4", "Viernes1", "Viernes2", "Viernes3", "Viernes4"])
#
# out_file="solucion.xlsx"
# df.to_excel(out_file, index=False)