from extreure_dades import extreure_dades
from indicadors import generar_indicadors
from triar_ela import millor_ela
import time

Tinici = time.time()
d=extreure_dades('ejemplar.txt')

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
            print(d['DS'][i],d['CMRAP'][e])
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
illa=None
l_ie=[IC,ICC,ICM]
l_ii=[IDmin, IDmax, Ippi]
l=[0]*d['N'] #us disponibles a la illa i per enviar
us_dispos=l[:]
l2=[[]]*d['N']
enviaments=l2[:] #a quines illes envia l'illa i
cost=[]
elems=[]
 #elements triats pr cada illa i, rap,rbp,ela

for ie in range(len(l_ie)):
    Ie=l_ie[ie][:]

    for ii in range(len(l_ii)):
        Ii=l_ii[ii][:]
        elem_illa=[]
        enviaments=l2[:]
        cost_acum=0
        for a in range(d['N']):
            elem_illa.append([-1,-1,-1,-1])

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
                if rbp[0]<rap[0] and us_dispos != [0]*d['N']: #rbp millor que rap i us_dispos te elements dif de 0
                    for i,e in enumerate(us_dispos):
                        if d['PPI'][i][illa]!=0 and e/(1-d['PPI'][i][illa])>= demanda:
                            candidats.append((e,i)) #candidat_i=(us_dispos,num_illa)
                    candidats=sorted(candidats, key=lambda indicador: indicador[0])

                    if candidats != []:

                        #print('ha entrat amb rap'+str(rap)+' i rbp '+ str(rbp) + 'i us dispos ' + str(us_dispos))
                        escollit=candidats[0][1]
                        us_dispos[escollit]-=demanda/(1-d['PPI'][escollit][illa])
                        enviaments[escollit]=illa
                        elem_illa[illa][1]=rbp[1]
                        cost_acum+=d['CRBP'][rbp[1]]
                        tipus2=True
                        Ii.pop(0)


                if rbp[0]>=rap[0] or tipus2==False:
                    #print('ha entrat  SEGON IF amb rap'+str(rap)+' i rbp '+ str(rbp) + 'i us dispos ' + str(us_dispos))
                    elem_illa[illa][0]=rap[1]
                    cost_acum += d['CRAP'][rap[1]]
                    #print('rap',rap[0], demanda)

                    Ii.pop(0)
                    if d['CMRAP'][rap[1]]>demanda:

                        us_sobrant=rap[0]-demanda
                        ela=millor_ela(d,Ie[2],us_sobrant)
                        us_dispos[illa]=us_sobrant
                        elem_illa[illa][2]=ela

                        cost_acum += d['CELA'][ela]




        for i in range(d['N']):
            elem_illa[i][3]=l_ECA[i]
            cost_acum+=d['CECA'][l_ECA[i]]

        cost.append(cost_acum)
        elems.append(elem_illa)

        #print(elem_illa)



print(cost)

print(elems)

print(enviaments)
