import csv
import pathlib
import os
import pandas as pd


#Fonction de chargement csv sous forme de dictionnaire
def open_csv(filename):
    actions = []
    filepath = os.path.join(pathlib.Path(__file__).parent.resolve(), filename)
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        actionlist = csv.DictReader(csvfile)
        for ligne in actionlist:
            name = ligne['name']
            try:
                cout = float(ligne['price'])
                pourcent_benef = float(ligne['profit'])
                benefice = round(cout * (pourcent_benef / 100), 2)
                if cout > 0 and pourcent_benef > 0:
                    actions.append((name, cout, benefice))
            except ValueError:
                continue
    return actions

#Fonction de calcul des bénéfices dynamique
def sac_a_dos(actions, budget_max):
    nombre_actions = len(actions)
    actions = [(name, int(price * 100), profit) for name, price, profit in actions]
    budget_max = int(budget_max * 100)
    tableau = [[0] * (budget_max + 1) for t in range(nombre_actions + 1)]
    for i in range(1, nombre_actions + 1):
        name, cout, benefice = actions[i - 1]
        for w in range(budget_max + 1):
            if cout <= w:
                tableau[i][w] = max(tableau[i - 1][w], tableau[i - 1][w - cout] + benefice)
            else:
                tableau[i][w] = tableau[i - 1][w]
    w = budget_max
    best_combinaison = []
    for i in range(nombre_actions, 0, -1):
        if tableau[i][w] != tableau[i - 1][w]:
            name, cout, benefice = actions[i - 1]
            best_combinaison.append((name, cout / 100, benefice))
            w -= cout
            
    cout_total = sum(action[1] for action in best_combinaison)
    profit_total = sum(action[2] for action in best_combinaison)
    
    
    return best_combinaison, cout_total, profit_total, tableau

#Fonction affichage du tableau des bénéfices
def afficher_tableau(tableau, step):
    df = pd.DataFrame(tableau)
    colonnes = df.columns[::step]
    df= df[colonnes]
    
    return df


#Affichage résultat
actions = open_csv('dataset1.csv')
best_combinaison, cout_total, profit, tableau = sac_a_dos(actions, 500)
for action in best_combinaison:
    print(f"{action[0]} Cout : {action[1]} Bénéfice: {round(action[2], 2)}")
print(f"Profit total après 2 ans : {round(profit, 2)}")
print(f"Cout total : {cout_total}")


print(afficher_tableau(tableau, 50))