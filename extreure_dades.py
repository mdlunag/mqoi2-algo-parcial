def extreure_dades(exemplar):
    dicc_dades={}
    file=open(exemplar,'r')
    l=[]
    for linia in file:
        l.append(linia.strip())
    #N
    N=int(l[0])
    dicc_dades['N'] = N

    #DS 1..N
    l_DS_str=l[1].split('*')
    l_DS_int=[]
    for DS in l_DS_str:
        l_DS_int.append(float(DS))
    dicc_dades['DS']=l_DS_int

    #PECA
    l_PECA_str=l[2].split('*')
    l_PECA_int=[]
    for PECA in l_PECA_str:
        l_PECA_int.append(float(PECA)/100)
    dicc_dades['PECA']=l_PECA_int

    #PPIij
    PPI=[]
    l_ppi_int=[]
    for ppi in l[3:3+N]:
        l_ppi=ppi.split('*') #llista dels valors de PPI de la fila i
        for e in l_ppi:
            l_ppi_int.append(float(e))
        PPI.append(l_ppi_int)
        l_ppi_int=[]
    dicc_dades['PPI']=PPI

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

    dicc_dades['NRAP']=l_elem[0]
    dicc_dades['CRAP']=l_elem[1]
    dicc_dades['CMRAP']=l_elem[2]
    dicc_dades['NRBP']=l_elem[3]
    dicc_dades['CRBP']=l_elem[4]
    dicc_dades['CMRBP']=l_elem[5]
    dicc_dades['NELA']=l_elem[6]
    dicc_dades['CELA']=l_elem[7]
    dicc_dades['CMELA']=l_elem[8]
    dicc_dades['NECA']=l_elem[9]
    dicc_dades['CECA']=l_elem[10]
    dicc_dades['CMECA']=l_elem[11]

    return dicc_dades
