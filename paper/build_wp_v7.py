import re, base64, html, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(_HERE)
s = open('WP_WhereExportControlsBind_v8.md', encoding='utf-8').read()
CAP = eval(open('captions_v7.py', encoding='utf-8').read())
def fig(label):
    name, cap = CAP[label]; p = os.path.join('..', 'figures', f'{name}.png')
    return f'<figure><img src="data:image/png;base64,{base64.b64encode(open(p, "rb").read()).decode()}" style="width:100%"><figcaption><b>{label}.</b> {html.escape(cap)}</figcaption></figure>'
def md2html(t):
    out = []; intable = False
    for line in t.split('\n'):
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '): continue
            tag = 'th' if not intable else 'td'; out.append(('<table>' if not intable else '') + '<tr>' + ''.join(f'<{tag}>{html.escape(c)}</{tag}>' for c in cells) + '</tr>'); intable = True; continue
        if intable: out.append('</table>'); intable = False
        if line.startswith('---'): continue
        m = re.match(r'^(#+) (.*)', line)
        if m: out.append(f'<h{len(m.group(1))}>{html.escape(m.group(2))}</h{len(m.group(1))}>'); continue
        if line.startswith('- '): out.append('<p class="li">• ' + html.escape(line[2:]) + '</p>'); continue
        if line.strip(): out.append('<p>' + html.escape(line) + '</p>')
    if intable: out.append('</table>')
    h = '\n'.join(out); h = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', h); h = re.sub(r'\*(.+?)\*', r'<i>\1</i>', h); return h
b = md2html(s); placed = []
for label in CAP:
    i = b.find(label)
    if i >= 0: j = b.find('</p>', i); b = b[:j+4] + fig(label) + b[j+4:]; placed.append(label)
b = re.sub(r'<p>\(Appendix Figure A\d\)(?: \(Appendix Figure A\d\))*</p>', '', b)
missing = [l for l in CAP if l not in placed]
if missing: b = b.replace('<h2>Figures</h2>', '<h2>Appendix figures (continued)</h2>' + ''.join(fig(l) for l in missing) + '<h2>Figures</h2>')
css = "body{font-family:Georgia,serif;max-width:860px;margin:40px auto;line-height:1.55;color:#222;font-size:11pt} h1{font-size:1.5em;line-height:1.25} h2{margin-top:2em;border-bottom:1px solid #ccc;page-break-after:avoid} h3{page-break-after:avoid} table{border-collapse:collapse;font-size:.86em;margin:1em 0;page-break-inside:avoid} td,th{border:1px solid #ccc;padding:4px 8px;text-align:left;vertical-align:top} figure{margin:1.6em 0;page-break-inside:avoid;text-align:center} figure img{max-height:8.6in;width:auto;max-width:100%} figcaption{font-size:.82em;color:#444;line-height:1.4;text-align:left} .li{margin:.2em 0 .2em 1em} @media print{body{max-width:none;margin:0.6in} h2{page-break-before:auto}} @page{size:A4;margin:0.75in}"
open('WP_WhereExportControlsBind_v8.html', 'w', encoding='utf-8').write(f'<!doctype html><html><head><meta charset="utf-8"><title>Where Export Controls Bind — WP v7</title><style>{css}</style></head><body>{b}</body></html>')
print("v7 HTML:", round(os.path.getsize('WP_WhereExportControlsBind_v8.html')/1e6, 1), "MB · 그림", b.count('<figure>'), "· 본문 외 배치:", missing)
