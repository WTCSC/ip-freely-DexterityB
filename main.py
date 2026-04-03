import subprocess
import socket

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

    return ip, status, ping_time

def get_ports(ports):
    if len(ports.split('-')) > 1:
        port_list = [port for port in range(int(ports.split('-')[0]), int(ports.split('-')[1]) + 1)]
        
    else:
        port_list = ports.split(',')

    return port_list

def check_port(ip, port, timeout = 3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    port_open = sock.connect_ex((ip, port))

    sock.close
    return port_open == 0

def main():
    do_ports = False
    ip = input("Input IP in CIDR notation: ")
    
    if len(ip.split(" ")) > 1:
        ports = get_ports(ip.split(" ")[1])
        ip = ip.split(" ")[2]

        do_ports = True

    hosts = get_hosts(ip)
    for host in hosts:
        result_ip, result_status, result_ping_time = ping(host)
        print(f"{result_ip}  -  {result_status} ({result_ping_time})")

        if do_ports and result_status == 'UP':
            for port in ports:
                print(f"Port {port} Open: {check_port(host, int(port))}")

if __name__ == "__main__":
    main()