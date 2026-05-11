import os
import glob

template_dir = r"c:\Users\Stiven\OneDrive\Desktop\Mis Software\marichuy\app\templates"
for filepath in glob.glob(os.path.join(template_dir, '**', '*.html'), recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'method="POST"' in content and 'csrf_token' not in content:
        content = content.replace('method="POST"', 'method="POST"\n    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
print("CSRF tokens added to all POST forms.")
