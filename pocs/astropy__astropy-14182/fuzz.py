import atheris
import sys
import io
import astropy.units as u
from astropy.table import QTable

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    # Guided fuzzing
    formats = ["ascii.fixed_width", "ascii.rst", "ascii.no_header", "ascii.commented_header"]
    if fdp.ConsumeBool():
        selected_format = "ascii.rst"
    else:
        selected_format = formats[fdp.ConsumeIntInRange(0, len(formats)-1)]

    # Create table (same)
    tbl = QTable({
        'wave': [350, 950] * u.nm,
        'response': [0.7, 1.2] * u.count
    })

    output_buffer = io.StringIO()  # ← Use StringIO, not /dev/null

    try:
        # Write to StringIO
        tbl.write(output_buffer, format=selected_format, header_rows=["name", "unit"])
    except TypeError as e:
        if selected_format == "ascii.rst":
            raise AssertionError(
                f"Bug triggered: ascii.rst format + header_rows caused {type(e).__name__}: {e}"
            )
    except Exception:
        # Ignore random exceptions
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
