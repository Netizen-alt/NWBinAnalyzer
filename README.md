# NWBinAnalyzer - เครื่องมือวิเคราะห์ไฟล์ NW.js Binary

**NWBinAnalyzer** เป็นเครื่องมือ Python สำหรับวิเคราะห์และแยกข้อความที่อ่านได้จากไฟล์ binary ที่คอมไพล์แล้วของ NW.js (.bin) เครื่องมือนี้ช่วยให้นักวิจัยด้านความปลอดภัยและผู้ที่ต้องการศึกษาโครงสร้างของแอปพลิเคชัน NW.js สามารถเข้าใจเนื้อหาของไฟล์ที่คอมไพล์แล้วได้ง่ายขึ้น

## 🏷️ ชื่อโปรเจค
**NWBinAnalyzer** (NW.js Binary Analyzer)
- **NW** = NW.js Framework
- **Bin** = Binary File
- **Analyzer** = เครื่องมือวิเคราะห์

## 🎯 วัตถุประสงค์การศึกษา

**⚠️ คำเตือน: เครื่องมือนี้ถูกพัฒนาขึ้นเพื่อการศึกษาและการวิจัยเท่านั้น**

- เรียนรู้โครงสร้างไฟล์ binary ของ NW.js
- ศึกษาการทำงานของ V8 JavaScript Engine
- วิเคราะห์การเข้ารหัสและการจัดเก็บข้อมูลใน constant pool
- เข้าใจการทำงานของระบบ packaging ในแอปพลิเคชัน desktop

## ✨ ความสามารถหลัก

### 🔍 **การแยกข้อความ (String Extraction)**
- ถอดรหัสข้อความ UTF-8 โดยตรง
- ตรวจหาข้อความที่ลงท้ายด้วย null terminator
- แยกข้อความที่มี length prefix (1, 2, และ 4 ไบต์)
- ตรวจหา Base64 encoded strings
- ตรวจหา Hexadecimal encoded strings
- วิเคราะห์รูปแบบของข้อมูล binary

### 📊 **การวิเคราะห์อัจฉริยะ**
- **การจัดหมวดหมู่**: แบ่งประเภทข้อความที่พบตามวัตถุประสงค์:
  - การเรียกใช้ API และฟังก์ชัน
  - เส้นทางไฟล์และทรัพยากร
  - URL และ network endpoints
  - การดำเนินการเข้ารหัส
  - โมดูล Node.js
  - ข้อความแสดงข้อผิดพลาด
  - ข้อความน่าสงสัย
  - รหัสสั้นๆ (อาจเป็นการปกปิด)

### 🔗 **การวิเคราะห์ความสัมพันธ์**
- หาความเชื่อมโยงระหว่างข้อความต่างๆ
- ตรวจหาข้อความที่มี prefix หรือ suffix คล้ายกัน
- วิเคราะห์ความสัมพันธ์เชิงโครงสร้าง

### 🎯 **การระบุฟังก์ชันการทำงาน**
- 🌐 การสื่อสารผ่านเครือข่าย (HTTP requests)
- 🔐 การดำเนินการเข้ารหัส
- 📁 การจัดการระบบไฟล์
- ⚙️ Worker threads และการประมวลผลเบื้องหลัง
- ✅ การตรวจสอบความถูกต้องของโค้ดและข้อมูล
- 📥 การดาวน์โหลดและอัปโหลดไฟล์
- 📝 ระบบ logging
- 🔄 ฟังก์ชัน auto-update
- ⚠️ การตรวจสอบความปลอดภัยและป้องกันการแก้ไข

## 🛠 การติดตั้ง

### ความต้องการระบบ
- Python 3.6 หรือใหม่กว่า
- ไม่ต้องติดตั้ง library เพิ่มเติม (ใช้ standard library เท่านั้น)

### ขั้นตอนการติดตั้ง
1. **ดาวน์โหลดโค้ด**
   ```bash
   git clone https://github.com/Netizen-alt/NWBinAnalyzer.git
   cd NWBinAnalyzer
   ```

2. **ตรวจสอบ Python version**
   ```bash
   python --version
   # หรือ
   python3 --version
   ```

3. **ทดสอบการทำงาน**
   ```bash
   python app.py --help
   ```

## 🚀 วิธีการใช้งาน

### การใช้งานพื้นฐาน
```bash
python app.py <ไฟล์.bin>
```

### ตัวอย่างการใช้งาน
```bash
# วิเคราะห์ไฟล์ binary
python app.py _bac_logic.bin

# วิเคราะห์ไฟล์หลายๆ ไฟล์
python app.py file1.bin
python app.py file2.bin
```

