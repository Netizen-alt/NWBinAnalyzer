# nw_bin_decompiler.py
import sys
import struct
import re

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

def extract_strings_from_binary(data, min_length=3):
    """Extract readable ASCII/UTF-8 strings from binary data"""
    strings = []
    
    # Look for null-terminated strings
    null_terminated = re.findall(b'[\x20-\x7e]{' + str(min_length).encode() + b',}\x00', data)
    for s in null_terminated:
        try:
            strings.append(s[:-1].decode('utf-8'))
        except:
            pass
    
    # Look for consecutive printable ASCII characters
    ascii_pattern = re.compile(b'[\x20-\x7e]{' + str(min_length).encode() + b',}')
    for match in ascii_pattern.finditer(data):
        try:
            decoded = match.group().decode('ascii')
            strings.append(decoded)
        except:
            pass
    
    # Look for length-prefixed strings (various sizes)
    for prefix_size in [1, 2, 4]:
        i = 0
        while i < len(data) - prefix_size:
            try:
                if prefix_size == 1:
                    length = data[i]
                elif prefix_size == 2:
                    length = struct.unpack('<H', data[i:i+2])[0]
                else:  # 4 bytes
                    length = struct.unpack('<I', data[i:i+4])[0]
                
                if 1 <= length <= 500 and i + prefix_size + length <= len(data):
                    string_data = data[i+prefix_size:i+prefix_size+length]
                    try:
                        decoded = string_data.decode('utf-8')
                        if len(decoded) >= min_length and all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in decoded):
                            strings.append(decoded)
                    except:
                        pass
            except:
                pass
            i += 1
    
    # Look for UTF-8 sequences
    i = 0
    while i < len(data):
        try:
            # Try to decode starting from this position
            for end in range(i + min_length, min(i + 100, len(data) + 1)):
                try:
                    decoded = data[i:end].decode('utf-8')
                    if len(decoded) >= min_length and all(c.isprintable() or c in '\n\r\t' for c in decoded):
                        strings.append(decoded)
                        break
                except:
                    continue
        except:
            pass
        i += 1
    
    # Look for base64-like patterns
    base64_pattern = re.compile(b'[A-Za-z0-9+/]{8,}={0,2}')
    for match in base64_pattern.finditer(data):
        try:
            import base64
            decoded = base64.b64decode(match.group()).decode('utf-8')
            if len(decoded) >= min_length and all(c.isprintable() or c in '\n\r\t' for c in decoded):
                strings.append(f"base64:{decoded}")
        except:
            pass
    
    # Look for hex-encoded strings
    hex_pattern = re.compile(b'[0-9a-fA-F]{' + str(min_length*2).encode() + b',}')
    for match in hex_pattern.finditer(data):
        if len(match.group()) % 2 == 0:
            try:
                hex_bytes = bytes.fromhex(match.group().decode('ascii'))
                decoded = hex_bytes.decode('utf-8')
                if len(decoded) >= min_length and all(c.isprintable() or c in '\n\r\t' for c in decoded):
                    strings.append(f"hex:{decoded}")
            except:
                pass
    
    return list(set(strings))  # Remove duplicates

def analyze_binary_structure(data):
    """Analyze binary data structure for patterns"""
    analysis = []
    
    # Check for common magic bytes
    if len(data) >= 4:
        magic = data[:4]
        analysis.append(f"Magic bytes: {magic.hex()}")
    
    # Check entropy (simple measure)
    if len(data) > 0:
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
        
        non_zero = sum(1 for count in byte_counts if count > 0)
        analysis.append(f"Unique bytes: {non_zero}/256")
    
    # Look for repeating patterns
    if len(data) >= 8:
        patterns = {}
        for i in range(len(data) - 3):
            pattern = data[i:i+4]
            if pattern in patterns:
                patterns[pattern] += 1
            else:
                patterns[pattern] = 1
        
        common_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:3]
        if common_patterns and common_patterns[0][1] > 1:
            analysis.append(f"Common 4-byte patterns: {[(p.hex(), count) for p, count in common_patterns]}")
    
    return analysis

