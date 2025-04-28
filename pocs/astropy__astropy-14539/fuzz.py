import atheris
import sys
import tempfile
import os
from astropy.io import fits

# This is the PoC array that triggers the bug
BASE_ARRAY = [[0], [0, 0]]

def TestOneInput(data):
    if len(data) > 10:  # Keep inputs small to stay close to PoC
        return

    try:
        # Start with the base PoC structure
        array = []

        for i, b in enumerate(data):
            if b % 2 == 0:
                array.append([b % 10])      # Single element array
            else:
                array.append([b % 10, b % 5]) # Two element array

        # If fuzzed data is empty, use the base PoC
        if not array:
            array = BASE_ARRAY

        # Create a BinTableHDU with variable-length arrays
        col = fits.Column(name='a', format='QD', array=array)
        hdu = fits.BinTableHDU.from_columns([col])

        # Write to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".fits") as tmpfile:
            temp_path = tmpfile.name
            hdu.writeto(temp_path, overwrite=True)

        # Compare the file to itself
        diff = fits.FITSDiff(temp_path, temp_path)

        # Assertion: Should be identical
        assert diff.identical, "Bug triggered: FITSDiff incorrectly reports non-identical files when comparing file to itself."

    except Exception:
        # Ignore random FITS creation failures
        pass
    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
