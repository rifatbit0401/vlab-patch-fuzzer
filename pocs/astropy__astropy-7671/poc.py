from types import ModuleType
from astropy.utils.introspection import minversion

# Create a fake module
test_module = ModuleType("test_module")
test_module.__version__ = '0.12.2'  # Set a valid version

# Versions where test_module should satisfy (should return True)
good_versions = ['0.12', '0.12.1', '0.12.0.dev', '0.12dev']

# Versions where test_module should not satisfy (should return False)
bad_versions = ['1', '1.2rc1']

# Check good versions
for version in good_versions:
    assert minversion(test_module, version), f"Expected {test_module.__version__} >= {version}"

# Check bad versions
for version in bad_versions:
    assert not minversion(test_module, version), f"Expected {test_module.__version__} < {version}"

print("PoC passed: minversion() behaves correctly!")
