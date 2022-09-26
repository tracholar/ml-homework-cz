

def qsort(arr):
    if len(arr) == 0:
        return arr

    q = arr[0]
    left = [x for x in arr[1:] if x <= q]
    right = [x for x in arr[1:] if x > q]
    return qsort(left) + [q] + qsort(right)

print(qsort([3,431,5,4,52,45,9]))


from random import randint
print(randint(0, 1))

x = list(range(10))
print(x[:4][::-1])