#Dibujando los resultados

import matplotlib.pyplot as plt
import xlrd
import pandas as pd
import random
import numpy as np

def leer_10resultados (file_name1, file_name2):
    # Leemos los 10 excel
    df_mediana = pd.DataFrame()
    df_cuartil25 = pd.DataFrame()
    df_cuartil75 = pd.DataFrame()
    df_fitnessmin=pd.DataFrame()
    df_restric_min=pd.DataFrame()
    tiempo_ejecucion = []
    for i in range(0, 10):
        f_name = file_name1 + str(i) + file_name2
        read_file = xlrd.open_workbook(f_name)
        sheet = read_file.sheet_by_name("Resultados")
        fitness_min = []
        mediana = []
        cuartil_25 = []
        cuartil_75 = []
        restricciones=[]

        # Almacemos la info que queremos dibujar
        for row in range(1, sheet.nrows):
            fitness_min.append(sheet.cell(row, 0).value)
            mediana.append(sheet.cell(row, 2).value)
            cuartil_25.append(sheet.cell(row, 3).value)
            cuartil_75.append(sheet.cell(row, 4).value)
            restricciones.append(sheet.cell(row, 5).value)
        # Generamos los dataframes
        col_name = str(i + 1)
        df_mediana[col_name] = mediana
        df_cuartil25[col_name] = cuartil_25
        df_cuartil75[col_name] = cuartil_75
        df_fitnessmin[col_name]=fitness_min
        df_restric_min[col_name] = restricciones
        sheet1 = read_file.sheet_by_name("Tiempo ejecución")

        tiempo_ejecucion.append(sheet1.cell(1, 0).value)

    return df_mediana, df_cuartil25, df_cuartil75, df_fitnessmin, tiempo_ejecucion, df_restric_min

#Leemos el baseline del archivo y lo almacenamos en un vector
filename_baseline="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\RESULTADOS\\" \
           "Resultados_baseline_11y21y31.xlsx"
read_file = xlrd.open_workbook(filename_baseline)
sheet = read_file.sheet_by_name("Resultados")
vector_baseline=[]
for row in range(1, sheet.nrows):
    vector_baseline.append(sheet.cell(row, 0).value)
sheet = read_file.sheet_by_name("Resultados_2")
for row in range(1, sheet.nrows):
    vector_baseline.append(sheet.cell(row, 0).value)
sheet = read_file.sheet_by_name("Resultados_3")
for row in range(1, sheet.nrows):
    vector_baseline.append(sheet.cell(row, 0).value)
sheet = read_file.sheet_by_name("Resultados_4")
for row in range(1, sheet.nrows):
    vector_baseline.append(sheet.cell(row, 0).value)
sheet = read_file.sheet_by_name("Resultados_5")
for row in range(1, sheet.nrows):
    vector_baseline.append(sheet.cell(row, 0).value)
sheet = read_file.sheet_by_name("Resultados_6")
for row in range(1, sheet.nrows):
    vector_baseline.append(sheet.cell(row, 0).value)
sheet = read_file.sheet_by_name("Resultados_7")
for row in range(1, sheet.nrows):
    vector_baseline.append(sheet.cell(row, 0).value)

tam11=46*75*20
tam11y21=90*75*20
tam11y21y31=158*75*20

min_10=min(random.sample(vector_baseline, tam11y21y31*10))
#min_20=min(random.sample(vector_baseline, tam11y21*20))
#min_30=min(random.sample(vector_baseline, tam11y21*30))

#print("LEN 10: ", len(random.sample(vector_baseline, tam11*20)))
#print("LEN 20: ", len(random.sample(vector_baseline, tam11y21*20)))
#print("LEN 30: ", len(random.sample(vector_baseline, tam11y21*30)))
#print("MIN 10: ", min_10)
#print("MIN 20: ", min_20)
#print("MIN 30: ", min_30)
#Leemos el archivo excel
file_name1_10="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\RESULTADOS\\" \
           "Resultados custom 1 curso 2 curso 3 curso 1 cuatri\\Resultados_Custom_11y21y31_Pop10_"
file_name2_10=".xlsx"

file_name1_20="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\RESULTADOS\\" \
           "Resultados iniciales 1 curso 2 curso 3 curso 1 cuatri\\Resultados_11y21y31_Pop10_"
file_name2_20=".xlsx"

file_name1_30="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\RESULTADOS\\" \
           "Resultados custom 1 curso 2 curso 1 cuatri\\Resultados_Custom_11y21_Pop30_"
file_name2_30=".xlsx"

