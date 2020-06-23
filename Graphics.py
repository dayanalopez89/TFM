#Dibujando los resultados

import matplotlib.pyplot as plt
import xlrd

#Leemos el archivo excel
file="C:\\Users\\tr5568\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\RESULTADOS\\Resultados_Prueba_0.xlsx"
#We want the sheet called Data
read_file=xlrd.open_workbook(file)
sheet=read_file.sheet_by_name("Resultados")
fitness_min=[]

for row in range(2,sheet.nrows):
    fitness_min.append(sheet.cell(row, 0).value)

#Dibujamos
plt.plot(fitness_min)
plt.xlabel("Generaciones")
plt.ylabel("Fitness min")

#Mostramos la figura
#plt.show()

#Guardamos la figura
plt.savefig("C:\\Users\\tr5568\\Desktop\\DAYANA\\PERSONAL\\" \
     "MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\FIGURAS\\Resultados_Prueba_0.jpg")