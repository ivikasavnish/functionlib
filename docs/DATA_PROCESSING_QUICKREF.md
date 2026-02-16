# Data Processing Module - Quick Reference

**32 functions for compression, encoding, serialization, and data transformation**

---

## Compression (8 functions)

```python
from functionlib.coding.data_processing import *

# Gzip compression
compressed = gzip_compress(b"data", compression_level=9)
original = gzip_decompress(compressed)

# Zlib compression
compressed = zlib_compress(b"data", level=9)
original = zlib_decompress(compressed)

# Bz2 compression
compressed = bz2_compress(b"data", compression_level=9)
original = bz2_decompress(compressed)

# String compression (auto-encoding)
compressed = compress_string("text data", method='gzip')  # or 'zlib', 'bz2'
text = decompress_string(compressed, method='gzip')
```

---

## Encoding (6 functions)

```python
# Base64
encoded = base64_encode(b"Hello")  # 'SGVsbG8='
decoded = base64_decode(encoded)   # b'Hello'

# Hex encoding
hex_str = hex_encode(b"Test")      # '54657374'
decoded = hex_decode(hex_str)       # b'Test'

# URL-safe base64
safe_encoded = url_safe_base64_encode(b"data>>")
decoded = url_safe_base64_decode(safe_encoded)
```

---

## Serialization (4 functions)

```python
# Pickle serialization
obj = {'key': 'value', 'nums': [1, 2, 3]}
serialized = serialize_object(obj)
restored = deserialize_object(serialized)

# JSON
json_str = to_json_string(obj, pretty=True)
parsed = from_json_string(json_str)
```

---

## CSV Processing (4 functions)

```python
# CSV to dictionaries
csv_data = "name,age\nJohn,30\nJane,25"
dicts = csv_to_dict_list(csv_data)
# [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]

# Dictionaries to CSV
csv_str = dict_list_to_csv(dicts)

# CSV to rows (list of lists)
rows = csv_to_rows(csv_data)
# [['name', 'age'], ['John', '30'], ['Jane', '25']]

# Rows to CSV
csv_str = rows_to_csv(rows)
```

---

## Binary Data (6 functions)

```python
# Pack/unpack integers
nums = [1, 2, 3, 4, 5]
packed = pack_integers(nums, format_char='i')  # 'i'=int, 'h'=short, 'q'=long
unpacked = unpack_integers(packed, format_char='i')

# Bytes to/from hex
hex_str = bytes_to_hex(b"\x01\x02\x03")           # '010203'
hex_str = bytes_to_hex(b"\x01\x02\x03", ':')      # '01:02:03'
data = hex_to_bytes('01:02:03')                    # handles separators

# Checksums
checksum = calculate_checksum(b"data", algorithm='md5')  # or 'sha1', 'sha256'
valid = verify_checksum(b"data", checksum, algorithm='md5')
```

---

## Data Transformation (4 functions)

```python
# Flatten nested dict
nested = {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
flat = flatten_dict(nested, separator='.')
# {'a.b.c': 1, 'a.b.d': 2, 'e': 3}

# Unflatten
restored = unflatten_dict(flat, separator='.')
# {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}

# Merge dictionaries
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
merged = merge_dicts(d1, d2)              # {'a': 1, 'b': 3, 'c': 4}
merged = merge_dicts(d1, d2, deep=True)   # deep merge for nested dicts

# Deep copy
copy = deep_copy_dict(original)
```

---

## Common Use Cases

### Compress and encode data for storage
```python
# Compress and base64 encode
data = "Large text data " * 1000
compressed = compress_string(data, method='gzip')
encoded = base64_encode(compressed)
# Store or transmit encoded

# Decode and decompress
compressed = base64_decode(encoded)
original = decompress_string(compressed, method='gzip')
```

### Configuration file processing
```python
# Save config with checksum
config = {'setting1': 'value1', 'setting2': 42}
json_str = to_json_string(config)
checksum = calculate_checksum(json_str.encode(), 'sha256')

# Later: verify and load
if verify_checksum(json_str.encode(), checksum, 'sha256'):
    config = from_json_string(json_str)
```

### CSV data processing
```python
# Read CSV, process, write back
csv_data = "name,score\nAlice,95\nBob,87"
records = csv_to_dict_list(csv_data)

# Process data
for record in records:
    record['grade'] = 'A' if int(record['score']) >= 90 else 'B'

# Write back
output_csv = dict_list_to_csv(records)
```

### Binary protocol handling
```python
# Pack data for network transmission
values = [12, 34, 56, 78]
packed = pack_integers(values, format_char='i')
hex_repr = bytes_to_hex(packed, ':')

# Later: receive and unpack
data = hex_to_bytes(hex_repr)
values = unpack_integers(data, format_char='i')
```

### Flatten for NoSQL storage
```python
# Flatten nested config for key-value store
config = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'credentials': {'user': 'admin', 'pass': 'secret'}
    }
}

flat = flatten_dict(config)
# Store each key-value pair separately
# 'database.host': 'localhost'
# 'database.port': 5432
# 'database.credentials.user': 'admin'
# etc.

# Later: restore structure
config = unflatten_dict(flat)
```

---

## Performance Tips

- **Compression**: `gzip` (slower, better ratio) vs `zlib` (faster) vs `bz2` (best ratio, slowest)
- **Level 9**: Maximum compression, slower
- **Level 1**: Fast compression, larger output
- **Base64**: Increases size by ~33%
- **Pickle**: Fast but Python-specific
- **JSON**: Slower but language-agnostic

---

*Part of FunctionLib - 1021 functions, zero dependencies*
