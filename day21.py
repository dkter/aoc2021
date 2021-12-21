from collections import deque, Counter
from itertools import product
from functools import lru_cache


with open("day21.in") as f:
    p1sp = int(f.readline().strip().split(":")[1])
    p2sp = int(f.readline().strip().split(":")[1])


p1 = 0
p2 = 0
p1p = p1sp
p2p = p2sp
die = 1
while p1 < 1000 and p2 < 1000:
    p1p += die * 3 + 3
    die += 3
    while p1p > 10:
        p1p -= 10
    p1 += p1p
    if p1 >= 1000:
        break

    p2p += die * 3 + 3
    die += 3
    while p2p > 10:
        p2p -= 10
    p2 += p2p


losing = min(p1, p2)
print(losing * (die - 1))


# pt2


# queue = deque([(0, 0, p1sp, p2sp)])
# p1_count = 0
# p2_count = 0
# while queue:
#     #print(queue)
#     p1, p2, p1p, p2p = queue.pop()
#     if p2_count >= 108: break
#     for roll in product((1, 2, 3), repeat=3):
#         for roll2 in product((1, 2, 3), repeat=3):
#             p1p_new = p1p + sum(roll)
#             while p1p_new > 10:
#                 p1p_new -= 10
#             p2p_new = p2p + sum(roll2)
#             while p2p_new > 10:
#                 p2p_new -= 10
#             p1_new = p1 + p1p_new
#             p2_new = p2 + p2p_new
#             if p1_new >= 21:
#                 p1_count += 1
#             elif p2_new >= 21:
#                 p2_count += 1
#             else:
#                 queue.append((p1_new, p2_new, p1p_new, p2p_new))


# print(p1_count)
# print(p2_count)


# binomial distribution
distr = Counter([
    (sum(i), sum(j))
    for i in product((1, 2, 3), repeat=3)
    for j in product((1, 2, 3), repeat=3)
])
print(distr)

# queue = deque([(0, 0, p1sp, p2sp, 1, [])])
# p1_count = 0
# p2_count = 0
# while queue:
#     if p1_count % 1000 == 0: print(p1_count, p2_count, len(queue))
#     if p1_count >= 444356092776315:
#         print("bad")
#         break
#     #if p2_count == 108: break
#     #print(queue)
#     p1, p2, p1p, p2p, ntimes, things = queue.pop()
#     for (roll1, roll2), roll_ntimes in distr.items():
#         p1p_new = p1p + roll1
#         if p1p_new > 10:
#             p1p_new -= 10
#         p2p_new = p2p + roll2
#         if p2p_new > 10:
#             p2p_new -= 10
#         p1_new = p1 + p1p_new
#         p2_new = p2 + p2p_new
#         ntimes_new = roll_ntimes * ntimes
#         if p1_new >= 21:
#             p1_count += ntimes_new
#         elif p2_new >= 21:
#             #print(p1, p2, roll1, roll2, p2p + roll2, "    ", ntimes ,ntimes_new)
#             p2_count += ntimes_new
#         else:
#             queue.append((p1_new, p2_new, p1p_new, p2p_new, ntimes_new))


# print(p1_count)
# print(p2_count)


@lru_cache
def get_num_wins(p1, p2, p1p, p2p):
    p1_count = 0
    p2_count = 0
    for (roll1, roll2), roll_ntimes in distr.items():
        p1p_new = p1p + roll1
        if p1p_new > 10:
            p1p_new -= 10
        p2p_new = p2p + roll2
        if p2p_new > 10:
            p2p_new -= 10
        p1_new = p1 + p1p_new
        p2_new = p2 + p2p_new
        if p1_new >= 21:
            # p1 won
            p1_count += roll_ntimes
        elif p2_new >= 21:
            # p2 won
            p2_count += roll_ntimes
        else:
            # continue
            p1ct_new, p2ct_new = get_num_wins(p1_new, p2_new, p1p_new, p2p_new)
            p1_count += p1ct_new * roll_ntimes
            p2_count += p2ct_new * roll_ntimes
    return (p1_count, p2_count)

p1_score, p2_score = get_num_wins(0, 0, p1sp, p2sp)

# (11997614504960505, 341960390180808)
#  444356092776315    341960390180808

p1_score //= 27  # idk why i have to do this but it works
print(max(p1_score, p2_score))
