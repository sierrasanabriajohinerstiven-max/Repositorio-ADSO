import os
import glob
import re

template_dir = r"c:\Users\Stiven\OneDrive\Desktop\Mis Software\marichuy\app\templates"
broken_pattern = 'method="POST"\n    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>'

count = 0
for filepath in glob.glob(os.path.join(template_dir, '**', '*.html'), recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if broken_pattern in content:
        # Revert
        content = content.replace(broken_pattern, 'method="POST"')
        # Re-apply correctly
        content = re.sub(r'(<form[^>]*method="POST"[^>]*>)', r'\1\n    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Fixed CSRF tokens in {count} files.")
