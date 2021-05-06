def millor_ela(d,indicador, us_sobrant):
    candidats=[]
    candidats_ELA=[]
    ela=-1
    for i in range(d['NELA']):
        if us_sobrant<=d['CMELA'][i]:
            candidats_ELA.append(i)

    if candidats_ELA==[]:
        ela=indicador[0][1]
        return ela

    else:
        ela=-1
        nela=0
        while ela not in candidats_ELA: #ens quedem amb el millor rap candidat segons indicador
            ela=indicador[nela][1]
            nela+=1
        return  ela
