# pycparse
Small library to parse .pyc files structure (works with python 3)
# Example
```python
import pyc
my_pyc_bytes = b"..."
header = pyc.PycHeader()
# Max header size - 16, if header smaller excess bytes will be ignored
header.analyze_header(my_pyc_bytes[:16])
print(f"Python version: {".".join(header.get_magic())}") # Return example: (3, 12)
# other fields (you need to make decision to use them by the version by yourself)
header.timestamp
header.bitfield
header.hash_val
header.filesize
# *Imagine some work with this values*
# Get code object by header
pyc.get_code_info(my_pyc_bytes, header)
# Getting header back in bytes
my_header = header.get_header()
```
That's all lol
