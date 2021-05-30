import time

def heuristica3(l_ie,l_ii,d, candidats_RAP, candidats_RBP, l_ECA, temps_inici):
    illa=None
    cost=[]
    elems=[] #elements triats pr cada illa i, rap,rbp,ela
    enviats=[]
    l_sol=[]
    l_sol_print=[]
    nsol=0
    opcio_candidats=[1,2,3,4] #1 o 2
    opcio_elas=[1,2]
    for opcio_candidat in opcio_candidats:
        for opcio_ela in opcio_elas:
            for ie in range(len(l_ie)):
                Ie=l_ie[ie][:]

                for ii in range(len(l_ii)):
                    Ii=l_ii[ii][:]
                    elem_illa=[]
                    cost_acum = 0
                    solucio=[]
                    us_dispos=[]
                    enviaments=[] #a quines illes envia l'illa i
                    for a in range(d['N']):
                        elem_illa.append([-1,-1,-1,-1])
                        enviaments.append([])
                        us_dispos.append(0)

                    while len(Ii)>0:


                        illa=Ii[0][1] #num illa
                        demanda=d['DS'][illa]
                        rap=(-1,-1)
                        rbp=(-1,-1)
                        nrap=0
                        nrbp=0

                        while rap[1] not in candidats_RAP[illa]: #ens quedem amb el millor rap candidat segons indicador
                            rap=Ie[0][nrap]
                            nrap+=1

                        while rbp[1] not in candidats_RBP[illa]:
                            rbp=Ie[1][nrbp]
                            nrbp+=1


                        candidats_ppi=[]
                        candidats_us=[]
                        tipus2=False
                        if rbp[0]<rap[0]: #rbp millor que rap i us_dispos te elements dif de 0

                            for i,e in enumerate(us_dispos):
                                if d['PPI'][i][illa]!=0 and e>=demanda/(1-d['PPI'][i][illa]):

                                    candidats_ppi.append((d['PPI'][i][illa],i)) #candidat_i=(us_dispos,num_illa)
                                    candidats_us.append((e,i)) #candidat_i=(us_dispos,num_illa)
                            if opcio_candidat==1:
                                candidats=sorted(candidats_ppi, key=lambda indicador: indicador[0]) #ordenem ordre creixent de ppi
                            if opcio_candidat==2:
                                candidats=sorted(candidats_ppi, key=lambda indicador: indicador[0],reverse=True) #ordenem decreient ppi
                            if opcio_candidat==3:
                                candidats=sorted(candidats_us, key=lambda indicador: indicador[0])
                            if opcio_candidat==4:
                                candidats=sorted(candidats_us, key=lambda indicador: indicador[0],reverse=True)

                            if candidats != []:

                                #print('ha entrat amb rap'+str(rap)+' i rbp '+ str(rbp) + 'i us dispos ' + str(us_dispos))
                                emisora=candidats[0][1]
                                us_dispos[emisora]-=demanda/(1-d['PPI'][emisora][illa])
                                enviaments[emisora].append(illa)
                                elem_illa[illa][1]=rbp[1]
                                cost_acum+=d['CRBP'][rbp[1]]
                                tipus2=True
                                Ii.pop(0)


                        if rbp[0]>=rap[0] or tipus2==False:

                            elem_illa[illa][0]=rap[1]
                            cost_acum += d['CRAP'][rap[1]]
                            Ii.pop(0)
                            us_sobrant=d['CMRAP'][rap[1]]-demanda
                            #ela=millor_ela(d,Ie[2],us_sobrant)#potser faria una funció per fer més òptima aquesta tria
                            if opcio_ela==1:
                                ela=Ie[2][0][1] #ens quedem amb el primer candidat de la llista segons indicador

                            if opcio_ela==2: #agafem ela que te una capacitat el mes semblant possible a les us sobrants
                                l_dif= [(Ie[2][i][1],abs(Ie[2][i][0]-us_sobrant)) for i in range(len(Ie[2]))]
                                l_ela=sorted(l_dif, key=lambda dif: dif[1])
                                ela=l_ela[0][0]

                            if us_sobrant>=d['CMELA'][ela]:
                                us_dispos[illa]=d['CMELA'][ela]
                            else:
                                us_dispos[illa]=us_sobrant
                            elem_illa[illa][2]=ela
                            #print(us_dispos, us_sobrant, demanda)

                            cost_acum += d['CELA'][ela]
                    nsol+=1

                    for i in range(d['N']):
                        elem_illa[i][3]=l_ECA[i]
                        cost_acum+=d['CECA'][l_ECA[i]]

                        if enviaments[i]==[] and us_dispos[i]!= 0 and elem_illa[i][2]!=-1 and elem_illa[i][0]!=-1: #treure ELAs q no envien

                            cost_acum-=d['CELA'][elem_illa[i][2]]
                            elem_illa[i][2]=-1

                        if elem_illa[i][2]!=-1: #no sembla que aporti millores
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

                    if l_sol_print==[]:
                        l_sol_print.append([solucio[0],solucio[1],nsol])

                    else:
                        sol_anterior=l_sol_print[-1]
                        if solucio[0]<sol_anterior[0]:
                            l_sol_print.append([solucio[0],solucio[1],nsol])
                            print([solucio[0],solucio[1],nsol])



                    cost.append(cost_acum)
                    elems.append(elem_illa)
                    enviats.append(enviaments)
                    l_sol.append(solucio)


            #print('soluuu',solucio)

    millor_sol=l_sol[l_sol_print[-1][2]-1]

    return elems, enviats, cost, l_sol_print, l_sol,millor_sol
