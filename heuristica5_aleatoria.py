import time
import random

def heuristica5_aleat(l_ie,l_ii,d, candidats_RAP, candidats_RBP, l_ECA, temps_inici, l_sol_print, millor_sol,temps5a,k):
    illa=None
    cost=[]
    elems=[] #elements triats pr cada illa i, rap,rbp,ela
    enviats=[]
    l_sol_post=[]
    l_sol_print_post=[]
    l_sol_print=l_sol_print.copy()
    millor_sol=millor_sol.copy()
    nsol=0
    opcio_candidats=[1,2,3,4]
    t_ini=time.time()
    t_final=time.time()
    while t_final-t_ini<temps5a:
        for opcio_candidat in opcio_candidats:
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

                        k_illa=min(k,len(Ii))-1
                        nilla=random.randint(0,k_illa)
                        illa=Ii[nilla][1] #num illa
                        demanda=d['DS'][illa]
                        l_rap=[]
                        l_rbp=[]
                        rap=(-1,-1)
                        rbp=(-1,-1)
                        nrap=0
                        nrbp=0
                        for e in range(len(Ie[0])+1):
                            if rap[1] in candidats_RAP[illa]:
                                l_rap.append(rap)
                            if nrap!=len(Ie[0]):
                                rap=Ie[0][nrap]
                            nrap+=1
                        if len(l_rap) >1:
                            k_rap=min(k,len(l_rap))-1
                            rap=l_rap[random.randint(0,k_rap)]
                        else:
                            rap=l_rap[0]

                        for e in range(len(Ie[1])+1): #ens quedem amb el millor rap candidat segons indicador
                            if rbp[1] in candidats_RBP[illa]:
                                l_rbp.append(rbp)
                            if nrbp!=len(Ie[1]):
                                rbp=Ie[1][nrbp]
                            nrbp+=1
                        if len(l_rbp) >1:
                            k_rbp=min(k,len(l_rbp))-1
                            rbp=l_rbp[random.randint(0,k_rbp)]
                        else:
                            rbp=l_rbp[0]

    #primer triem raps i rbps segons si d>cmrbp millor
                        if demanda<=d['CMRBP'][rbp[1]]:
                            elem_illa[illa][1]=rbp[1]
                            cost_acum+=d['CRBP'][rbp[1]]
                            Ii.pop(nilla)
                        else:
                            elem_illa[illa][0]=rap[1]
                            cost_acum += d['CRAP'][rap[1]]
                            us_sobrant=d['CMRAP'][rap[1]]-demanda

                            ela=Ie[2][0][1] #ens quedem amb el primer candidat de la llista segons indicador
                            if us_sobrant>=d['CMELA'][ela]:
                                us_dispos[illa]=d['CMELA'][ela]
                            else:
                                us_dispos[illa]=us_sobrant
                            elem_illa[illa][2]=ela
                            cost_acum += d['CELA'][ela]
                            Ii.pop(nilla)

    #mirem illa per illa qui pot donarnos us, si ningu pot passa a posarse rap

                    for illa in range(d['N']): #illa que mirem
                        demanda=d['DS'][illa]
                        if elem_illa[illa][1]!= -1: #té rbp

                            candidats_ppi=[]
                            candidats_us=[]
                            for i,e in enumerate(us_dispos): #i es illa emisora
                                if d['PPI'][i][illa]!=0 and e>=demanda/(1-d['PPI'][i][illa]):
                                    candidats_ppi.append((d['PPI'][i][illa],i)) #candidat_i=(us_dispos,num_illa)
                                    candidats_us.append((e,i))
                            if opcio_candidat==1:
                                candidats=sorted(candidats_ppi, key=lambda indicador: indicador[0]) #ordenem ordre creixent de ppi
                            if opcio_candidat==2:
                                candidats=sorted(candidats_ppi, key=lambda indicador: indicador[0],reverse=True) #ordenem decreient ppi
                            if opcio_candidat==3:
                                candidats=sorted(candidats_us, key=lambda indicador: indicador[0])
                            if opcio_candidat==4:
                                candidats=sorted(candidats_us, key=lambda indicador: indicador[0],reverse=True)
                            k_candidat=min(k,len(candidats))-1

                            if candidats != []:

                                #print('ha entrat amb rap'+str(rap)+' i rbp '+ str(rbp) + 'i us dispos ' + str(us_dispos))
                                emisora=candidats[random.randint(0,k_candidat)][1]
                                #emisora=candidats[0][1]

                                us_dispos[emisora]-=demanda/(1-d['PPI'][emisora][illa])
                                enviaments[emisora].append(illa)
                            else: #ningu pot donarli, ha de tenir rap, treiem rbp
                                cost_acum-=d['CRBP'][elem_illa[illa][1]]
                                elem_illa[illa][1] = -1
                                rap=(-1,-1)
                                nrap=0
                                l_rap=[]
                                '''
                                for e in range(len(Ie[0])+1):
                                    if rap[1] in candidats_RAP[illa]:
                                        l_rap.append(rap)
                                    if nrap!=len(Ie[0]):
                                        rap=Ie[0][nrap]
                                    nrap+=1
                                if len(l_rap) >1:
                                    k_rap=min(k,len(l_rap))-1
                                    rap=l_rap[random.randint(0,k_rap)]
                                else:
                                    rap=l_rap[0]
                                '''
                                while rap[1] not in candidats_RAP[illa]: #ens quedem amb el millor rap candidat segons indicador
                                    rap=Ie[0][nrap]
                                    nrap+=1

                                elem_illa[illa][0]=rap[1]
                                cost_acum += d['CRAP'][rap[1]]
                                us_sobrant=d['CMRAP'][rap[1]]-demanda
                                ela=Ie[2][0][1] #ens quedem amb el primer candidat de la llista segons indicador
                                if us_sobrant>=d['CMELA'][ela]:
                                    us_dispos[illa]=d['CMELA'][ela]
                                else:
                                    us_dispos[illa]=us_sobrant
                                elem_illa[illa][2]=ela
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
                            cost_acum-=d['CELA'][elem_illa[i][2]]
                            cost_acum+=d['CELA'][ela]
                            elem_illa[i][2]=ela

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

                        if elem_illa[i][0]!=-1: #mirem si podria anar un rap mes barat
                            enviat=0
                            for illa_enviada in enviaments[i]:
                                enviat+=d['DS'][illa_enviada]/(1-d['PPI'][i][illa_enviada])
                            l_rap=l_ie[0][0].copy() #indicador de preu i raps
                            rap=l_rap[0][1]
                            rebut=enviat+d['DS'][i]
                            while rebut>d['CMRAP'][rap]:
                                l_rap.pop(0)
                                rap=l_rap[0][1]
                            cost_acum-=d['CRAP'][elem_illa[i][0]]
                            cost_acum+=d['CRAP'][rap]
                            elem_illa[i][0]=rap


                    temps_final_i=time.time()-temps_inici
                    t_final=time.time()

                    for i in range(len(elem_illa)):
                        for i2 in range(len(elem_illa[i])):
                                elem_illa[i][i2] +=1

                    for i in range(len(enviaments)):
                        for i2 in range(len(enviaments[i])):
                                    enviaments[i][i2]+=1

                    solucio=[cost_acum,temps_final_i, elem_illa,enviaments,'h5a']

                    if l_sol_print_post==[]:
                        l_sol_print_post.append([solucio[0],solucio[1],nsol,'h5a'])

                    else:
                        sol_anterior=l_sol_print_post[-1][0]
                        if solucio[0]<sol_anterior:
                            l_sol_print_post.append([solucio[0],solucio[1],nsol,'h5a'])

                    if solucio[0]<l_sol_print[-1][0]:
                        l_sol_print.append([solucio[0],solucio[1],nsol,'h5a'])



                    cost.append(cost_acum)
                    elems.append(elem_illa)
                    enviats.append(enviaments)
                    l_sol_post.append(solucio)


                #print('soluuu',solucio)

    millor_sol_post=l_sol_post[l_sol_print_post[-1][2]-1]

    if millor_sol_post[0]<millor_sol[0]:
        millor_sol = millor_sol_post

    return elems, enviats, cost, l_sol_print_post, l_sol_post, l_sol_print, millor_sol
