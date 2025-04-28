from astropy.io import fits

# Create a FITS file with a variable-length array (VLA)
col = fits.Column(name='a', format='QD', array=[[0], [0, 0]])
hdu = fits.BinTableHDU.from_columns([col])

# Write the FITS file to disk
hdu.writeto('diffbug.fits', overwrite=True)

# Compare the file to itself
diff = fits.FITSDiff('diffbug.fits', 'diffbug.fits')

# Assertion: We expect the files to be identical
assert diff.identical, "Bug triggered: FITSDiff reports non-identical files when comparing a file to itself!"
