
def diversify(alist, window_size):
    output = []
    tmp = []
    for i, a in enumerate(alist):

        tmp2 = []
        for x in tmp:
            start = max(0, len(output) - window_size + 1)
            end = len(output)
            if x not in output[start:end]:
                output.append(x)
            else:
                tmp2.append(x)
        tmp = tmp2


        start = max(0, len(output) - window_size + 1)
        end = len(output)

        if a in output[start:end]:
            tmp.append(a)
        else:
            output.append(a)

    for x in tmp:
        start = max(0, len(output) - window_size + 1)
        end = len(output)
        if x not in output[start:end]:
            output.append(x)

    return output

print(diversify([1,1,2,3,4], 3))