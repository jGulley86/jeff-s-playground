#!/bin/bash
# Usage: recalc.sh IN_XLSX OUT_DIR PROFILE_DIR
# Headless LibreOffice round-trip with a private profile that forces a full
# recalculation of OOXML files on load (OOXMLRecalcMode=0 "always").
set -euo pipefail
IN="$1"; OUT="$2"; PROF="$3"
mkdir -p "$PROF/user" "$OUT"
cat > "$PROF/user/registrymodifications.xcu" <<'XCU'
<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="OOXMLRecalcMode" oor:op="fuse"><value>0</value></prop></item>
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="ODFRecalcMode" oor:op="fuse"><value>0</value></prop></item>
</oor:items>
XCU
/usr/bin/soffice -env:UserInstallation=file://"$PROF" --headless --norestore --convert-to xlsx:"Calc MS Excel 2007 XML" --outdir "$OUT" "$IN"
