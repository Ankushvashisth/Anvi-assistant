import sys
import os

files = ['remote.txt', 'status.txt', 'curl_output.txt']
output = []
for f in files:
    if not os.path.exists(f):
        output.append(f"--- {f} (NOT FOUND) ---")
        continue
        
    output.append(f"--- {f} ({os.path.getsize(f)} bytes) ---")
    try:
        with open(f, 'rb') as fp:
            content = fp.read()
            # Try to decode utf-16le (powershell default), then utf-8
            decoded = False
            for enc in ['utf-16', 'utf-8', 'cp1252', 'latin1']:
                try:
                    text = content.decode(enc)
                    output.append(text)
                    decoded = True
                    break
                except UnicodeDecodeError:
                    continue
            
            if not decoded:
                output.append(f"(COULD NOT DECODE)")
    except Exception as e:
        output.append(f"Error reading {f}: {e}")

with open('debug_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
