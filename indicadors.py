def generar_indicadors(d):
    cost_RAP=d['CRAP']
    capac_RAP=d['CMRAP']
    cost_RBP=d['CRBP']
    capac_RBP=d['CMRBP']
    cost_ELA=d['CELA']
    capac_ELA=d['CMELA']
    DS=d['DS']
    PECA=d['PECA']
    PPI=d['PPI']


    #generem llista de tuples, primer nombre es el valor de l'indicador, el segon l'index incial EX:[(Irap0,0),(Irap1,1),...,(IrapNRAP-1,NRAP-1)]
    ICrap= [(cost_RAP[i] ,i) for i in range(len(cost_RAP))]
    ICrbp= [(cost_RBP[i] ,i) for i in range(len(cost_RBP))]
    ICela= [(cost_ELA[i] ,i) for i in range(len(cost_ELA))]


    ICCrap= [(cost_RAP[i] / capac_RAP[i],i) for i in range(len(cost_RAP))]
    ICCrbp= [(cost_RBP[i] / capac_RBP[i],i) for i in range(len(cost_RBP))]
    ICCela= [(cost_ELA[i] / capac_ELA[i],i) for i in range(len(cost_ELA))]


    ICMrap= [(capac_RAP[i],i) for i in range(len(cost_RAP))]
    ICMrbp= [(capac_RBP[i],i) for i in range(len(cost_RBP))]
    ICMela= [(capac_ELA[i],i) for i in range(len(cost_ELA))]

    ID= [(DS[i],i) for i in range(len(DS))]

    sumppi=[]
    sumppi_i=0
    for i in range(len(PPI)):
        for j in range(len(PPI[i])):
            sumppi_i+=PPI[i][j]
        sumppi.append(sumppi_i)
        sumppi_i=0


    Ippi= [(sumppi[i]/DS[i],i) for i in range(len(DS))]


    # ordenem de forma creixent els valors dels indicadors
    ICrap=sorted(ICrap, key=lambda indicador: indicador[0]) #llista dels indicadors ICrap ordenars de forma creixent
    ICrbp=sorted(ICrbp, key=lambda indicador: indicador[0])
    ICela=sorted(ICela, key=lambda indicador: indicador[0])
    IC=[ICrap,ICrbp, ICela] #llista formada per 3 llistes, cadascuna corresponent als indicadors de RAP, RBP, ELA

    ICCrap=sorted(ICCrap, key=lambda indicador: indicador[0])
    ICCrbp=sorted(ICCrbp, key=lambda indicador: indicador[0])
    ICCela=sorted(ICCela, key=lambda indicador: indicador[0])
    ICC=[ICCrap, ICCrbp, ICCela]

    ICMrap=sorted(ICMrap, key=lambda indicador: indicador[0])
    ICMrbp=sorted(ICMrbp, key=lambda indicador: indicador[0])
    ICMela=sorted(ICMela, key=lambda indicador: indicador[0])
    ICM=[ICMrap, ICMrbp, ICMela]

    IDmin = sorted(ID, key=lambda indicador: indicador[0])

    Ippi=sorted(Ippi, key=lambda indicador: indicador[0])

    #ordenem de forma decreixent l'indicador de la demanda
    IDmax=sorted(ID, key=lambda indicador: indicador[0], reverse=True)


    return IC,ICC,ICM,IDmin,IDmax,Ippi
