# Deep Dive: Blue Team Detection Mechanics (`detector.py`)

Building a secure network perimeter requires proactive defenses. This module analyzes the working of local real-time detection script.

## 1. Stateful MAC-to-IP Binding Tables

The `detector.py` uses Scapy to sniff asynchronous network traffic at Layer 2, building an internal state machine to map trusted IPs to MAC addresses.

## 2. Detection Trigger Logic

The script filters all incoming **ARP Operation 2 (Reply)** packets and checks against the cached ARP table as shown below.

```text
Inbound ARP Frame ---> Extract Sender IP & Sender MAC
                             |
                             v
               Does Sender IP exist in Trusted DB?
                   /                       \
                 YES                       NO
                 /                           \
  Does MAC match Trusted MAC?          Dynamically cache new binding
       /               \
     YES                \---> [CRITICAL ALERT] 
     /                         MAC Spoofing/Poisoning Detected!
Keep Routing                   Log Timestamp & Threat Actor Vector
```

Because an attacker must constantly flood the network to maintain an ARP spoof, the script catches these conflicting mappings within two seconds of the initial burst, outputting alert logs for instant incident responses.