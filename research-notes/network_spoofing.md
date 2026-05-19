# Deep Dive: Layer 2 & 3 Network Interception Engine

This module breaks down how vulnerabilities in fundamental local area network protocols influence application layer behavior.

## 1. ARP Cache Poisoning via Gratuitous ARP Replies (`attacker.py`)
The Address Resolution Protocol (ARP) was designed under a legacy assumption of total network trust. Because it lacks cryptographic signatures or state verification, the attacker script abuses **Gratuitous ARP replies** and update local ARP cache mappings without validating their legitimacy.

By continuously flooding the victim device with unrequested ARP packets, the local hardware cache is poisoned—forcing the victim's physical Layer 2 Ethernet frames to map the gateway's IP address directly to the attacker machine's MAC address.

## 2. In-Flight DNS Modification (`dns_spoof.py`)
Once positioned as a Man-in-the-Middle (MitM), standard DNS queries transmitted over unencrypted UDP (Port 53) are processed. 

### Overcoming the Linux Forwarding Race Condition
In early iterations, using an `iptables` forwarding rule while natively passing altered payloads caused a severe race condition: the original network packet leaked through to the true router. The client device would receive two conflicting answers, throwing a browser network crash or an unresolvable `NXDOMAIN` error.

The solution implemented in this architecture relies on a strict kernel-to-userland boundary handoff:
1. `iptables` traps inbound UDP port 53 packets and hooks them into Linux kernelspace via **`NFQUEUE`**.
2. `dns_spoof.py` binds to the queue, converting raw hex bytes into structured Scapy `IP()` layers.
3. Upon discovering a match for `login.google.net`, a custom `DNSRR` layer is built.
4. **Critical Mechanism:** The script calls `packet.drop()` to instantly kill the authentic query, preventing it from reaching the upstream gateway. Simultaneously, Scapy's `send()` function directly injects the spoofed response onto the local line.

### Interaction with Browser Security Mechanisms
Modern browsers enforce strict security constraints like HTTP Strict Transport Security (HSTS). To prevent the browser from instantly dropping the forged answer due to a lack of valid SSL handshakes over Port 443, the injection strictly points to an unencrypted captive portal scenario (`Port 80`). This exploits the initialization gap before the browser can mandate an encrypted TLS upgrade.

Although higher-layer protections such as TLS and HSTS provide important defensive barriers, compromise at Layer 2 and Layer 3 still enables:
- traffic interception
- DNS manipulation
- packet visibility
- request redirection