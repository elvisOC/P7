import csv
import pathlib
import os
import pandas as pd

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

def knapsack(actions, budget_max):
    nombre_actions = len(actions)
    tableau = [[0] * (budget_max + 1) for _ in range(nombre_actions + 1)]
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
            best_combinaison.append(actions[i - 1])
            w -= cout
            
    cout_total = sum(action[1] for action in best_combinaison)
    profit_total = sum(action[2] for action in best_combinaison)
    
    
    return best_combinaison, cout_total, profit_total, tableau

def afficher_tableau(tableau):
    df = pd.DataFrame(tableau)
    df.columns = [f"€{i}" for i in range(len(df.columns))]
    df.index = [f"A{i}" for i in range(len(df))]
    return df


actions = open_csv('actions_P1.csv')
best_combinaison, cout_total, profit, tableau = knapsack(actions, 500)
for action in best_combinaison:
    print(f"{action[0]} Cout : {action[1]} Bénéfice: {round(action[2], 2)}")
print(f"Profit total après 2 ans : {round(profit, 2)}")


print(afficher_tableau(tableau))