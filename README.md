# Ultrasound Signal Generator Control via PyVISA

A Python-based control program for configuring and operating a **GW Instek AFG-3022 arbitrary function generator** for burst-mode ultrasound experiments.

The program communicates with the signal generator through **PyVISA** and allows the user to configure the VISA address and major ultrasound waveform parameters from a single **USER SETTINGS** section at the beginning of the Python script.

The main adjustable parameters include:

- VISA instrument address
- carrier frequency
- output amplitude
- burst duration
- pulse repetition frequency (PRF)
- total output duration
- output-channel control

> **Important:** Always verify the waveform and output settings before connecting the signal generator to a power amplifier, ultrasound transducer, or experimental system.

---

# Overview

This program was developed to simplify control of the:

**GW Instek AFG-3022 Arbitrary Function Generator**

for ultrasound stimulation experiments.

Instead of manually configuring the signal generator for every experiment, the major waveform parameters can be defined directly at the beginning of the Python script.

The overall workflow is:

```text
Install IOLSPrerequisites
        ↓
Install Keysight IO Libraries Suite Main
        ↓
Open Keysight Connection Expert
        ↓
Connect and detect the GW Instek AFG-3022
        ↓
Identify the VISA resource address
        ↓
Edit USER SETTINGS in the Python script
        ↓
Set ultrasound waveform parameters
        ↓
Run the Python script
        ↓
Configure burst-mode output
        ↓
Enable signal-generator output
        ↓
Maintain output for the specified duration
        ↓
Automatically disable output
        ↓
Close the VISA connection
```

---

# Hardware

## Signal Generator

The program is intended for use with:

**GW Instek AFG-3022 Arbitrary Function Generator**

The Python program communicates with the instrument using VISA commands.

The current implementation sends commands for:

- sine-wave generation
- carrier frequency
- output voltage
- burst mode
- number of cycles per burst
- pulse repetition period
- internal burst trigger
- channel output control

---

## Experimental Signal Chain

A typical experimental configuration is:

```text
Computer
   ↓
PyVISA
   ↓
Keysight VISA / IO Libraries
   ↓
GW Instek AFG-3022
   ↓
Power Amplifier
   ↓
Ultrasound Transducer
   ↓
Experimental Target
```

The signal generator provides the electrical waveform that is subsequently amplified before driving the ultrasound transducer.

---

# Prerequisite: Keysight IO Libraries Suite

Before running the Python program, the **Keysight IO Libraries Suite** must be installed.

Download the Keysight IO Libraries Suite from the official Keysight website: https://www.keysight.com/find/iosuiteproductcounter

For the installation package used in this project, two installer files are used:

```text
IOLSPrerequisites-21.1.17-windows-x64.exe
IOLibrariesSuiteMain-21.1.17-windows-x64.exe
```

The installation order is important.

Install them in the following order:

```text
1. IOLSPrerequisites-21.1.17-windows-x64.exe
        ↓
2. IOLibrariesSuiteMain-21.1.17-windows-x64.exe
```

---

## Step 1 — Install IOLS Prerequisites

First, run:

```text
IOLSPrerequisites-21.1.17-windows-x64.exe
```

Complete the prerequisite installation before proceeding to the main Keysight IO Libraries Suite installer.

---

## Step 2 — Install Keysight IO Libraries Suite Main

After the prerequisite installation is complete, run:

```text
IOLibrariesSuiteMain-21.1.17-windows-x64.exe
```

Complete the installation.

After installation, **Keysight Connection Expert** should be available on the computer.

---

# Keysight Connection Expert

Keysight Connection Expert is used to verify communication between the computer and the signal generator and to determine the VISA resource address.

After installation:

1. Connect the **GW Instek AFG-3022** to the computer.
2. Turn on the signal generator.
3. Open **Keysight Connection Expert**.
4. Confirm that the signal generator is detected.
5. Find the VISA resource address assigned to the instrument.
6. Copy the VISA address into the Python script.

For example:

```text
ASRL4::INSTR
```

The VISA address is system dependent.

Another computer or another connection may show a different address, for example:

```text
ASRL3::INSTR
ASRL5::INSTR
USB0::...
TCPIP0::...
```

Therefore, always verify the actual VISA address in **Keysight Connection Expert** before running the Python program.

---

# Python Requirements

The program requires:

- Python 3
- PyVISA
- Keysight IO Libraries Suite / VISA implementation

Install PyVISA using:

```bash
pip install pyvisa
```

Alternatively, if using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# Repository Structure

