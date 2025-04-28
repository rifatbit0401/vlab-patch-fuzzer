import atheris
import sys
from astropy.io import fits

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    try:
        # Try interpreting the input bytes as a FITS header
        hdr = fits.Header.fromstring(fdp.ConsumeBytes(len(data)))
        
        # Optional: check some property if parsing succeeds
        if not isinstance(hdr, fits.Header):
            raise AssertionError("Parsed object is not a Header instance!")
        
        # Optional: Try accessing a field (if exists)
        if 'SIMPLE' in hdr:
            _ = hdr['SIMPLE']
            
    except (TypeError, ValueError, OSError):
        # Expected kinds of exceptions on broken input
        pass
    except Exception as e:
        # Unexpected exceptions — these are interesting
        raise

def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
