import csv
from itertools import combinations
import pathlib
import os

#Fonction de chargement csv sous forme de dictionnaire
def open_csv(filename):
    actions = []
    filepath = os.path.join(pathlib.Path(__file__).parent.resolve(), filename)
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        actionlist = csv.DictReader(csvfile)
        for ligne in actionlist:
            nom = ligne['Actions #']
            cout = int(float(ligne['Coût par action (en euros)']))
            pourcent_benef = float(ligne['Bénéfice (après 2 ans)'].replace('%', '').strip())
            benefice = round(cout * (pourcent_benef / 100), 2)
            actions.append((nom, cout, benefice))
    return actions


#Fonction de calcul des bénéfices brute force
def find_best_combinaison(actions, budget_max):
    best_profit = 0
    best_combinaison = []
    
    for i in range(1, len(actions) + 1):
        for combinaison in combinations(actions, i):
            cout_total = sum(action[1] for action in combinaison)
            if cout_total <= budget_max:
                profit_total = sum(action[2] for action in combinaison)
                if profit_total > best_profit:
                    best_profit = profit_total
                    best_combinaison = combinaison
    return best_combinaison, best_profit

#Affichage résultat
actions = open_csv('actions_P1.csv')
best_combinaison, profit = find_best_combinaison(actions, 500)
for action in best_combinaison:
    print(f"{action[0]} Cout : {action[1]} Bénéfice: {round(action[2], 2)}")
print(f"Profit total après 2 ans : {round(profit, 2)}")