#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
สคริปต์สำหรับสร้างไฟล์ binary ตัวอย่างเพื่อทดสอบ NWBinAnalyzer
"""

import struct
import os

def write_varint(value):
    """เขียนค่า variable-length integer"""
    result = b''
    while value >= 0x80:
        result += bytes([(value & 0x7F) | 0x80])
        value >>= 7
    result += bytes([value & 0x7F])
    return result

def create_simple_bin():
    """สร้างไฟล์ binary ตัวอย่างขนาดเล็ก"""
    
    # Magic header สำหรับ NW.js
    data = b'\x8e\x06\xde\xc0'
    
    # Constant pool entries
    strings = [
        "hello",
        "world", 
        "test",
        "createHash",
        "node:crypto"
    ]
    
    # เขียนจำนวน entries
    data += write_varint(len(strings))
    
    # เขียนแต่ละ string
    for s in strings:
        string_bytes = s.encode('utf-8')
        data += write_varint(len(string_bytes))
        data += string_bytes
    
    # บันทึกไฟล์
    with open('test_simple.bin', 'wb') as f:
        f.write(data)
    
    print(f"✅ สร้างไฟล์ test_simple.bin สำเร็จ ({len(data)} bytes)")

def create_complex_bin():
    """สร้างไฟล์ binary ตัวอย่างที่ซับซ้อนขึ้น"""
    
    # Magic header
    data = b'\x8e\x06\xde\xc0'
    
    # Constant pool entries ที่หลากหลาย
    entries = [
        # Plain strings
        "require",
        "module",
        "exports",
        
        # API calls
        "createHash",
        "readFileSync", 
        "writeFileSync",
        "verifySignature",
        
        # Crypto related
        "sha256",
        "RSA-SHA256",
        "aes-128-gcm",
        
        # File paths
        "./config.json",
        "/tmp/log.txt",
        "worker.js",
        
        # URLs
        "https://api.example.com",
        "http://localhost:3000",
        
        # Error messages
        "Invalid signature",
        "File not found",
        "Hash mismatch",
        
        # Binary data (จำลอง)
        b'\x01\x02\x03\x04\x05',
        b'\xff\xfe\xfd\xfc',
        
        # Empty string
        "",
        
        # Unicode
        "ทดสอบ",
        "🔐🌐📁",
    ]
    
    # เขียนจำนวน entries
    data += write_varint(len(entries))
    
    # เขียนแต่ละ entry
    for entry in entries:
        if isinstance(entry, str):
            entry_bytes = entry.encode('utf-8')
        else:
            entry_bytes = entry
            
        data += write_varint(len(entry_bytes))
        data += entry_bytes
    
    # บันทึกไฟล์
    with open('sample.bin', 'wb') as f:
        f.write(data)
    
    print(f"✅ สร้างไฟล์ sample.bin สำเร็จ ({len(data)} bytes)")

def create_corrupted_bin():
    """สร้างไฟล์ binary ที่เสียหายเพื่อทดสอบการจัดการข้อผิดพลาด"""
    
    # Magic header ผิด
    data = b'\x8e\x06\xde\xc1'  # ไบต์สุดท้ายผิด
    
    # ข้อมูลที่เสียหาย
    data += b'\x05'  # constant count = 5
    data += b'\x03ABC'  # string length=3, data="ABC"
    data += b'\xff\xff\xff\xff'  # length ผิดปกติ
    
    with open('corrupted.bin', 'wb') as f:
        f.write(data)
    
    print(f"✅ สร้างไฟล์ corrupted.bin สำเร็จ ({len(data)} bytes)")

if __name__ == '__main__':
    print("🔧 กำลังสร้างไฟล์ตัวอย่างสำหรับทดสอบ NWBinAnalyzer...")
    print()
    
    create_simple_bin()
    create_complex_bin() 
    create_corrupted_bin()
    
    print()
    print("📁 ไฟล์ที่สร้างขึ้น:")
    for filename in ['test_simple.bin', 'sample.bin', 'corrupted.bin']:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  - {filename} ({size} bytes)")
    
    print()
    print("🚀 ทดสอบด้วยคำสั่ง:")
    print("  python ../app.py test_simple.bin")
    print("  python ../app.py sample.bin")
    print("  python ../app.py corrupted.bin")
