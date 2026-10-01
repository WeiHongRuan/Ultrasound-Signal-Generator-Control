"""
Ultrasound Signal Generator Control via PyVISA

This script connects to a VISA-compatible signal generator and configures
a sinusoidal burst waveform for ultrasound experiments.

Before running:
1. Install Keysight IO Libraries Suite / Keysight Connection Expert.
2. Confirm that the signal generator is detected.
3. Copy the VISA resource address shown by Connection Expert.
4. Install Python dependency:
       pip install pyvisa
5. Edit ONLY the USER SETTINGS section below for routine use.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import pyvisa


# ============================================================
# USER SETTINGS
# Edit the parameters in this section before running the script.
# ============================================================

# VISA address shown in Keysight Connection Expert.
# Example:
# VISA_ADDRESS = "ASRL4::INSTR"
VISA_ADDRESS = "ASRL4::INSTR"

# Ultrasound / waveform parameters
FREQUENCY_HZ = 300e3          # Carrier frequency in Hz (300e3 = 300 kHz)
AMPLITUDE_VPP = 0.37468       # Signal-generator output amplitude in Vpp
BURST_LENGTH_MS = 0.75        # Burst duration in milliseconds
PRF_HZ = 100                  # Pulse repetition frequency in Hz

# Output control
OUTPUT_DURATION_S = 3.0       # Total time for which output remains enabled
ENABLE_CHANNEL_2 = True       # Also control OUTP2 if the instrument supports CH2

# Experiment-specific example amplitudes from the original setup:
# 0.25 MI -> 0.37468 Vpp
# 0.75 MI -> 1.413302 Vpp
#
# IMPORTANT:
# These voltage values are specific to the original experimental system.
# They are NOT universal MI-to-voltage conversions. Acoustic output depends
# on the signal generator, amplifier, transducer, loading conditions, and
# calibration of the complete ultrasound setup.


@dataclass(frozen=True)
class UltrasoundParameters:
    """Container for burst-mode ultrasound signal parameters."""

    frequency_hz: float
    amplitude_vpp: float
    burst_length_ms: float
    prf_hz: float


def connect_instrument(visa_address: str):
    """
    Connect to a VISA-compatible signal generator.

    Parameters
    ----------
    visa_address : str
        VISA resource address reported by Keysight Connection Expert,
        for example "ASRL4::INSTR".

    Returns
    -------
    tuple
        (resource_manager, instrument)
    """
    rm = pyvisa.ResourceManager()
    instrument = rm.open_resource(visa_address)

    identity = instrument.query("*IDN?").strip()
    print(f"Connected to: {identity}")
    print(f"VISA address: {visa_address}")

    return rm, instrument


def validate_parameters(params: UltrasoundParameters) -> tuple[float, int]:
    """
    Validate ultrasound parameters and calculate PRP and cycles per burst.

    Returns
    -------
    tuple
        (pulse_repetition_period_s, cycles_per_burst)
    """
    if params.frequency_hz <= 0:
        raise ValueError("FREQUENCY_HZ must be greater than 0.")

    if params.amplitude_vpp <= 0:
        raise ValueError("AMPLITUDE_VPP must be greater than 0.")

    if params.burst_length_ms <= 0:
        raise ValueError("BURST_LENGTH_MS must be greater than 0.")

    if params.prf_hz <= 0:
        raise ValueError("PRF_HZ must be greater than 0.")

    burst_length_s = params.burst_length_ms / 1000.0
    prp_s = 1.0 / params.prf_hz

    if burst_length_s >= prp_s:
        raise ValueError(
            "Burst length must be shorter than the pulse repetition period (1 / PRF)."
        )

    cycles_per_burst = round(params.frequency_hz * burst_length_s)

    if cycles_per_burst < 1:
        raise ValueError("Calculated cycles per burst must be at least 1.")

    return prp_s, cycles_per_burst


def configure_ultrasound_signal(instrument, params: UltrasoundParameters) -> None:
    """
    Configure the signal generator for sinusoidal burst-mode output.
    """
    prp_s, cycles_per_burst = validate_parameters(params)

    # Basic waveform
    instrument.write("FUNC SIN")
    instrument.write(f"FREQ {params.frequency_hz}")
    instrument.write(f"VOLT {params.amplitude_vpp}")

    # Burst mode
    instrument.write("BURS:STAT ON")
    instrument.write(f"BURS:NCYC {cycles_per_burst}")
    instrument.write(f"BURS:INT {prp_s}")
    instrument.write("BURS:TRIG:SOUR INT")

    print("\nSignal configuration")
    print("--------------------")
    print(f"Frequency       : {params.frequency_hz / 1e3:.3f} kHz")
    print(f"Amplitude       : {params.amplitude_vpp:.6f} Vpp")
    print(f"Burst length    : {params.burst_length_ms:.3f} ms")
    print(f"PRF             : {params.prf_hz:.3f} Hz")
    print(f"PRP             : {prp_s:.6f} s")
    print(f"Cycles / burst  : {cycles_per_burst}")


def set_output(instrument, enabled: bool, enable_channel_2: bool) -> None:
    """Turn the signal-generator output on or off."""
    state = "ON" if enabled else "OFF"

    instrument.write(f"OUTP {state}")

    if enable_channel_2:
        instrument.write(f"OUTP2 {state}")

    print(f"Output {state}")


def main() -> None:
    """
    Main execution function.

    Routine users normally only need to edit the USER SETTINGS section
    at the top of this file.
    """
    parameters = UltrasoundParameters(
        frequency_hz=FREQUENCY_HZ,
        amplitude_vpp=AMPLITUDE_VPP,
        burst_length_ms=BURST_LENGTH_MS,
        prf_hz=PRF_HZ,
    )

    rm = None
    instrument = None

    try:
        print("Connecting to signal generator...")
        rm, instrument = connect_instrument(VISA_ADDRESS)

        configure_ultrasound_signal(instrument, parameters)

        print(f"\nOutput duration: {OUTPUT_DURATION_S:.3f} s")
        set_output(instrument, True, ENABLE_CHANNEL_2)

        time.sleep(OUTPUT_DURATION_S)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    except Exception as exc:
        print(f"\nError during signal-generator control: {exc}")

    finally:
        # Always try to switch output OFF before closing the VISA connection.
        if instrument is not None:
            try:
                set_output(instrument, False, ENABLE_CHANNEL_2)
            except Exception as exc:
                print(f"Warning: failed to switch output OFF: {exc}")

            try:
                instrument.close()
            except Exception:
                pass

        if rm is not None:
            try:
                rm.close()
            except Exception:
                pass

        print("VISA connection closed.")


if __name__ == "__main__":
    main()
