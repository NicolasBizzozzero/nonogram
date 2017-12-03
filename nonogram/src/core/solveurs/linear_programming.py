# -*-   coding: utf-8 -*-
import numpy as np
import time
from gurobipy import *  #TODO: Importer les element uns par uns

from nonogram.src.core.vrac.decorateurs import timeit
from nonogram.src.core.solveurs.solveur_utils import CASE_BLANCHE, CASE_NOIRE, CASE_VIDE,\
    GrilleImpossible
from nonogram.src.core.solveurs.dynamic_programming import propagation


#sequence est une liste de deux lists, 
#premier liste contient les sequence des lignes et deuxiem sequence des colones
def PL(contraintes_lignes, contraintes_colonnes,instancename,grille,mode,mode_PL):
    #Declaration 
    N , M ,time1 = len(contraintes_lignes), len(contraintes_colonnes),  time.time()
    m , c = Model("coloration")  ,0
    not_interdit_Y = not_interdit(contraintes_lignes,N,M,mode_PL)
    not_interdit_Z = not_interdit(contraintes_colonnes,M,N,mode_PL)
    
    
    #varibale type 1 X i,j
    lx = np.array([[m.addVar(vtype=GRB.BINARY,  name="x,%d,%d," % (i,j)) for j in range(M)\
                   ]for i in range(N)])
    #varibale type 2 Y i,j,t
    ly = np.array([[[ m.addVar(vtype=GRB.BINARY,  name="y,%d,%d,%d," % (i,j,t)) if j in not_interdit_Y[i][t] else None\
                     for t in range(len(contraintes_lignes[i]))] for j in range(M)] for i in range(N)])
    


    lz = np.array([[[ m.addVar(vtype=GRB.BINARY,  name="z,%d,%d,%d," % (i,j,t)) if i in not_interdit_Z[j][t] else None\
                     for t in range(len(contraintes_colonnes[j]))]  for i in range(N) ]for j in range(M)])
    
    #objectife
    m.update()
    obj = LinExpr()
    obj = sum(sum(lx))
    #sup
    if mode == 'with_propagation':
        c,k = ajoute_contraints(m,grille,contraintes_lignes, contraintes_colonnes,lx,ly,lz)
        print("Algorithme dynamique a decidé pour " + str(k) + " case")
        if k == N*M:
            return (grille , 0,0,0)
    
   

    
    #lignes:
    # Yijt =1 0<=j < M un bloc commence a une seul case    
    for i in range(N):
        for t in range(len(contraintes_lignes[i])):
            l1 = [ly[i,k][t] for k in range(M) if ly[i,k][t] != None]
            if len(l1) > 0:
                m.addConstr(quicksum(key1 for key1 in l1 ),GRB.EQUAL, 1 , "C:%d/mutuelle/L:%d" % (c,i))
                c +=1 
                
    #l'order , Decalage  et Q10                  
    for i in range(N):
        for j in range(M):
            for t in range(len(contraintes_lignes[i])):
                if ly[i,j][t] != None:
                    l1 = []
                    for t1 in range(t+1 ,len(contraintes_lignes[i]) ):
                        l1 += [ly[i,k][t1] for k in range(0,j+contraintes_lignes[i][t]+1) \
                                                    if k < M and  ly[i,k][t1] != None]
                    if len(l1) > 0:
                        m.addConstr( len(l1) * ly[i,j][t] + quicksum(keyy for keyy in l1)<= len(l1) , "C:%d/ordre/L:%d" % (c,i))
                        c +=1
                    l1 = [ lx[i,k] for k in range(j,j+contraintes_lignes[i][t]) if k < M]
                    if len(l1) > 0:
                        m.addConstr(contraintes_lignes[i][t] * ly[i,j][t] <= quicksum(keyx for keyx in l1), "C:%d/Q10/L:%d" % (c,i))
                        c +=1
            for t in range(len(contraintes_colonnes[j])):
                if lz[j,i][t] != None:
                    l1 = []
                    for t1 in range(t+1,len(contraintes_colonnes[j]) ):
                        
                        l1 += [lz[j,k][t1]  for k in range\
                                        (0,i+contraintes_colonnes[j][t]+1) if k < N  and  lz[j,k][t1] != None]
                    if len(l1)> 0:
                        m.addConstr( len(l1) * lz[j,i][t] + quicksum(keyz for keyz in l1) <= len(l1) , "C:%d/ordre/C:%d" % (c,j))  
                        c +=1
                    l1 = [lx[k,j] for k in range(i,i+contraintes_colonnes[j][t]) if k < N]
                    if len(l1) > 0:
                        m.addConstr(contraintes_colonnes[j][t] * lz[j,i][t] <= quicksum(keyx for keyx in l1 ), "C:%d/Q10/C:%d" % (c,j))
                        c +=1
    
    #LES COLONES 
    # Zijt =1 0<=j < M un bloc commence a une seul case        
    for j in range(M):
        for t in range(len(contraintes_colonnes[j]) ):
            l1 = [lz[j,i][t] for i in range(N)  if lz[j,i][t] != None]
            if len(l1) > 0:
                m.addConstr(quicksum(key1 for key1 in l1),GRB.EQUAL, 1 ,  "C:%d/mutuelle/C:%d" % (c,j))
                c += 1  
    # definition de l'objectif
    m.setObjective(obj,GRB.MINIMIZE)
    m.update()
    time2 = time.time()
    #Ecriteur de la programme linaire dans ficher .pl
    m.write(str(mode)+"_"+str(mode_PL)+"_programme/"+str(instancename)+".lp")
    
    # Resolution
    time3 = time.time()
    m.optimize()
    time4= time.time()
    
    #Construction grille
    for i in range(N):
        for j in range(M):
            if grille[i,j] == 0:
                val =  lx[i,j].x
                if val < 0 or (val >= 0 and val < .5) :
                    grille[i,j] = -1
                else:
                    grille[i,j] = 1
                
    t_toatal = time.time()
    return (grille,time2-time1,time4-time3,t_toatal - time1)


