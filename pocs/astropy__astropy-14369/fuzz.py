import atheris
import sys
import astropy.units as u
from astropy.io import ascii
import warnings
import io

def TestOneInput(data):
    try:
        warnings.simplefilter("ignore", category=u.UnitsWarning)

        # Ignore random fuzz input — we force our crashing unit
        fuzzed_unit = "10+3J/m/s/kpc2"  

        table_text = f"""\
Title:
Authors:
Journal-ref:
Comments:
===========================================================================
Byte-by-byte Description of file: table1.dat
---------------------------------------------------------------------------
   1-  7  F7.3   ---    Frequency  Observed Frequency (GHz)
   9- 13  F5.1   ---    SNR        Signal to Noise Ratio
  15- 21  F7.3   {fuzzed_unit}    Fint      Integrated Flux
---------------------------------------------------------------------------
 115.271  16.0    1.23
 230.538  10.0    2.34
"""

        table = ascii.read(io.StringIO(table_text), format='cds')
        unit = table['Fint'].unit

        # ✨ Immediately trigger assertion
        expected_unit = (10**3) * u.J / u.m / u.s / u.kpc**2
        assert unit == expected_unit, (
            f"Bug triggered! Wrong parsing.\n"
            f"Expected: {expected_unit}\n"
            f"Got: {unit}"
        )

    except AssertionError:
        print("Assertion failed! Bug reproduced!")
        raise

    except Exception:
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