```text
Ultrasound-Signal-Generator-Control/
├── signal_generator_control.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Quick Start

## 1. Install Keysight software

Install:

```text
IOLSPrerequisites-21.1.17-windows-x64.exe
```

first.

Then install:

```text
IOLibrariesSuiteMain-21.1.17-windows-x64.exe
```

---

## 2. Open Keysight Connection Expert

Open:

```text
Keysight Connection Expert
```

and confirm that the **GW Instek AFG-3022** is detected.

---

## 3. Find the VISA Address

For example:

```text
ASRL4::INSTR
```

Copy this address.

---

## 4. Open the Python Program

Open:

```text
signal_generator_control.py
```

All parameters that normally need to be changed are placed near the beginning of the script under:

```python
# ============================================================
# USER SETTINGS
# Edit the parameters in this section before running the script.
# ============================================================
```

The main settings are:

```python
VISA_ADDRESS = "ASRL4::INSTR"

FREQUENCY_HZ = 300e3
AMPLITUDE_VPP = 0.37468
BURST_LENGTH_MS = 0.75
PRF_HZ = 100

OUTPUT_DURATION_S = 3.0
ENABLE_CHANNEL_2 = True
```

For routine experimental use, these are normally the only parameters that need to be edited.

---

# User Settings

## VISA Address

The VISA address is defined by:

```python
VISA_ADDRESS = "ASRL4::INSTR"
```

This address must match the VISA resource address shown in:

**Keysight Connection Expert**

For example, if Connection Expert shows:

```text
ASRL5::INSTR
```

change the Python setting to:

```python
VISA_ADDRESS = "ASRL5::INSTR"
```

Do not assume that:

```text
ASRL4::INSTR
```

will be valid on every computer.

---

# Ultrasound / Waveform Parameters

The major waveform parameters are located directly below the VISA address.

---

## Carrier Frequency

```python
FREQUENCY_HZ = 300e3
```

This defines the sinusoidal carrier frequency.

The default value corresponds to:

```text
300,000 Hz
= 300 kHz
```

For example:

```python
FREQUENCY_HZ = 500e3
```

corresponds to:

```text
500 kHz
```

---

## Output Amplitude

```python
AMPLITUDE_VPP = 0.37468
```

This defines the electrical output amplitude of the signal generator in:

```text
Vpp
```

or:

```text
volts peak-to-peak
```

Example values used in the original experimental system include:

```text
0.25 MI → 0.37468 Vpp
0.75 MI → 1.413302 Vpp
```

These values were used for the original experimental setup.

> **Important:** These values should not be interpreted as universal MI-to-voltage conversion values.

The relationship between signal-generator voltage and acoustic output depends on:

- signal generator
- power amplifier
- amplifier gain
- ultrasound transducer
- transducer frequency response
- electrical impedance
- coupling conditions
- experimental loading
- hydrophone calibration
- measurement geometry

Therefore, another ultrasound system must be independently calibrated before associating a particular input voltage with a mechanical index or acoustic pressure.

---

## Burst Length

```python
BURST_LENGTH_MS = 0.75
```

This defines the duration of each ultrasound burst.

The default value corresponds to:

```text
0.75 ms
```

The program automatically converts this value into seconds internally.

For example:

```text
0.75 ms
= 0.00075 s
```

---

## Pulse Repetition Frequency

```python
PRF_HZ = 100
```

This defines the:

**Pulse Repetition Frequency (PRF)**

The default value corresponds to:

```text
100 Hz
```

The program automatically calculates the:

**Pulse Repetition Period (PRP)**

using:

```text
PRP = 1 / PRF
```

For:

```text
PRF = 100 Hz
```

the PRP is:

```text
PRP = 1 / 100
    = 0.01 s
    = 10 ms
```

---

# Burst Cycle Calculation

The number of sinusoidal cycles contained within each burst is automatically calculated by the program.

The relationship is:

```text
Cycles per burst
=
Carrier frequency × Burst duration
```

Using the default parameters:

```text
Carrier frequency = 300 kHz
Burst duration    = 0.75 ms
```

therefore:

```text
300,000 Hz × 0.00075 s
= 225 cycles
```

Thus:

```text
Cycles per burst = 225
```

The program automatically sends this calculated value to the signal generator.

---

# Burst Timing Validation

The program also verifies that:

```text
Burst duration < Pulse Repetition Period
```

For the default parameters:

```text
Burst duration = 0.75 ms
PRP            = 10 ms
```

therefore:

```text
0.75 ms < 10 ms
```

and the configuration is valid.

If the burst duration is equal to or longer than the PRP, the program will stop and display an error instead of enabling the output.

---

# Output Duration

The total time for which the signal generator output remains enabled is defined by:

```python
OUTPUT_DURATION_S = 3.0
```

The default corresponds to:

```text
3 seconds
```

The execution sequence is:

```text
Output ON
    ↓
Wait 3 seconds
    ↓
