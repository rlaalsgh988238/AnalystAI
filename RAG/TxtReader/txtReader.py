# 키값
keyPath = '../../.idea/Key/key.txt'

def read_file(file_path):
    if file_path == 'key':
        with open(keyPath, 'r', encoding='utf-8') as file:
            key = file.read().strip()
        return key
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(content)
        return None