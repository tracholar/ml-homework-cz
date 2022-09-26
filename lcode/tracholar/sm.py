
def main():
    n = int(input().strip())
    if n < 3:
        print(0)
        return

    line = input().strip()
    arr = [int(x.strip()) for x in line.split(' ') if len(x.strip())>0]

    P = 0
    for j, A in enumerate(arr):
        if j in (0, n-1):
            continue
        left = sum(1 for x in arr[:j] if x < A)
        right = sum(1 for x in arr[j+1:] if x < A)

        P += left * right

    print(P)

main()