Output OFF
```

For example:

```python
OUTPUT_DURATION_S = 10.0
```

will maintain the output for:

```text
10 seconds
```

before automatically disabling it.

---

# Output Channel Control

The program includes:

```python
ENABLE_CHANNEL_2 = True
```

When this is set to:

```python
True
```

the program sends output commands to:

```text
OUTP
OUTP2
```

If Channel 2 is not required, change the parameter to:

```python
ENABLE_CHANNEL_2 = False
```

---

# Default Experimental Configuration

The default parameters currently included in the program are:

| Parameter | Default | Description |
|---|---:|---|
| Signal generator | GW Instek AFG-3022 | Arbitrary function generator |
| VISA address | `ASRL4::INSTR` | Example VISA communication address |
| Waveform | Sine | Carrier waveform |
| Carrier frequency | `300 kHz` | Ultrasound carrier frequency |
| Output amplitude | `0.37468 Vpp` | Signal-generator electrical output |
| Burst length | `0.75 ms` | Duration of each burst |
| PRF | `100 Hz` | Pulse repetition frequency |
| PRP | `10 ms` | Automatically calculated from PRF |
| Cycles per burst | `225` | Automatically calculated |
| Output duration | `3 s` | Total signal-generator output time |
| Channel 2 | Enabled | Controlled through `OUTP2` |

---

# Program Workflow

After the user-defined parameters have been entered, the script performs the following operations:

```text
Read USER SETTINGS
        ↓
Initialize PyVISA Resource Manager
        ↓
Open VISA connection
        ↓
Connect to GW Instek AFG-3022
        ↓
Query instrument identification
(*IDN?)
        ↓
Validate waveform parameters
        ↓
Calculate PRP
        ↓
Calculate cycles per burst
        ↓
Configure sine waveform
        ↓
Configure carrier frequency
        ↓
Configure output amplitude
        ↓
Enable burst mode
        ↓
Configure number of cycles
        ↓
Configure pulse repetition period
        ↓
Configure internal burst trigger
        ↓
Enable output
        ↓
Wait for OUTPUT_DURATION_S
        ↓
Disable output
        ↓
Close instrument connection
        ↓
Close VISA Resource Manager
```

---

# VISA Connection Test

When the script connects successfully, it sends:

```text
*IDN?
```

to the signal generator.

The connected instrument should return its identification information.

The terminal will display something similar to:

```text
Connected to: ...
VISA address: ASRL4::INSTR
```

This allows the user to verify that the Python program is communicating with the expected instrument before the waveform is generated.

---

# Instrument Commands

The current implementation sends VISA / SCPI-style commands including:

```text
*IDN?
FUNC SIN
FREQ
VOLT
BURS:STAT
BURS:NCYC
BURS:INT
BURS:TRIG:SOUR
OUTP
OUTP2
```

These commands are used to configure the signal generator.

### `*IDN?`

Queries the connected instrument identity.

### `FUNC SIN`

Sets the waveform to sine.

### `FREQ`

Sets the carrier frequency.

### `VOLT`

Sets the electrical output amplitude.

### `BURS:STAT`

Enables burst mode.

### `BURS:NCYC`

Sets the number of cycles per burst.

### `BURS:INT`

Sets the burst repetition interval.

### `BURS:TRIG:SOUR`

Sets the burst trigger source.

### `OUTP`

Controls the primary output.

### `OUTP2`

Controls the second output channel.

The current command sequence was developed for the experimental configuration using the **GW Instek AFG-3022**.

If another signal-generator model is used, supported commands and channel behavior should be verified using the corresponding programming manual.

---

# Error Handling

The program includes parameter validation and exception handling.

Examples of invalid conditions include:

```text
frequency <= 0
amplitude <= 0
burst length <= 0
PRF <= 0
burst duration >= PRP
```

If an invalid configuration is detected, the program stops before enabling the output.

---

# Automatic Output Shutdown

The Python program uses a `finally` block to attempt to disable the signal-generator output before closing the VISA connection.

The intended behavior is:

```text
Normal execution
        ↓
Output OFF
        ↓
Close connection
```

and, if possible:

```text
Error / interruption
        ↓
Attempt Output OFF
        ↓
