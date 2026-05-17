from scapy.all import ARP, sniff
from datetime import datetime

# Known legitimate MAC addresses
TRUSTED = {
    "192.168.1.1"  : "08:aa:89:a5:11:a6",  # Router
    "192.168.1.23" : "70:a6:cc:6f:58:47",  # Kali laptop
    "192.168.1.20" : "a6:6f:c5:26:a0:e8",  # Phone
    "192.168.1.21" : "b0:cb:d8:c6:50:84",  # ESP32
}

arp_table = {}
alert_log = open("/home/kali/Documents/arp_project/arp_alerts.log", "a")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    alert_log.write(line + "\n")
    alert_log.flush()

def process_packet(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 2:
        src_ip  = packet[ARP].psrc
        src_mac = packet[ARP].hwsrc.lower()

        # Check against trusted devices
        if src_ip in TRUSTED:
            trusted_mac = TRUSTED[src_ip].lower()
            if src_mac != trusted_mac:
                log(f"[!!!] ALERT — ARP POISONING DETECTED!")
                log(f"      IP       : {src_ip}")
                log(f"      Real MAC : {trusted_mac}")
                log(f"      Fake MAC : {src_mac}")
                log(f"      Someone is impersonating {src_ip}!")
                print("="*50)

        # Track all MAC changes
        if src_ip in arp_table:
            if arp_table[src_ip] != src_mac:
                log(f"[!] MAC CHANGE DETECTED for {src_ip}")
                log(f"    Was : {arp_table[src_ip]}")
                log(f"    Now : {src_mac}")
        else:
            log(f"[+] New device seen: {src_ip} → {src_mac}")

        arp_table[src_ip] = src_mac

log("[*] ARP Anomaly Detector started...")
log(f"[*] Watching {len(TRUSTED)} trusted devices\n")

try:
    sniff(filter="arp", prn=process_packet, store=0, iface="wlan0")
except KeyboardInterrupt:
    log("[*] Detector stopped.")
    alert_log.close()
