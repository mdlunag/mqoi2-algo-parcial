import time

def heuristica1(l_ie,l_ii,d, candidats_RAP, candidats_RBP, l_ECA, temps_inici,l_sol_print, millor_sol):
    illa=None
    cost=[]
    elems=[] #elements triats pr cada illa i, rap,rbp,ela
    enviats=[]
    l_sol1=[]
    l_sol_print1=[]
    l_sol_print=l_sol_print[:]
    nsol=0
    opcio_elas=1

    for ie in range(len(l_ie)):
        Ie=l_ie[ie][:]

        for ii in range(len(l_ii)):
            Ii=l_ii[ii][:]
            elem_illa=[]
            cost_acum = 0
            solucio=[]
            us_dispos=0
            enviaments=[] #a quines illes envia l'illa i
            for a in range(d['N']):
                elem_illa.append([-1,-1,-1,-1])
                enviaments.append([])


            while len(Ii)>0:

                '''if len(Ii)>1 and Ii[0][0]==Ii[1][0]: #si hi ha empat entre 2 millors illes
                    illa1=Ii[0][1]
                    illa2=Ii[1][1]

                    if ii==0:
                        I2_illa1=(l_ii[2][i][1] for i in range(len(l_ii[2])) if l_ii[2][i][1] == illa1)
                        if I2_illa1>I2_illa2:
                            Illa=0
                        else:
                            illa=0
                    if ii==1:
                        pass
                    if ii==2:

                else:'''

                illa=Ii[0][1] #num millor illa segons indicador
                demanda=d['DS'][illa]
                rap=(-1,-1)
                nrap=0

                while rap[1] not in candidats_RAP[illa]: #ens quedem amb el millor rap candidat segons indicador
                    rap=Ie[0][nrap]
                    nrap+=1
                elem_illa[illa][0]=rap[1]

                cost_acum += d['CRAP'][rap[1]]

                ela=Ie[2][0][1] #ens quedem amb el primer candidat de la llista segons indicador



                elem_illa[illa][2]=ela
                us_sobrant=d['CMRAP'][rap[1]]-demanda
                us_dispos=0
                if us_sobrant>=d['CMELA'][ela]:
                    us_dispos=d['CMELA'][ela]
                else:
                    us_dispos=us_sobrant
                Ii.pop(0)

                while len(Ii)>0 and Ii[0][0]/(1-d['PPI'][illa][Ii[0][1]]) <= us_dispos:
                    rbp=(-1,-1)
                    nrbp=0
                    while rbp[1] not in candidats_RBP[Ii[0][1]]:
                        rbp=Ie[1][nrbp]
                        nrbp+=1
                    elem_illa[Ii[0][1]][1]=rbp[1]
                    cost_acum+=d['CRBP'][rbp[1]]
                    us_dispos -= Ii[0][0]/(1-d['PPI'][illa][Ii[0][1]])
                    enviaments[illa].append(Ii[0][1])
                    Ii.pop(0)

                cost_acum += d['CELA'][ela]


            nsol+=1
            for i in range(d['N']):
                elem_illa[i][3]=l_ECA[i]
                cost_acum+=d['CECA'][l_ECA[i]]

                if enviaments[i]==[] and elem_illa[i][2]!=-1 and elem_illa[i][0]!=-1: #treure ELAs q no envien

                    cost_acum-=d['CELA'][elem_illa[i][2]]
                    elem_illa[i][2]=-1

                if elem_illa[i][2]!=-1:
                    enviat=0
                    for illa_enviada in enviaments[i]:
                        enviat+=d['DS'][illa_enviada]/(1-d['PPI'][i][illa_enviada])
                    l_elas=l_ie[0][2].copy() #indicador de preu i elas
                    ela=l_elas[0][1]
                    while enviat>d['CMELA'][ela]:
                        l_elas.pop(0)
                        ela=l_elas[0][1]


            temps_final_i=time.time()-temps_inici

            for i in range(len(elem_illa)):
                for i2 in range(len(elem_illa[i])):
                        elem_illa[i][i2] +=1

            for i in range(len(enviaments)):
                for i2 in range(len(enviaments[i])):
                            enviaments[i][i2]+=1

            solucio=[cost_acum,temps_final_i, elem_illa,enviaments]


            if l_sol_print1==[]:
                l_sol_print1.append([solucio[0],solucio[1],nsol])

            else:
                sol_anterior=l_sol_print1[-1][0]
                if solucio[0]<sol_anterior:
                    l_sol_print1.append([solucio[0],solucio[1],nsol])

            if solucio[0]<l_sol_print[-1][0]:
                l_sol_print.append([solucio[0],solucio[1],nsol])



            cost.append(cost_acum)
            elems.append(elem_illa)
            enviats.append(enviaments)
            l_sol1.append(solucio)

            #print('soluuu',solucio)

    millor_sol1=l_sol1[l_sol_print1[-1][2]-1]
    print(millor_sol1)
    if millor_sol1[0]<millor_sol[0]:
        millor_sol = millor_sol1
    print(millor_sol)

    return elems, enviats, cost, l_sol_print1, l_sol1, l_sol_print,millor_sol
