def inputdata():
    prefixs = "192.168.1"
    suffixs = "10, 22, 35-47, 112, 200-225, 252"
    ips = generateIP(prefixs, suffixs)
    vlan = "99"
    vrf = "default"
    port_s = "ICMP, 22, 80, 443, 3725, 445, 135, 137, 138, 139, 1024-4096"
    ports = generatePort(port_s)
    return ips, vlan, vrf, ports

def generateIP(prefixs, suffixs):
    ips_l = []
    for suffix in suffixs.split(', '):
        if suffix == "":
            continue
        if "-" in suffix:
            a, b = suffix.split('-')
            for j in range(int(a), int(b) + 1, 1):
                ips_l.append(prefixs + "." + str(j))
        else:
            ips_l.append(prefixs + "." + suffix)
    return set(ips_l)

def generatePort(ports):
    ports_l = []
    for port in ports.split(', '):
        if port == "":
            continue
        if "-" in port:
            a, b = port.split('-')
            for j in range(int(a), int(b) + 1, 1):
                ports_l.append(str(j))
        else:
            ports_l.append(port)
    return set(ports_l)

def printInfo(ips, vlan, vrf, ports):
    print(">>>" + "="*50 +">>>")
    print(">>> Generate Connection Testing Command >>>")
    print(">>>" + "="*50 +">>>")
    print("IPs : " + ", ".join(sorted(ips)))
    print("VLAN : " + vlan)
    print("VRF : " + vrf)
    print("PORTs : " + ", ".join(sorted(ports)))
    print(">>>" + "="*50 +">>>")

def generateTraceroute(ip, vlan, vrf):
    print("traceroute " + ip + " source v " + vlan + " v " + vrf)

def generateTelnet(ip, port, vlan, vrf):
    print("telnet " + ip + " " + port + " s v " + vlan + " v " + vrf)

def generateCommand(ips, vlan, vrf, ports):
    print(">>> Generate Command >>>")
    print(">>>" + "="*40 +">>>")
    for ip in ips:
        for port in ports:
            if port == "ICMP":
                generateTraceroute(ip, vlan, vrf)
            else:
                generateTelnet(ip, port, vlan, vrf)
        print(">>>" + "="*40 +">>>")

if __name__ == "__main__":
    ips, vlan, vrf, ports = inputdata()
    printInfo(ips, vlan, vrf, ports)
    generateCommand(ips, vlan, vrf, ports)