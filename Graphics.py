#Dibujando los resultados

import matplotlib.pyplot as plt
import xlrd
import pandas as pd
import numpy as np


#Leemos el archivo excel
file_name1="C:\\Users\\tr5568\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\RESULTADOS\\" \
           "Resultados iniciales 1 curso 1 cuatri\\Resultados_11_Pop10_"
file_name2=".xlsx"
#Creamos los dataframes para almacenar la información
df_mediana=pd.DataFrame()
df_cuartil25=pd.DataFrame()
df_cuartil75=pd.DataFrame()
tiempo_ejecucion=[]

#Leemos los 10 excel
for i in range(0,10):
    f_name=file_name1+str(i)+file_name2
    read_file=xlrd.open_workbook(f_name)
    sheet=read_file.sheet_by_name("Resultados")
    fitness_min=[]
    mediana=[]
    cuartil_25=[]
    cuartil_75=[]

    #Almacemos la info que queremos dibujar
    for row in range(1,sheet.nrows):
        fitness_min.append(sheet.cell(row, 0).value)
        mediana.append(sheet.cell(row, 2).value)
        cuartil_25.append(sheet.cell(row, 3).value)
        cuartil_75.append(sheet.cell(row, 4).value)

    #Generamos los dataframes
    col_name="Generación "+str(i)
    df_mediana[col_name]=mediana
    df_cuartil25[col_name]=cuartil_25
    df_cuartil75[col_name]=cuartil_75

    sheet1=read_file.sheet_by_name("Tiempo ejecución")

    tiempo_ejecucion.append(sheet1.cell(1,0).value)

#Realizamos la media de las 10 ejecuciones
#La columna df_mediana["media"] será la que vamos a dibujar
#print(df_mediana)
#Mediana
df_mediana["media"]=df_mediana.sum(axis=1)
df_mediana["media"]=df_mediana["media"]/10
#Cuartil 25
df_cuartil25["media"]=df_cuartil25.sum(axis=1)
df_cuartil25["media"]=df_cuartil25["media"]/10
#Cuartil 75
df_cuartil75["media"]=df_cuartil75.sum(axis=1)
df_cuartil75["media"]=df_cuartil75["media"]/10
#print(df_mediana["media"])

#Cálculo del tiempo medio de ejecución
media_tiempo_ejec=sum(tiempo_ejecucion)/10
#print("TIEMPOS DE EJECUCIÓN: ", tiempo_ejecucion)
#print("MEDIA DEL TIEMPO DE EJECUCIÓN: ", media_tiempo_ejec)
#Dibujamos

plt.figure()
plt.plot(df_mediana["media"], "mediumblue")
plt.plot(df_cuartil25["media"], "cornflowerblue", df_cuartil75["media"], "cornflowerblue")
plt.xlabel("Generaciones")
plt.ylabel("Fitness min")
x=np.arange(0, 75)
plt.fill_between(x, df_cuartil25["media"], df_cuartil75["media"], color="cornflowerblue")


# Añado leyenda, tamaño de letra 10, en esquina superior derecha
plt.legend(('Mediana', 'Cuartil 25', 'Cuartil 75'),
prop = {'size': 10}, loc='upper right')

#Añado un título a la figura
plt.title("Resultados 1º, 2º y 3º curso 1º cuatri (n=10)")
#Mostramos la figura
#plt.show()

#Guardamos la figura
#fig_name="C:\\Users\\tr5568\\Desktop\\DAYANA\\PERSONAL\\" \
    #"MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\FIGURAS\\Resultados_11y21y31_Pop10.jpg"
#plt.savefig(fig_name)