#si in veut non interdit pour les lignes: N est nombres des lignes , M est nombres des colones et indice = 0
#si on veut  non interdit pour les colone : N est nombre des colones et M est nombre des lignes et  indice = 1
def not_interdit(sequence,N,M,mode_PL):
    if mode_PL == 'Optimize':
        return_list = []
        for i in range(N):
            L = []
            l = sequence[i]
            for t in range(len(l) ):
                interdit = []
                o = 0
                #Les blocs avant
                for t1 in range(0,t):
                    for h in range(l[t1]):
                        interdit += [o]
                        o +=1
                    #case blanch
                    interdit += [o]
                    o +=1
                #Depasse la ligne
                for o in range(M-1,0,-1):
                    if o + l[t] > M:
                        interdit += [o] 
                o = M-1
                #Les blocs apres
                for t1 in range(len(l)-1,t,-1):
                    for h in range(l[t1]):
                        interdit += [o] 
                        o -=1
                    #case blanch
                    interdit += [o] 
                    o -=1 
                #pas confondre entre le bloc actuel et les bloc apres
                for t1 in range(l[t],1,-1):
                    interdit += [o] 
                    o -=1 
                L.append([k for k in range(M) if k not in interdit])
            return_list.append(L)
        return return_list
    return [[[j for j in range(M)] for t in range(len(sequence[i]))] for i in range(N)]


# t_c : temps contruction
# t_r : temps resolution
# t_t : temps total de PL
# t_2 - t_1 + T_t : temps total de temps total
def resoudre(contraintes_lignes, contraintes_colonnes, grille_preremplie=None):
    # Initialisation des variables
    N, M = len(contraintes_lignes), len(contraintes_colonnes)
    if not grille_preremplie:
        grille = np.full((N, M), CASE_VIDE)
    else:
        grille = grille_preremplie

    instancename = "INSTANCE"

    grille , t_c,t_R,t_T =  PL(contraintes_lignes, contraintes_colonnes, instancename, grille,'with_propagation',"Optimize")
    #return (grille, t_c,t_R,t_T,t2-t1, t_T + (t2-t1))
    return grille


if __name__ == '__main__':
    pass
