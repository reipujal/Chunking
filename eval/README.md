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

## Resultados Stage 0 — S4620 (TF-IDF baseline, 2026-06-16)

| recall@1 | recall@3 | recall@5 | recall@10 | MRR |
|----------|----------|----------|-----------|-----|
| 61.5% | 88.5% | 96.2% | 100.0% | 0.755 |

- 28 preguntas extraídas · 1 excluida (ordering, sin opciones) · 1 no mapeada (Unit 9 Appendix — API integration no chunkeada)
- El baseline léxico ya alcanza 100% recall@10 — confirma que el corpus cubre bien el material
- Área débil: `configuration` recall@1=37.5% (mejor a @5=100%) — las queries de config son menos específicas léxicamente

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

---

## Próximos pasos (Stage 1+)

- [ ] Afinar gold a nivel de lección (sub-span dentro de la unidad)
- [ ] Añadir más documentos: `python eval/extract_assessments.py --src S4615`
- [ ] Swapear retriever por embeddings y comparar con el baseline TF-IDF
- [ ] MCQ-accuracy (Stage 2): `answer(question, context) -> letter` con LLM reader