def categorize_strings(strings):
    """Categorize strings by their likely purpose"""
    categories = {
        'api_calls': [],
        'file_paths': [],
        'urls': [],
        'crypto_related': [],
        'node_modules': [],
        'error_messages': [],
        'config_keys': [],
        'suspicious': [],
        'short_codes': [],
        'other': []
    }
    
    for s in strings:
        if not s or len(s.strip()) == 0:
            continue
            
        s_lower = s.lower()
        
        # API calls and functions 
        if any(pattern in s_lower for pattern in ['create', 'read', 'write', 'fetch', 'request', 'connect', 'verify', 'hash', 'encrypt', 'decrypt', 'sign']):
            categories['api_calls'].append(s)
        # File paths
        elif any(pattern in s for pattern in ['/', '\\', '.js', '.bin', '.log', '.html', '.png']):
            categories['file_paths'].append(s)
        # URLs
        elif any(pattern in s_lower for pattern in ['http://', 'https://', 'localhost']):
            categories['urls'].append(s)
        # Crypto related
        elif any(pattern in s_lower for pattern in ['sha', 'rsa', 'aes', 'gcm', 'hash', 'signature', 'crypto', 'key', 'cert']):
            categories['crypto_related'].append(s)
        # Node modules
        elif any(pattern in s for pattern in ['node:', 'require', 'module', 'Buffer']):
            categories['node_modules'].append(s)
        # Error messages
        elif any(pattern in s_lower for pattern in ['failed', 'error', 'invalid', 'not found', 'mismatch']):
            categories['error_messages'].append(s)
        # Suspicious strings
        elif any(pattern in s_lower for pattern in ['sussy', 'sus', 'bypass', 'hack']):
            categories['suspicious'].append(s)
        # Short codes (might be obfuscated identifiers)
        elif len(s) <= 5 and s.isalnum():
            categories['short_codes'].append(s)
        # Config-like keys
        elif any(pattern in s_lower for pattern in ['config', 'option', 'setting', 'env', 'dir', 'path', 'name']):
            categories['config_keys'].append(s)
        else:
            categories['other'].append(s)
    
    return categories

def find_string_relationships(strings):
    """Find potential relationships between strings"""
    relationships = []
    
    # Group related strings
    for i, s1 in enumerate(strings):
        for j, s2 in enumerate(strings[i+1:], i+1):
            # Skip empty strings
            if not s1 or not s2:
                continue
                
            # Check if one is contained in another
            if s1 in s2 and s1 != s2:
                relationships.append(f"'{s1}' is part of '{s2}'")
            elif s2 in s1 and s1 != s2:
                relationships.append(f"'{s2}' is part of '{s1}'")
            
            # Check for similar prefixes/suffixes
            elif len(s1) > 3 and len(s2) > 3:
                if s1.startswith(s2[:3]) or s2.startswith(s1[:3]):
                    relationships.append(f"Similar prefix: '{s1}' <-> '{s2}'")
                elif s1.endswith(s2[-3:]) or s2.endswith(s1[-3:]):
                    relationships.append(f"Similar suffix: '{s1}' <-> '{s2}'")
    
    return relationships[:20]  # Limit to first 20 relationships

