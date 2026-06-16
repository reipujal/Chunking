# Eval — Retrieval Harness for SAP SD Chunking

Subsistema de medición independiente del gate de validación.
**No está cableado a pre-commit ni a CI** — un recall no es pass/fail binario.

---

## Cómo correr

```bash
# 1. Extraer gold set de un documento (solo hace falta una vez por doc)
python eval/extract_assessments.py --src S4620

# 2. Calcular métricas contra el corpus actual
python eval/score.py --src S4620
```

Los resultados se escriben en `eval/results/<SRC>_<fecha>.md` y `.json`.

Para un PDF en ruta explícita:
```bash
python eval/extract_assessments.py --src S4620 --pdf "docu sap/processed/S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
```

---

## Arquitectura

```
eval/
  extract_assessments.py   # PDF -> gold JSON (preguntas del Learning Assessment de SAP)
  retriever.py             # interfaz retrieve(query, k) + baseline TF-IDF
  score.py                 # gold + retriever -> recall@k, MRR, informe
  gold/<SRC>_assessments.json
  results/<SRC>_<fecha>.md  (.json)
  README.md
```

---

## Contrato: gold = span de páginas físicas (anti-circularidad)

Las preguntas salen **únicamente** de las secciones "Learning Assessment" del PDF (escritas por SAP).
El `gold_page_span` es el rango de páginas físicas del contenido de la unidad que la pregunta evalúa —
**no** la página donde aparece la pregunta, **no** un chunk_id.

La pertenencia a chunk se deriva mecánicamente en `score.py` (solape de páginas):
```
gold_chunk_ids = chunks cuyo sources[].file contiene SRC
                 Y cuyo sources[].pages solapa gold_page_span
```

Esto garantiza que el gold set sobrevive a re-chunkings futuros.

---

## Esquema del gold JSON

```json
{
  "doc": "S4620",
  "pdf_relative_path": "processed/S4620_EN_Col17...",
  "offset": 6,
  "generated_at": "2026-06-16",
  "total_physical_pages": 129,
  "questions": [{
    "id": "S4620-LA-U3-Q2",
    "unit": "Unit 3: Condition Records",
    "question": "You can create new pricing condition records today for next year.",
    "options": {},
    "question_type": "tf",
    "correct": "True",
    "answer_key_found": true,
    "answer_explanation": "You can create pricing condition records ...",
    "gold_page_span": [39, 49],
    "mappable": true,
    "excluded": false,
    "exclude_reason": "",
    "notes": ""
  }]
}
```

Páginas son siempre **físicas** (= footer + offset). El frontmatter de los chunks también usa páginas físicas.

---

## Métricas

| Métrica | Definición |
|---------|-----------|
| recall@k | 1 si algún gold-chunk está en el top-k; 0 si no |
| MRR | 1/rango del primer gold-chunk en top-10; 0 si ninguno |

Agregación: global + por área + por chunk_type.

---

## Resultados — TF-IDF baseline (2026-06-16)

| Documento | Q | Mapeables | recall@1 | recall@5 | recall@10 | MRR |
|-----------|---|-----------|----------|----------|-----------|-----|
| S4620 | 28 | 26 | 61.5% | 96.2% | 100.0% | 0.755 |
| S4600 | 36 | 21 | 57.1% | 85.7% | 95.2% | 0.718 |
| S4605 | 42 | 31 | 61.3% | 93.5% | 96.8% | 0.747 |
| S4610 | 26 | 26 | 61.5% | 92.3% | 92.3% | 0.727 |
| S4615 | 35 | 30 | 70.0% | 83.3% | 90.0% | 0.762 |

**Notas por documento:**
- S4620: 1 no mapeada (Unit 9 Appendix — API integration intencionalmente no chunkeada)
- S4600: 13 no mapeadas — Units 2, 3, 5 delegadas a S4605/S4610 (esperado)
- S4605: 11 excluidas (preguntas abiertas sin opciones T/F/MCQ) · 0 no mapeadas
- S4610: formato "That's correct." (vs "Correct.") — corregido en extractor 2026-06-16 · 0 no mapeadas
- S4615: 5 no mapeadas — Units 1-2 phys 9-17 (intro, no chunkeadas)

**Patrón general:** recall@1 estable en ~60-70%; recall@5 > 85%; recall@10 > 90%.
El baseline léxico es robusto para el corpus SD con su léxico SAP especializado.
Área débil estructural: `configuration` (recall@1 ~37-50%) — queries de customizing son menos específicas léxicamente.

---

## Limitaciones conocidas

1. **Gold a nivel de unidad** (indulgente): cualquier chunk que cite cualquier página de la unidad
   es gold para todas las preguntas de esa unidad. El recall es optimista.
   Afinar a nivel de lección es el siguiente paso (Stage 1).

2. **Retriever TF-IDF** (léxico): es el suelo, no el techo. Swappable: implementar
   `retrieve()` con embeddings y re-correr `score.py` sin tocar el gold.

3. **Offset crítico**: si el offset se detecta incorrectamente, los page spans son erróneos
   y los gold_chunk_ids también. El offset se verifica en el log de extracción.

4. **Preguntas con `correct=None`**: se incluyen en el eval de retrieval (no necesitan
   correct para recall/MRR). Solo son relevantes para MCQ-accuracy (Stage 2).

5. **MCQ multi-respuesta**: el heurístico de inferencia de `correct` devuelve una sola letra
   incluso en preguntas "choose the correct answers" (plural). Afecta solo a la futura
   accuracy — no al retrieval.

6. **Preguntas abiertas (S4605 et al.)**: preguntas sin opciones T/F ni MCQ se excluyen
   automáticamente — son correctas pero no evaluables con el heurístico actual.

---

## Próximos pasos (Stage 1+)

- [ ] Afinar gold a nivel de lección (sub-span dentro de la unidad)
- [ ] Extender a S4650/S4680 cuando se procesen
- [ ] Swapear retriever por embeddings y comparar con el baseline TF-IDF
- [ ] MCQ-accuracy (Stage 2): `answer(question, context) -> letter` con LLM reader
