def closure(states):
    # variabila states este un set de stari
    # functia returneaza toate starile accesibile dintr-un nod cu lambda tranzitii
    # vom face acest lucru tot cu un BFS
    viz = {s: False for s in nfa.keys()} # un vector de frecventa sub forma unui dictionar
    q = [*states]
    closure = set()

    while q:
        nod = q.pop(0)
        closure.add(nod)
        viz[nod] = True

        for tranzition in nfa[nod]:
            if tranzition[1] is None:
                if viz[tranzition[0]] == False:
                    q.append(tranzition[0])

    return closure

def goto(states, symbol = None):
    # funtia returneaza toate starile care sunt accesibile din setul de stari initiale prin symbol
    reachable = set()
    for node in states:
        for tranzition in nfa[node]:
            if tranzition[1] == symbol:
                reachable.add(tranzition[0])
    return closure(reachable)

def add_transition(dfa, begin, end, symbol):
    begin = frozenset(begin)
    end = frozenset(end)
    if begin in dfa.keys():
        dfa[begin].add((end, symbol))
    else:
        dfa[begin] = set()
        dfa[begin].add((end, symbol))

def convert(dfa, start, finish):
    start = closure(start)
    for symbol in alphabet:
        new_state = goto(start, symbol)
        if len(new_state) > 0:
            if frozenset(new_state) not in dfa.keys():
                add_transition(dfa, start, new_state, symbol)
                convert(dfa, new_state, finish)
            else:
                add_transition(dfa, start, new_state, symbol)

def find_finish(finish, dfa):
    # functie ce afla starile finale din dfa ul obtinut
    temp = set()
    for state in dfa.keys():
        if state & finish:
            temp.add(state)

    for value in dfa.values():
        for transition in value:
            if transition[0] & finish:
                temp.add(transition[0])

    return temp

def encode(dfa, finish, start):
    d = {}
    M = set()
    k = 0
    for state in dfa.keys():
        if state not in M:
            M.add(state)
            k += 1
            d[state] = k

    for value in dfa.values():
        for transition in value:
            if transition[0] not in M:
                M.add(transition[0])
                k += 1
                d[transition[0]] = k


    temp = {d[state] : set() for state in dfa.keys()}

    for state in dfa.keys():
        for transition in dfa[state]:
            temp[d[state]].add((d[transition[0]], transition[1]))

    temp_start = d[frozenset(start)]
    temp_finish = {d[frozenset(i)] for i in finish}
    return temp, temp_finish, temp_start

def complete(dfa, finish):
    for node in finish:
        if node not in dfa.keys():
            dfa[node] = set()
    return dfa

def remove_unreachable_states(dfa):
    nod = start
    reachable = {nod}
    viz = {key:0 for key in dfa.keys()}

    q = [nod]
    while len(q) != 0:
        nod = q.pop(0)
        for tranzitie in dfa[nod]:
            if viz[tranzitie[0]] == 0:
                q.append(tranzitie[0])
                viz[tranzitie[0]] = 1
                reachable.add(tranzitie[0])

    temp = {}
    for state in dfa.keys():
        if state in reachable:
            temp[state] = dfa[state]
    dfa = temp

    return reachable, dfa

def minimize(dfa, states):
    P = [set(finish), states - set(finish)]
    W = [set(finish), states - set(finish)]

    while len(W) != 0:
        A = W.pop()
        #print(A, "stare")
        for symbol in alphabet:
            X = set()
            for item in dfa.items():
                for transition in item[1]:
                    if transition[1] == symbol and transition[0] in A:
                        X.add(item[0])
            #print(X, symbol)
            for Y in P:
                temp1 = X & Y
                temp2 = Y - X
                if temp1 != set() and temp2 != set():
                    P.remove(Y)
                    P.append(temp1)
                    P.append(temp2)
                    if Y in W:
                        W.remove(Y)
                        W.append(temp1)
                        W.append(temp2)
                    else:
                        if len(temp1) <= len(temp2):
                            W.append(temp1)
                        else:
                            W.append(temp2)
    return(P)

def build_dfa(dfa, states):
    m_dfa = {frozenset(element): set() for element in states}

    for key in m_dfa:
        for node in key:
            if node in dfa.keys():
                m_dfa[key] |= dfa[node]

    m_dfa = {k: v for k, v in m_dfa.items()}

    temp = {}
    for key in m_dfa.keys():
        ok = 0
        if m_dfa[key] != set():
            ok = 1
        else:
            for node in key:
                if node in finish:
                    ok = 1
                    break
        if ok == 1:
            temp[key] = m_dfa[key]

    m_dfa = temp

    for node in m_dfa.keys():
        temp = set()
        for transition in m_dfa[node]:
            for key in m_dfa.keys():
                if transition[0] in key:
                    temp.add((key, transition[1]))
        m_dfa[node] = temp

    return m_dfa

def find_start(m_dfa, start):
    for key in m_dfa.keys():
        if start in key:
            return key

def BFS(start):
    nod = start
    reachable = {nod}
    viz = {key: 0 for key in dfa.keys()}
    q = [nod]
    while len(q) != 0:
        nod = q.pop(0)
        for tranzitie in dfa[nod]:
            if viz[tranzitie[0]] == 0:
                q.append(tranzitie[0])
                viz[tranzitie[0]] = 1
                reachable.add(tranzitie[0])
    return reachable & finish

def remove_traps(dfa):
    temp = {}
    for key in dfa.keys():
        ok = BFS(key)
        if ok != set() or key in finish:
            temp[key] = dfa[key]

    for item in temp.items():
        X = set()
        for transition in item[1]:
            if transition[0] in temp.keys():
                X.add(transition)
        temp[item[0]] = X

    return temp

f = open("Input")

n = int(f.readline())

nfa = {i: set() for i in range(1, n + 1)}

m = int(f.readline())

alphabet = set()

for i in range(m):
    line = f.readline().split()
    if len(line) == 3:
        x, y, z = line
        nfa[int(x)].add((int(y), z))
        alphabet.add(z)
    else:
        x, y = line
        nfa[int(x)].add((int(y), None))

start = set([int(f.readline())])
finish = set(int(state) for state in f.readline().split())
dfa = {}

convert(dfa, start, finish)
finish = find_finish(finish, dfa)
dfa, finish, start = encode(dfa, finish, start)
dfa = complete(dfa, finish)

f = open("Output", "w")
f.write("NFA to DFA:\n")
f.write("Initial state: " + str(start) + "\n")
f.write("Final states: " + str(finish) + "\n")
f.write("Transitions:\n")
for key in dfa.keys():
    f.write(str(key) + ' : ' + str(dfa[key]) + '\n')


states, dfa = remove_unreachable_states(dfa)
dfa = remove_traps(dfa)
minimum_states = minimize(dfa, states)
#print(minimum_states)
m_dfa = build_dfa(dfa, minimum_states)
start = find_start(m_dfa, start)
finish = find_finish(frozenset(finish), m_dfa)

f.write("\nMIN DFA:\n")
f.write("Initial state: " + str(start) + "\n")
f.write("Final states: " + str(finish) + "\n")
for key in m_dfa.keys():
    f.write((str({int(element) for element in key}) + ' : ' + str(m_dfa[key]) + '\n'))


