from extreure_dades import extreure_dades
from indicadors import generar_indicadors
from triar_ela import millor_ela
import time
from heuristica3 import heuristica3

temps_inici = time.time()
d=extreure_dades('ejemplar.txt')

#PREPROCES
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


#heuristica3
l_ie=[IC,ICC, ICM]
l_ii=[IDmin, IDmax, Ippi]

#l_ie=[ICM]
#l_ii=[IDmax]

elems, enviats, cost, l_sol_print, l_sol=heuristica3(l_ie,l_ii,d, candidats_RAP, candidats_RBP,l_ECA, temps_inici)
temps_final=time.time()-temps_inici
millor_sol=l_sol[l_sol_print[-1][2]-1]


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


#Prints per comprovar

#print('elems',elems)

#print('enviats',enviats)

print('COST',cost)

#print('l_sol_print',l_sol_print)

#print('millor_sol_enviaments',millor_sol[3])

print('nombre illes: ',d['N'])



#solucio=[cost_acum,temps_final, elem_illa,enviaments]
