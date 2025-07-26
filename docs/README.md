# NWBinAnalyzer Documentation

📚 เอกสารประกอบสำหรับ NWBinAnalyzer - เครื่องมือวิเคราะห์ไฟล์ NW.js Binary

## 📖 สารบัญเอกสาร

### 🚀 เริ่มต้นใช้งาน
- [คู่มือการติดตั้ง](installation.md)
- [คู่มือเริ่มต้นใช้งาน](getting-started.md)
- [ตัวอย่างการใช้งาน](examples.md)

### 🔧 เอกสารทางเทคนิค
- [รูปแบบไฟล์ NW.js Binary](binary-format.md)
- [อัลกอริทึมการแยก String](string-extraction.md)
- [การวิเคราะห์และจัดหมวดหมู่](analysis-algorithms.md)

### 📊 การใช้งานขั้นสูง
- [การปรับแต่งและคอนฟิก](configuration.md)
- [การขยายฟังก์ชันการทำงาน](extending.md)
- [การแก้ไขปัญหา](troubleshooting.md)

### 🎓 ทรัพยากรการเรียนรู้
- [ทฤษฎี Reverse Engineering](reverse-engineering-theory.md)
- [V8 JavaScript Engine](v8-engine.md)
- [NW.js Architecture](nwjs-architecture.md)

### 🔬 งานวิจัยและอ้างอิง
- [บทความและงานวิจัยที่เกี่ยวข้อง](research.md)
- [แหล่งข้อมูลเพิ่มเติม](references.md)

## 🎯 เอกสารฉบับย่อ

### คำสั่งใช้งานพื้นฐาน
```bash
python app.py <file.bin>
```

### ฟังก์ชันหลัก
- **String Extraction**: แยกข้อความจาก binary data
- **Categorization**: จัดหมวดหมู่ strings
- **Analysis**: วิเคราะห์ functionality
- **Relationships**: หาความสัมพันธ์ระหว่าง strings

### รูปแบบไฟล์ที่รองรับ
- ไฟล์ .bin ของ NW.js
- Magic header: `8e 06 de c0`
- V8 bytecode format

## 🤝 การมีส่วนร่วม

หากคุณต้องการปรับปรุงเอกสาร:
1. แก้ไขไฟล์ .md ที่เกี่ยวข้อง
2. ตรวจสอบการใช้ภาษาและรูปแบบ
3. ทดสอบตัวอย่างโค้ด (ถ้ามี)

## 📝 หมายเหตุ

เอกสารนี้จัดทำขึ้นเพื่อการศึกษาเท่านั้น กรุณาใช้งานอย่างมีจริยธรรม
