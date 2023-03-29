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

import matplotlib.pyplot as plt

list_bit = [32, 64, 128, 256, 512, 1024]
n_logn = []
n_2 = []

bit_used_dim = range(len(list_bit))
plt.plot(bit_used_dim, list_bit, 'b-', label='O(n)', linewidth = 3)
plt.xticks(bit_used_dim, list_bit)
plt.legend()
plt.xlabel(xlabel='p and q Bit-size[bit]')
plt.ylabel(ylabel='')
plt.show()