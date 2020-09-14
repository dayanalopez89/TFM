import xlrd



def lectura_datos_excel(file):

    read_file=xlrd.open_workbook(file)
    sheet=read_file.sheet_by_name("Asignaturas y Grupos")
    dict_horas={}
    dict_asignaturas={}
    dict_contador={}
    dict_profesores={}
    vector_11_ES=[]
    vector_12_ES=[]
    vector_11_EU=[]
    vector_12_EU=[]
    vector_21_ES=[]
    vector_22_ES=[]
    vector_21_EU=[]
    vector_22_EU=[]
    vector_21_IN=[]
    vector_22_IN=[]
    vector_31_ES=[]
    vector_32_ES=[]
    vector_31_EU=[]
    vector_32_EU=[]
    vector_41_ES=[]
    vector_42_ES=[]
    vector_41_EU=[]
    vector_42_EU=[]
    vector_41_IN=[]
    vector_42_IN=[]

    for row in range(1,sheet.nrows):
        if str(sheet.cell(row,0).value)=="IIG":
            curso=str(sheet.cell(row,1).value)
            cuatri = int(sheet.cell(row, 2).value)
            codigo=int(sheet.cell(row, 6).value)
            idioma=str(sheet.cell(row, 9).value)
            tipo=sheet.cell(row, 10).value
            horas_semana=sheet.cell(row, 11).value
            profesor1=int(sheet.cell(row, 12).value)
            profesor2=sheet.cell(row, 13).value
            vector_prof = []
            vector_prof.append(profesor1)
            if profesor2!="":
                #print("PROFESOR 2: ", int(profesor2))
                vector_prof.append(int(profesor2))



            if "3" in curso:
                #print(str(curso[-2:]))
                if str(curso[-2:])!=".0":
                    opt = "-" + str(curso[-2:])
                else:
                    opt=""
                curso=int(3)

            else:
                curso=int(float(curso))
                #print(curso)
                opt=""
            codigo_asign=str(codigo)+"-"+str(tipo)+str(idioma)+"-"+str(curso)+str(cuatri)+opt
            if not codigo_asign in dict_contador:
                dict_contador[codigo_asign]=1
                codigo_asign=str(codigo)+"-"+str(tipo)+str(1).zfill(2)+str(idioma)+"-"+str(curso)+str(cuatri)+opt

            else:
                dato=dict_contador[codigo_asign]
                dict_contador[codigo_asign]=dato+1
                codigo_asign = str(codigo) + "-" + str(tipo) + str(dato+1).zfill(2) + str(idioma) + "-" + str(curso) + str(
                    cuatri) + opt

            dict_horas[codigo_asign]=int(horas_semana)
            dict_profesores[codigo_asign]=vector_prof
            #Append para 1º curso. 2 cuatrimestres y dos idiomas: ES y EU
            if curso==1 and cuatri==1 and idioma=="ES":vector_11_ES.append(codigo_asign)
            elif curso==1 and cuatri==1 and idioma=="EU": vector_11_EU.append(codigo_asign)
            elif curso==1 and cuatri==2 and idioma=="ES": vector_12_ES.append(codigo_asign)
            elif curso == 1 and cuatri == 2 and idioma == "EU":vector_12_EU.append(codigo_asign)

            # Append para 2º curso. 2 cuatrimestres y 3 idiomas: ES, EU e IN
            if curso == 2 and cuatri == 1 and idioma == "ES":
                vector_21_ES.append(codigo_asign)
            elif curso == 2 and cuatri == 1 and idioma == "EU":
                vector_21_EU.append(codigo_asign)
            elif curso == 2 and cuatri == 1 and idioma == "IN":
                vector_21_IN.append(codigo_asign)
            elif curso == 2 and cuatri == 2 and idioma == "ES":
                vector_22_ES.append(codigo_asign)
            elif curso == 2 and cuatri == 2 and idioma == "EU":
                vector_22_EU.append(codigo_asign)
            elif curso == 2 and cuatri == 2 and idioma == "IN":
                vector_22_IN.append(codigo_asign)

            # Append para 3º curso. 2 cuatrimestres y dos idiomas: ES y EU
            if curso==3 and cuatri==1 and idioma=="ES":vector_31_ES.append(codigo_asign)
            elif curso==3 and cuatri==1 and idioma=="EU": vector_31_EU.append(codigo_asign)
            elif curso==3 and cuatri==2 and idioma=="ES": vector_32_ES.append(codigo_asign)
            elif curso == 3 and cuatri == 2 and idioma == "EU":vector_32_EU.append(codigo_asign)

            # Append para 4º curso. 2 cuatrimestres y 3 idiomas: ES, EU e IN
            if curso == 4 and cuatri == 1 and idioma == "ES":
                vector_41_ES.append(codigo_asign)
            elif curso == 4 and cuatri == 1 and idioma == "EU":
                vector_41_EU.append(codigo_asign)
            elif curso == 4 and cuatri == 1 and idioma == "IN":
                vector_41_IN.append(codigo_asign)
            elif curso == 4 and cuatri == 2 and idioma == "ES":
                vector_42_ES.append(codigo_asign)
            elif curso == 4 and cuatri == 2 and idioma == "EU":
                vector_42_EU.append(codigo_asign)
            elif curso == 4 and cuatri == 2 and idioma == "IN":
                vector_42_IN.append(codigo_asign)

    dict_asignaturas[1, 1, "ES"]=vector_11_ES
    dict_asignaturas[1, 1, "EU"]=vector_11_EU
    dict_asignaturas[1, 2, "ES"]= vector_12_ES
    dict_asignaturas[1, 2, "EU"]= vector_12_EU

    dict_asignaturas[2, 1, "ES"]=vector_21_ES
    dict_asignaturas[2, 1, "EU"]=vector_21_EU
    dict_asignaturas[2, 1, "IN"]= vector_21_IN
    dict_asignaturas[2, 2, "ES"]= vector_22_ES
    dict_asignaturas[2, 2, "EU"]= vector_22_EU
    dict_asignaturas[2, 2, "IN"]= vector_22_IN

    dict_asignaturas[3, 1, "ES"]=vector_31_ES
    dict_asignaturas[3, 1, "EU"]=vector_31_EU
    dict_asignaturas[3, 2, "ES"]= vector_32_ES
    dict_asignaturas[3, 2, "EU"]= vector_32_EU

    dict_asignaturas[4, 1, "ES"]=vector_41_ES
    dict_asignaturas[4, 1, "EU"]=vector_41_EU
    dict_asignaturas[4, 1, "IN"]= vector_41_IN
    dict_asignaturas[4, 2, "ES"]= vector_42_ES
    dict_asignaturas[4, 2, "EU"]= vector_42_EU
    dict_asignaturas[4, 2, "IN"]= vector_42_IN

    #print(dict_asignaturas[3, 1, "ES"])
    #print(dict_horas)
    return dict_asignaturas, dict_horas, dict_profesores

#file="C:\\Users\\tr5568\\OneDrive - Axalta\\Desktop\\DAYANA\\PERSONAL\\" \
     #"MÁSTER INGENIERÍA COMPUTACIONAL Y SISTEMAS INTELIGENTES\\TFM\\AsignaturasGruposProfesorado-20200702-Dayana.xlsx"
#asign, horas, profes= lectura_datos_excel(file)

#print(asign[3, 1, "ES"])
#print(profes["26011-GL02ES-11"])
