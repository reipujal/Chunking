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

## Estado real medido (2026-06-08 — POST-REMEDIACIÓN; regenerado desde disco)

- **Total chunks en disco:** 74  — índice e inventario **sincronizados** (74/74).
- **Validador:** restaurado desde HEAD y **endurecido** (detecta NUL, cross-refs truncados/rotos como ERROR, sync disco↔índice). Resultado: **74 OK / 0 errores / 2 warnings**.
- **Quality dist:** 44 high / 30 medium.
- **Corrupción del proceso paralelo (reparada):** 5 chunks de pricing truncados a media escritura + 13 chunks adicionales corruptos (3 con bytes NUL, 10 con cross-ref truncado que el validador NO detectaba). Todos restaurados desde HEAD o completados. 0 NUL, 0 refs rotas corpus-wide.
- **git index.lock:** persiste (no liberable por permisos del FS montado); las reparaciones se hicieron por escritura directa de archivos, no por git. Falta `git commit` manual del usuario.

## Documentos procesados

| Documento | Fuente | Chunks (real) | Procesado por | Estado |
|---|---|---|---|---|
| S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf | S4615 | 31 | Claude | processed/ |
| S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf | S4610 | 15 | Claude | processed/ |
| S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf | S4605 | 18 | Codex + Claude re-read | processed/ |
| S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf | S4620 | 10 | Claude | completado; 0 errores; PDF en root (regla de inmutabilidad de fuente) |

---

## Hallazgos históricos — RE-VERIFICAR, NO ASUMIR (ver REGLA 12 / ROL 16)

> Estos NO son hechos: son afirmaciones a refutar. ROL 16 detectó una corrección fantasma (cash-sales) ya resuelta.
> Hasta que ROL 16 re-verifique cada fila, ningún "CORREGIDO" cuenta como evidencia.

| Fecha | Hallazgo | Estado declarado | Verificación 2026-06-08 |
|---|---|---|---|
| 2026-06-07 | S4605 extraído por Codex al 30-50% del texto | CORREGIDO (re-read) | no re-verificado |
| 2026-06-07 | Billing type en cash-sales-process-001 | declarado CORREGIDO (a BV) | RESUELTO 2026-06-08 — la "corrección" a BV era erronea: S4615 dice literalmente *billing document type CS*. Revertido a CS (fiel a fuente); discrepancia con la convencion BV de S4605 documentada en ambos chunks + cross-ref reciproco |
| 2026-06-07 | Workshop chunk prohibido | CORREGIDO (disuelto) | OK — no existe en disco |
| 2026-06-07 | 7 chunks quality:high con densidad 80-99 w/p | CORREGIDO (a medium) | validador endurecido marca high con 80-99 w/p como ERROR; settlement a medium |
| 2026-06-07 | relative_path sin "processed/" en 19 S4605 chunks | CORREGIDO | no re-verificado |
| 2026-06-07 | Billing generic tag false positive en validator | CORREGIDO (validator) | no re-verificado |

---

## Gaps conocidos (no corregibles sin nuevos PDFs)

| Gap | Prioridad |
|---|---|
| Credit management (0 chunks en área) | ALTA |
| ATP / availability check | MEDIA |
| Output determination | MEDIA |
| Returns end-to-end desde nivel pedido | MEDIA |
| Pricing procedure / condition technique | CUBIERTO (S4620 — 10 chunks) |

---

## Reglas de CLAUDE.md más recientes

- **Active voice**: no "The source/course states" en body text
- **SPRO no-tcode**: "Not stated in source." — 5 palabras máximo
- **Questions answered**: cada pregunta listada debe responderse en el body
- **Alias specificity**: no aliases genéricos de una sola palabra
- **Quality 80-99 w/p**: quality:medium sin excepciones (validador lo fuerza como ERROR)
- **Case 3b**: order type ≠ delivery type ≠ billing type (verificar coherencia interna)
