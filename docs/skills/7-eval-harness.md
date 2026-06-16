# Skill 7 — Retrieval Eval Harness (document close gate)

> **Cuándo leer:** después de Skill 6 (coverage review), antes de marcar el documento como `completed`.
> Obligatorio para cada documento procesado. No requiere chunks nuevos — solo el PDF en `docu sap/processed/`.

## Por qué existe

"0 errores + coverage OK" mide calidad estructural, no calidad de recuperación. El eval harness mide si el TF-IDF baseline puede recuperar el chunk correcto cuando se pregunta sobre el contenido del documento. Un recall@10 bajo señala: aliases pobres, body sin léxico funcional, o chunks mal particionados.

Anti-circularidad: las preguntas vienen de las secciones "Learning Assessment" escritas por SAP, **nunca** sintetizadas desde los chunks.

## Prerequisito: usar Bash tool (no PowerShell)

`pdftotext` está en `/mingw64/bin/` (MINGW64/Git Bash), no en el PATH de PowerShell. Siempre ejecutar desde el **Bash tool**, con `cd` al workspace primero.

## Comando estándar

```bash
cd "c:/Users/aranu/Desktop/IA/Chunking"
python3 eval/extract_assessments.py --src [SRC]
python3 eval/score.py --src [SRC]
```

Sustituir `[SRC]` por la clave del documento: `S4600`, `S4605`, `S4610`, `S4615`, `S4620`, etc.

**Salidas:**
- `eval/gold/[SRC]_assessments.json` — gold set (preguntas + gold_page_span)
- `eval/results/[SRC]_YYYY-MM-DD.md` — informe de métricas
- `eval/results/[SRC]_YYYY-MM-DD.json` — datos crudos

## Qué miden las métricas

| Métrica | Qué indica |
|---|---|
| recall@1 | El chunk correcto está en el primer resultado |
| recall@5 | El chunk correcto está entre los 5 primeros |
| recall@10 | El chunk correcto está entre los 10 primeros |
| MRR | Rango recíproco medio del primer hit correcto |

El gold es a nivel de **unidad** (indulgente): cualquier chunk cuyas `sources[].pages` solapan el rango físico de la unidad cualifica. Recall@10 es un techo, no la calidad real de RAG con embeddings.

## Umbrales de referencia (TF-IDF baseline, corpus SD)

| Métrica | Saludable | Investigar |
|---|---|---|
| recall@1 | ≥ 55% | < 45% |
| recall@5 | ≥ 80% | < 70% |
| recall@10 | ≥ 90% | < 80% |
| MRR | ≥ 0.70 | < 0.60 |

Referencia establecida por S4600–S4620 (sesión 2026-06-16).

## Preguntas no-mapeables (not-mappable)

Una pregunta es no-mapenable si ningún chunk cita páginas de `[SRC]` que solapen su `gold_page_span`.

**Causas esperadas (no acción):**
- Páginas de esa unidad delegadas a otro documento más profundo (p.ej. S4600-U2 → cubierto por S4605).
- Unidades de sólo 2-3 páginas de introducción nunca chunkeadas.
- Siempre justificadas en la coverage table o processing log.

**Causas que requieren acción:**
- Unidad con contenido funcional extenso y 0 chunks en ese rango de páginas → gap real; aplicar Skill 6.

## Preguntas sin `answer_key_found`

En algunos documentos, las preguntas de texto libre (sin opciones T/F ni MCQ) se excluyen automáticamente — comportamiento correcto. Ejemplo: S4605 tiene 11 excluidas (preguntas abiertas tipo "¿Cuántos niveles tiene un documento de ventas?").

El campo `correct` no afecta a recall/MRR; sólo importa para métricas de exactitud (no implementadas todavía).

## Notas por documento

| Documento | Offset | Notas de extracción |
|---|---|---|
| S4600 | +8 | 13 no-mapeables: U2, U3, U5 delegados a S4605/S4610. Esperado. |
| S4605 | +8 | 11 excluidas (preguntas abiertas sin opciones). 0 no-mapeables. |
| S4610 | +6 | Formato "That's correct." (corregido en extractor 2026-06-16). 0 no-mapeables. |
| S4615 | +8 | 5 no-mapeables: U1-U2 phys 9-17 (intro, no chunkeadas). Gap menor. |
| S4620 | +6 | 1 no-mapeable: U9 Appendix API content (intencional). |

## Resultados corpus SD (baseline 2026-06-16)

| Documento | Q | Mapeables | recall@1 | recall@5 | recall@10 | MRR |
|---|---|---|---|---|---|---|
| S4620 | 28 | 26 | 61.5% | 96.2% | 100.0% | 0.755 |
| S4600 | 36 | 21 | 57.1% | 85.7% | 95.2% | 0.718 |
| S4605 | 42 | 31 | 61.3% | 93.5% | 96.8% | 0.747 |
| S4610 | 26 | 26 | 61.5% | 92.3% | 92.3% | 0.727 |
| S4615 | 35 | 30 | 70.0% | 83.3% | 90.0% | 0.762 |

## Integración en el cierre de documento

Paso en el flujo estándar (después de Skill 6):

```
Skill 5 (validar + batch audit)
  → Skill 6 (coverage review)
    → Skill 7 (eval harness)
      → marcar completed en _source_inventory.md
```

En el processing log, añadir entrada:
```
## [SRC] — Eval harness ([fecha])
recall@1=[X]%  recall@5=[X]%  recall@10=[X]%  MRR=[X.XXX]
Mapeables: [N]/[M]  Not-mappable: [K] ([razón])
```

## Extender a nuevos documentos

Cuando se procese un documento nuevo (p.ej. S4650):

```bash
python3 eval/extract_assessments.py --src S4650
python3 eval/score.py --src S4650
```

Si el extractor detecta offset incorrecto (los bloques LA no coinciden con el contenido esperado de las unidades), verificar con `pdftotext` manual y añadir el offset real a la tabla de Skill 6 y a `_source_inventory.md`.
