# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np

# 2 2 37
# 3 3 inf
# 4 4 148
# 5 5 254
# 6 6 397
# 50 50 11734

v0 = 70
n1 = 50
n2 = 50

data = pd.read_csv("RPD2.csv", encoding = 'utf-8', index_col='job')
data['delta'] = data['beta'] - data['alpha']
data = np.array(data)

m1 = np.array([x for k, x in enumerate(data) if k%2 == 0])
m2 = np.array([x for k, x in enumerate(data) if k%2 == 1])
m1 = m1[:n1]
m2 = m2[:n2]

max_l = sum(m1[:, 2]) + sum(m2[:, 2])

dp = np.zeros((max_l+1, n1+1, n2+1)) + float('inf')
dp[:, 0, 0] = 0


# %%
path = np.empty((max_l+1, n1+1, n2+1), dtype=tuple)
path[0,0,0] = ()


# %%
A = lambda i, j: v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m1[i, 0] - m2[j, 0] >= 0

T = lambda t, k, h: max(0, t - k[h, 3])

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


# %%
H = np.zeros((n1, n2), dtype=object)
for i in range(n1):
    for j in range(n2):
        H[i, j] = construct_H(i, j)

for i in range(n1+1):
    for j in range(n2+1):

        p1 = sum(m1[:i, 2])
        p2 = sum(m2[:j, 2])

        l1 = max(p1, p2)
        l2 = p1 + p2

        for l in range(l1, l2+1):
            if i < n1 and v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m1[i, 0] >= 0:
                l_prime = l + m1[i, 2]
                tardiness = dp[l, i, j] + T(l_prime, m1, i)

                if tardiness < dp[l_prime, i+1, j]:
                    dp[l_prime, i+1, j] = tardiness
                    path[l_prime, i+1, j] = (l, i, j, f'do m1 job {i}')

            if j < n2 and v0 + sum(m1[:i, 4]) + sum(m2[:j, 4]) - m2[j, 0] >= 0:
                l_prime = l + m2[j, 2]
                tardiness = dp[l, i, j] + T(l_prime, m2, j)

                if tardiness < dp[l_prime, i, j+1]:
                    dp[l_prime, i, j+1] = tardiness
                    path[l_prime, i, j+1] = (l, i, j, f'do m2 job {j}')

            if i < n1 and j < n2 and H[i, j]:
                for (x, y, x_prime, y_prime) in H[i, j]:
                    sum_m1 = sum(m1[x:x_prime+1, 2])
                    sum_m2 = sum(m2[y:y_prime+1, 2])

                    l_prime = l + max(sum_m1, sum_m2)

                    s1 = sum(T(l + sum(m1[x:h+1, 2]), m1, h) for h in range(x, x_prime+1))
                    s2 = sum(T(l + sum(m2[y:h+1, 2]), m2, h) for h in range(y, y_prime+1))
                    
                    tardiness = dp[l, x, y] + s1 + s2

                    if tardiness < dp[l_prime, x_prime+1, y_prime+1]:
                        dp[l_prime, x_prime+1, y_prime+1] = tardiness
                        path[l_prime, x_prime+1, y_prime+1] = (l, x, y, f'do m1 jobs {x} to {x_prime}, m2 jobs {y} to {y_prime}')

min_tardy = min(dp[:, -1, -1])
min_tardy_l = np.where(dp[:, -1, -1] == min_tardy)[0][0]

print(f'Total weighted tardiness: {min_tardy}')
print(f'完成所有Job且有最少tardiness的完成時間: {min_tardy_l}')
print(f'完成所有Job的最短時間: {np.where(dp[:, -1, -1] != float("inf"))[0][0]}')


# %%
previous = (min_tardy_l, n1, n2, 'done')
job_seq = []
while previous:
    job_seq.append(previous)
    l, i, j, _ = previous
    previous = path[l, i, j]

(list(reversed(job_seq)))


# %%



