import numpy as np
from astropy.modeling import models as m
from astropy.modeling.separable import separability_matrix

# # Flat model: All components combined directly
# flat_model = m.Pix2Sky_TAN() & m.Linear1D(10) & m.Linear1D(5)

# # Nested model: One compound model nested inside
# nested_linear = m.Linear1D(10) & m.Linear1D(5)
# nested_model = m.Pix2Sky_TAN() & nested_linear

# Compare separability matrices
flat_sep = separability_matrix(m.Linear1D(10) & m.Linear1D(5) & m.Linear1D(10) & m.Linear1D(5))
nested_sep = separability_matrix(m.Linear1D(10) & m.Linear1D(5) & (m.Linear1D(10) & m.Linear1D(5)))

# Generic assertion: the separability matrices should match
assert np.array_equal(flat_sep, nested_sep), (
    "\nBug triggered due to nested compound model!\n"
    "Flat model and nested model should have the same separability matrix.\n"
    f"Flat separability:\n{flat_sep}\n"
    f"Nested separability:\n{nested_sep}"
)
