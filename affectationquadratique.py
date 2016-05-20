from time import *
from tkinter import *
from random import *
from math import *
from time import *

#AFFECTATION QUADRATIQUE
nbModules = 12
nbColonnes = 4
modules = [i+1 for i in range(nbModules)]
#start with 5
#modules[0] = 5
#modules[4] = 1

nombresDeLiaisons = [[0 for i in range(nbModules)] for j in range(nbModules)]
nombresDeLiaisons[1][0] = 180
nombresDeLiaisons[2][0] = 120
nombresDeLiaisons[9][0] = 104
nombresDeLiaisons[10][0] = 112
nombresDeLiaisons[2][1] = 96
nombresDeLiaisons[3][1] = 2445
nombresDeLiaisons[4][1] = 78
nombresDeLiaisons[6][1] = 1395
nombresDeLiaisons[8][1] = 120
nombresDeLiaisons[9][1] = 135
nombresDeLiaisons[5][2] = 221
nombresDeLiaisons[8][2] = 315
nombresDeLiaisons[9][2] = 390
nombresDeLiaisons[4][3] = 108
nombresDeLiaisons[5][3] = 570
nombresDeLiaisons[6][3] = 750
nombresDeLiaisons[8][3] = 234
nombresDeLiaisons[11][3] = 140
nombresDeLiaisons[6][4] = 225
nombresDeLiaisons[7][4] = 135
nombresDeLiaisons[9][4] = 156
nombresDeLiaisons[6][5] = 615
nombresDeLiaisons[11][5] = 45
nombresDeLiaisons[7][6] = 2400
nombresDeLiaisons[9][6] = 187
nombresDeLiaisons[10][9] = 36
nombresDeLiaisons[11][9] = 1200
nombresDeLiaisons[11][10] = 225
for i in range(nbModules):
    for j in range(nbModules):
        nombresDeLiaisons[i][j] = nombresDeLiaisons[j][i] 
#shuffle(modules)

#1 - Distance entre deux emplacements en fonction de d
def distanceEntreEmplacements(i, j, d = 1):
    xi = i%nbColonnes
    yi = int(i/nbColonnes)
    xj = j%nbColonnes
    yj = int(j/nbColonnes)
    deltaX = xi-xj if xi>xj else xj-xi
    deltaY = yi-yj if yi>yj else yj-yi
    return fabs(deltaX+deltaY) * d

def nombreDeLiaisonsEntreModules(m1,m2):
    return nombresDeLiaisons[m1-1][m2-1]

def coutEntreModules(lesModules, m1, m2):
    #print("==================[",m1,",",m2,"]==================")
    #print("Distance : ", distanceEntreEmplacements(lesModules.index(m1), lesModules.index(m2)))
    #print("Nombre de liaisons :", nombreDeLiaisonsEntreModules(m1, m2))
    return distanceEntreEmplacements(lesModules.index(m1), lesModules.index(m2)) * nombreDeLiaisonsEntreModules(m1, m2)

def coutSolution(solution):
    cout = 0
    # Comme le nombre de liaisons entre deux modules non lies est de 0
    # on peut boucler sur tous les modules
    for i in range(len(solution)):
        for j in range(i,len(solution)):
            cout += coutEntreModules(solution, solution[i], solution[j])
    return cout

def nombreTotaleDeLiaisonsPourModule(m1):
    liaisons = 0
    for i in range(m1-1,len(nombresDeLiaisons[m1-1])):
        liaisons += nombresDeLiaisons[m1-1][i]
    return liaisons

def rechercheExhaustiveAvecElagage():
    meilleureSolutionInitiale = (list(modules), coutSolution(modules))
    solutionDepart = []
    modulesAPlacer = list(modules)
    cout = 0
    def parcours_recursif( cout, meilleure_solution , listModulesPlaces , listModulesNonPlaces ):
        for module in listModulesNonPlaces:
            nouveauCout = cout
            if len(listModulesPlaces)==1:
                print("Step : ", listModulesPlaces[0])
            listModulesPlaces.append(module)
            for i in range(len(listModulesPlaces)):
                nouveauCout = nouveauCout + coutEntreModules(listModulesPlaces, listModulesPlaces[i], module)
            #print("Nouveau cout : ",  nouveauCout, " - ", listModulesPlaces)
            if nouveauCout > meilleure_solution[1]:
                listModulesPlaces.pop()
                return meilleure_solution

            copieListeModulesNonPlaces = list( listModulesNonPlaces )
            copieListeModulesNonPlaces.remove( module )
            
            if len( listModulesPlaces ) == nbModules:
                if nouveauCout < meilleure_solution[1]:
                    print("Meilleur cout : ", nouveauCout, " - ", listModulesPlaces, " < ", meilleure_solution[1])
                    meilleure_solution = (list(listModulesPlaces), nouveauCout)
            else:
                meilleure_solution = parcours_recursif(nouveauCout, meilleure_solution , listModulesPlaces, copieListeModulesNonPlaces )
            listModulesPlaces.pop()
        return meilleure_solution
    return parcours_recursif(cout, meilleureSolutionInitiale , solutionDepart , modulesAPlacer )

def rechercheExhaustiveAvecElagageAvance():
    meilleureSolutionInitiale = (list(modules), coutSolution(modules))
    solutionDepart = []
    modulesAPlacer = list(modules)
    cout = 0
    def parcours_recursif( cout, meilleure_solution , listModulesPlaces , listModulesNonPlaces ):
        for module in listModulesNonPlaces:
            nouveauCout = cout
            if len(listModulesPlaces)==1:
                print("Step : ", listModulesPlaces[0])
            listModulesPlaces.append(module)
            for i in range(len(listModulesPlaces)):
                nouveauCout = nouveauCout + coutEntreModules(listModulesPlaces, listModulesPlaces[i], module)
            copieListeModulesNonPlaces = list( listModulesNonPlaces )
            copieListeModulesNonPlaces.remove( module )
            coutExclusion = nouveauCout
            for i in range(len(copieListeModulesNonPlaces)):
                coutExclusion += nombreTotaleDeLiaisonsPourModule(copieListeModulesNonPlaces[i])
            if coutExclusion > meilleure_solution[1]:
                #print("Elagage ", listModulesPlaces, " - ", coutExclusion)
                listModulesPlaces.pop()
                return meilleure_solution
            
            if len( listModulesPlaces ) == nbModules:
                if nouveauCout < meilleure_solution[1]:
                    print("Meilleur cout : ", nouveauCout, " - ", listModulesPlaces, " < ", meilleure_solution[1])
                    meilleure_solution = (list(listModulesPlaces), nouveauCout)
            else:
                meilleure_solution = parcours_recursif(nouveauCout, meilleure_solution , listModulesPlaces, copieListeModulesNonPlaces )
            listModulesPlaces.pop()
        return meilleure_solution
    return parcours_recursif(cout, meilleureSolutionInitiale , solutionDepart , modulesAPlacer )
start_time = time()
laSolution = rechercheExhaustiveAvecElagageAvance()
elapsed_time = time() - start_time
nb = 0
for i in range(nbModules):
    nb += nombreTotaleDeLiaisonsPourModule(i+1)
        
print("Nombre total de liaisons : ", nb)
print("elapsed time : ", elapsed_time)
print("solution : ", laSolution[0])
print("cout : ", laSolution[1])
