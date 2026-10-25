"""Generate wp.tex from the Markdown manuscript: pandoc → LaTeX, then (1) section numbering, (2) references with hanging indent,
(3) appendix lettering, (4) all tables as non-breaking floats with captions, (5) figures after first mention (appendix figures inside their appendix section)."""
import re, subprocess
import os as _os; _HERE = _os.path.dirname(_os.path.abspath(__file__)); MD = _os.path.join(_HERE, 'WP_WhereExportControlsBind_v8.md'); CAPF = _os.path.join(_HERE, 'captions_v7.py')
md = open(MD, encoding='utf-8').read(); title = re.search(r'^# (.+)$', md, flags=re.M).group(1); abstract = re.search(r'\*\*Abstract\.\*\* (.+?)\n\n', md, flags=re.S).group(1).strip(); body = md[md.index('## 1. Introduction'):]
CAP = eval(open(CAPF, encoding='utf-8').read())
tex = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'latex', '--wrap=none', '--shift-heading-level-by=-1'], input=body, capture_output=True, text=True).stdout
tex = re.sub(r'\\hypertarget\{[^}]*\}\{%\n', '', tex); tex = re.sub(r'\\label\{[^}]*\}\}', '', tex)
tex = re.sub(r'\\section\{\d\.\s+', r'\\section{', tex); tex = re.sub(r'\\subsection\{\d\.\d\s+', r'\\subsection{', tex)
# references
i = tex.index('\\section{References}'); j = tex.index('\\section{Appendix A.', i); ref = tex[i + len('\\section{References}'):j]
ref = ref.replace('\\begin{itemize}', '').replace('\\end{itemize}', '').replace('\\tightlist', '').replace('\\item', '\\par\\noindent\\hangindent=1.5em\\hangafter=1 ')
tex = tex[:i] + '\\clearpage\\section*{References}\\begingroup\\footnotesize\\setstretch{1.0}' + ref + '\\endgroup\n' + tex[j:]
tex = tex.replace('\\section{Appendix A.', '\\appendix\\renewcommand{\\thefigure}{A\\arabic{figure}}\\setcounter{figure}{0}\\renewcommand{\\thetable}{A\\arabic{table}}\\setcounter{table}{0}\n\\section{Appendix A.', 1)
tex = re.sub(r'\\section\{Appendix ([A-F])\.\s+', r'\\section{', tex)
tex = tex.replace('\\section{Data dictionary and value-chain taxonomy}', '\\clearpage\\section{Data dictionary and value-chain taxonomy}\n\\noindent Table A1 lists the crosswalks released with the package; the trade baskets, control dates and extraction rules follow.\n'); tex = tex.replace('\\section{Acknowledgements and disclosures}', '\\section*{Acknowledgements and disclosures}')
k = tex.find('\\section{Figures}'); tex = tex[:k] if k > 0 else tex
tex = re.sub(r'\n\(Appendix Figure A\d\)(?:\s*\(Appendix Figure A\d\))*\s*\n', '\n', tex)
# tables → floats
def conv(m):
    cap = m.group(1); body = m.group(2); sm = re.match(r'\[\]\{(@\{\}.*?@\{\})\}', body, flags=re.S); spec = sm.group(1); body = body[sm.end():]
    body = re.sub(r'\\endfirsthead.*?\\endhead\n', '', body, flags=re.S); body = body.replace('\\bottomrule\\noalign{}\n\\endlastfoot\n', '').replace('\\toprule\\noalign{}', '\\toprule').replace('\\midrule\\noalign{}', '\\midrule').replace('\\endfirsthead\n', '').replace('\\endhead\n', '').replace('\\endfoot\n', '').replace('\\endlastfoot\n', '').rstrip() + '\n\\bottomrule\n'
    # 데이터 행 사이에 점선: \midrule 이후의 각 행 끝 \\ 뒤에 \hdashline
    hdr, sep, rows = body.partition('\\midrule\n')
    rows = re.sub(r'(\\\\)\n(?=\S)', r'\1\n\\hdashline\n', rows)
    rows = re.sub(r'\\hdashline\n(?=\\bottomrule)', '', rows)   # 마지막 행과 bottomrule 사이 점선 제거
    body = hdr + sep + rows
    capline = f'\\caption*{{\\textbf{{{cap}}}}}' if cap else ''
    return f"\n\\begin{{table}}[htbp]\\centering\\footnotesize\\setstretch{{1.05}}{capline}\\begin{{tabular}}{{{spec}}}{body}\\end{{tabular}}\\end{{table}}\n"
