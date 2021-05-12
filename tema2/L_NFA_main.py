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

def expand(poz):
    # functia returneaza toate starile accesibile dintr-un nod cu lambda tranzitii
    # vom face acest lucru tot cu un BFS
    viz = {s: False for s in a.keys()} # un vector de frecventa sub forma unui dictionar
    q = [poz]
    expanded = set()

    while q:
        nod = q.pop(0)
        expanded.add(nod)
        viz[nod] = True

        for tranzitie in a[nod]:
            if tranzitie[1] is None:
                if viz[tranzitie[0]] == False:
                    q.append(tranzitie[0])

    return expanded

def is_accepted(cuvant):
    stari_curente = accesibile[start] # ca sa nu fac bfs-uri de foarte multe ori pentru acelasi nod

    for litera in cuvant:
        stari_noi = set()
        for nod in stari_curente:
            for tranzitie in a[nod]:
                if litera == tranzitie[1]:
                    stari_noi |= accesibile[tranzitie[0]]

        if not stari_noi:
            return 0
        stari_curente = stari_noi

    return bool(stari_curente & finish)

f = open("Input")

n = int(f.readline())

a = {int(stare): [] for stare in f.readline().split()}

m = int(f.readline())

for i in range(m):
    lin = f.readline().split()
    if len(lin) == 3:
        x, y, z = lin
        a[int(x)].append((int(y), z))
    else:
        x, y = lin
        a[int(x)].append((int(y), None))

start = int(f.readline())
nrF = int(f.readline())
finish = set(int(stare_f) for stare_f in f.readline().split())
nrCuv = int(f.readline())
lista_cuvinte = [f.readline().strip() for i in range(nrCuv)]

f.close()
print(a)
print()
f = open("Output", "w")

accesibile = {}
for nod in a.keys():
    accesibile[nod] = expand(nod)
print(accesibile)

# for item in a.items():
#     for elem in item[1]:
#         if elem[1] == None:
#             for tranzitie in a[elem[0]]:
#                 item[1].append(tranzitie)
#             a[elem[0]] = []
# print(a) - alta modalitate de rezolvare

for cuv in lista_cuvinte:
    raspuns = is_accepted(cuv)
    print(f"Cuvantul {cuv}", end=" ")
    print("este acceptat! " if raspuns else "nu este acceptat!")
#     f.write("DA\n" if raspuns else "NU\n")
#     print(drum)

f.close()