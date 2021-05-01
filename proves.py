PPI=[]
l_ppi_int=[]
for ppi in l[2:2+N]:
    l_ppi=ppi.split('*') #llista dels valors de PPI de la fila i
    for e in l_ppi:
        l_ppi_int.append(int(e))
    PPI.append(l_ppi_int)
    l_ppi_int=[]
    print(PPI)


cost_RAP=d['CRAP']
capac_RAP=d['CMRAP']
cost_RBP=d['CRBP']
capac_RBP=d['CMRBP']
cost_ELA=d['CELA']
capac_ELA=d['CMELA']
DS=d['DS']
PECA=d['PECA']

Irap= [(cost_RAP[i] / capac_RAP[i],i) for i in range(len(cost_RAP))]
Irbp= [(cost_RBP[i] / capac_RBP[i],i) for i in range(len(cost_RBP))]
Iela= [(cost_ELA[i] / capac_ELA[i],i) for i in range(len(cost_ELA))]
ID= [(DS[i],i) for i in range(len(DS))]
Ipeca= [(PECA[i],i) for i in range(len(PECA))]
Ipeca_ds= [(PECA[i] / DS[i],i) for i in range(len(DS))]

# ordenem de forma creixent els valors dels indicadors
Irap=sorted(Irap, key=lambda indicador: indicador[0])
Irbp=sorted(Irbp, key=lambda indicador: indicador[0])
Iela=sorted(Iela, key=lambda indicador: indicador[0])
Ipeca=sorted(Ipeca, key=lambda indicador: indicador[0])
Ipeca_ds=sorted(Ipeca_ds, key=lambda indicador: indicador[0])
#ordenem de forma decreixent l'indicador de la demanda
ID=sorted(ID, key=lambda indicador: indicador[0], reverse=True)


#Preproces
candidats=[]
candidats_i=[]
for i in range(d['N']):
    for e in range(len(d['CMECA'])):
        if d['DS'][i]<=(1-d['PECA'][i])*d['CMECA'][e]:
            candidats_i.append(e)
    candidats.append(candidats_i)
    candidats_i=[]