tex = re.sub(r'(?:\\textbf\{(Table [A-G]?\d\.[^}]*)\}\n\n)?\\begin\{longtable\}(.*?)\\end\{longtable\}', lambda m: conv(m), tex, flags=re.S)
tex = tex.replace('\\columnwidth', '\\linewidth')
import re as _re
def _narrow(m):
    blk = m.group(0)
    if 'Crosswalk' in blk: blk = blk.replace('\\real{0.5000}', '\\real{0.26}', 1).replace('\\real{0.5000}', '\\real{0.74}', 1)
    if 'Trade-flow tests' in blk: blk = blk.replace('\\begin{table}[htbp]', '\\begin{table}[H]', 1)
    if 'Shareholders and finances' in blk: blk = blk.replace('\\begin{table}[htbp]', '\\begin{table}[H]', 1)
    if 'Corrections (four audit rounds)' in blk: blk = blk.replace('\\begin{table}[htbp]', '\\begin{table}[H]\\scriptsize', 1).replace('\\real{0.3333}', '\\real{0.30}', 1).replace('\\real{0.3333}', '\\real{0.46}', 1).replace('\\real{0.3333}', '\\real{0.24}', 1)
    return blk
tex = _re.sub(r'\\begin\{table\}.*?\\end\{table\}', _narrow, tex, flags=_re.S)
tex = tex.replace('ASCM vs own trend', 'ASCM\\newline vs own trend').replace('Annual SDID, 27 donors', 'Annual SDID\\newline (27 donors)').replace('ASCM vs peers', 'ASCM\\newline vs peers').replace('SDID vs peers', 'SDID\\newline vs peers')
# figures
def figenv(label, width):
    name, cap = CAP[label]; cap = cap.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_'); lab = label.replace('Appendix Figure ', 'A').replace('Figure ', 'F')
    pos = 'H' if label in ('Appendix Figure A4', 'Appendix Figure A7') else 'htbp'
    return f'\n\\begin{{figure}}[{pos}]\\centering\\includegraphics[width={width}\\textwidth]{{../figures/{name}.pdf}}\\caption{{{cap}}}\\label{{fig:{lab}}}\\end{{figure}}\n'
ia = tex.index('\\appendix'); head, app = tex[:ia], tex[ia:]
for label in sorted([l for l in CAP if not l.startswith('Appendix')], key=lambda x: int(x.split()[1])):
    m = re.search(re.escape(label) + r'(?![0-9])', head); end = head.find('\n\n', m.end()); head = head[:end] + figenv(label, 0.9) + head[end:]
place = {'Methods battery and bounds (feed)': ['Appendix Figure A1', 'Appendix Figure A2'], 'Randomization and Romano--Wolf': ['Appendix Figure A3'], 'Designation, exposure, compliance': ['Appendix Figure A4', 'Appendix Figure A5', 'Appendix Figure A6'], 'State capital and the memory makers': ['Appendix Figure A7']}
for sec, labels in place.items():
    i = app.index('\\section{' + sec); j = app.find('\n\\section{', i + 10); j = app.index('\\end{document}') if j < 0 else j
    app = app[:j] + ''.join(figenv(l, 0.7 if l in ('Appendix Figure A3', 'Appendix Figure A7') else 0.84) for l in labels) + '\n' + app[j:]
