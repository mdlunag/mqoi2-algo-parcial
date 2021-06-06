import time
import random

def heuristica1_aleat(l_ie,l_ii,d, candidats_RAP, candidats_RBP, l_ECA, temps_inici,l_sol_print, millor_sol,temps1a,k):
    illa=None
    cost=[]
    elems=[] #elements triats pr cada illa i, rap,rbp,ela
    enviats=[]
    l_sol1=[]
    l_sol_print1=[]
    l_sol_print=l_sol_print[:]
    nsol=0
    opcio_elas=1
    l_reves=[True,False]
    t_ini=time.time()
    t_final=time.time()
    l_k=k
    while t_final-t_ini<temps1a:
        for k in l_k:
            for reves in l_reves:
                for ie in range(len(l_ie)):
                    Ie=l_ie[ie][:]

                    for ii in range(len(l_ii)):
                        Ii=l_ii[ii][:]
                        if ii==1:
                            ii_r=0
                        else:
                            ii_r=1
                        Ii_r=l_ii[ii_r][:]
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
                            k_illa=min(k,len(Ii))-1
                            nilla=random.randint(0,k_illa) #index illa
                            illa=Ii[nilla][1] #num illa
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
                            Ii.pop(nilla)
                            Ii_r.pop(len(Ii_r)-nilla-1)
                            cost_acum += d['CELA'][ela]
                            if not reves:
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


                            else:

                                while len(Ii)>0 and Ii_r[0][0]/(1-d['PPI'][illa][Ii_r[0][1]]) <= us_dispos:
                                    rbp=(-1,-1)
                                    nrbp=0
                                    while rbp[1] not in candidats_RBP[Ii_r[0][1]]:
                                        rbp=Ie[1][nrbp]
                                        nrbp+=1
                                    elem_illa[Ii_r[0][1]][1]=rbp[1]
                                    cost_acum+=d['CRBP'][rbp[1]]
                                    us_dispos -= Ii_r[0][0]/(1-d['PPI'][illa][Ii_r[0][1]])
                                    enviaments[illa].append(Ii_r[0][1])
                                    Ii_r.pop(0)
                                    Ii.pop(-1)




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
                                elem_illa[i][2]=ela

                            if elem_illa[i][0]!=-1: #mirem si podria anar un rap mes barat
                                enviat=0
                                for illa_enviada in enviaments[i]:
                                    enviat+=d['DS'][illa_enviada]/(1-d['PPI'][i][illa_enviada])
                                l_rap=l_ie[0][0].copy() #indicador de preu i raps
                                rap=l_rap[0][1]
                                rebut=enviat+d['DS'][i]
                                while rebut>d['CMRAP'][rap]:
                                    rap=l_rap[0][1]
                                    l_rap.pop(0)

                                cost_acum-=d['CRAP'][elem_illa[i][0]]
                                cost_acum+=d['CRAP'][rap]
                                elem_illa[i][0]=rap

                            if elem_illa[i][1]!=-1: #mirem si podria anar un rbp mes barat
                                rebut=d['DS'][i]
                                l_rbp_preu=[]
                                rbp=(-1,-1)
                                nrbp=0
                                for e in range(len(l_ie[0][1])+1):

                                    if rbp[1] in candidats_RBP[i]:
                                        l_rbp_preu.append(rbp)
                                    if nrbp!=len(l_ie[0][1]):
                                        rbp=Ie[1][nrbp]
                                    nrbp+=1
                                rbp=l_rbp_preu[0]

                                while rebut>d['CMRBP'][rbp[1]]:
                                    l_rbp_preu.pop(0)
                                    rbp=l_rbp_preu[0][1]
                                cost_acum-=d['CRBP'][elem_illa[i][1]]
                                cost_acum+=d['CRBP'][rbp[1]]
                                elem_illa[i][1]=rbp[1]



                        temps_final_i=time.time()-temps_inici
                        t_final=time.time()

                        for i in range(len(elem_illa)):
                            for i2 in range(len(elem_illa[i])):
                                    elem_illa[i][i2] +=1

                        for i in range(len(enviaments)):
                            for i2 in range(len(enviaments[i])):
                                        enviaments[i][i2]+=1

                        solucio=[cost_acum,temps_final_i, elem_illa,enviaments,'h1a']


                        if l_sol_print1==[]:
                            l_sol_print1.append([solucio[0],solucio[1],nsol,'h1a'])

                        else:
                            sol_anterior=l_sol_print1[-1][0]
                            if solucio[0]<sol_anterior:
                                l_sol_print1.append([solucio[0],solucio[1],nsol,'h1a'])

                        if solucio[0]<l_sol_print[-1][0]:
                            l_sol_print.append([solucio[0],solucio[1],nsol,'h1a'])



                        cost.append(cost_acum)
                        elems.append(elem_illa)
                        enviats.append(enviaments)
                        l_sol1.append(solucio)

                        #print('soluuu',solucio)

    millor_sol1=l_sol1[l_sol_print1[-1][2]-1]
    if millor_sol1[0]<millor_sol[0]:
        millor_sol = millor_sol1

    return elems, enviats, cost, l_sol_print1, l_sol1, l_sol_print,millor_sol
