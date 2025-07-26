#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
สคริปต์ทดสอบฟังก์ชันต่างๆ ของ NWBinAnalyzer
"""

import sys
import os

# เพิ่มโฟลเดอร์หลักเข้าไปใน path เพื่อ import app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import (
        read_varint, 
        extract_strings_from_binary,
        analyze_binary_structure,
        categorize_strings,
        find_string_relationships,
        analyze_functionality
    )
    print("✅ Import ฟังก์ชันจาก app.py สำเร็จ")
except ImportError as e:
    print(f"❌ ไม่สามารถ import ฟังก์ชันได้: {e}")
    sys.exit(1)

def test_read_varint():
    """ทดสอบฟังก์ชัน read_varint"""
    print("\n🧪 ทดสอบ read_varint...")
    
    test_cases = [
        (b'\x05', 5),
        (b'\x80\x01', 128),
        (b'\xff\x01', 255),
        (b'\x80\x80\x01', 16384),
    ]
    
    for data, expected in test_cases:
        try:
            result, offset = read_varint(data, 0)
            if result == expected:
                print(f"  ✅ {data.hex()} → {result}")
            else:
                print(f"  ❌ {data.hex()} → {result} (คาดหวัง {expected})")
        except Exception as e:
            print(f"  ❌ {data.hex()} → Error: {e}")

def test_extract_strings():
    """ทดสอบฟังก์ชัน extract_strings_from_binary"""
    print("\n🧪 ทดสอบ extract_strings_from_binary...")
    
    # สร้างข้อมูล binary ทดสอบ
    test_data = b'hello\x00world\x00\x05test!\x03abc\xff\xfeinvalid'
    
    try:
        strings = extract_strings_from_binary(test_data)
        print(f"  ✅ พบ strings: {strings}")
        
        expected_strings = ['hello', 'world', 'test!', 'abc']
        found_expected = [s for s in expected_strings if s in strings]
        print(f"  📊 พบ strings ที่คาดหวัง: {found_expected}")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_categorize_strings():
    """ทดสอบฟังก์ชัน categorize_strings"""
    print("\n🧪 ทดสอบ categorize_strings...")
    
    test_strings = [
        'createHash',
        'readFileSync', 
        'https://example.com',
        './config.json',
        'RSA-SHA256',
        'require',
        'Invalid signature',
        'sussy',
        'abc',
        'logDir'
    ]
    
    try:
        categories = categorize_strings(test_strings)
        
        print("  📊 ผลการจัดหมวดหมู่:")
        for category, items in categories.items():
            if items:
                print(f"    {category}: {items}")
                
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_analyze_functionality():
    """ทดสอบฟังก์ชัน analyze_functionality"""
    print("\n🧪 ทดสอบ analyze_functionality...")
    
    test_strings = [
        'fetch', 'https://api.com', 'request',
        'createHash', 'verifySignature', 'crypto',
        'readFile', 'writeFile', 'fs',
        'worker', 'thread',
        'download', 'upload',
        'sussy', 'verification failed'
    ]
    
    try:
        functionality = analyze_functionality(test_strings)
        print("  🎯 ฟังก์ชันที่ตรวจพบ:")
        for func in functionality:
            print(f"    {func}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_find_relationships():
    """ทดสอบฟังก์ชัน find_string_relationships"""
    print("\n🧪 ทดสอบ find_string_relationships...")
    
    test_strings = [
        'readFile',
        'readFileSync',
        'writeFile', 
        'createHash',
        'createCipher',
        'test',
        'testing',
        'config.json',
        'config'
    ]
    
    try:
        relationships = find_string_relationships(test_strings)
        print("  🔗 ความสัมพันธ์ที่พบ:")
        for rel in relationships[:5]:  # แสดง 5 อันแรก
            print(f"    {rel}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_with_sample_file():
    """ทดสอบด้วยไฟล์ตัวอย่าง"""
    print("\n🧪 ทดสอบด้วยไฟล์ตัวอย่าง...")
    
    # สร้างไฟล์ตัวอย่างก่อน
    if not os.path.exists('test_simple.bin'):
        print("  📁 ไม่พบไฟล์ test_simple.bin, กำลังสร้าง...")
        try:
            from create_sample import create_simple_bin
            create_simple_bin()
        except:
            print("  ❌ ไม่สามารถสร้างไฟล์ตัวอย่างได้")
            return
    
    # ทดสอบการอ่านไฟล์
    try:
        with open('test_simple.bin', 'rb') as f:
            data = f.read()
        
        print(f"  ✅ อ่านไฟล์ test_simple.bin สำเร็จ ({len(data)} bytes)")
        
        # ตรวจสอบ magic header
        if data[:4] == b'\x8e\x06\xde\xc0':
            print("  ✅ Magic header ถูกต้อง")
        else:
            print("  ❌ Magic header ไม่ถูกต้อง")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

def main():
    """รันการทดสอบทั้งหมด"""
    print("🧪 เริ่มทดสอบ NWBinAnalyzer Functions")
    print("=" * 50)
    
    test_read_varint()
    test_extract_strings()
    test_categorize_strings()
    test_analyze_functionality()
    test_find_relationships()
    test_with_sample_file()
    
    print("\n" + "=" * 50)
    print("✅ การทดสอบเสร็จสิ้น!")
    print("\n💡 เรียกใช้คำสั่งนี้เพื่อทดสอบไฟล์ตัวอย่าง:")
    print("   python ../app.py test_simple.bin")

if __name__ == '__main__':
    main()
