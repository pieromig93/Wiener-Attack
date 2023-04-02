# Wiener Attack per l'esame di PSSR - Piero Migliorato

# Per prima cosa bisogna valutare se è possibile applicare il teorema di Wiener sulla coppia {e, N} - chiave pubblica e N=p*q oppure vado a generare
# delle crendenziali che rispettano tali vincoli.

# I vincoli imposti dal teorema di Wiener sono:
#   - q < p < 2q 
#   - d < (N^1/4)/3

from sympy import symbols, solve
import matplotlib.pyplot as plt
import gen_key as gk
import time

# ! Il programma si basa sul concetto che una frazione tra 2 numeri è possibile esprimerla come una serie di frazioni, chiamate continous fractions vediamo come calcolarle

def cf_exp(num, den):
    # definisco la lista dove mettere tutti i coefficienti a_i, cioè i quozienti
    a = []

    # la floor division(a//b) mi restituisce il quoziente della divisione
    q = num//den
    # prendo il resto con l'operazione di modulo 
    r = num % den
    a.append(q)

    # computo la prima operazione, se ottengo resto diverso da zero vado avanti nel trovare i valori di q che mi interessano finché non trovo che il resto è zero.
    while(r!=0):
        # quindi il nuovo numeratore diventa il quoziente dell'operazione precendente, mentre il nuovo denominatore diventa è il resto 
        num, den = den, r
        q = num//den
        r = num % den
        a.append(q)

    return a

# partendo dai valori dei quozienti posizionati in una lista andiamo a calcolare i convergenti
def convergents(a):
    num = []
    den = []
    c = []

    for i in range(len(a)):
        if i == 0:
            num.append(a[i])
            den.append(1)

        elif i == 1:
            num.append((a[i]*a[i-1])+1)
            den.append(a[i])
            
        else:
            num.append(num[i-1]*a[i]+num[i-2])
            den.append(den[i-1]*a[i]+den[i-2])            
        c.append(num[i]/den[i])
    
    return c, num, den

def hack_RSA(e, N, num, den):
    for i in range(len(num)):
        p_k = num[i]
        p_d = den[i]

        if p_k != 0:
            # calcolo il totiente possibile
            p_phi = (e*p_d-1)//p_k
            
            # costruisco l'equazione di secondo grado che poi risolvo cercando i valori di fattorizzazione di N
            p = symbols('p', integer=True)
            roots = solve(p**2 +(p_phi-N-1)*p + N, p)
            # print(f"Possible value -> |k: {p_k}|d: {p_d}| possible_phi:{p_phi}|")
            # se le radici sono due 
            if len(roots)==2:
                p1,p2 = roots
                p_N = p1*p2
                print(f"POSSIBLE VALUE:\n-k: {p_k}\n-d: {p_d}\n-possible_phi:{p_phi}\n-possibile_N: {p_N}\n-roots: {p1}, {p2}\n")
                if p_N==N:
                    print(f"%%%%% Founded d-value: {p_d} %%%%%")
                    break

    return p_d

# dimensione in bit iniziale di p e q
starting_bit = 32

# lista che mi serve per stampare il grafico ed ottenere una lista di valori ce contiene il numero di bit utilizzati
bit_used = []

# Lista dei tempi medi
mean_exec_time = []

i = 1
while i<64:
    k = 0
    while k<3:
        # Lista che contiene i tempi di esecuzione
        execution_time = []

        '''
        Generazione delle chiavi con vulnerabilità partendo da valori randomici di bit che viene incrementata all'aumentare del
        di iterazioni
        (è possibile scegliere un valore più grande aumentando la dimensione del parametro passato)
        '''
        print("\n-----------------------------")
        print("++++++GENERATING KEY...++++++")
        bit=starting_bit*i
        N, e, d, p, q = gk.create_keypair(bit)
        print(f"Bit used: {bit}\n- N: {N}\n- e:{e}\n- d:{d}\n- p:{p}\n- q:{q}\n")

        # prendo il tempo dopo la generazione delle chiavi per non invalidare la misura
        starting_time = time.time()

        # Calcolo i coefficienti per le frazioni continue
        print("++++++COMPUTING THE A-COEFFICIENTS...++++++")
        a = cf_exp(e, N)
        print(f"A coefficients: {a}")

        # Calcolo i convergenti
        c, num, den = convergents(a)

        # lancio la suite d'attacco
        founded_d = hack_RSA(e, N, num, den)
        
        # gestione dei tempi
        end_time = time.time()
        execution_time.append(end_time-starting_time)
        
        k=k+1
    
    # Salvo il valore dei bit utilizzati
    bit_used.append(bit)

    # Calcolo il tempo medio su 3 esecuzioni a bit fissati
    mean_exec_time.append(sum(execution_time)/len(execution_time))
    i=i*2
    time.sleep(2)

print(mean_exec_time)
print(bit_used)

bit_used_dim = range(len(bit_used))
plt.plot(bit_used_dim, mean_exec_time, 'r-', label='Mean Exec Time', linewidth = 4)
plt.scatter(x=bit_used_dim, y=mean_exec_time)
plt.xticks(bit_used_dim, bit_used)
plt.legend()
plt.xlabel(xlabel='p and q Bit-size[bit]')
plt.ylabel(ylabel='Time[s]')
plt.show()