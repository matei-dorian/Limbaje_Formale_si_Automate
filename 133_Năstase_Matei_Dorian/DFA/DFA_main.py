# n -> numarul de stari
# a -> graful
# m -> numarul de muchii
# start -> starea initiala
# nrF -> numar de stari finale
# finish -> starile finale
# nrCuv -> numarul de cuvinte ce trebuie sa fie verificate
# lista_cuvinte -> cuvintele
# Cum memmoram DFA-ul?
#     Pentru reprezentarea cat mai usoara si rapida a DFA-ului in memorie vom asocia DFA-ului un graf pe care o sa-l memoram
# prin lista de adiacenta. Pentru a crea lista de adiacenta vom folosi un dictionar unde cheia reprezinta nodul din care incepe
# tranzitia iar valoarea va fi o lista de tupluri de forma (nod, valoare), unde nod reprezinta starea in care ajungem prin tranzitie,
# iar valoare reprezinta litera de care avem nevoie pentru a face tranzitia.
#     Pentru verificarea acceptarii unui cuvant vom avea nevoie sa verificam daca nodul in care ajungem este stare finala
#     Vom memora starile finale intr un set pentru a raspunde in O(1) la intrebarea este nodul x stare finala?

def is_Accepted(cuv):
    nod = start  # mereu pornim din starea initiala
    drum = [nod]
    pas = 0
    for l in cuv:  # parcurgem litera cu litera cuvantul dat
        for tranzitie in a[nod]:  # vedem daca exista o tranzitie cu litera curenta
            if tranzitie[1] == l:
                nod = tranzitie[0]  # am trecut la o stare noua
                drum.append(nod)
                pas += 1
                break
    if pas < len(cuv):  # verificam daca am folosit toate literele
        return (drum, 0)
    return (drum, nod in finish)



f = open("Input_DFA")

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

f = open("Output_DFA", "w")

for cuv in lista_cuvinte:
    drum, raspuns = is_Accepted(cuv)
    print(f"Cuvantul {cuv}", end=" ")
    print("este acceptat! " if raspuns else "nu este acceptat!\n", end = "")
    if raspuns:
        print("Stările parcurse sunt:", *drum)
    f.write("DA\n" if raspuns else "NU\n")

f.close()
