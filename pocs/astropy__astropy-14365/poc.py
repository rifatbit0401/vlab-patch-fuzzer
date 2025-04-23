from astropy.io import ascii
from io import StringIO

qdp_content = """
REaD SERR 1 2
NO NO NO NO
1 1.0 0.1 2.0 0.2
2 2.0 0.1 3.0 0.2
"""

try:
    table = ascii.read(qdp_content, format='qdp')
except Exception as e:
    print("Unexpected error:", e)
else:
    print("✅ Table parsed successfully:")
    print(table)
