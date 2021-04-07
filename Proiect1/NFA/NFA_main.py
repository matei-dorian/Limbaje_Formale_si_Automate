# n -> numarul de stari
# a -> graful
# m -> numarul de muchii
# start -> starea initiala
# nrF -> numar de stari finale
# finish -> starile finale
# nrCuv -> numarul de cuvinte ce trebuie sa fie verificate
# lista_cuvinte -> cuvintele

#   Cum memmoram NFA-ul?
#   Pentru reprezentarea cat mai usoara si rapida a NFA-ului in memorie vom asocia NFA-ului un graf pe care o sa-l memoram
# prin lista de adiacenta. Pentru a crea lista de adiacenta vom folosi un dictionar unde cheia reprezinta nodul din care incepe
# tranzitia iar valoarea va fi o lista de tupluri de forma (nod, valoare), unde nod reprezinta starea in care ajungem prin tranzitie,
# iar valoare reprezinta litera de care avem nevoie pentru a face tranzitia.
#   Pentru verificarea acceptarii unui cuvant vom avea nevoie sa facem un BFS pe graf. Functia de BFS va returna 1 daca
# cuvantul este acceptat sau 0 daca nu este acceptat si un vector de tupluri de forma (nod, pas) pe care l vom folosi pentru
# reconstituirea drumului.
#   Reconstituirea drumului se face plecand de la starea finala spre cea initiala folosind vectorul returnat de functia BFS
# care cuprinde toate starile vizitate
#   Vom memora starile finale intr un set pentru a raspunde in O(1) la intrebarea "Este nodul x stare finala?"

def BFS(cuv):
    poz = 0
    q = []
    q.append((start, poz))
    drum = []   # parte de initializare -> in coada avem nodul de start

    while len(q) > 0:
        nod, lg = q.pop(0)

        drum.append((nod, lg))
        if lg == len(cuv):  # daca am ajuns la finalul cuvantului verificam daca am ajuns intr-o stare finala
            if nod in finish:
                return (1, drum)
        else:   # daca mai sunt litere de parcurs -> vizitam vecinii
            for tranzitie in a[nod]:
                if cuv[lg] == tranzitie[1]:
                    q.append((tranzitie[0], lg + 1))

    return (0, [])


def Reconstituire_drum(cuv, drum):
    nod, poz = drum[len(drum) - 1]  # pornim de la starea finala
    sol = [nod]
    for pas in drum[len(drum) - 2::-1]:  # parcurgem rumul in sens invers
        if pas[1] == poz - 1:
            for tranzitie in a[pas[0]]:
                if tranzitie[0] == nod and tranzitie[1] == cuv[poz - 1]:  # verificam sa existe tranzitia
                    nod = pas[0]
                    poz -= 1
                    sol.append(nod)
                    break
    print(sol[::-1])
    return sol[::-1]


f = open("Input_NFA")

n = int(f.readline())

a = {int(stare): [] for stare in f.readline().split()}

m = int(f.readline())

for i in range(m):
    x, y, z = f.readline().split()
    a[int(x)].append((int(y), z))

start = int(f.readline())
nrF = int(f.readline())
finish = set(int(stare_f) for stare_f in f.readline().split())
nrCuv = int(f.readline())
lista_cuvinte = [f.readline().strip() for i in range(nrCuv)]

f.close()

f = open("Output_NFA", "w")

for cuv in lista_cuvinte:
    raspuns, drum = BFS(cuv)
    print(f"Cuvantul {cuv}", end=" ")
    print("este acceptat! " if raspuns else "nu este acceptat!")
    if raspuns:
        print("Starile parcurse sunt: ", end="")
        sol = Reconstituire_drum(cuv, drum)
        sol = ", ".join([str(nod) for nod in sol])
    f.write("DA: " + sol + "\n" if raspuns else "NU\n")

f.close()
