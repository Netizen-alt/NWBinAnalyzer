# รูปแบบไฟล์ NW.js Binary

📄 เอกสารอธิบายโครงสร้างและรูปแบบของไฟล์ .bin ที่ NW.js ใช้งาน

## 🏗️ โครงสร้างไฟล์โดยรวม

```
┌─────────────────┬──────────────────┬─────────────────┐
│   Magic Header  │  Constant Pool   │   Bytecode      │
│     (4 bytes)   │    Section       │   Section       │
└─────────────────┴──────────────────┴─────────────────┘
```

## 🔍 รายละเอียดแต่ละส่วน

### 1. Magic Header (4 bytes)
```
Offset: 0x00
Size: 4 bytes
Value: 8E 06 DE C0 (little-endian)
```

**วัตถุประสงค์**:
- ระบุว่าไฟล์เป็น NW.js binary
- ตรวจสอบความถูกต้องของรูปแบบไฟล์
- ป้องกันการเปิดไฟล์ผิดประเภท

### 2. Constant Pool Section

#### 2.1 Constant Pool Count
```
Offset: 0x04
Size: Variable (Varint encoding)
Purpose: จำนวน entries ใน constant pool
```

#### 2.2 Constant Pool Entries
แต่ละ entry มีโครงสร้าง:
```
┌─────────────┬─────────────────┐
│   Length    │      Data       │
│  (Varint)   │   (Variable)    │
└─────────────┴─────────────────┘
```

**ประเภทข้อมูลใน Constant Pool**:
- UTF-8 strings
- Function names
- Variable names
- Object properties
- Error messages
- Binary data (serialized objects)

### 3. Variable-length Integer (Varint) Encoding

**รูปแบบการเข้ารหัส**:
- ใช้ 7 บิตต่อไบต์สำหรับข้อมูล
- บิตที่ 8 (MSB) เป็น continuation bit
- `1` = มีไบต์ต่อไป, `0` = ไบต์สุดท้าย

**ตัวอย่าง**:
```
Value: 5
Binary: 00000101
Encoded: 05

Value: 128
Binary: 10000000 00000001
Encoded: 80 01

Value: 16384
Binary: 10000000 10000000 00000001
Encoded: 80 80 01
```

**อัลกอริทึมการอ่าน**:
```python
def read_varint(data, offset):
    value = 0
    shift = 0
    while True:
        byte = data[offset]
        value |= (byte & 0x7F) << shift
        offset += 1
        if byte < 0x80:
            break
        shift += 7
    return value, offset
```

## 📊 ตัวอย่างการวิเคราะห์ไฟล์

### ไฟล์ตัวอย่าง (hex dump):
```
Offset    Hex                              ASCII
00000000: 8e06 dec0 0548 656c 6c6f 0557  .....Hello.W
00000010: 6f72 6c64 0374 6573 74         orld.test
```

### การแปลความหมาย:
```
8e06 dec0           Magic header
05                  Varint: length = 5
48656c6c6f          UTF-8: "Hello"
05                  Varint: length = 5  
576f726c64          UTF-8: "World"
03                  Varint: length = 3
746573 74           UTF-8: "test"
```

## 🔐 ประเภทข้อมูลใน Constant Pool

### 1. String Literals
```
Type: UTF-8 encoded strings
Usage: Variable names, function names, string constants
Example: "require", "module", "exports"
```

### 2. Object Properties
```
Type: Property names and keys
Usage: Object member access
Example: "toString", "valueOf", "constructor"
```

### 3. Function Metadata
```
Type: Function signatures and names
Usage: Function declarations and calls
Example: "createHash", "readFileSync"
```

### 4. Error Messages
```
Type: Error strings and messages
Usage: Exception handling
Example: "Invalid signature", "File not found"
```

### 5. Binary Data
```
Type: Serialized objects or bytecode
Usage: Complex data structures
Example: Compiled bytecode, object graphs
```

## 🛠️ เครื่องมือวิเคราะห์

### การใช้ NWBinAnalyzer
```bash
python app.py target.bin
```

### การแยก String ด้วยตนเอง
```python
# อ่าน magic header
with open('file.bin', 'rb') as f:
    magic = f.read(4)
    if magic != b'\x8e\x06\xde\xc0':
        print("Invalid file format")
        
    # อ่าน constant count
    count_data = f.read(1)  # อาจต้องอ่านเพิ่ม
    count = decode_varint(count_data)
```

## ⚠️ ข้อจำกัดและข้อควรทราบ

### ข้อจำกัด
1. **Bytecode Section**: ไม่สามารถ decompile V8 bytecode ได้โดยตรง
2. **Obfuscation**: อาจมีการปกปิดหรือเข้ารหัสข้อมูล
3. **Version Compatibility**: รูปแบบอาจเปลี่ยนไปตามเวอร์ชัน NW.js

### ข้อควรระวัง
1. **Legal**: ตรวจสอบสิทธิ์ก่อนวิเคราะห์ไฟล์
2. **Security**: ไฟล์อาจมี malicious code
3. **Ethics**: ใช้เพื่อการศึกษาเท่านั้น

## 📚 แหล่งข้อมูลเพิ่มเติม

- [V8 Bytecode Format](https://v8.dev/docs/bytecode)
- [NW.js Documentation](https://nwjs.io/)
- [Binary File Analysis Techniques](https://en.wikipedia.org/wiki/Binary_file)

---

**หมายเหตุ**: ข้อมูลนี้จัดทำขึ้นจากการศึกษาและวิเคราะห์เพื่อการศึกษาเท่านั้น
