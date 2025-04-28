import sys
from astropy.table import QTable
import astropy.units as u

# Create a simple QTable with units
tbl = QTable({
    'wave': [350, 950] * u.nm,
    'response': [0.7, 1.2] * u.count
})

# Attempt to write the table using ascii.rst with multiple header rows
try:
    tbl.write(sys.stdout, format="ascii.rst", header_rows=["name", "unit"])
except Exception as e:
    print("\n\n--- Bug Triggered ---")
    print(f"Exception: {type(e).__name__}: {e}")
    print("----------------------")
