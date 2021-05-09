def extreure_dades(exemplar):
    dicc_dades={}
    file=open(exemplar,'r')
    l=[]
    for linia in file:
        l.append(linia.strip())
    #N
    N=int(l[0])
    dicc_dades['N'] = N #nombre d'illes

    #DS 1..N
    l_DS_str=l[1].split('*')
    l_DS_int=[]
    for DS in l_DS_str:
        l_DS_int.append(float(DS))
    dicc_dades['DS']=l_DS_int #llista on cada element es la DS de la illa i

    #PECA
    l_PECA_str=l[2].split('*')
    l_PECA_int=[]
    for PECA in l_PECA_str:
        l_PECA_int.append(float(PECA)/100)
    dicc_dades['PECA']=l_PECA_int #llista on cada element es el PECA de la illa i

    #PPIij
    PPI=[]
    l_ppi_int=[]
    for ppi in l[3:3+N]:
        l_ppi=ppi.split('*') #llista dels valors de PPI de la fila i
        for e in l_ppi:
            l_ppi_int.append(float(e)/100)
        PPI.append(l_ppi_int)
        l_ppi_int=[]
    dicc_dades['PPI']=PPI #llista on cada element es una llista amb les perdues PPIij de la illa i

    #NRAP,CRAP,CMRAP,NRBP...
    l_elem_int=[]
    l_elem=[]
    for linia in l[3+N:]:
        if '*' in linia:
            l_elem_str=linia.split('*')
            for elem in l_elem_str:
                l_elem_int.append(float(elem))
            l_elem.append(l_elem_int)
            l_elem_int=[]
        else:
            l_elem.append(int(linia))

    dicc_dades['NRAP']=l_elem[0] #nombre de raps
    dicc_dades['CRAP']=l_elem[1] #llista amb els costos de RAP
    dicc_dades['CMRAP']=l_elem[2] #llista amb els costos de RAP
    dicc_dades['NRBP']=l_elem[3] #nombre de rbps
    dicc_dades['CRBP']=l_elem[4] #llista amb els costos de RBP
    dicc_dades['CMRBP']=l_elem[5] #llista amb els costos de RBP
    dicc_dades['NELA']=l_elem[6] #nombre de elas
    dicc_dades['CELA']=l_elem[7] #llista amb els costos de ELA
    dicc_dades['CMELA']=l_elem[8] #llista amb els costos de ELA
    dicc_dades['NECA']=l_elem[9] #nombre de ecas
    dicc_dades['CECA']=l_elem[10] #llista amb els costos de ECA
    dicc_dades['CMECA']=l_elem[11] #llista amb els costos de ECA

    return dicc_dades
