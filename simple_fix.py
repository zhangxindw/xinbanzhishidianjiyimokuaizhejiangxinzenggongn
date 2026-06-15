# Simple script to add Vue Router history mode support
import os

file_path = '/root/xinbanzhishidianjiyimokuaizhejiang/backend/app.py'

with open(file_path, 'r') as f:
    lines = f.readlines()

# Find the line with 'if __name__ =='
insert_idx = None
for i, line in enumerate(lines):
    if 'if __name__ ==' in line:
        insert_idx = i
        break

if insert_idx is not None:
    # Add the catch-all route before the main block
    new_lines = [
        '\n',
        '# Vue Router history mode support\n',
        '@app.route("/<path:path>")\n',
        'def catch_all(path):\n',
        '    if path.startswith("api/"):\n',
        '        return jsonify({"status": "error", "message": "Not found"}), 404\n',
        '    file_path = os.path.join(app.static_folder, path)\n',
        '    if os.path.exists(file_path) and os.path.isfile(file_path):\n',
        '        return send_from_directory(app.static_folder, path)\n',
        '    return send_from_directory(app.static_folder, "index.html")\n',
        '\n'
    ]
    
    lines = lines[:insert_idx] + new_lines + lines[insert_idx:]
    
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print('Done!')
else:
    print('Not found')
