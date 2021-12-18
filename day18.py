from functools import reduce
from math import ceil
from copy import deepcopy
from itertools import accumulate, permutations
from pprint import pprint


def split(num):
    #print(f"split {num}")
    return [num // 2, ceil(num / 2)]


def sn_reduce(sn):
    done = False
    while not done:
        #print(sn)
        should_continue = False
        # explode
        for i, a in enumerate(sn):
            if isinstance(a, list):
                for ai, b in enumerate(a):
                    if isinstance(b, list):
                        for bi, c in enumerate(b):
                            if isinstance(c, list):
                                for ci, d in enumerate(c):
                                    if isinstance(d, list):
                                        #print(f"explode {d}")
                                        should_continue = True
                                        # get left
                                        if i == ai == bi == ci == 0:
                                            pass
                                        elif ci == 1:
                                            assert isinstance(c[0], int)
                                            c[0] += d[0]
                                        elif bi == 1:
                                            if isinstance(b[0], int):
                                                b[0] += d[0]
                                            else:
                                                assert isinstance(b[0][1], int)
                                                b[0][1] += d[0]
                                        elif ai == 1:
                                            if isinstance(a[0], int):
                                                a[0] += d[0]
                                            elif isinstance(a[0][1], int):
                                                a[0][1] += d[0]
                                            else:
                                                assert isinstance(a[0][1][1], int)
                                                a[0][1][1] += d[0]
                                        elif i == 1:
                                            if isinstance(sn[0], int):
                                                sn[0] += d[0]
                                            elif isinstance(sn[0][1], int):
                                                sn[0][1] += d[0]
                                            elif isinstance(sn[0][1][1], int):
                                                sn[0][1][1] += d[0]
                                            else:
                                                assert isinstance(sn[0][1][1][1], int)
                                                sn[0][1][1][1] += d[0]
                                        else:
                                            assert False

                                        # right (a little trickier, max depth is 4)
                                        if i == ai == bi == ci == 1:
                                            pass
                                        elif ci == 0:
                                            if isinstance(c[1], int):
                                                c[1] += d[1]
                                            else:
                                                assert isinstance(c[1][0], int)
                                                c[1][0] += d[1]
                                        elif bi == 0:
                                            if isinstance(b[1], int):
                                                b[1] += d[1]
                                            elif isinstance(b[1][0], int):
                                                b[1][0] += d[1]
                                            else:
                                                assert isinstance(b[1][0][0], int)
                                                b[1][0][0] += d[1]
                                        elif ai == 0:
                                            if isinstance(a[1], int):
                                                a[1] += d[1]
                                            elif isinstance(a[1][0], int):
                                                a[1][0] += d[1]
                                            elif isinstance(a[1][0][0], int):
                                                a[1][0][0] += d[1]
                                            else:
                                                assert isinstance(a[1][0][0][0], int)
                                                a[1][0][0][0] += d[1]
                                        elif i == 0:
                                            if isinstance(sn[1], int):
                                                sn[1] += d[1]
                                            elif isinstance(sn[1][0], int):
                                                sn[1][0] += d[1]
                                            elif isinstance(sn[1][0][0], int):
                                                sn[1][0][0] += d[1]
                                            elif isinstance(sn[1][0][0][0], int):
                                                sn[1][0][0][0] += d[1]
                                            else:
                                                assert isinstance(sn[1][0][0][0][0], int)
                                                sn[1][0][0][0][0] += d[1]
                                        else:
                                            assert False

                                        c[ci] = 0
                                        break
                                else:
                                    continue
                                break
                        else:
                            continue
                        break
                else:
                    continue
                break
        if should_continue:
            continue


        # split
        done = True
        for i, a in enumerate(sn):
            if isinstance(a, int) and a >= 10:
                sn[i] = split(a)
                done = False
                break
            elif isinstance(a, list):
                for ai, b in enumerate(a):
                    if isinstance(b, int) and b >= 10:
                        a[ai] = split(b)
                        done = False
                        break
                    elif isinstance(b, list):
                        for bi, c in enumerate(b):
                            if isinstance(c, int) and c >= 10:
                                b[bi] = split(c)
                                done = False
                                break
                            elif isinstance(c, list):
                                for ci, d in enumerate(c):
                                    if isinstance(d, int) and d >= 10:
                                        c[ci] = split(d)
                                        done = False
                                        break
                                    elif isinstance(d, list):
                                        assert False
                                else:
                                    continue
                                break
                        else:
                            continue
                        break
                else:
                    continue
                break
    return sn


def add(a, b):
    return sn_reduce([deepcopy(a), deepcopy(b)])


def magnitude(sn):
    if isinstance(sn, int):
        return sn
    else:
        return 3*magnitude(sn[0]) + 2*magnitude(sn[1])


snailfish_numbers = []
with open("day18.in") as f:
    for line in f:
        snailfish_numbers.append(eval(line.strip()))

sn_sum = reduce(add, snailfish_numbers)
#print(sn_sum)
#print()
#pprint(list(accumulate(snailfish_numbers, func=add)))
print(magnitude(sn_sum))



# pt2
# this might take a while
max_mag = 0
for a, b in permutations(snailfish_numbers, 2):
    mag = magnitude(add(a, b))
    if mag > max_mag:
        max_mag = mag

print(max_mag)

# actually it's pretty quick! 2 seconds on my machine
