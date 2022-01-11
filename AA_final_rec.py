# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np

v0 = 70
n1 = 5
n2 = 5

data = pd.read_csv("RPD2.csv", encoding = 'utf-8', index_col='job')
data['delta'] = data['beta'] - data['alpha']
data = np.array(data)
m1 = np.array([x for k, x in enumerate(data) if k % 2 == 0])
m2 = np.array([x for k, x in enumerate(data) if k % 2 == 1])


# %%
m1 = m1[:n1]
m1


# %%
m2 = m2[:n2]
m2


# %%
# def A(i, j):
#     return v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m1[i, 0] - m2[j, 0] >= 0
A = lambda i, j: v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m1[i, 0] - m2[j, 0] >= 0


# %%
def construct_H(i, j):
    H = set()
    if not (i < n1 and j < n2):
        return H

    i_prime, j_prime = i, j
    s1 = m1[i_prime, 2]
    s2 = m2[j_prime, 2]

    while i_prime < n1 and j_prime < n2 and s1 != s2 and A(i_prime, j_prime):
        H.add((i, j, i_prime, j_prime))

        if s1 < s2:
            i_prime += 1
            if i_prime < n1:
                s1 += m1[i_prime, 2]
        else:
            j_prime += 1
            if j_prime < n2:
                s2 += m2[j_prime, 2]
    return H

# construct_H(2,2)


# %%
T = lambda t, k, h: max(0, t - k[h, 3])

def g(i, j, l):
    H = construct_H(i, j)
    # if H: print(f'{i}, {j}, H: {H}')
    
    def L(i, j, i_prime, j_prime):
        s1 = sum(T(l + sum(m1[i:h+1, 2]), m1, h) for h in range(i, i_prime+1))
        s2 = sum(T(l + sum(m2[j:h+1, 2]), m2, h) for h in range(j, j_prime+1))

        sum_m1 = sum(m1[i:i_prime+1, 2])
        sum_m2 = sum(m2[j:j_prime+1, 2])

        rec = g(i_prime + 1, j_prime + 1, l + max(sum_m1, sum_m2))
        return rec + s1 + s2

    # def z1():
    #     if v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m1[i, 0] >= 0:
    #         td = T(l + m1[i, 2], m1, i)
    #         # print(f'{i}, {j}, do m1 {i}, td = {td}')
    #         return g(i + 1, j, l + m1[i, 2]) + td
    #     # print(f'{i}, {j}, cannot do m1 {i}')
    #     return float('inf')

    # def z2():
    #     if v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m2[j, 0] >= 0:
    #         td = T(l + m2[j, 2], m2, j)
    #         # print(f'{i}, {j}, do m2 {j}, td = {td}')
    #         return g(i, j + 1, l + m2[j, 2]) + td
    #     # print(f'{i}, {j}, cannot do m2 {j}')
    #     return float('inf')
        
    # def z3():
    #     if len(H) != 0:
    #         # print(f'{i}, {j}, do block start')
    #         mi = float('inf')
    #         arg_mi = ()
    #         for x,y,i_prime,j_prime in H:
    #             td = L(x,y,i_prime,j_prime)
    #             if td < mi:
    #                 mi = td
    #                 arg_mi = (x,y,i_prime,j_prime)
    #         # print(f'{i}, {j}, do block {arg_mi}, td = {mi}')
    #         return mi
    #     # print(f'{i}, {j}, cannot do block')
    #     return float('inf')

    z1 = lambda: g(i + 1, j, l + m1[i, 2]) + T(l + m1[i, 2], m1, i) \
        if v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m1[i, 0] >= 0 else float('inf')
    z2 = lambda: g(i, j + 1, l + m2[j, 2]) + T(l + m2[j, 2], m2, j) \
        if v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m2[j, 0] >= 0 else float('inf')
    z3 = lambda: min(L(i,j,i_prime,j_prime) for i,j,i_prime,j_prime in H) \
        if H else float('inf')

    if i == n1 and j == n2:
        # print(f'{i}, {j}, done')
        return 0
    if i < n1 and j == n2:
        return z1()
    if i == n1 and j < n2:
        return z2()

    x1 = z1()
    x2 = z2()
    x3 = z3()
    
    # print(f'{i}, {j}, {x1}, {x2}, {x3}')

    return min(x1, x2, x3)


# %%
print(g(0,0,0))


# %%



