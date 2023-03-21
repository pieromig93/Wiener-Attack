# Wiener Attack per l'esame di PSSR - Piero Migliorato

# Per prima cosa bisogna valutare se è possibile applicare il teorema di Wiener sulla coppia {e, N} - chiave pubblica e N=p*q oppure vado a generare
# delle crendenziali che rispettano tali vincoli.

# I vincoli imposti dal teorema di Wiener sono:
#   - q < p < 2q 
#   - d < (N^1/4)/3

from sympy import symbols, solve
import matplotlib.pyplot as plt
import gen_key as gk
import math

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

# partendo dai valori dei quozienti andiamo a calcolare i convergenti
def convergents(a):
    num = []
    den = []
    c = []

    for i in range(len(a)):
        if i == 0:
            num.append(int(a[i]))
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
            print(f"Possible value -> |k: {p_k}|d: {p_d}| possible_phi:{p_phi}|")
            # se le radici sono due 
            if len(roots)==2:
                p1,p2 = roots
                p_N = p1*p2
                print(f"Possible value -> |k: {p_k}|d: {p_d}| possible_phi:{p_phi}| possibile_N: {p_N}|roots: {p1}, {p2}")
                if p_N==N:
                    print(f"Founded d-value: {p_d}")
                    break

    return p_d


# Generazione delle chiavi con weakness
print("++++++GENERATING KEY...++++++")
N, e, d, p, q = gk.create_keypair(2048)
print(f"N: {N}, e:{e}, d:{d}, p:{p}, q:{q}")
tot_N = (p-1)*(q-1)
# Calcolo i coefficienti per le frazioni continue
print("++++++COMPUTING THE A-COEFFICIENTS...++++++")
a = cf_exp(e, N)
print(f"A coefficients: {a}")

# Calcolo i convergenti
c, num, den = convergents(a)

# plt.hlines(e/N, 0, 100, linestyles='dashdot', label='e/N')
# plt.plot(c, 'r-.', label='convergents')
# plt.scatter(x=[range(0, len(c))], y=c, label='convergent points')
# plt.legend()
# plt.axis([0, len(a), 0.1, 1.1])
# plt.show()

# pi_exp = [3,7,15,1,292,1,1,1,2]
# c_pi, num_pi, den_pi = convergents(pi_exp)

# plt.hlines(math.pi, 0, 100, linestyles='dashdot', label='pi')
# plt.plot(c_pi, 'r-.', label='convergents of pi')
# plt.scatter(x=[range(0, len(c_pi))], y=c_pi )
# plt.legend()
# plt.axis([0, len(pi_exp), 2.9, 3.2])
# print(c_pi)
# plt.show()

# lancio la suite d'attacco
founded_d = hack_RSA(e, N, num, den)

# Aggiungere sotto suggerimento dell'Ing. Fioretti il tempo impiegato dalle varie esecuzioni su chiavi di lunghezza comune