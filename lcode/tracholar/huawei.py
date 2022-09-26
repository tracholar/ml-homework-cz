import sys


def norm_ip(ip):
    return '.'.join([str(int(x)) for x in ip.split('.')])

if __name__ == '__main__':
    n = int(sys.stdin.readline().strip())

    monthIps = set()
    dayIps = {}

    for line in sys.stdin:
        if line.strip() == '':
            continue

        dt, ip, url, result = line.strip().split('|')
        day = int(dt[-2:])
        ip = norm_ip(ip)

        if result == 'success' and url == '/login.do':
            monthIps.add(ip)

            if day not in dayIps:
                dayIps[day] = set()

            dayIps[day].add(ip)


    # 月活
    print(len(monthIps), end=' ')
    # 日活
    for day in range(1, 32):
        if day not in dayIps:
            print(0, end=' ')
        else:
            print(len(dayIps[day]), end=' ')

            