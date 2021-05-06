from extreure_dades import extreure_dades
from indicadors import generar_indicadors
from triar_ela import millor_ela
import time
from heuristica3 import heuristica3

temps_inici = time.time()
d=extreure_dades('ejemplar_2.txt')

#Preproces

#nova demanda
DS=d['DS']
PECA=d['PECA']
DS_nova=[]
for i in range(len(DS)):
    DS_nova.append(DS[i]/(1-PECA[i]))
d['DS']=DS_nova
print(DS_nova)


#escollim el ECA de cada illa
ECA_i=0
l_ECA=[]
cost=10e15
for i in range(d['N']):
    cost=10e15
    for e in range(len(d['CMECA'])):
        if d['DS'][i]<=d['CMECA'][e]:
            if d['CECA'][e]<=cost:
                ECA_i=e
                cost=d['CECA'][e]
    l_ECA.append(ECA_i)
print(l_ECA)

#candidats RAP
candidats_RAP=[]
candidats_RAP_i=[]
for i in range(d['N']):
    for e in range(d['NRAP']):
        if d['DS'][i]<=d['CMRAP'][e]:
            candidats_RAP_i.append(e)
    candidats_RAP.append(candidats_RAP_i)
    candidats_RAP_i=[]

print(candidats_RAP)

#candidats RBP
candidats_RBP=[]
candidats_RBP_i=[]
for i in range(d['N']):
    for e in range(d['NRBP']):
        if d['DS'][i]<=d['CMRBP'][e]:
            candidats_RBP_i.append(e)
    candidats_RBP.append(candidats_RBP_i)
    candidats_RBP_i=[]

print(candidats_RBP)

#Generem indicadors

IC,ICC,ICM,IDmin,IDmax,Ippi=generar_indicadors(d)

#print(d)


#heuristica3
l_ie=[IC,ICC,ICM]
l_ii=[IDmin, IDmax, Ippi]
elems, enviats, cost, l_sol_print, l_sol=heuristica3(l_ie,l_ii,d, candidats_RAP, candidats_RBP,l_ECA, temps_inici)
"""
illa=None
l_ie=[IC,ICC,ICM]
l_ii=[IDmin, IDmax, Ippi]

#l_ie=[IC]
#l_ii=[IDmax]
l=[0]*d['N'] #us disponibles a la illa i per enviar
us_dispos=l[:]
enviaments=[] #a quines illes envia l'illa i
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
        cost_acum=0
        solucio=[]
        for a in range(d['N']):
            elem_illa.append([-1,-1,-1,-1])
            enviaments.append([])

        while len(Ii)>0:

            if len(Ii)>1 and Ii[0][1]==Ii[1][1]: #si hi ha empat entre 2 millors illes
                pass
            else:

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
        temps_final_i=time.time()-temps_inici
        solucio=[cost_acum,temps_final_i, elem_illa,enviaments]


        if l_sol_print==[]:
            l_sol_print.append([solucio[0],solucio[1],nsol])

        else:
            sol_anterior=l_sol_print[-1]
            if solucio[0]<sol_anterior[0]:
                l_sol_print.append([solucio[0],solucio[1],nsol])
                print('a')

        cost.append(cost_acum)
        elems.append(elem_illa)
        enviats.append(enviaments)
        l_sol.append(solucio)

        for i in range(len(elems)):
            for i2,e2 in enumerate(elems[i]):
                for i3,e3 in enumerate(elems[i][i2]):
                    elems[i][i2][i3] = elems[i][i2][i3]+1

        for i in range(len(enviats)):
            for i2 in range(len(enviats[i])):
                for i3,e in enumerate(enviats[i][i2]):
                        enviats[i][i2][i3]=e+1
"""
temps_final=time.time()-temps_inici
#per escriure fitxer
millor_sol=l_sol[l_sol_print[-1][2]-1]



        #print(elem_illa)



print(elems)

print(enviats)

print(cost)

print(l_sol_print)

print(millor_sol[2])

#escriure fitxer solucio

with open('sol.txt', 'w') as f:
    for sol in l_sol_print:
        f.write(f"{sol[0]}*{sol[1]}\n")
    f.write(f'{len(l_sol_print) - 1}\n')
    f.write(f"{l_sol_print[-1][0]}*{temps_final}\n")
    for e in (millor_sol[2]):
        f.write(f"{e[0]}*{e[1]}*{e[2]}*{e[3]}\n")
    for e in(millor_sol[3]):
        if e ==[]:
            f.write('0\n')
        else:
            e_str=map(str,e)
            f.write(f"{len(e)}*{'*'.join(e_str)}\n")








#solucio=[cost_acum,temps_final, elem_illa,enviaments]
#si rebo 100 al RAP, demanda de 50, puc enviar 50 al ELA
