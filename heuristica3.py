import time

def heuristica3(l_ie,l_ii,d, candidats_RAP, candidats_RBP, l_ECA, temps_inici):
    illa=None
    cost=[]
    elems=[] #elements triats pr cada illa i, rap,rbp,ela
    enviats=[]
    l_sol=[]
    l_sol_print=[]
    nsol=0

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
            print('indicador ii',l_ii[ii])

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

                candidats=[]
                tipus2=False
                if rbp[0]<rap[0]: #rbp millor que rap i us_dispos te elements dif de 0
                    for i,e in enumerate(us_dispos):
                        if d['PPI'][i][illa]!=0 and e>=demanda/(1-d['PPI'][i][illa]):
                            candidats.append((e,i)) #candidat_i=(us_dispos,num_illa)
                    candidats=sorted(candidats, key=lambda indicador: indicador[0]) #ordenem ordre creixent

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
                    ela=Ie[2][0][1] #ens quedem amb el primer candidat de la llista segons indicador
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

                if enviaments[i]==[] and us_dispos[i]!= 0: #treure ELAs q no envien
                    elem_illa[i][2]=-1
                    cost_acum-=d['CELA'][elem_illa[i][2]]


            temps_final_i=time.time()-temps_inici
            print(cost_acum)
            solucio=[cost_acum,temps_final_i, elem_illa,enviaments]


            if l_sol_print==[]:
                l_sol_print.append([solucio[0],solucio[1],nsol])

            else:
                sol_anterior=l_sol_print[-1]
                if solucio[0]<sol_anterior[0]:
                    l_sol_print.append([solucio[0],solucio[1],nsol])
                    print('a')

            for i in range(len(elem_illa)):
                for i2 in range(len(elem_illa[i])):
                        elem_illa[i][i2] +=1

            for i in range(len(enviaments)):
                for i2 in range(len(enviaments[i])):
                            enviaments[i][i2]+=1

            cost.append(cost_acum)
            elems.append(elem_illa)
            enviats.append(enviaments)
            l_sol.append(solucio)

            print('soluuu',solucio)


    return elems, enviats, cost, l_sol_print, l_sol
