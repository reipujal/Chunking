import os, re, glob

chunks_dir = 'chunks'
entries = []

for md_file in sorted(glob.glob(chunks_dir + '/**/*.md', recursive=True)):
    basename = os.path.basename(md_file)
    if basename.startswith('_'):
        continue
    with open(md_file, encoding='utf-8') as f:
        content = f.read()
    m_id = re.search(r'^id:\s*(.+)', content, re.MULTILINE)
    m_title = re.search(r'^title:\s*[\"\'](.*)[\"\']\s*$', content, re.MULTILINE)
    if not m_title:
        m_title = re.search(r'^title:\s*(.+)', content, re.MULTILINE)
    m_area = re.search(r'^area:\s*(.+)', content, re.MULTILINE)
    m_type = re.search(r'^chunk_type:\s*(.+)', content, re.MULTILINE)
    m_status = re.search(r'^status:\s*(.+)', content, re.MULTILINE)
    chunk_id = m_id.group(1).strip() if m_id else 'unknown'
    title = m_title.group(1).strip() if m_title else 'unknown'
    area = m_area.group(1).strip() if m_area else 'unknown'
    chunk_type = m_type.group(1).strip() if m_type else 'unknown'
    status = m_status.group(1).strip() if m_status else 'unknown'
    rel_path = md_file.replace(os.sep, '/')
    entries.append((area, chunk_id, title, chunk_type, status, rel_path))

entries.sort(key=lambda x: (x[0], x[1]))

lines = ['# Chunk Index', '', f'Total chunks: {len(entries)}', '',
         '| ID | Title | Area | Type | Status | Path |',
         '|---|---|---|---|---|---|']
for area, chunk_id, title, chunk_type, status, path in entries:
    lines.append(f'| {chunk_id} | {title} | {area} | {chunk_type} | {status} | {path} |')

with open('chunks/_index.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f'Index regenerated: {len(entries)} chunks')
