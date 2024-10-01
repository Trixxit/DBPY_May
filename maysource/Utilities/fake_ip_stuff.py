import random


def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def random_ipv6():
    return "2001:" + ":".join(f"{random.randint(0, 65535):04x}" for _ in range(7))

def random_mac():
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

def random_data_usage():
    return f"{random.randint(100, 1000)}GB/month"

def random_bandwidth():
    choices = ['1 Gbps', '500 Mbps', '100 Mbps', '10 Gbps']
    return random.choice(choices)

def random_model(prefix, num_range):
    return f"{prefix}{random.randint(*num_range)}"

def random_version():
    return f"{random.randint(1, 10)}.{random.randint(0, 9)}.{random.randint(0, 20)}"

def random_signal_strength():
    return f"-{random.randint(30, 80)} dBm"

def randomize_data():
    return (
        f"- IP Address: {random_ip()}\n"
        f"- IPv6 Address: {random_ipv6()}\n"
        f"- Router Model: {random_model('Cisco XR', (1000, 9999))} Series\n"
        f"- Modem Number: {random_model('ZX', (9001, 9999))}-B{random.randint(12, 99)}\n"
        f"- MAC Address: {random_mac()}\n"
        f"- DNS Server: {random_ip()}, {random_ip()}\n"
        f"- Subnet Mask: 255.255.255.{random.randint(0, 255)}\n"
        f"- Default Gateway: {random_ip()}\n"
        f"- DHCP Range: {random_ip()} to {random_ip()}\n"
        f"- Network Band: {random.choice(['2.4GHz', '5GHz', '2.4GHz & 5GHz Dual Band'])}\n"
        f"- SSID: MySecureNet_{random.choice(['2G', '5G'])}\n"
        f"- Wireless Channel: {random.randint(1, 11)} for 2.4GHz, {random.randint(36, 64)} for 5GHz\n"
        f"- Firewall Version: {random_version()}\n"
        f"- Port Forwarding Rules: Port {random.randint(20, 80)} to {random_ip()}, Port {random.randint(80, 160)} to {random_ip()}\n"
        f"- VPN Service: {random.choice(['Enabled', 'Disabled'])}\n"
        f"- NAT Type: {random.choice(['Open', 'Moderate', 'Strict'])}\n"
        f"- Signal Strength: {random_signal_strength()} for 5GHz, {random_signal_strength()} for 2.4GHz\n"
        f"- Data Usage: {random_data_usage()}\n"
        f"- Load Balancer Model: LB-{random.randint(3000, 5000)}X\n"
        f"- Network Switch Model: NetSwitch Pro {random.randint(24, 48)}P\n"
        f"- Wireless Access Point Model: WAP{random.randint(200, 500)}N\n"
        f"- Ethernet Cable Type: Cat{random.randint(5, 7)}\n"
        f"- Uplink Speed: {random_bandwidth()}\n"
        f"- Downlink Speed: {random_bandwidth()}\n"
        f"- Bandwidth Cap: {random.choice(['None', '500GB', '1TB'])}\n"
        f"- Cloud Backup Service: {'Enabled' if random.choice([True, False]) else 'Disabled'} ({random.randint(100, 1000)} GB Storage)\n"
        f"- Remote Access: {'Enabled' if random.choice([True, False]) else 'Disabled'} (via SSH)\n"
        f"- Security Protocol: WPA{random.randint(2, 3)}\n"
        f"- Device Priority Settings: High Priority to IP {random_ip()} (Gaming Console)\n"
        f"- Guest Network: {'Enabled' if random.choice([True, False]) else 'Disabled'} (SSID: GuestNet_{random.choice(['2.4G', '5G'])})\n"
        f"- Firmware Version: {random_version()}\n"
    )
