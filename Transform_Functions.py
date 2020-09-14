
import pandas as pd
import numpy as np


def getCodificacion(planificacion, asignaturas):
    values=planificacion.values
    ind=list(values[0])
    for v in values:
        ind+=list(v)
    return ind

def getSolucion(individuo, bloques, asignaturas):
    #Convertimos el individuo en un dataframe que contenga la solución como un
    #horario convencional
    df = pd.DataFrame(data=np.reshape(list(individuo), (len(asignaturas), 20)),
                         columns=bloques, index=asignaturas)
    return df


asignaturas=["Asign1", "Asign2", "Asign3"]
bloques=["Lunes1", "Lunes2", "Lunes3", "Lunes4",
         "Martes1", "Martes2", "Martes3", "Martes4",
         "Miércoles1", "Miércoles2", "Miércoles3", "Miércoles4",
         "Jueves1", "Jueves2", "Jueves3", "Jueves4",
         "Viernes1", "Viernes2", "Viernes3", "Viernes4"]
print(len(bloques))
print(len(asignaturas))
df = pd.DataFrame({'Lunes': [ 0, 1, 0],'Martes': [0, 1, 0],'Miércoles': [0, 0, 0],
                   'Jueves': [0, 0, 0],'Viernes': [0, 0, 0]}, index=asignaturas,
                  columns=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])

individuo=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

#print(getSolucion(individuo, bloques, asignaturas))


