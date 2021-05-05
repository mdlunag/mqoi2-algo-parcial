def millor_ela(d,indicador, cap_min):
    candidats=[]
    candidats_ELA=[]
    ela='no'
    for i in range(d['NELA']):
        if cap_min<=d['CMELA'][i]:
            candidats_ELA.append(i)

    if candidats_ELA==[]:
        ela=indicador[0][1]

    else:
        ela=-1
        nela=0
        while ela not in candidats_ELA: #ens quedem amb el millor rap candidat segons indicador
            ela=indicador[nela][1]
            nela+=1
        return  ela
    return ela
