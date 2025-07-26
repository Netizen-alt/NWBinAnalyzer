# การแก้ไขปัญหา (Troubleshooting)

🔧 คู่มือแก้ไขปัญหาและข้อผิดพลาดที่อาจเกิดขึ้นขณะใช้งาน NWBinAnalyzer

## 🚨 ปัญหาที่พบบ่อย

### 1. ไฟล์ไม่ใช่ NW.js Binary
```
Error: Not a valid NW.js .bin file.
```

**สาเหตุ**:
- ไฟล์ไม่มี magic header ที่ถูกต้อง (`8e 06 de c0`)
- ไฟล์เสียหายหรือไม่สมบูรณ์
- ไฟล์เป็น format อื่นที่ไม่ใช่ NW.js

**วิธีแก้ไข**:
```bash
# ตรวจสอบ magic header
hexdump -C file.bin | head -1

# ควรเห็น: 8e 06 de c0 ที่ตำแหน่งเริ่มต้น
00000000  8e 06 de c0 ...
```

**การแก้ไข**:
1. ตรวจสอบว่าไฟล์ถูกต้อง
2. ลองกับไฟล์ .bin อื่นๆ
3. ตรวจสอบว่าไฟล์ไม่เสียหาย

### 2. Python Version ไม่รองรับ
```
SyntaxError: invalid syntax
```

**สาเหตุ**: ใช้ Python เวอร์ชันที่เก่าเกินไป

**วิธีแก้ไข**:
```bash
# ตรวจสอบเวอร์ชัน Python
python --version
python3 --version

# ต้องเป็น Python 3.6 หรือใหม่กว่า
```

### 3. ไม่พบ Strings
```
[+] All extracted strings (0):
```

**สาเหตุ**:
- ไฟล์มี strings น้อยมาก
- Strings ถูก obfuscate หรือ encode
- ไฟล์เป็น bytecode ที่ไม่มี constant pool

**วิธีแก้ไข**:
```python
# ลด min_length เพื่อหา strings สั้นๆ
extracted_strings = extract_strings_from_binary(data, min_length=2)

# ดู hex dump เพื่อหาข้อมูล
print(f"Hex dump: {data[:100].hex()}")
```

### 4. Unicode/Encoding Errors
```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**สาเหตุ**: Binary data ที่ไม่ใช่ valid UTF-8

**วิธีแก้ไข**: โปรแกรมจัดการอัตโนมัติแล้ว แต่ถ้ายังเกิดปัญหา:
```python
try:
    decoded = data.decode('utf-8')
except UnicodeDecodeError:
    # ลองใช้ encoding อื่น
    for encoding in ['latin-1', 'cp1252', 'ascii']:
        try:
            decoded = data.decode(encoding)
            break
        except:
            continue
```

### 5. Memory Error (ไฟล์ใหญ่เกินไป)
```
MemoryError: cannot allocate memory
```

**สาเหตุ**: ไฟล์มีขนาดใหญ่เกินไป

**วิธีแก้ไข**:
```python
# อ่านไฟล์ทีละส่วน
def process_large_file(filepath, chunk_size=1024*1024):
    with open(filepath, 'rb') as f:
        # อ่าน header ก่อน
        header = f.read(4)
        if header != b'\x8e\x06\xde\xc0':
            return
        
        # อ่านทีละ chunk
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            process_chunk(chunk)
```

## 🔍 การ Debug และวินิจฉัย

### 1. เปิด Verbose Mode
เพิ่มการ print debug information:
```python
def decompile_bin(filepath, verbose=False):
    if verbose:
        print(f"[DEBUG] Opening file: {filepath}")
        print(f"[DEBUG] File size: {os.path.getsize(filepath)} bytes")
    # ...existing code...
