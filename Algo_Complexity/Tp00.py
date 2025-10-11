import random
import time
import pandas as pd

sizes = [10**4, 10**5, 10**6]
tests = 30
tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

result = []

def recherche_sequntielle(tab, x):
    comp = 0
    for i in range(len(tab)):
        comp += 1
        if tab[i] == x:
            return i, comp
    return -1, comp

def recherche_sequntielle_optimise(tab, x):
    comp = 0
    for i in range(len(tab)):
        comp += 1
        if tab[i] == x:
            return i, comp
        elif tab[i] > x:
            return -1, comp
    return -1, comp

def recherche_binaire_iterative(tab, x):
    g, d = 0, len(tab) - 1
    comp = 0
    while g <= d:
        m = (g + d) // 2
        comp += 1
        if tab[m] == x:
            return m, comp
        elif tab[m] < x:
            g = m + 1
        else:
            d = m - 1
    return -1, comp

def recherche_binaire_recursive(tab, x, g, d, comp=0):
    if g > d:
        return -1, comp
    m = (g + d) // 2
    comp += 1
    if tab[m] == x:
        return m, comp
    elif tab[m] < x:
        return recherche_binaire_recursive(tab, x, m + 1, d, comp)
    else:
        return recherche_binaire_recursive(tab, x, g, m - 1, comp)

# run tests
for n in sizes:
    tab = sorted(random.sample(range(10**7), n))
    print(f"Rechercher et Test de la table {n}...")

    for algo_name, algo_func in [
        ("SeqSimple", recherche_sequntielle),
        ("SeqOpt", recherche_sequntielle_optimise),
        ("BinIter", recherche_binaire_iterative),
        ("BinReq", lambda t, x: recherche_binaire_recursive(t, x, 0, len(t) - 1)),
    ]:
        total_time = 0
        total_comp = 0

        for _ in range(tests):
            x = random.choice(tab + [10**8])

            start = time.time()
            _, comp = algo_func(tab, x)
            end = time.time()

            total_time += (end - start)
            total_comp += comp

        avg_time = total_time / tests
        avg_comp = total_comp / tests

        result.append((algo_name, n, avg_comp, avg_time))

# build DataFrame
df = pd.DataFrame(result, columns=["Algorithms", "Size", "Avg Comp", "Avg Time(s)"])
print("\n=== Result Summary ===\n")
print(df.pivot(index="Size", columns=["Algorithms"], values=["Avg Comp", "Avg Time(s)"]))
