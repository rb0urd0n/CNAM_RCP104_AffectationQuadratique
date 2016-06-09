from time import *
from tkinter import *
from random import *
from math import *
from time import *

#AFFECTATION QUADRATIQUE
#Initialisations
nbModules = 12
nbColonnes = 4
modules = [i+1 for i in range(nbModules)]

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

#Distance entre deux emplacements en fonction de d unite de distance
def distanceEntreEmplacements(i, j, d = 1):
    xi = i%nbColonnes
    yi = int(i/nbColonnes)
    xj = j%nbColonnes
    yj = int(j/nbColonnes)
    deltaX = xi-xj if xi>xj else xj-xi
    deltaY = yi-yj if yi>yj else yj-yi
    return fabs(deltaX+deltaY) * d

#Nombre de liaisons entre module m1 et module m2
def nombreDeLiaisonsEntreModules(m1,m2):
    return nombresDeLiaisons[m1-1][m2-1]

#Cout entre module m1 et module m2 dans la disposition lesModules
def coutEntreModules(lesModules, m1, m2):
    #print("==================[",m1,",",m2,"]==================")
    #print("Distance : ", distanceEntreEmplacements(lesModules.index(m1), lesModules.index(m2)))
    #print("Nombre de liaisons :", nombreDeLiaisonsEntreModules(m1, m2))
    return distanceEntreEmplacements(lesModules.index(m1), lesModules.index(m2)) * nombreDeLiaisonsEntreModules(m1, m2)

#Cout de la solution
def coutSolution(solution):
    cout = 0
    # Comme le nombre de liaisons entre deux modules non lies est de 0
    # on peut boucler sur tous les modules
    for i in range(len(solution)):
        for j in range(i,len(solution)):
            cout += coutEntreModules(solution, solution[i], solution[j])
    return cout

#Nombre total de liaisons pour module m1 en considerant une distance de 1
def nombreTotaleDeLiaisonsPourModule(m1):
    liaisons = 0
    for i in range(m1-1,len(nombresDeLiaisons[m1-1])):
        liaisons += nombresDeLiaisons[m1-1][i]
    return liaisons

#Inverse deux modules aléatoirement
def inverseDeuxModulesAleatoirement(dispositionInitiale):
    module1 = floor(uniform(0, len(dispositionInitiale)))
    module2 = floor(uniform(0, len(dispositionInitiale)))
    while module2 == module1:
        module2 = floor(uniform(0, len(dispositionInitiale)))
    return inverseDeuxModules(dispositionInitiale, module1, module2)

#Inverse les modules aux positions module1 et module2
def inverseDeuxModules(dispositionInitiale, module1, module2):
    oldValueModule1 = dispositionInitiale[module1]
    dispositionInitiale[module1] = dispositionInitiale[module2]
    dispositionInitiale[module2] = oldValueModule1
    return dispositionInitiale

#Renverse la sous liste entre depart et arrivee dans la liste
def renverseSousListe( liste , depart , arrivee ):
    longueur = len( liste )
    while( depart!=arrivee):
        position_depart = liste[depart]
        liste[depart] = liste[arrivee]
        liste[arrivee] = position_depart
        delta = abs( depart - arrivee ) 
        if (  delta == 1 or delta == (longueur-1)):
            break
        depart = (depart+1)%longueur
        arrivee = (arrivee-1)%longueur
    return liste

#Rechercher exhaustive des solutoins avec elagage basique
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
            #Calcul du nouveau cout avec le module ajoute
            for i in range(len(listModulesPlaces)):
                nouveauCout = nouveauCout + coutEntreModules(listModulesPlaces, listModulesPlaces[i], module)
            #print("Nouveau cout : ",  nouveauCout, " - ", listModulesPlaces)
            if nouveauCout > meilleure_solution[1]:
                #Elagage
                listModulesPlaces.pop()
                return meilleure_solution

            copieListeModulesNonPlaces = list( listModulesNonPlaces )
            copieListeModulesNonPlaces.remove( module )
            
            if len( listModulesPlaces ) == nbModules:
                if nouveauCout < meilleure_solution[1]:
                    #Une meilleure solution est trouvee
                    print("Meilleur cout : ", nouveauCout, " - ", listModulesPlaces, " < ", meilleure_solution[1])
                    meilleure_solution = (list(listModulesPlaces), nouveauCout)
            else:
                meilleure_solution = parcours_recursif(nouveauCout, meilleure_solution , listModulesPlaces, copieListeModulesNonPlaces )
            listModulesPlaces.pop()
        return meilleure_solution
    return parcours_recursif(cout, meilleureSolutionInitiale , solutionDepart , modulesAPlacer )