### ตัวอย่างผลลัพธ์
```
[+] Magic Header OK: 8e06dec0
[+] Constant Pool Entries: 28

[00] Length: 79
     Binary data (79 bytes):
       Magic bytes: 1cccf146
       Unique bytes: 45/256

[13] Length: 129
     Extracted strings: ['createHash']

[+] String Analysis:

  📋 API CALLS (15):
    - 'createHash'
    - 'readFileSync'
    - 'writeRequestBody'
    - 'verifySignature'
    ...

  📋 CRYPTO RELATED (8):
    - 'RSA-SHA256'
    - 'aes-128-gcm'
    - 'sha'
    ...

[+] Detected Functionality:
  🌐 Network communication (HTTP requests)
  🔐 Cryptographic operations
  📁 File system operations
  ✅ Code/data verification
```

## 📁 โครงสร้างไฟล์

```
NWBinAnalyzer/
├── app.py              # ไฟล์หลักของเครื่องมือ
├── README.md           # คู่มือการใช้งาน (ไฟล์นี้)
├── examples/           # ตัวอย่างไฟล์ทดสอบ
├── docs/              # เอกสารเพิ่มเติม
└── LICENSE            # ใบอนุญาตการใช้งาน
```

## 🔧 ฟังก์ชันหลักของโค้ด

### `read_varint(data, offset)`
อ่านค่า variable-length integer จาก binary data (รูปแบบที่ V8 ใช้)

### `extract_strings_from_binary(data, min_length=3)`
แยกข้อความที่อ่านได้จาก binary data ด้วยวิธีต่างๆ

### `analyze_binary_structure(data)`
วิเคราะห์โครงสร้างของ binary data เพื่อหารูปแบบและคุณสมบัติ

### `categorize_strings(strings)`
จัดหมวดหมู่ข้อความที่พบตามวัตถุประสงค์การใช้งาน

### `find_string_relationships(strings)`
หาความสัมพันธ์และการเชื่อมโยงระหว่างข้อความต่างๆ

### `analyze_functionality(strings)`
วิเคราะห์ฟังก์ชันการทำงานของโปรแกรมจากข้อความที่พบ

## 🎓 ข้อมูลทางเทคนิคสำหรับการศึกษา

### รูปแบบไฟล์ NW.js .bin
- **Magic Header**: `8e 06 de c0` (4 ไบต์แรก)
- **Constant Pool Count**: Variable-length integer
- **Constant Pool Entries**: แต่ละ entry มี length และ data

### การเข้ารหัส Variable-length Integer (Varint)
- ใช้ 7 บิตต่อไบต์สำหรับข้อมูล
- บิตที่ 8 เป็น continuation bit
- Little-endian byte order

### รูปแบบการจัดเก็บข้อความ
1. **Null-terminated strings**: ลงท้ายด้วย `\0`
2. **Length-prefixed strings**: มี length อยู่ข้างหน้า
3. **Raw UTF-8 sequences**: ข้อความ UTF-8 โดยตรง

## ⚠️ ข้อจำกัดและข้อควรทราบ

### ข้อจำกัด
- เครื่องมือนี้แสดงเฉพาะ constant pool strings เท่านั้น
- ไม่สามารถ decompile V8 bytecode ได้อย่างสมบูรณ์
- อาจมีข้อความบางส่วนที่แยกไม่ได้เนื่องจากการเข้ารหัสพิเศษ

### การใช้งานที่เหมาะสม
- การวิเคราะห์เพื่อความปลอดภัย
- การศึกษาโครงสร้างแอปพลิเคชัน
- การวิจัยด้าน reverse engineering
- การเรียนรู้เทคโนโลยี V8 และ NW.js

## 🔍 ตัวอย่างการวิเคราะห์

เมื่อเครื่องมือพบข้อความเหล่านี้ในไฟล์:
- `createHash`, `verifySignature` → ระบบเข้ารหัส
- `readFileSync`, `writeRequestBody` → การจัดการไฟล์
- `https://`, `fetch` → การสื่อสารเครือข่าย
- `sussy`, `verification failed` → ระบบตรวจสอบความปลอดภัย

## 📚 แหล่งข้อมูลเพิ่มเติม

- [NW.js Documentation](https://nwjs.io/)
- [V8 JavaScript Engine](https://v8.dev/)
- [Node.js Binary Formats](https://nodejs.org/)

## 📄 สิทธิ์การใช้งาน

**NWBinAnalyzer** พัฒนาขึ้นเพื่อการศึกษาเท่านั้น กรุณาใช้งานอย่างมีจริยธรรมและเคารพสิทธิ์ของผู้อื่น

### การอ้างอิง
หากคุณใช้งาน NWBinAnalyzer ในงานวิจัยหรือโปรเจค กรุณาอ้างอิงดังนี้:
```
NWBinAnalyzer - NW.js Binary File Analyzer
เครื่องมือวิเคราะห์ไฟล์ Binary ของ NW.js เพื่อการศึกษา
```
