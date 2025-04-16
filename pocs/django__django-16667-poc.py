import atheris
import sys
import datetime
from django import forms
from django.forms.widgets import SelectDateWidget
from django.conf import settings

# Minimal Django setup
if not settings.configured:
    settings.configure(USE_L10N=False)

def fuzz_value_from_datadict(y, m, d):
    widget = SelectDateWidget()
    data = {
        'my_date_year': str(y),
        'my_date_month': str(m),
        'my_date_day': str(d),
    }
    print(f"Trying: {data}")
    print(widget.value_from_datadict(data, files=None, name='my_date'))

def to_big_int(b):
    try:
        return int.from_bytes(b, byteorder="big", signed=False)
    except:
        return 0

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    # Fuzz arbitrary-length bytes → convert to int (for year)
    year_bytes = fdp.ConsumeBytes(12)  # up to 96-bit number
    y = to_big_int(year_bytes)

    # Month and Day as normal ints
    m = fdp.ConsumeIntInRange(1, 12)
    d = fdp.ConsumeIntInRange(1, 31)

    try:
        fuzz_value_from_datadict(y, m, d)
    except OverflowError as e:
        sys.stderr.write(f"🔥 OverflowError: {e}\n")
        raise
    except Exception:
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
