import atheris
import sys
from astropy.io import fits

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    # Generate a random-length string consisting of printable ASCII characters
    random_str = fdp.ConsumeUnicodeNoSurrogates(100)  # limit max size to 100 for efficiency
    
    # Append two single quotes to simulate the bug condition
    value = random_str + "''"
    
    try:
        card = fits.Card('TESTKEY', value)
        reconstructed_card = fits.Card.fromstring(str(card))
        
        # Assertion: Reconstructed value must match original value
        assert card.value == reconstructed_card.value, (
            f"Mismatch!\nOriginal:      {repr(card.value)}\n"
            f"Reconstructed: {repr(reconstructed_card.value)}"
        )
        
    except AssertionError:
        print("Asserion Violation")
    except Exception:
        # Ignore any non-interesting exceptions (e.g., if input is malformed)
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
