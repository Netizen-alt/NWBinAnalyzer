# อัลกอริทึมการแยก String

🔍 เอกสารอธิบายวิธีการและอัลกอริทึมที่ใช้ในการแยก strings จาก binary data

## 🎯 ภาพรวมการทำงาน

NWBinAnalyzer ใช้หลายเทคนิคในการแยก strings จาก binary data เพื่อให้ได้ผลลัพธ์ที่ครอบคลุมและแม่นยำที่สุด

```
Binary Data → Multiple Extraction Methods → String Collection → Deduplication → Final Results
```

## 🔧 วิธีการแยก String

### 1. Direct UTF-8 Decoding
**วัตถุประสงค์**: แยก strings ที่เป็น UTF-8 ตรงๆ

```python
try:
    decoded = const_data.decode('utf-8')
    if decoded.strip():
        strings.append(decoded)
except UnicodeDecodeError:
    # ล้มเหลว ไปใช้วิธีอื่น
    pass
```

**ข้อดี**:
- รวดเร็วและแม่นยำ
- รองรับ Unicode characters
- ไม่มี false positives

**ข้อเสีย**:
- ใช้ได้เฉพาะ valid UTF-8 data เท่านั้น

### 2. Null-terminated String Detection
**วัตถุประสงค์**: หา strings ที่ลงท้ายด้วย null byte (`\x00`)

```python
pattern = b'[\x20-\x7e]{3,}\x00'
matches = re.findall(pattern, data)
for match in matches:
    string = match[:-1].decode('utf-8')  # ตัด \x00 ออก
```

**Pattern Explanation**:
- `[\x20-\x7e]`: Printable ASCII characters (space ถึง ~)
- `{3,}`: อย่างน้อย 3 ตัวอักษร
- `\x00`: Null terminator

### 3. Length-prefixed String Extraction
**วัตถุประสงค์**: หา strings ที่มี length prefix

```python
for prefix_size in [1, 2, 4]:  # 1, 2, หรือ 4 bytes
    for i in range(len(data) - prefix_size):
        # อ่าน length
        if prefix_size == 1:
            length = data[i]
        elif prefix_size == 2:
            length = struct.unpack('<H', data[i:i+2])[0]
        else:
            length = struct.unpack('<I', data[i:i+4])[0]
        
        # ตรวจสอบว่า length สมเหตุสมผล
        if 1 <= length <= 500:
            string_data = data[i+prefix_size:i+prefix_size+length]
            # ลองแปลงเป็น string
```

**รูปแบบ Length-prefixed**:
```
┌─────────┬─────────────────┐
│ Length  │    String Data  │
│ (1-4B)  │   (Variable)    │
└─────────┴─────────────────┘
```

### 4. Consecutive Printable ASCII Detection
**วัตถุประสงค์**: หา sequences ของ printable ASCII characters

```python
ascii_pattern = re.compile(b'[\x20-\x7e]{3,}')
for match in ascii_pattern.finditer(data):
    decoded = match.group().decode('ascii')
```

**Character Range**:
- `\x20` (space) ถึง `\x7e` (~)
- รวม: ตัวอักษร, ตัวเลข, สัญลักษณ์

### 5. UTF-8 Sequence Detection
**วัตถุประสงค์**: หา UTF-8 sequences ที่ไม่มี delimiter ชัดเจน

```python
for start in range(len(data)):
    for end in range(start + 3, min(start + 100, len(data) + 1)):
        try:
            decoded = data[start:end].decode('utf-8')
            if all(c.isprintable() or c in '\n\r\t' for c in decoded):
                strings.append(decoded)
                break
        except UnicodeDecodeError:
            continue
```

### 6. Base64 Pattern Detection
**วัตถุประสงค์**: หา strings ที่ encode เป็น Base64

```python
base64_pattern = re.compile(b'[A-Za-z0-9+/]{8,}={0,2}')
for match in base64_pattern.finditer(data):
    try:
        decoded = base64.b64decode(match.group()).decode('utf-8')
        strings.append(f"base64:{decoded}")
    except:
        pass
```

### 7. Hexadecimal Pattern Detection
**วัตถุประสงค์**: หา strings ที่ encode เป็น hex

```python
hex_pattern = re.compile(b'[0-9a-fA-F]{6,}')
for match in hex_pattern.finditer(data):
    if len(match.group()) % 2 == 0:
        try:
            hex_bytes = bytes.fromhex(match.group().decode('ascii'))
            decoded = hex_bytes.decode('utf-8')
            strings.append(f"hex:{decoded}")
        except:
            pass
```

## 📊 การกรองและทำความสะอาด

### Minimum Length Filtering
```python
min_length = 3  # อย่างน้อย 3 ตัวอักษร
if len(decoded) >= min_length:
    strings.append(decoded)
```

### Character Validation
```python
def is_valid_string(s):
    return all(c.isprintable() or c in '\n\r\t' for c in s)
```

### Deduplication
```python
unique_strings = list(set(strings))  # ลบของซ้ำ
```

## 🎛️ การปรับแต่งพารามิเตอร์

### ความยาวขั้นต่ำ (min_length)
```python
# สำหรับ strings ทั่วไป
min_length = 3

# สำหรับ function names และ identifiers
min_length = 2

# สำหรับ error messages และ descriptions
min_length = 5
```

### ขอบเขตการค้นหา
```python
# ขอบเขตสำหรับ UTF-8 detection
max_string_length = 100

# ขอบเขตสำหรับ length-prefixed strings
max_prefix_length = 500
```

## 🔍 การวิเคราะห์คุณภาพ

### Precision vs Recall
```
Precision = True Positives / (True Positives + False Positives)
Recall = True Positives / (True Positives + False Negatives)
```

### การประเมินผล
1. **True Positives**: Strings ที่แยกออกมาถูกต้อง
2. **False Positives**: Binary data ที่แปลงเป็น string ผิดๆ
3. **False Negatives**: Strings ที่มีอยู่แต่แยกไม่ออก

## ⚡ การเพิ่มประสิทธิภาพ

### 1. Early Termination
```python
if len(decoded) >= min_length:
    strings.append(decoded)
    break  # หยุดการค้นหาต่อ
```

### 2. Caching Results
```python
string_cache = {}
if data_hash in string_cache:
    return string_cache[data_hash]
```

### 3. Parallel Processing
```python
from multiprocessing import Pool

def extract_strings_parallel(data_chunks):
    with Pool() as pool:
        results = pool.map(extract_strings_from_binary, data_chunks)
    return flatten(results)
```

## 🧪 การทดสอบและ Validation

### Unit Tests
```python
def test_null_terminated():
    data = b'hello\x00world\x00'
    strings = extract_strings_from_binary(data)
    assert 'hello' in strings
    assert 'world' in strings
```

### Integration Tests
```python
def test_real_binary_file():
    with open('sample.bin', 'rb') as f:
        data = f.read()
    strings = extract_strings_from_binary(data)
    assert len(strings) > 0
```

## 📈 การปรับปรุงในอนาคต

### 1. Machine Learning Approach
- ใช้ ML models เพื่อระบุ string patterns
- Training บน datasets ของ known strings

### 2. Context-aware Extraction
- วิเคราะห์ context รอบๆ เพื่อเพิ่มความแม่นยำ
- ใช้ linguistic patterns

### 3. Format-specific Optimizations
- เพิ่มการรองรับ formats เฉพาะ
- Custom extractors สำหรับ different encodings

---

**หมายเหตุ**: อัลกอริทึมเหล่านี้ออกแบบมาเพื่อความครอบคลุม อาจมี trade-off ระหว่างความเร็วและความแม่นยำ
