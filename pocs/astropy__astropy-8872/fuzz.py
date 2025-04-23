import atheris
import sys
import numpy as np
from astropy import units as u

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    try:
        # Randomly select a dtype from lower-precision floating types
        dtypes = [np.float16, np.float32, np.int8, np.int16]
        chosen_dtype = fdp.PickValueInList(dtypes)

        # Generate an array of length 3 with the chosen dtype
        arr = np.array(
            fdp.ConsumeFloatListInRange(3,1,100)if np.issubdtype(chosen_dtype, np.floating)
            else fdp.ConsumeIntListInRange(3, 1, 1000), dtype=chosen_dtype)
        print(arr)
        # Wrap into Quantity
        q = u.Quantity(arr, unit=u.km)
        if chosen_dtype == np.float16 or chosen_dtype == np.float32:
            assert q.dtype == chosen_dtype
        else:
            assert q.dtype == np.float64
            
        # Assertion: the dtype must be preserved (fixed in PR #8872)
        # if q.dtype != chosen_dtype:
            # raise RuntimeError(f"BUG: Quantity changed dtype from {chosen_dtype} to {q.dtype}")
        print("No Violation")
    except AssertionError:
        print("Assertion Violation")
    except Exception as e:
        if "separable" in str(e):
            raise
        print(f"Unexpected error: {e}\n")   
    
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