df_mediana_10, df_cuartil25_10, df_cuartil75_10, df_fitnessmin_10, tiempo_ejecucion_10, df_rest_10=leer_10resultados(file_name1_10, file_name2_10)
df_mediana_20, df_cuartil25_20, df_cuartil75_20, df_fitnessmin_20, tiempo_ejecucion_20, df_rest_20=leer_10resultados(file_name1_20, file_name2_20)
df_mediana_30, df_cuartil25_30, df_cuartil75_30, df_fitnessmin_30, tiempo_ejecucion_30, df_rest_30=leer_10resultados(file_name1_30, file_name2_30)

#Realizamos la media de las 10 ejecuciones
#La columna df_mediana["media"] será la que vamos a dibujar
#print(df_mediana)
#Mediana
df_mediana_10["media"]=df_mediana_10.sum(axis=1)
df_mediana_10["media"]= df_mediana_10["media"] / 10
#Cuartil 25
df_cuartil25_10["media"]=df_cuartil25_10.sum(axis=1)
df_cuartil25_10["media"]= df_cuartil25_10["media"] / 10
#Cuartil 75
df_cuartil75_10["media"]=df_cuartil75_10.sum(axis=1)
df_cuartil75_10["media"]= df_cuartil75_10["media"] / 10
#Fitness min
df_fitnessmin_10["media"]=df_fitnessmin_10.sum(axis=1)
df_fitnessmin_10["media"]= df_fitnessmin_10["media"] / 10

df_rest_10["media"]=df_rest_10.sum(axis=1)
df_rest_10["media"]= df_rest_10["media"] / 10
#print(df_mediana["media"])

#Cálculo del tiempo medio de ejecución
media_tiempo_ejec_10= sum(tiempo_ejecucion_10) / 10
#print(media_tiempo_ejec_30)

#Mediana
df_mediana_20["media"]=df_mediana_20.sum(axis=1)
df_mediana_20["media"]= df_mediana_20["media"] / 10
# #Cuartil 25
df_cuartil25_20["media"]=df_cuartil25_20.sum(axis=1)
df_cuartil25_20["media"]= df_cuartil25_20["media"] / 10
# #Cuartil 75
df_cuartil75_20["media"]=df_cuartil75_20.sum(axis=1)
df_cuartil75_20["media"]= df_cuartil75_20["media"] / 10
# #Fitness min
df_fitnessmin_20["media"]=df_fitnessmin_20.sum(axis=1)
df_fitnessmin_20["media"]= df_fitnessmin_20["media"] / 10
#
df_rest_20["media"]=df_rest_20.sum(axis=1)
df_rest_20["media"]= df_rest_20["media"] / 10
# #print(df_mediana["media"])
# #
# #Cálculo del tiempo medio de ejecución
media_tiempo_ejec_20= sum(tiempo_ejecucion_20) / 10
# #
# #Mediana
df_mediana_30["media"]=df_mediana_30.sum(axis=1)
df_mediana_30["media"]= df_mediana_30["media"] / 10
# #Cuartil 25
df_cuartil25_30["media"]=df_cuartil25_30.sum(axis=1)
df_cuartil25_30["media"]= df_cuartil25_30["media"] / 10
# #Cuartil 75
df_cuartil75_30["media"]=df_cuartil75_30.sum(axis=1)
df_cuartil75_30["media"]= df_cuartil75_30["media"] / 10
# #Fitness min
df_fitnessmin_30["media"]=df_fitnessmin_30.sum(axis=1)
df_fitnessmin_30["media"]= df_fitnessmin_30["media"] / 10
#
df_rest_30["media"]=df_rest_30.sum(axis=1)
df_rest_30["media"]= df_rest_30["media"] / 10
#  #print(df_mediana["media"])
# #
# # #Cálculo del tiempo medio de ejecución
media_tiempo_ejec_30= sum(tiempo_ejecucion_30) / 10

#print("TIEMPOS DE EJECUCIÓN: ", tiempo_ejecucion)
#print("MEDIA DEL TIEMPO DE EJECUCIÓN: ", media_tiempo_ejec_10)
#print(df_mediana)



#Dibujamos boxplot
#data = pd.DataFrame()

# #data["10"]=df_mediana_10.iloc[74, 0:10]
# #data["20"]=df_mediana_20.iloc[74, 0:10]
# #data["30"]=df_mediana_30.iloc[74, 0:10]
# #
# #data["1º"]=df_mediana_10.iloc[74, 0:10]
# #data["1º y 2º"]=df_mediana_20.iloc[74, 0:10]
# #data["1º, 2º y 3º"]=df_mediana_30.iloc[74, 0:10]
# #
# data["10"]=df_fitnessmin_10.iloc[74, 0:10]
# data["20"]=df_fitnessmin_20.iloc[74, 0:10]
# data["30"]=df_fitnessmin_30.iloc[74, 0:10]
# # # print(data)
# plt.figure()
# fig, ax = plt.subplots()
# ax.set_title("Función objetivo generación 75 1º curso 1º cuatrimestre")
# ax.set_xlabel("Tamaño población")
# ax.set_ylabel("Función objetivo")
# #print("MIN_10: :", min_10)
# ax.plot(list(range(1,4)), [min_10, min_10, min_10], 'r', linewidth=2)
# ax.legend(["Baseline"])
# # #print(data)
# boxplot=data.boxplot( column=["10", "20", "30"], ax=ax)
# fig_name="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
#        "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\FIGURAS\\Boxplot_zoom75_fitnessmin_11+baseline.jpg"
# plt.savefig(fig_name)


