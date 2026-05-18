# Multi-Layer IoT Security Attack Chain & Defence System

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

attacker.py

### Stage 3 - DNS Spoofing

iptables FORWARDED through Linux Kernel using NFQUEUE.<br>dns_spoof.py

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

## Key Findings 
1. ARP protocol has zero authentication — any LAN device can impersonate any other device
2. EV1527 433MHz protocol uses fixed codes — no rolling code, no encryption, trivially replayable

---

## Screenshots

|        Evidence        |              Description                 |
|------------------------|------------------------------------------|
| fing_before.jpg        | Phone ARP table — real router MAC        |
| fing_during.jpg        | Phone ARP table — spoofed to Kali MAC    |
| dns_spoof_output.jpg   | DNS queries intercepted and redirected   |
| logic2_credentials.jpg | Credentials decoded at UART signal level |
| dashboard.jpg          | Live monitoring dashboard                |
| detector_alert.jpg     | ARP anomaly detection output             |
| wireshark_arp.jpg      | ARP poison packets at packet level       |
| wireshark_dns.jpg      | DNS spoofing at packet level             |
| relay_multimeter.jpg   | Voltage spike on relay actuation         |

---
