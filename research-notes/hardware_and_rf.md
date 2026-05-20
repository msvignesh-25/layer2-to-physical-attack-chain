# Deep Dive: Physical Bus Exposure & Sub-GHz RF Replay

This section documents the transition from digital network session manipulation to physical microelectronic exploitation.

## 1. Bus Sniffing & Logic Analysis (UART/SPI)

Even if a core micro-controller securely holds firmware logic, physical hardware lines on a circuit lack encryption by default.Connecting a Logic Analyzer directly to these transmission lines allows for the interception of plaintext traffic.

* **UART Tracing:** The credentials captured from the web handler are passed in the clear over the bare circuit traces.
* **SPI Register Monitoring:** Hardware commands sent to the CC1101 transceiver module pass standard unencrypted SPI configuartion, allowing use to monitor operating frequencies and channel modes.

## 2. Fixec-Code RF Failure Architecture (EV1527)

Many low-cost actuation systems use legacy **EV1527 fixed-code chips**.

### The Vulnerability

An EV1527 frame consists of a 24-bit payload:
* **20 Bits:** Unique pre-programmed transmiited identifier
* **4 Bits:** Control/Button data command

Because there is zero cryptographic freshness validation, no rolling-code sequencing (like KeeLoq), and no challenge-respone authentication, **the signal is entirely static**.
