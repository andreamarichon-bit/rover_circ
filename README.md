# Rover CIRC 2026 Heist Mission Scripts

Mission software developed for the **Canadian International Rover Challenge (CIRC) 2026**, 
Heist task. Scripts are split between ground station (operator laptop) and onboard 
computer (Raspberry Pi / ESP32 on the rover).

**Team:** CIUDSE Rover Team - UABC  
**Competition:** CIRC 2026 (August 2026)
---

## Repository Structure

```text
heist_mission/
├── calculadora_cables/         # Ground station only
│   └── calculadora_cables.py
├── puente_serial/              # Ground station + Rover
│   ├── control_consola.py      # Ground station
│   └── puente_consola.py       # Rover (RPi)
├── control_morse/              # Ground station + Rover
│   ├── generador_morse.py      # Ground station
│   └── controlador_morse.py    # Rover (RPi)
└── apagador_de_luces/          # Ground station + Rover
    ├── control_luces.py        # Ground station
    └── apagador_luces.py       # Rover (RPi)
```
---

## Scripts

### Cable Calculator`calculadora_cables.py`
Operator inputs the total number of cables and their colors left to right. 
The script applies the competition's decision tree rules (3–6 cable configurations) and outputs which cable to cut. Runs on ground station laptop.

### Serial Bridge `puente_serial/`
Tunnels the security console's serial port (XLR3, 115200 baud, 3.3V TTL, 8N1) over the rover's RF link to the operator.
- `puente_consola.py` — reads serial output from the console and transmits it to ground station via socket; forwards operator keystrokes back to the console.
- `control_consola.py` — receives the console stream and renders it on the operator's terminal, allowing full interactive login and navigation.

### Morse Controller `control_morse/`
Automates vault entry by translating the vault code into Morse pulses at 
competition-spec timing (dit = 66.7 ms, dah = 200.1 ms, per ITU-R M.1677-1).
- `generador_morse.py`  takes the vault code string, encodes it to Morse, and sends the pulse sequence to the rover.
- `controlador_morse.py`  receives the sequence and drives a solenoid or servo to physically press the arcade button at the correct timing.

### Light Kill Switch `apagador_de_luces/`
Emergency light shutoff for stealth navigation through camera detection zones.
- `control_luces.py`  operator-side trigger (keyboard shortcut).
- `apagador_luces.py`  rover-side handler that cuts all visible light output immediately.
---

## Competition Context
The Heist task takes place at night. Operators work from a tent with no direct 
line of sight to the rover — all navigation is camera-based. Communication must 
be fully autonomous (no internet, cellular, or satellite). Heavy RF interference 
is expected on-site as all teams transmit simultaneously.

**Status:** Scripts developed and ready. Hardware integration and field testing 
pending before competition (August 2026).
