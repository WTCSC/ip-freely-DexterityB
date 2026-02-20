import subprocess

def get_hosts(full_ip):
    split_ip = full_ip.split("/")
    ip = split_ip[0].split(".")
    mask = int(split_ip[1])
    hosts = []

    if mask >= 24:
        first_part = ip[0]
        second_part = ip[1]
        third_part = ip[2]
        last_min = int(ip[3]) + 1
        for fourth in range(last_min, 255):
            hosts.append(f"{first_part}.{second_part}.{third_part}.{fourth}")

    elif mask >= 16:
        first_part = ip[0]
        second_part = ip[1]
        third_min = int(ip[2])
        for third in range(third_min, 255):
            for fourth in range(1, 255):
                hosts.append(f"{first_part}.{second_part}.{third}.{fourth}")

    elif mask >= 8:
        first_part = ip[0]
        second_min = int(ip[1])
        for second in range(second_min, 255):
            for third in range(1, 255):
                for fourth in range(1, 255):
                    hosts.append(f"{first_part}.{second}.{third}.{fourth}")

    else:
        first_min = int(ip[0])
        for first in range(first_min, 255):
            for second in range(1, 255):
                for third in range(1, 255):
                    for fourth in range(1, 255):
                        hosts.append(f"{first}.{second}.{third}.{fourth}")

    return hosts

def ping(ip):
    command = ['ping', '-c', '1', '-W', '1', ip]
    ping_result = subprocess.run(command, capture_output=True, text=True)
    
    if ping_result.returncode == 0:
        status = 'UP'
    else:
        status = 'DOWN'



    print(ping_result)
    print(status)
    split_stdout = ping_result.stdout.split('time=')
    ping_time = split_stdout[1].split("\n")[0]
    print(ping_time)

def main():
    ip = input("Input IP in CIDR notation: ")
    hosts = get_hosts(ip)
    print(hosts)



ping("8.8.8.8")