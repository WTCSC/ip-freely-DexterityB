import subprocess

def get_hosts(full_ip):
    split_ip = full_ip.split("/")
    ip = split_ip[0].split(".")
    mask = int(split_ip[1])
    hosts = []

    if mask == 32:
        return [split_ip[0]]
    
    elif mask >= 24:
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
    try:
        command = ['ping', '-c', '1', '-W', '1', ip]
        ping_result = subprocess.run(command, capture_output=True, text=True)
    
        if ping_result.returncode == 0:
            status = 'UP'
            split_stdout = ping_result.stdout.split('time=')
            ping_time = split_stdout[1].split("\n")[0]
        else:
            status = 'DOWN'
            ping_time = 'No response'
    except:
        status = 'Error'
        ping_time = 'Error occured'

    return f"{ip}  -  {status} ({ping_time})"

def main():
    ip = input("Input IP in CIDR notation: ")
    hosts = get_hosts(ip)
    for host in hosts:
        print(ping(host))

if __name__ == "__main__":
    main()