def analyze_functionality(strings):
    """Analyze what the code might be doing based on strings"""
    functionality = []
    
    # Check for different capabilities
    if any('fetch' in s.lower() or 'request' in s.lower() or 'http' in s.lower() for s in strings):
        functionality.append("🌐 Network communication (HTTP requests)")
    
    if any('crypto' in s.lower() or 'hash' in s.lower() or 'sign' in s.lower() for s in strings):
        functionality.append("🔐 Cryptographic operations")
    
    if any('file' in s.lower() or 'read' in s.lower() or 'write' in s.lower() for s in strings):
        functionality.append("📁 File system operations")
    
    if any('worker' in s.lower() for s in strings):
        functionality.append("⚙️ Worker threads/background processing")
    
    if any('verify' in s.lower() or 'signature' in s.lower() for s in strings):
        functionality.append("✅ Code/data verification")
    
    if any('download' in s.lower() or 'upload' in s.lower() for s in strings):
        functionality.append("📥 File download/upload")
    
    if any('log' in s.lower() for s in strings):
        functionality.append("📝 Logging system")
    
    if any('update' in s.lower() for s in strings):
        functionality.append("🔄 Auto-update functionality")
    
    if any('sus' in s.lower() for s in strings):
        functionality.append("⚠️ Security/anti-tamper checks")
    
    return functionality

def decompile_bin(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    if data[0:4] != b'\x8e\x06\xde\xc0':
        print("Not a valid NW.js .bin file.")
        return

    print(f"[+] Magic Header OK: {data[0:4].hex()}")
    offset = 4
    const_count, offset = read_varint(data, offset)
    print(f"[+] Constant Pool Entries: {const_count}")

    all_strings = []
    
    for i in range(const_count):
        length, offset = read_varint(data, offset)
        const_data = data[offset:offset+length]
        
        print(f"\n[{i:02}] Length: {length}")
        
        # Try direct UTF-8 decode first
        try:
            decoded = const_data.decode('utf-8')
            if decoded.strip():  # Only show non-empty strings
                print(f"     Direct UTF-8: {repr(decoded)}")
                all_strings.append(decoded)
            else:
                print(f"     Empty/whitespace string")
                all_strings.append(decoded)
        except:
            # If direct decode fails, extract strings from binary
            extracted_strings = extract_strings_from_binary(const_data, min_length=3)
            if extracted_strings:
                print(f"     Extracted strings: {extracted_strings}")
                all_strings.extend(extracted_strings)
            else:
                # Show binary analysis
                analysis = analyze_binary_structure(const_data)
                print(f"     Binary data ({len(const_data)} bytes):")
                for info in analysis:
                    print(f"       {info}")
                if len(const_data) <= 50:
                    print(f"       Hex: {const_data.hex()}")
                else:
                    print(f"       Hex (first 50): {const_data[:50].hex()}...")
        
        offset += length

    # Print all unique strings found
    unique_strings = list(set(all_strings))
    if unique_strings:
        print(f"\n[+] All extracted strings ({len(unique_strings)}):")
        for i, s in enumerate(sorted(unique_strings), 1):
            print(f"  {i:2}. {repr(s)}")
        
        # Categorize strings
        print(f"\n[+] String Analysis:")
        categories = categorize_strings(unique_strings)
        
        for category, items in categories.items():
            if items:
                print(f"\n  📋 {category.upper().replace('_', ' ')} ({len(items)}):")
                for item in sorted(items)[:10]:  # Show first 10 items
                    print(f"    - {repr(item)}")
                if len(items) > 10:
                    print(f"    ... and {len(items) - 10} more")
        
        # Analyze functionality
        print(f"\n[+] Detected Functionality:")
        functionality = analyze_functionality(unique_strings)
        for func in functionality:
            print(f"  {func}")
        
        # Show relationships
        print(f"\n[+] String Relationships:")
        relationships = find_string_relationships(unique_strings)
        for rel in relationships[:10]:  # Show first 10 relationships
            print(f"  {rel}")
        if len(relationships) > 10:
            print(f"  ... and {len(relationships) - 10} more relationships")
    
    print("\n[!] This tool shows constant pool and extracted strings.")
    print("[!] Full opcode decompilation requires V8 bytecode parser (complex).")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python nw_bin_decompiler.py <file.bin>")
        sys.exit(1)

    decompile_bin(sys.argv[1])