#Recherche exhaustive avec elagage avance
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

#Recuit simule
def recuitSimule( nbIterations, coeffTemperature ):
    meilleureDisposition = list(modules)
    meilleurCout = coutSolution(meilleureDisposition)
    print( "Solution initiale : ", meilleureDisposition, " - ", meilleurCout)

    dispositionCourante = list( meilleureDisposition )
    coutCourant = meilleurCout
    temp = meilleurCout * nbModules 

    temperature = temp
    
    for i in range( nbIterations ):
        nouvelleDisposition = list( dispositionCourante )
        nouvelleDisposition = inverseDeuxModulesAleatoirement(nouvelleDisposition)
        nouvelle_longueur = coutSolution( nouvelleDisposition )
        delta = nouvelle_longueur - coutCourant

        if ( delta < 0) or ( uniform( 0.0, 1.0 ) < exp( -delta/temperature ) ):
            dispositionCourante = nouvelleDisposition
            coutCourant = nouvelle_longueur
            if (coutCourant < meilleurCout):
                print("Longueur : ", coutCourant, " - Iteration : ", i)
                meilleureDisposition = list(dispositionCourante)
                meilleurCout = coutCourant
                
        temperature = coeffTemperature * temperature 
    return ( meilleureDisposition , meilleurCout )

#Tabou avec diversification
def algorithmeTabou( solutionInitiale, tailleListeTabou = 10, nbDiversification = 20, nbIteration = 500, deltaAspiration = 50 ):
    meilleureDispositionGlobale = list(solutionInitiale)
    meilleureCoutGlobal = coutSolution(solutionInitiale)
    meilleureSolutionGlobale = (meilleureDispositionGlobale, meilleureCoutGlobal)
    
    for div in range( nbDiversification ) :
        meilleureDisposition = list(solutionInitiale)
        shuffle(meilleureDisposition)
        meilleurCout = coutSolution( meilleureDisposition )
        meilleureSolution = ( meilleureDisposition , meilleurCout )
        dispositionCourante = list(meilleureDisposition)
        coutCourant = meilleurCout
        
        listeTabou = []
        for iter in range( nbIteration ):
            solutionTmp = None
            coutTmp = None
            meilleurMouvement = None
            meilleureSolutionTmp = (None, None)
            
            for i in range( nbModules-1 ):
                for j in range( i+1 , nbModules ):
                    mouvement = ( i , j )
                    if mouvement not in listeTabou:
                        solutionTmp = inverseDeuxModules(dispositionCourante, i, j)
                        coutTmp = coutSolution(solutionTmp)
                        if meilleureSolutionTmp[0] == None or coutTmp < meilleureSolutionTmp[1]:
                            meilleureSolutionTmp = (solutionTmp, coutTmp)
                            meilleurMouvement = mouvement
            dispositionCourante = list(meilleureSolutionTmp[0])
            coutCourant = meilleureSolutionTmp[1]
            if ( coutCourant < meilleurCout ):
                meilleurCout = coutCourant
                meilleureSolution = ( list( dispositionCourante ) , meilleurCout )
            listeTabou.append( meilleurMouvement )
            if len( listeTabou ) > tailleListeTabou:
                listeTabou.pop(0)
        if meilleureSolution[1] < meilleureSolutionGlobale[1] :
            meilleureSolutionGlobale = (list(meilleureSolution[0]), meilleureSolution[1])
        #print("Diversification n ", div+1, " : ", meilleureSolutionGlobale[0], " - ", meilleureSolutionGlobale[1])
    return meilleureSolutionGlobale

start_time = time()
#laSolution = rechercheExhaustiveAvecElagageAvance()
#laSolution = recuitSimule(10000,0.999)
laSolution = algorithmeTabou(modules, 15, 15)
elapsed_time = time() - start_time

print("elapsed time : ", elapsed_time)
print("solution : ", laSolution[0])
print("cout : ", laSolution[1])