```

### 2. ตรวจสอบ Binary Structure
```python
def analyze_file_structure(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    print(f"First 16 bytes: {data[:16].hex()}")
    print(f"Last 16 bytes: {data[-16:].hex()}")
    
    # หา pattern ที่น่าสนใจ
    printable_count = sum(1 for b in data if 32 <= b <= 126)
    print(f"Printable bytes: {printable_count}/{len(data)} ({printable_count/len(data)*100:.1f}%)")
```

### 3. Step-by-step Analysis
```python
def debug_constant_pool(data):
    offset = 4  # ข้าม magic header
    
    try:
        const_count, offset = read_varint(data, offset)
        print(f"[DEBUG] Constant count: {const_count}")
        
        for i in range(min(const_count, 10)):  # แสดงแค่ 10 อันแรก
            length, offset = read_varint(data, offset)
            const_data = data[offset:offset+length]
            print(f"[DEBUG] Entry {i}: length={length}, data={const_data[:20].hex()}...")
            offset += length
            
    except Exception as e:
        print(f"[DEBUG] Error at offset {offset}: {e}")
```

## 🛠️ เครื่องมือเพิ่มเติม

### 1. Hex Editor
```bash
# Ubuntu/Debian
sudo apt install hexedit

# macOS
brew install hexedit

# Windows
# ใช้ HxD หรือ 010 Editor
```

### 2. File Analysis
```bash
# ตรวจสอบประเภทไฟล์
file file.bin

# ดู strings ที่มีอยู่
strings file.bin

# ดู hex dump
hexdump -C file.bin | head -20
```

### 3. Python Debug Tools
```python
import pdb

def debug_function():
    pdb.set_trace()  # breakpoint
    # code ที่ต้องการ debug
```

## 📋 Checklist การแก้ปัญหา

### เมื่อเกิดปัญหาใหม่
- [ ] ตรวจสอบ Python version (>= 3.6)
- [ ] ตรวจสอบไฟล์มีอยู่จริงและอ่านได้
- [ ] ตรวจสอบ magic header ของไฟล์
- [ ] ลองกับไฟล์ทดสอบอื่น
- [ ] เปิด verbose/debug mode
- [ ] ตรวจสอบ error message อย่างละเอียด

### เมื่อผลลัพธ์ไม่ตรงคาดหวัง
- [ ] ตรวจสอบ min_length setting
- [ ] ลองเปลี่ยน encoding
- [ ] ดู binary data โดยตรง
- [ ] เปรียบเทียบกับเครื่องมืออื่น

## 🆘 การขอความช่วยเหลือ

### ข้อมูลที่ควรรวบรวม
1. **Python version**: `python --version`
2. **OS information**: Windows/Linux/macOS version
3. **File information**: ขนาดไฟล์, แหล่งที่มา
4. **Error message**: คัดลอกทั้งหมด
5. **Command used**: คำสั่งที่ใช้รัน
6. **Expected vs Actual**: ผลลัพธ์ที่คาดหวัง vs ได้จริง

### รูปแบบการรายงานปัญหา
```
**Environment:**
- Python: 3.8.5
- OS: Windows 10
- File size: 2.1 MB

**Command:**
python app.py target.bin

**Error:**
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff

**Expected:**
Should extract strings successfully

**Additional info:**
File obtained from NW.js app version 0.50.0
```

## 💡 เคล็ดลับการใช้งาน

### 1. การทดสอบไฟล์ใหม่
```bash
# ลองกับไฟล์ตัวอย่างก่อน
python app.py examples/test_simple.bin

# ถ้าทำงาน แล้วค่อยลองไฟล์จริง
python app.py your_file.bin
```

### 2. การเปรียบเทียบผลลัพธ์
```bash
# บันทึกผลลัพธ์
python app.py file.bin > output.txt

# เปรียบเทียบกับ strings command
strings file.bin > strings_output.txt
diff output.txt strings_output.txt
```

### 3. การ Backup
```bash
# สำรองไฟล์ก่อนวิเคราะห์
cp original.bin backup.bin
```

---

**หมายเหตุ**: หากยังแก้ปัญหาไม่ได้ ให้ตรวจสอบเอกสารอื่นๆ หรือสร้าง issue ใน repository