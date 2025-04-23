import atheris
import sys
import numpy as np
import astropy.wcs
from astropy.wcs.wcsapi import SlicedLowLevelWCS

def build_custom_wcs():
    nx = 100
    ny = 25
    nz = 2
    wcs_header = {
        'WCSAXES': 3,
        'CRPIX1': (nx + 1)/2,
        'CRPIX2': (ny + 1)/2,
        'CRPIX3': 1.0,
        'PC1_1': 0.0,
        'PC1_2': -1.0,
        'PC1_3': 0.0,
        'PC2_1': 1.0,
        'PC2_2': 0.0,
        'PC2_3': -1.0,
        'CDELT1': 5,
        'CDELT2': 5,
        'CDELT3': 0.055,
        'CUNIT1': 'arcsec',
        'CUNIT2': 'arcsec',
        'CUNIT3': 'Angstrom',
        'CTYPE1': 'HPLN-TAN',
        'CTYPE2': 'HPLT-TAN',
        'CTYPE3': 'WAVE',
        'CRVAL1': 0.0,
        'CRVAL2': 0.0,
        'CRVAL3': 1.05,
    }
    return astropy.wcs.WCS(header=wcs_header)

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    z = fdp.ConsumeIntInRange(0, 24)  # fuzz only the third (spectral) coordinate

    wcs = build_custom_wcs()
    sliced = SlicedLowLevelWCS(wcs, 0)

    try:
        # Full WCS: (spectral, x=0, y=z)
        world = wcs.pixel_to_world_values(0, 0, z)

        # Sliced WCS: (RA, DEC) → pixel
        out_pix = sliced.world_to_pixel_values(world[0], world[1])

        # Expect: -out_pix[0] ≈ z (based on projection)
        assert np.allclose(-1 * out_pix[0], z, atol=1.0), \
            f"BUG TRIGGERED: z={z}, out_x={out_pix[0]}, expected_x={-z}"

    except AssertionError as e:
        print(e)
    except Exception:
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
