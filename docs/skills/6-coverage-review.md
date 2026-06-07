# Skill 6 — Source-Coverage Review (document close gate)

> **Cuándo leer:** después de escribir todos los chunks de un documento y de pasar Skill 5 (validar + batch audit), **antes** de marcar el documento como `completed`. También como pasada retroactiva para documentos chunkeados antes de que existiera este gate.

## Por qué existe

"0 errores del validador" ≠ "documento completo". La densidad (palabras/página) mide la riqueza *interna* de un chunk, no si el contenido del documento se capturó ni si el chunk es fiel al volumen de su fuente. Este gate mide dos cosas que ninguna otra fase mide:
- **Cobertura:** ¿qué páginas con contenido real no entraron en ningún chunk?
- **Fidelidad de extracción:** ¿el chunk tiene un volumen razonable respecto a sus páginas fuente?

Es el cierre del **objetivo 1** (chunks óptimos) por documento. Token-eficiente: el triaje mira solo las páginas marcadas, nunca re-lee el PDF entero.

## Placeholders (sustituir antes de ejecutar)

- `DOC` = ruta del PDF (p.ej. `docu sap/processed/S4610_…pdf`)
- `SRC` = clave de fuente que aparece en `sources[].file` (p.ej. `S4610`)
- Offset: S46xx → etiqueta impresa = física − 8. **Citar siempre páginas FÍSICAS.**

## Step A — Cribado (coverage-map + extraction-ratio)

```bash
python3 - <<'PYEOF'
import subprocess, re, yaml
from pathlib import Path
DOC="docu sap/processed/[exact PDF].pdf"   # substitute
SRC="[S46xx]"                              # substitute
pages=subprocess.run(["pdftotext","-layout",DOC,"-"],capture_output=True,text=True).stdout.split("\f")
pw=[len(p.split()) for p in pages]
covered=set(); ratios=[]
for c in Path('chunks').rglob('*.md'):
    if c.name.startswith('_'): continue
    t=c.read_text(encoding='utf-8',errors='replace'); fm=yaml.safe_load(t.split('---',2)[1])
    if not any(SRC in s.get('file','') for s in (fm.get('sources') or [])): continue
    body=len(t.split('---',2)[2].split()); pr=[]
    for src in fm['sources']:
        for seg in str(src.get('pages','')).split(','):
            m=re.match(r'(\d+)-(\d+)',seg.strip())
            if m: pr+=list(range(int(m.group(1)),int(m.group(2))+1))
            elif seg.strip().isdigit(): pr.append(int(seg.strip()))
    covered|=set(pr); sw=sum(pw[i-1] for i in pr if 1<=i<=len(pw))
    if sw: ratios.append((round(body/sw,2),fm['id']))
unc=[(i+1,w) for i,w in enumerate(pw) if w>=100 and (i+1) not in covered]
cl=[]
for pg,w in unc:
    if cl and pg==cl[-1][-1]+1: cl[-1].append(pg)
    else: cl.append([pg])
print(f"{SRC}: covered {len(covered)}/{len(pw)} pages")
print("  uncovered >=100w clusters (>=3p):", [(c[0],c[-1]) for c in cl if len(c)>=3])
print("  ratio <0.5 (under):", sorted([r for r in ratios if r[0]<0.5]))
print("  ratio >1.5 (review):", sorted([r for r in ratios if r[0]>1.5]))
PYEOF
```

## Step B — Triaje (barato; NO re-leer el PDF entero)

Para cada cluster, `pdftotext -layout -f A -l B "$DOC" -` SOLO esas páginas. Aplica:

**Cluster de páginas no cubiertas (≥3 consecutivas, ≥100w):**
- Cabecera "Learning Assessment" / opciones A·B·C·D / "Choose the correct answer" → **skip legítimo**. Justifícalo en el log; NO crear chunk.
- Cover / TOC / "Course Overview" / solo objetivos de unidad → **skip legítimo**.
- Contenido funcional real (definiciones, pasos, customizing, escenarios de workshop con sustancia) → **GAP REAL**.

**Outlier de extraction-ratio:**
- `<0.5` (sub-extracción) → abre el chunk y re-lee SUS páginas; si omitió contenido sustancial, expándelo (fiel, en tus palabras).
- `>1.5` → ¿las páginas citadas son figura/tabla (texto escaso, contenido rico)? Si la prosa **describe** la figura/tabla → legítimo (lo espera el protocolo de rasterización); anótalo. Si añade afirmaciones **no presentes en la fuente** → recorta o marca `<!-- inferred -->`. Solo revisa outliers **extremos** (>3); ignora 1,5–2,5 salvo sospecha.

## Step C — Actuar sobre los GAPS REALES (regla workshop/merge)

- Si ya existe un chunk para ese concepto → **fusiona** el detalle ahí (cross-ref + `last_updated` a hoy). No dupliques.
- Si no existe y el contenido supera 300 palabras autónomas → crea un chunk propio (área + `chunk_type` correctos).
- **Nunca** un chunk-workshop multi-tema. **Nunca** elimines contenido al "corregir" (regla de preservación de contenido).
- Provenance: `transactions`/`tables` solo tokens literales; lo demás en `<!-- inferred -->`.
- **Escritura atómica** (el watcher trunca in-place): escribe a `/tmp`, mueve a `chunks/…`, **re-lee** para confirmar (sin truncar, sin NUL, `## Cross-References` cerrada).

## Step D — Re-cribar y cerrar

1. Re-ejecuta Step A → no debe quedar ningún cluster ≥100w sin cubrir **ni justificar**.
2. `python3 validate_chunks.py chunks/` → **0 errores**.
3. Regenera `_index.md` desde disco con script (Skill 5).
4. `_processing_log.md`: entrada de coverage (gaps cerrados, skips justificados con motivo, decisiones de fusión).
5. `_source_inventory.md`: registra coverage final (p.ej. `covered 145/168`).

## Criterio de "hecho"

Validador 0 errores **y** cada cluster ≥100w o bien chunkeado o bien **justificado en el log con motivo** **y** outliers de ratio triados **y** log + inventario actualizados. Solo entonces el documento es `completed`.
