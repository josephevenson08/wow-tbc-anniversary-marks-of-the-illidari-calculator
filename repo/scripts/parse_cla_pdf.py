import pdfplumber
p="/root/.claude/uploads/cd5ad460-f011-5f57-9752-a3e1e8911ee0/f3795261-CLA_for_Team_Rapid_Release__BT__Week_2_BT_in_3_24_00_on_September_06_2026_01_54_14_in_Black_Temple.pdf"
pdf=pdfplumber.open(p)
for pi in (1,2):
    pg=pdf.pages[pi]
    ws=pg.extract_words()
    lines={}
    for w in ws:
        k=round(w['top']/4)
        lines.setdefault(k,[]).append(w)
    print(f"===== PAGE {pi}")
    for k in sorted(lines):
        row=sorted(lines[k],key=lambda w:w['x0'])
        print(" ".join(f"{w['text']}@{round(w['x0'])}" for w in row)[:900])
