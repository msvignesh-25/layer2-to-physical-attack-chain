# Multi-Layer IoT Security Attack Chain & Defence System

[![Detailed Gallery](https://img.shields.io/badge/Detailed_Gallery-View%20PDF-red?style=for-the-badge&logo=adobeacrobatreader)](Attack_Chain_Detailed_Gallery.pdf)

> A complete end-to-end cyber-physical attack demonstration combining network, application, hardware and RF layers — built entirely in an isolated home lab environment for security research and awareness purposes.

---

## ⚠️ Disclaimer
This project was built and tested exclusively on personally owned devices in an isolated home lab environment. All techniques demonstrated are for educational and security awareness purposes only. Performing these attacks on networks or devices without explicit permission is illegal.

---

## Project Overview

This project demonstrates a complete attack chain spanning Layer 2 through physical actuation — showing how a single network-level vulnerability (ARP) can cascade into credential theft and physical device control.

---

## Attack Chain

```
Layer 2 -> ARP Poisoning (Kali + Scapy)
Layer 3 -> DNS Spoofing (Kali + netfilterqueue)
Layer 7 -> Web Server (ESP32 WiFi)
UART Signal Capture (Salae Logic Analyser)
RF Layer -> 433 MHz Signal Replay (CC1101 + ESP32)
Physical -> Replay actuation (433 MHz relay)
Defence -> ARP Anomaly Detector (Python)
Monitor -> Live Dashboard (Flask)

```
---

## Hardware Used

|         Component      |               Purpose             |
|------------------------|-----------------------------------|
| Kali Linux             | Attacker machine                  |
| ESP32                  | Web server + RF transmitter       |
| CC1101 433MHz          | RF signal capture and replay      |
| 433MHz Relay           | Target physical device            |
| Saleae Logic Analyzer  | UART signal capture               |
| Mobile                 | Victim device                     |

---

## Project Structure

```
arp_project/
├── attacker.py                    # ARP poisoner
├── dns_spoof.py                   # DNS interceptor
├── detector.py                    # ARP anomaly detector
├── cred_receiver.py               # Credential receiver
├── dashboard/
│   ├── app.py                     # Flask dashboard
│   └── templates/
│       └── index.html             # Dashboard UI
├── attack_timeline.txt            # Full attack timeline
framework/
├── threat_model.txt               # STRIDE threat model
analysis/
├── rf_vulnerability_analysis.txt  # RF security analysis
── README.md                       # This file

```

---

## Proof of Concept

### Stage 1 - RECON

Identify devices for victim and gateway and get their IP and MAC addresses.

### Stage 2 - ARP Poisoning

Network traffic redirection via `attacker.py`.<br>Falsely maps the Gateway IP to the Attacker's MAC address using forged ARP responses.

### Stage 3 - DNS Spoofing

Traffic intercepted via iptables FORWARD and sent to Linux Kernel using NFQUEUE.<br>`dns_spoof.py` processes the queue to inject malicious DNS responses.

### Stage 4 - Credential Capture

ESP32 hosts fake login page. Credentials captured via:
- Serial Monitor
- Flask Dashboard
- Logic Analyser

### Stage 5 - RF Replay Attack

CC1101 captures 433 MHz EV1527 signal. Replays signal to actuate physical relay. Demonstrated via audible + multimter test

### Stage 6 - Defence

detector.py
Detects MAC spoofing within 2 seconds, Logs all alerts

---
## Demo video
https://github.com/user-attachments/assets/c20af01b-5252-4365-91fc-ec1da15313e3

**NOTE**: To hear the physical relay triggering during credential capture, turn on the audio 

---

## Key Findings 
1. **ARP** protocol has **zero authentication** — any LAN device can impersonate any other device
2. EV1527 433MHz protocol uses **fixed codes** — no rolling code, no encryption, trivially replayable
3. Unencrypted **DNS** Resolution is *Vulnerable* to Injection — Local **DNS over UDP** lacks integrity checks, allowing forged packets to overwrite routing tables before      legitimate gateway responds
4. Fixed-code **Cryptographic Failures** — The absence of rolling-code mechanisms or dynamic handshakes ensures that any wireless signal captured over the air can be           *indefinitetly replayed* to manipulate physical hardware

---

## Screenshots

|        Evidence        |              Description                 |
|------------------------|------------------------------------------|
| [before_poison.jpg](assets/before_arp-poison.jpg)      | Phone ARP table — real router MAC        |
| [during_poison.jpg](assets/during_arp-poison.jpg)        | Phone ARP table — spoofed to Kali MAC    |
| [dns_spoof_output.png](assets/dns_spoof_output.png)   | DNS queries intercepted and redirected   |
| [logic2_credentials_data.jpg](assets/Logic2_credentials.png) | Credentials decoded at UART signal level |
| [logic2_credentials_wave.jpg](assets/Logic2_credentials_raw.png) | Credentials decoded at UART signal level (raw) |
| [dashboard.jpg](assets/dashboard.jpg)          | Live monitoring dashboard                |
| [detector_alert.jpg](assets/detector_alert.png)     | ARP anomaly detection output             |
| [wireshark_arp.jpg](assets/wireshark_arp.png)      | ARP poison packets at packet level       |
| [wireshark_dns.jpg](assets/wireshark_dns.png)      | DNS spoofing at packet level             |

---
