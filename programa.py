from extreure_dades import extreure_dades
from indicadors import generar_indicadors
import time

Tinici = time.time()
d=extreure_dades('ejemplar.txt')
Irap,Irbp,Iela,Ipeca,Ipeca_ds,ID=generar_indicadors(d)
print(d)

#Preproces
#escollim el ECA de cada illa
ECA_i=0
l_ECA=[]
cost=10e15
for i in range(d['N']):
    cost=10e15
    for e in range(len(d['CMECA'])):
        if d['DS'][i]<=(1-d['PECA'][i])*d['CMECA'][e]:
            if d['CECA'][e]<=cost:
                ECA_i=e
                cost=d['CECA'][e]
    l_ECA.append(ECA_i)
    print(l_ECA)

#candidats RAP
candidats_RAP=[]
candidats_RAP_i=[]
for i in range(d['N']):
    for e in range(len(d['CMRAP'])):
        if d['DS'][i]<=(1-d['PECA'][i])*d['CMRAP'][e]:
            candidats_RAP_i.append(e)
    candidats_RAP.append(candidats_RAP_i)
    candidats_RAP_i=[]

print(candidats_RAP)

#candidats RBP
candidats_RBP=[]
candidats_RBP_i=[]
for i in range(d['N']):
    for e in range(len(d['CMRBP'])):
        if d['DS'][i]<=(1-d['PECA'][i])*d['CMRBP'][e]:
            candidats_RBP_i.append(e)
    candidats_RBP.append(candidats_RBP_i)
    candidats_RBP_i=[]

print(candidats_RBP)



#heuristica4

ID_h1=ID
while len(ID_h1)>0:
    illa=ID_h1[0]
    index=illa[1]
    DS=illa[0]
    RAP=
