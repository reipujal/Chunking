# Audit Context Shared — SAP SD Knowledge Base
## Regenerar antes de cada auditoría

---

## Estado del corpus (actualizar antes de cada ejecución)

```bash
cd c:/Users/aranu/Desktop/IA/Chunking
python3 validate_chunks.py 2>&1 | tail -8
python3 -c "
import re, yaml
from pathlib import Path
chunks = list(Path('chunks').rglob('*.md'))
chunks = [c for c in chunks if not c.name.startswith('_')]
wcs, quals = [], {}
for c in chunks:
    txt = c.read_text(encoding='utf-8')
    body = txt.split('---', 2)
    if len(body) < 3: continue
    try: fm = yaml.safe_load(body[1])
    except: continue
    wc = len(body[2].split())
    pages_str = str(fm.get('sources', [{}])[0].get('pages', '1'))
    parts = pages_str.split('-')
    pages = abs(int(parts[1])-int(parts[0]))+1 if len(parts)==2 else 1
    wcs.append(wc/max(pages,1))
    quals[fm.get('quality','?')] = quals.get(fm.get('quality','?'),0)+1
print(f'Total chunks: {len(chunks)}')
print(f'Density mean: {sum(wcs)/len(wcs):.0f} w/p')
print(f'Quality dist: {quals}')
"
```

---

## Documentos procesados

| Documento | Fuente | Chunks | Procesado por | Estado |
|---|---|---|---|---|
| S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf | S4615 | ~18 | Claude | processed/ |
| S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf | S4610 | ~11 | Claude | processed/ |
| S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf | S4605 | ~18 | Codex + Claude re-read | processed/ |
| S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf | S4620 | 10 | Claude | pending move to processed/ |

---

## Hallazgos históricos conocidos (para contexto, no para reabrir)

| Fecha | Hallazgo | Estado |
|---|---|---|
| 2026-06-07 | S4605 extraído por Codex al 30-50% del texto disponible | CORREGIDO (re-read completo) |
| 2026-06-07 | Billing type CS incorrecto en cash-sales-process-001 | CORREGIDO (→ BV) |
| 2026-06-07 | Workshop chunk prohibido (CLAUDE.md violation) | CORREGIDO (disuelto) |
| 2026-06-07 | 7 chunks quality:high con densidad 80-99 w/p | CORREGIDO (→ medium) |
| 2026-06-07 | relative_path sin "processed/" en 19 S4605 chunks | CORREGIDO |
| 2026-06-07 | Billing generic tag false positive en validator | CORREGIDO (validator) |

---

## Gaps conocidos (no corregibles sin nuevos PDFs)

| Gap | Prioridad |
|---|---|
| Pricing procedure / condition technique | ALTA |
| Credit management (0 chunks en área) | ALTA |
| ATP / availability check | MEDIA |
| Output determination | MEDIA |
| Returns end-to-end desde nivel pedido | MEDIA |

---

## Reglas de CLAUDE.md más recientes (añadidas 2026-06-07)

- **Active voice**: no "The source/course states" en body text
- **SPRO no-tcode**: "Not stated in source." — 5 palabras máximo
- **Questions answered**: cada pregunta listada debe responderse en el body
- **Alias specificity**: no aliases genéricos de una sola palabra
- **Quality 80-99 w/p**: quality:medium sin excepciones
- **Case 3b**: order type ≠ delivery type ≠ billing type (verificar coherencia interna)
