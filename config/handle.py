import chardet
import json
# Detect file encoding
with open('db_backup.json', 'rb') as file:
    result = chardet.detect(file.read())
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}") # likely utf-16
# Load JSON using the correct encoding
# If utf-16-le, you can also use 'utf-16' to handle BOM automatically
if 'utf-16' in encoding.lower():
    encoding = 'utf-16'
with open('db_backup.json', 'r', encoding=encoding) as file:
    data = json.load(file)
#Save as UTF-8 to avoid BOM issues in the future
with open('db_backup_utf8.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
print("Converted JSON to UTF-8 successfully!")