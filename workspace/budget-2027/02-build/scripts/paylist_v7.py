"""v7 privacy helper (critic v6 O8): per-person compensation amounts, rounded to the nearest $5k in the md.

amounts(XLSX, RECON_JSON) -> list of {"v": float, "kind": str}
    Every per-person amount the notes could quote for an identified employee: annual salary, 2027 salary, and the
    2027 payroll tax / benefits / total at the roster's own rates and at the SD rates. Sources: the HC tabs (rows with
    an employee name; open seats and placeholders are not people), Fld Eng Budget rows 13-21 with a name, Fld Ops Payroll
    rows 76-77 (named), and the two Logistics&WH seats matched to a person by name (RECON_JSON). Names are read only to
    decide whether a row is a person; they are never returned, written or printed. Nothing is written to disk.
round_text(text, amounts) -> (text, n_replaced)
    Replaces each exact occurrence (0 or 2 decimals, with thousands separators) of an amount that is not already a
    multiple of 5,000 by '~' + the amount rounded to the nearest 5,000 ('<5,000' below 2,500).

Usage as a check:
  python3 -I paylist_v7.py XLSX RECON_JSON FILE [FILE ...]
Exit 1 if any FILE still holds an exact per-person amount; prints file, line and amount length only.
"""
import sys, re, json
import openpyxl

PLACEHOLDER = {"backfill", "tbd", "open", "new hire", "vacant"}


def _num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0


def _is_name(s):
    return isinstance(s, str) and s.strip() != "" and s.strip().lower() not in PLACEHOLDER


def amounts(xlsx, recon):
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    R = json.load(open(recon))
    feb, fop = wb["Fld Eng Budget"], wb["Fld Ops Payroll"]
    sd_t, sd_b = _num(feb["B22"].value), _num(feb["B23"].value)
    fo_t, fo_b = _num(fop["B7"].value), _num(fop["B8"].value)
    out = []

    def add(base, t, b, kind):
        out.extend([{"v": base, "kind": kind + " salary"}, {"v": base * t, "kind": kind + " tax"},
                    {"v": base * b, "kind": kind + " benefits"}, {"v": base * (1 + t + b), "kind": kind + " cost"}])

    for d in ("FO", "PO", "CO", "FE", "PE"):
        ws = wb[f"HC-{d}"]
        t, b = _num(ws["D6"].value), _num(ws["D7"].value)
        for r in range(14, 58):
            sal = ws.cell(r, 4).value
            if not isinstance(sal, (int, float)) or not _is_name(ws.cell(r, 2).value):
                continue
            z = _num(ws.cell(r, 26).value)
            out.append({"v": float(sal), "kind": "HC annual"})
            add(z, t, b, "HC 2027")
            add(z, sd_t, sd_b, "HC 2027 at SD rates")
    for r in range(13, 22):
        parts = [x.strip() for x in str(feb.cell(r, 1).value).split("–")]
        if len(parts) < 2 or not _is_name(parts[1]):
            continue
        out.append({"v": _num(feb.cell(r, 2).value), "kind": "FEB annual"})
        add(sum(_num(feb.cell(59 + r - 13, c).value) for c in range(2, 14)), sd_t, sd_b, "FEB 2027")
    for cell, row in (("H15", 76), ("H16", 77)):
        out.append({"v": _num(fop[cell].value), "kind": "FOP annual"})
        add(sum(_num(fop.cell(row, c).value) for c in range(6, 18)), fo_t, fo_b, "FOP 2027")
    for e in R["lw"]["seats"]:
        if e["overlap"]:
            out.append({"v": e["annual"], "kind": "LW annual"}); out.append({"v": e["cost_2027"], "kind": "LW cost"})
    return [a for a in out if abs(a["v"]) >= 1000]


def _forms(v):
    f = []
    if round(abs(v)) % 5000 != 0:
        f.append(f"{abs(v):,.0f}")
    if abs(abs(v) - round(abs(v) / 5000) * 5000) > 0.004:
        f.append(f"{abs(v):,.2f}")
    return f


def _r5(v):
    r = round(abs(v) / 5000) * 5000
    return "<5,000" if r == 0 else f"~{r:,.0f}"


def patterns(am):
    pats = {}
    for a in am:
        for s in _forms(a["v"]):
            pats[s] = _r5(a["v"])
    return sorted(pats.items(), key=lambda kv: -len(kv[0]))


# md sections that hold no per-person data (fleet depreciation, unit cost, revenue, DeploySum, GL variance table): numbers
# there that happen to equal a per-person amount are coincidences and are left alone (counted, not changed).
NO_PEOPLE = ("## Depreciation schedule summary", "## Unit-cost reconciliation", "## Revenue", "## DeploySum refresh",
             "### Variance scan")


def _blocks(text):
    """Split md text into (people_section: bool, chunk) keeping every character."""
    out, cur, flag = [], [], True
    for line in text.split("\n"):
        if line.startswith("## ") or line.startswith("### Variance scan"):
            if cur:
                out.append((flag, "\n".join(cur))); cur = []
            flag = not line.startswith(NO_PEOPLE)
        cur.append(line)
    out.append((flag, "\n".join(cur)))
    return out


def _rx(s):
    return re.compile(r"(?<![\d,.])" + re.escape(s) + r"(?![\d]|[.,]\d)")


def round_text(text, am, md=True):
    n = 0; parts = []
    for people, chunk in (_blocks(text) if md else [(True, text)]):
        if people:
            for s, rep in patterns(am):
                chunk, k = _rx(s).subn(rep, chunk)
                n += k
        parts.append(chunk)
    return "\n".join(parts), n


def find(text, am, md=True):
    hits, skipped, line0 = [], 0, 1
    for people, chunk in (_blocks(text) if md else [(True, text)]):
        for s, _ in patterns(am):
            for m in _rx(s).finditer(chunk):
                if people:
                    hits.append((line0 + chunk[:m.start()].count("\n"), len(s)))
                else:
                    skipped += 1
        line0 += chunk.count("\n") + 1
    return hits, skipped


if __name__ == "__main__":
    am = amounts(sys.argv[1], sys.argv[2])
    tot = sk = 0
    for f in sys.argv[3:]:
        hits, skipped = find(open(f, encoding="utf-8").read(), am, md=f.endswith(".md"))
        sk += skipped
        for line, ln in hits:
            tot += 1
            print(f"EXACT {f} line {line} (length {ln})")
    print(f"paylist_v7: {len(am)} per-person amounts ({len(patterns(am))} forms) checked in {len(sys.argv) - 3} files; "
          f"exact hits {tot}; coincidental equal numbers in non-people md sections (not changed) {sk}")
    sys.exit(1 if tot else 0)