head = re.sub(r'\n\\section\{', r'\n\\FloatBarrier\\Needspace*{12\\baselineskip}\n\\section{', head); app = re.sub(r'\n\\section\{', r'\n\\FloatBarrier\\Needspace*{8\\baselineskip}\n\\section{', app); tex = head + app
pre = r'''\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}\usepackage{fontspec}\setmainfont{TeX Gyre Pagella}\usepackage{xcolor}\definecolor{house}{HTML}{6E0E18}
\usepackage{fancyhdr}\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small\itshape Where Export Controls Bind}\fancyhead[R]{\small\itshape Kyung and Kim (2026)}\fancyfoot[C]{\small\thepage}\renewcommand{\headrulewidth}{0.3pt}
\usepackage{setspace}\setstretch{1.15}\raggedbottom\usepackage{microtype}\usepackage{graphicx}\usepackage{booktabs,array,calc}\usepackage{arydshln}\setlength{\dashlinedash}{1pt}\setlength{\dashlinegap}{2pt}\setlength{\arrayrulewidth}{0.3pt}\renewcommand{\arraystretch}{1.35}\usepackage{caption}\captionsetup{font=small,labelfont={bf,color=house},justification=justified,singlelinecheck=false}
\usepackage{amsmath,amssymb}\usepackage[hidelinks]{hyperref}\usepackage{float}\usepackage{placeins}\usepackage{needspace}\usepackage{enumitem}\setlist{noitemsep,topsep=2pt}
\setcounter{topnumber}{3}\setcounter{bottomnumber}{3}\setcounter{totalnumber}{4}\renewcommand{\topfraction}{0.9}\renewcommand{\bottomfraction}{0.75}\renewcommand{\textfraction}{0.1}\renewcommand{\floatpagefraction}{0.85}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}\newcommand{\passthrough}[1]{#1}\setlength{\parskip}{4pt}\emergencystretch=2.5em\hyphenpenalty=200\tolerance=2000
\usepackage{titlesec}\titleformat{\section}{\large\bfseries\color{house}}{\thesection}{0.8em}{}\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.8em}{}\titlespacing{\section}{0pt}{14pt}{6pt}\titlespacing{\subsection}{0pt}{10pt}{4pt}
\begin{document}
\begin{titlepage}\thispagestyle{empty}\centering\vspace*{0.4cm}{\Large\bfseries\color{house} TITLE_HERE\par}\vspace{0.7cm}{\large Heekwon Kyung\textsuperscript{a} \quad Sanghoon Kim\textsuperscript{b}\par}\vspace{0.3cm}{\footnotesize \textsuperscript{a} Research Fellow, Korea Institute for Industrial Economics and Trade (KIET), Sejong, Republic of Korea; hee0718@kiet.re.kr; +82-44-287-3288 (corresponding author)\\ \textsuperscript{b} Senior Research Fellow, Korea Institute for Industrial Economics and Trade (KIET), Sejong; sanghoon\_kim@kiet.re.kr; +82-44-287-3181\par}\vspace{0.3cm}{\small Working paper, version 1 --- 25 October 2026\par}\vspace{0.6cm}
\begin{minipage}{0.92\textwidth}\begin{center}\textbf{Abstract}\end{center}\small\setstretch{1.0}ABSTRACT_HERE\vspace{0.35cm}\par\noindent\footnotesize\textbf{Keywords:} export controls; economic statecraft; weaponized interdependence; semiconductors; China; global value chains. \textbf{JEL:} F13, F51, F52, L63, O33, O38.\end{minipage}\vfill\end{titlepage}
'''
esc = lambda s: s.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_').replace('#', '\\#')
doc = pre.replace('TITLE_HERE', esc(title)).replace('ABSTRACT_HERE', esc(abstract)) + tex + '\n\\end{document}\n'
for a, b in {'有価証券報告書': 'yūka shōken hōkokusho', '长存控股': 'Changcun Holdings', '长鑫科技': 'Changxin Technology', '非经常性损益': 'non-recurring items', '主要会计数据': 'key accounting data', '招股说明书': 'prospectus'}.items(): doc = doc.replace(a, b)
doc = re.sub(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+', '', doc)
open('wp.tex', 'w', encoding='utf-8').write(doc); print("tex 생성 · 표", doc.count('\\begin{table}'), "· longtable 잔여", doc.count('longtable'), "· 그림", doc.count('\\begin{figure}'))