Close connection
```

This reduces the possibility of accidentally leaving the output enabled after the Python program stops.

However, software shutdown should **not** be considered the only safety mechanism.

Always check the physical instrument output state after:

- Python exceptions
- communication errors
- program interruption
- computer failure
- VISA communication loss
- unexpected instrument behavior

---

# Safety and Experimental Use

Before enabling ultrasound output:

1. Confirm that the connected instrument is the **GW Instek AFG-3022**.
2. Confirm the VISA address in Keysight Connection Expert.
3. Verify the carrier frequency.
4. Verify the electrical output voltage.
5. Verify the burst duration.
6. Verify the PRF.
7. Verify the total stimulation duration.
8. Verify the amplifier input and operating limits.
9. Verify the ultrasound transducer operating limits.
10. Confirm that the complete ultrasound system has been appropriately calibrated.
11. Verify the generated electrical waveform with an oscilloscope before experimental use when appropriate.

The relationship between the electrical signal and acoustic output should be determined experimentally for the specific ultrasound system.

---

# Example Configuration

For the current default configuration:

```python
VISA_ADDRESS = "ASRL4::INSTR"

FREQUENCY_HZ = 300e3
AMPLITUDE_VPP = 0.37468
BURST_LENGTH_MS = 0.75
PRF_HZ = 100

OUTPUT_DURATION_S = 3.0
ENABLE_CHANNEL_2 = True
```

the program calculates:

```text
Carrier frequency
= 300 kHz

Burst duration
= 0.75 ms

PRF
= 100 Hz

PRP
= 10 ms

Cycles per burst
= 225
```

and maintains the signal-generator output for:

```text
3 seconds
```

before automatically turning it off.

---

# Running the Program

From the repository directory, run:

```bash
python signal_generator_control.py
```

If the VISA connection is successful, the script will:

1. connect to the GW Instek AFG-3022;
2. query the instrument identity;
3. display the selected parameters;
4. configure the waveform;
5. configure burst mode;
6. enable the output;
7. maintain the output for the specified duration;
8. disable the output;
9. close the VISA connection.

---

# Troubleshooting

## Instrument Not Found

If the program cannot connect to:

```text
ASRL4::INSTR
```

open **Keysight Connection Expert** and confirm the actual VISA address.

The VISA address may change depending on the computer or connection.

---

## PyVISA Error

Confirm that PyVISA is installed:

```bash
pip install pyvisa
```

Also confirm that both Keysight installers were installed in the correct order:

```text
1. IOLSPrerequisites-21.1.17-windows-x64.exe
2. IOLibrariesSuiteMain-21.1.17-windows-x64.exe
```

---

## Signal Generator Not Detected in Connection Expert

Check:

- signal-generator power
- computer connection
- USB / serial cable
- Keysight IO Libraries installation
- instrument communication settings

Restarting Keysight Connection Expert after reconnecting the instrument may also be necessary.

---

## `*IDN?` Does Not Return

Check:

- signal-generator power
- USB / serial connection
- VISA address
- communication settings
- Keysight Connection Expert instrument detection

---

## Unsupported Instrument Command

If the instrument reports an error after a command such as:

```text
BURS:INT
```

or:

```text
OUTP2
```

verify the corresponding command in the programming manual for the **GW Instek AFG-3022**.

---

# Installation and Execution Summary

The complete setup sequence is:

```text
IOLSPrerequisites-21.1.17-windows-x64.exe
        ↓
IOLibrariesSuiteMain-21.1.17-windows-x64.exe
        ↓
Keysight Connection Expert
        ↓
Detect GW Instek AFG-3022
        ↓
Copy VISA address
        ↓
Install PyVISA
        ↓
Open signal_generator_control.py
        ↓
Edit USER SETTINGS
        ↓
Run Python script
        ↓
Generate configured ultrasound waveform
```

---

# Notes

This repository contains **signal-generator control code only**.

It does not include:

- experimental datasets
- acoustic calibration data
- hydrophone calibration data
- amplifier calibration files
- transducer calibration data
- measured acoustic pressure
- mechanical-index calibration files

The waveform parameters included in the script represent the original experimental configuration and may need to be modified for another setup.

---

# Intended Use

This program was developed to simplify repeatable configuration of an ultrasound stimulation waveform using the **GW Instek AFG-3022**.

It is intended to reduce repetitive manual configuration while keeping the major experimental parameters easily accessible at the beginning of the script.

The main user-editable workflow is:

```text
Find VISA address
        ↓
Set VISA_ADDRESS
        ↓
Set FREQUENCY_HZ
        ↓
Set AMPLITUDE_VPP
        ↓
Set BURST_LENGTH_MS
        ↓
Set PRF_HZ
        ↓
Set OUTPUT_DURATION_S
        ↓
Run the program
```

---

# Author

**Wei-Hong Ruan**

Biomedical Engineer / Neuroscience Researcher

Research interests include:

- Focused ultrasound neuromodulation
- Closed-loop neurotechnology
- EEG and neural signal processing
- Functional neuroimaging
- Biomedical instrumentation
- Multimodal neuroscience

GitHub:

https://github.com/WeiHongRuan

---

# License

No open-source license has been assigned yet.

Add a license only after confirming how others should be permitted to use, modify, distribute, or build upon this code.
