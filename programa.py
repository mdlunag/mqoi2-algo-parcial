from extreure_dades import extreure_dades
from indicadors import generar_indicadors
from triar_ela import millor_ela
import time
from heuristica3 import heuristica3
from heuristica4 import heuristica4
from heuristica1 import heuristica1
from heuristica5 import heuristica5
from postpro import postpro
from heuristica3_aleatoria import heuristica3_aleat
from heuristica5_aleatoria import heuristica5_aleat
from heuristica1_aleatoria import heuristica1_aleat


temps1a=70
temps5a=20
k=2
k1=[4,5]
temps_inici = time.time()
d=extreure_dades('ejemplar_prueba_1.txt')

#PREPROCES
#nova demanda
DS=d['DS']
PECA=d['PECA']
DS_nova=[]
for i in range(len(DS)):
    DS_nova.append(DS[i]/(1-PECA[i]))
d['DS']=DS_nova

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
#print(l_ECA)

#candidats RAP de cada illa
candidats_RAP=[]
candidats_RAP_i=[]
for i in range(d['N']):
    for e in range(d['NRAP']):
        if d['DS'][i]<=d['CMRAP'][e]:
            candidats_RAP_i.append(e)
    candidats_RAP.append(candidats_RAP_i)
    candidats_RAP_i=[]


#print(candidats_RAP)

#candidats RBP
candidats_RBP=[]
candidats_RBP_i=[]
for i in range(d['N']):
    for e in range(d['NRBP']):
        if d['DS'][i]<=d['CMRBP'][e]:
            candidats_RBP_i.append(e)
    candidats_RBP.append(candidats_RBP_i)
    candidats_RBP_i=[]

#print(candidats_RBP)

#Generem indicadors

IC,ICC,ICM,IDmin,IDmax,Ippi=generar_indicadors(d)


#heuristica3
l_ie=[IC,ICC, ICM]
l_ii=[IDmin, IDmax, Ippi]
l_ii_1=[IDmin, IDmax]


#l_ie=[ICM]
#l_ii=[IDmax]
l_sol_print3=[[100000000000,0.001,1]]
millor_sol3=[100000000000,0,[],[]]

elems3, enviats3, cost3, l_sol_print3, l_sol3, millor_sol3=heuristica3(l_ie,l_ii, d, candidats_RAP, candidats_RBP,l_ECA, temps_inici)
#elems3a, enviats_3a, cost3a, l_sol_print3a, l_sol3a, l_sol_print,millor_sol3a=heuristica3_aleat(l_ie,l_ii,d, candidats_RAP, candidats_RBP,l_ECA, temps_inici,l_sol_print3,millor_sol3,temps3a,k)
elems1, enviats1, cost1, l_sol_print1, l_sol1, l_sol_print,millor_sol1=heuristica1(l_ie,l_ii_1, d, candidats_RAP, candidats_RBP, l_ECA, temps_inici, l_sol_print3, millor_sol3)
elems1a, enviats1a, cost1a, l_sol_print1a, l_sol1a, l_sol_print,millor_sol1a=heuristica1_aleat(l_ie,l_ii_1, d, candidats_RAP, candidats_RBP, l_ECA, temps_inici, l_sol_print, millor_sol1,temps1a,k1)
elems4, enviats4, cost4, l_sol_print4, l_sol4, l_sol_print,millor_sol4=heuristica4(l_ie,l_ii, d, candidats_RAP, candidats_RBP,l_ECA, temps_inici,l_sol_print,millor_sol1a)
elems5, enviats5, cost5, l_sol_print5, l_sol5, l_sol_print,millor_sol5=heuristica5(l_ie,l_ii, d, candidats_RAP, candidats_RBP,l_ECA, temps_inici,l_sol_print,millor_sol4)
elems5a, enviats5a, cost5a, l_sol_print5a, l_sol_5a, l_sol_print,millor_sol=heuristica5_aleat(l_ie,l_ii, d, candidats_RAP, candidats_RBP,l_ECA, temps_inici,l_sol_print,millor_sol5,temps5a,k)


temps_final=time.time()-temps_inici


#escriure fitxer solucio

with open('sol.txt', 'w') as f:
    for sol in l_sol_print:
        f.write(f"{sol[0]}*{sol[1]}\n")
    f.write(f'{len(l_sol_print) - 1}\n')
    f.write(f"{l_sol_print[-1][0]}*{l_sol_print[-1][1]}\n")
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

'''
print("COST",cost3a)
#sprint('l_sol_print',l_sol_print5a)
print(millor_sol)

'''
#print('COST',cost3,cost1, cost4)

print('heuri 3\n',l_sol_print3, '\nheuri 1a\n',l_sol_print1a,'\nheuri 5\n',l_sol_print5, '\nheuri 5a\n',l_sol_print5a)

print('millor_sol',millor_sol1[0],  millor_sol1a[0], millor_sol5[0],l_sol_print5a[-1][0])

print('nombre illes: ',d['N'])

print('L_SOL_PRINT_TOT: ',l_sol_print)
print('MILLOR SOL: ', millor_sol)

print('1a:',l_sol_print1a[-1],'\n5a',l_sol_print5a[-1],'\nheuri1:',millor_sol1)


#solucio=[cost_acum,temps_final, elem_illa,enviaments]
