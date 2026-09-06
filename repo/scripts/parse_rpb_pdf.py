import pdfplumber, json
p="/root/.claude/uploads/cd5ad460-f011-5f57-9752-a3e1e8911ee0/c9952254-RPB_for_Team_Rapid_Release__BT__Week_2_BT_in_3_24_00_on_Sun_Sep_06_2026_01_54_14_GMT0200_Central_European_Summer_Time_in_Black_Temple_.pdf"
pdf=pdfplumber.open(p)
out={}
for pi in (0,1):
    pg=pdf.pages[pi]
    words=pg.extract_words(use_text_flow=False, keep_blank_chars=False)
    # group by line (top)
    lines={}
    for w in words:
        key=round(w['top'],0)
        # merge near tops
        placed=False
        for k in list(lines):
            if abs(k-key)<=2.5:
                lines[k].append(w); placed=True; break
        if not placed: lines[key]=[w]
    ordered=sorted(lines.items())
    # header line = first
    hdr=sorted(ordered[0][1], key=lambda w:w['x0'])
    cols=[(w['text'], (w['x0']+w['x1'])/2) for w in hdr]
    print(f"--- PAGE {pi} cols:", [c[0] for c in cols])
    res=[]
    for top,ws in ordered[1:]:
        ws=sorted(ws,key=lambda w:w['x0'])
        # label = words left of first column start
        firstcolx=hdr[0]['x0']-15
        label=" ".join(w['text'] for w in ws if w['x1']<=firstcolx)
        vals={}
        for w in ws:
            if w['x1']<=firstcolx: continue
            cx=(w['x0']+w['x1'])/2
            best=min(cols,key=lambda c:abs(c[1]-cx))
            vals.setdefault(best[0],[]).append(w['text'])
        if label:
            res.append((round(top),label,{k:" ".join(v) for k,v in vals.items()}))
    out[pi]=(cols,res)
    for top,label,vals in res[:60]:
        print(f"{top:5} | {label[:55]:55} | {vals}")