#data2 = pd.DataFrame()
#data["10"]=df_mediana_10.iloc[74, 0:10]
#data["20"]=df_mediana_20.iloc[74, 0:10]
#data["30"]=df_mediana_30.iloc[74, 0:10]
#
# #data["1º"]=df_mediana_10.iloc[74, 0:10]
# #data["1º y 2º"]=df_mediana_20.iloc[74, 0:10]
# #data["1º, 2º y 3º"]=df_mediana_30.iloc[74, 0:10]
#
#data2["10"]=df_rest_10.iloc[74, 0:10]
#data2["20"]=df_rest_20.iloc[74, 0:10]
#data2["30"]=df_rest_30.iloc[74, 0:10]
# print("Resultados restricciones incumplidas")
# print(data2)
#plt.figure()
#fig, ax = plt.subplots()
# ax.set_title("Restricciones incumplidas generación 75, 1º, 2º y 3º curso 1º cuatrimestre")
# ax.set_xlabel("Tamaño población")
# ax.set_ylabel("Restricciones incumplidas")
# #print("MIN_10: :", min_10)
# #ax.plot(list(range(1,4)), [min_10, min_10, min_10], 'r', linewidth=2)
# #ax.legend(["Baseline"])
# # #print(data)
# boxplot=data2.boxplot( column=["10"], ax=ax)
# fig_name="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
#        "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\FIGURAS\\Boxplot_zoom75_rest_custom_11y21y31.jpg"
# plt.savefig(fig_name)

#Dibujamos mediana y cuartiles
#
plt.figure()
plt.plot(df_mediana_20["media"], "mediumblue", label='Mediana op. no personalizados')
plt.plot(df_mediana_10["media"], "green", label="Mediana op. personalizados")
plt.plot(df_cuartil25_20["media"], "cornflowerblue", df_cuartil75_20["media"], "cornflowerblue")
plt.plot(df_cuartil25_10["media"], "mediumseagreen", df_cuartil75_10["media"], "mediumseagreen")
v_baseline=np.repeat(min_10, 75, axis=0)
plt.plot(v_baseline, "red", label="Baseline")
plt.plot()
plt.xlabel("Generaciones")
plt.ylabel("Función objetivo")
# # #px=74
# # py=min(df_mediana_30["media"])
# # # # # Pinto las coordenadas con un punto negro
# # # #punto = plt.plot([px], [py], 'bo')
# # print("valor mediana", py)
# # # #plt.xticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80])
# # # #plt.annotate(r'$m_p=0.01, ratio=0.05$',
# # # #             xy=(75, py), xycoords='data',
# # # #             xytext=(0, +10), textcoords='offset points', fontsize=10)
# # # # Hago un señalización con flecha
# # # #nota = plt.annotate(r'$Generación=75, Mediana Fitness = 7.4$',
# # # #         xy=(px, py),
# # # #         xycoords='data',
# # # #         xytext=(35, 300),
# # # #         fontsize=9,
# # # #         arrowprops=dict(arrowstyle="->",
# # # #         connectionstyle="arc3,rad=.2"))
x=np.arange(0, 75)
plt.fill_between(x, df_cuartil25_20["media"], df_cuartil75_20["media"], color="cornflowerblue")
plt.fill_between(x, df_cuartil25_10["media"], df_cuartil75_10["media"], color="mediumseagreen")
# # #texto1 = plt.text(40, 200, r'$Valor \thinspace mínimo\thinspace mediana=10.5$', fontsize=9)
# # #
# # # # Añado leyenda, tamaño de letra 10, en esquina superior derecha
plt.legend(prop = {'size': 10}, loc='upper right')
# # #
# #Añado un título a la figura
plt.title("Resultados comparativa 1º, 2º, 3º curso y 1º cuatrimestre (n=10)")
# # # #Mostramos la figura
# # # #plt.show()
# # # #
# #Guardamos la figura
fig_name="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
       "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\FIGURAS\\Resultados_comparativa_11y21y31_Pop10+baseline.jpg"
plt.savefig(fig_name)