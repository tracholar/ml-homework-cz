

import random

def sample_max(arr):
    n = 0 # count for max
    max_value = None
    idx = None

    for i, x in enumerate(arr):
        if max_value is None or x > max_value:
            max_value = x
            n = 0
            idx = i
        elif x < max_value:
            continue
        elif x == max_value:
            n += 1
            if random.random() < 1.0/n:
                idx = i

    return idx

print(sample_max([1,2,3,6,6,6]))