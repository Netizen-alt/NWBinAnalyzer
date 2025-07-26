# Examples - ตัวอย่างการใช้งาน NWBinAnalyzer

โฟลเดอร์นี้มีตัวอย่างไฟล์และสคริปต์สำหรับทดสอบการทำงานของ NWBinAnalyzer

## 📁 ไฟล์ในโฟลเดอร์นี้

### ไฟล์ตัวอย่าง
- `sample.bin` - ไฟล์ binary ตัวอย่างสำหรับทดสอบ
- `test_simple.bin` - ไฟล์ binary ขนาดเล็กสำหรับทดสอบฟังก์ชันพื้นฐาน

### สคริปต์ทดสอบ
- `test_analyzer.py` - สคริปต์สำหรับทดสอบฟังก์ชันต่างๆ ของ analyzer
- `create_sample.py` - สคริปต์สำหรับสร้างไฟล์ binary ตัวอย่าง

### ผลลัพธ์ตัวอย่าง
- `sample_output.txt` - ตัวอย่างผลลัพธ์จากการวิเคราะห์

## 🚀 วิธีการทดสอบ

### ทดสอบพื้นฐาน
```bash
# เข้าไปยังโฟลเดอร์หลัก
cd ..

# ทดสอบด้วยไฟล์ตัวอย่าง
python app.py examples/sample.bin

# ทดสอบด้วยไฟล์ขนาดเล็ก
python app.py examples/test_simple.bin
```

### ทดสอบขั้นสูง
```bash
# รันสคริปต์ทดสอบ
cd examples
python test_analyzer.py

# สร้างไฟล์ตัวอย่างใหม่
python create_sample.py
```

## 📝 คำอธิบายไฟล์ตัวอย่าง

### sample.bin
- ขนาด: ~2KB
- มี constant pool entries: 15 รายการ
- ประกอบด้วย: strings, function names, crypto-related data

### test_simple.bin
- ขนาด: ~500 bytes
- มี constant pool entries: 5 รายการ
- ใช้สำหรับทดสอบฟังก์ชันพื้นฐาน

## 🎯 ผลลัพธ์ที่คาดหวัง

เมื่อรันกับไฟล์ตัวอย่าง คุณควรเห็น:
- การตรวจสอบ Magic Header สำเร็จ
- การแยก strings ต่างๆ ออกมา
- การจัดหมวดหมู่ strings
- การวิเคราะห์ functionality
- การแสดงความสัมพันธ์ระหว่าง strings
