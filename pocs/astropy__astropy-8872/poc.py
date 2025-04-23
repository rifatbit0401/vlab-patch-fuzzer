import numpy as np
from astropy import units as u

# Create an array with a specific dtype
arr = np.array([1, 2, 3], dtype=np.float16)

# Wrap it as a Quantity
q = arr * u.km

# Check if the dtype is preserved
print("Original dtype:", arr.dtype)
print("Quantity dtype:", q.dtype)

# Assertion to verify fix
assert q.dtype == np.float16, f"Expected dtype float16, but got {q.dtype}"
