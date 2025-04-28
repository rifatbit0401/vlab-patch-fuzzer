from astropy.io import ascii
import astropy.units as u

# Directly reading the same text as in the GitHub issue
table = ascii.read("""
Title:
Authors:
Journal-ref:
Comments:
===========================================================================
Byte-by-byte Description of file: table1.dat
---------------------------------------------------------------------------
   1-  7  F7.3   ---    Frequency  Observed Frequency (GHz)
   9- 13  F5.1   ---    SNR        Signal to Noise Ratio
  15- 21  F7.3   10+3J/m/s/kpc2    Fint      Integrated Flux (10^3 Jy km/s kpc2)
---------------------------------------------------------------------------
 115.271  16.0    1.23
 230.538  10.0    2.34
""", format='cds')

# Print the parsed unit for the 'Fint' column
print("Parsed unit:", table['Fint'].unit)

# Expected unit if parsed correctly
expected_unit = (10**3) * u.J / u.m / u.s / u.kpc**2

# Assertion to trigger bug
assert table['Fint'].unit == expected_unit, "Bug triggered: Incorrect unit parsing!"
