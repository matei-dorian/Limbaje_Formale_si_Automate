# am codificat lamba cu * si varful stivei cu $

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
            if tranzitie[1] == '*':
                if viz[tranzitie[0]] == False:
                    q.append(tranzitie[0])

    return expanded

def is_accepted(cuvant):
    stari_curente = accesibile[start] # ca sa nu fac bfs-uri de foarte multe ori pentru acelasi nod

    for litera in cuvant:
        stari_noi = set()  # vedem daca putem ajunge in stari noi
        for nod in stari_curente:
            for tranzitie in a[nod]:
                if litera == tranzitie[1]:
                    if tranzitie[2] == '*' or s[len(s) - 1] == tranzitie[2]:
                        if(tranzitie[2] != '*'):  # daca putem citi de pe stiva
                            if len(s) == 0:  # daca stiva e goala iesim -> cuvantul nu e acceptat
                                return 0
                            else:
                                s.pop()  # scoatem din stiva
                        for l in tranzitie[3].split(): # adaugam elemente noi
                            if l != '*':
                                s.append(l)

                        stari_noi |= accesibile[tranzitie[0]]
                    else:  # daca nu putem citi de pe stiva iesim -> cuvantul nu este acceptat
                        return 0
        if not stari_noi:  # daca nu putem ajunge in nicio stare noua -> cuvantul nu este acceptat
            return 0

        stari_curente = stari_noi

    return bool(stari_curente & finish)



f = open("Input")

n = int(f.readline())

a = {int(stare): [] for stare in f.readline().split()}

m = int(f.readline())

for i in range(m):
    x, y, z, cuv1, cuv2 = f.readline().split()
    a[int(x)].append((int(y), z, cuv1, cuv2))

start = int(f.readline())
finish = set(int(stare_f) for stare_f in f.readline().split())
nrCuv = int(f.readline())
lista_cuvinte = [f.readline().strip() for i in range(nrCuv)]
s = ['$']  # initial avem stiva vida
f.close()


accesibile = {}  # un dictionar in care tinem pentru fiecare nod lambda closer-ul
for nod in a.keys():
    accesibile[nod] = expand(nod)


f = open("Output", "w")

for cuv in lista_cuvinte:
    raspuns = is_accepted(cuv)
    print(f"Cuvantul {cuv}", end=" ")
    print("este acceptat!" if raspuns else "nu este acceptat!", end = "\n")
    f.write("DA\n" if raspuns else "NU\n")

f.close()