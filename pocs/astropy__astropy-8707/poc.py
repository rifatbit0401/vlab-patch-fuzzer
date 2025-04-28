from astropy.io import fits

# Step 1: Create a FITS header in bytes (not str)
header_bytes = b"SIMPLE  =                    T / Standard FITS format\nEND\n"

# Step 2: Try to parse using Header.fromstring()
hdr = fits.Header.fromstring(header_bytes)

# Step 3: Assert that the header parsed correctly
assert isinstance(hdr, fits.Header), "Header.fromstring() failed to parse bytes input correctly"

# Optional: assert that SIMPLE keyword is set correctly
assert hdr['SIMPLE'] is True, "Parsed header missing expected SIMPLE keyword"
