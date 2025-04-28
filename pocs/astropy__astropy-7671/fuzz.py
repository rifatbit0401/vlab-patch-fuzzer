import atheris
import sys
from types import ModuleType
from astropy.utils.introspection import minversion

# Set up the test module (constant target)
test_module = ModuleType("test_module")
test_module.__version__ = '0.12.2'

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    try:
        # Consume fuzzed data as a "required version" string
        required_version = fdp.ConsumeUnicodeNoSurrogates(30)  # limit size so it's manageable
        # print(required_version)
        # Call minversion with the fuzzed required version
        result = minversion(test_module, required_version)
        
        # Make sure the result is boolean
        assert isinstance(result, bool), f"minversion returned non-bool: {result}"
        print("okay")
    except (ValueError, TypeError):
        # Acceptable exceptions if required_version is invalid
        pass
    except Exception as e:
        # Unexpected crash → interesting
        print("unexpected crash")
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
