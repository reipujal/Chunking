# Tarea para agente (Sonnet): pasada retroactiva de cobertura — 4 documentos procesados

## Por qué
S4605, S4610, S4615 y S4620 se chunkearon **antes** de que existiera el source-coverage gate (CLAUDE.md *Preventive Rule 6* / `docs/skills/5-validate-log.md` Step 6c). Ninguno lo pasó. Esta es una **pasada retroactiva única** para llevarlos al objetivo 1 (chunks óptimos) y, de paso, validar el gate como proceso repetible (objetivo 2).

No es reprocesar de cero: es **detectar y cerrar gaps reales sin tocar lo que ya está bien**, gastando los mínimos tokens.

## Lee primero (en orden)
`AGENTS.md`, `CLAUDE.md` (completo, atención a *Preventive Rules*), `docs/skills/2-extract.md`, `docs/skills/5-validate-log.md` (Step 6c), `docs/examples.md`, y para método/estado: `docs/audit/analisis_estrategia_pdf_a_chunk_2026-06-08.md` y `docs/audit/audit_context_shared.md`.

## Pre-vuelo (ROL 0 — bloqueante)
Antes de empezar: `python3 validate_chunks.py chunks/` debe dar **0 errores**; disco↔índice↔inventario sincronizados; sin `.git/index.lock`; **una sola sesión** sobre este workspace. Si algo falla, detente y reporta solo eso.

## Offsets de página (citar SIEMPRE páginas FÍSICAS)
Todos los S46xx: etiqueta impresa = física − 8.
PDFs: `docu sap/processed/S4605_…pdf`, `…/S4610_…pdf`, `…/S4615_…pdf`, `…/S4620_…pdf` (los cuatro en `processed/`).

## Procedimiento por documento (orden: S4610 → S4605 → S4615 → S4620)
1. **Cribado:** ejecuta el script coverage-map + extraction-ratio de `5-validate-log.md` Step 6c (sustituye DOC y SRC). Da: clusters de páginas ≥100w no cubiertas, y ratios body/fuente fuera de 0,5–1,5.
2. **Triaje (barato):** para cada item marcado, `pdftotext -layout -f A -l B` SOLO esas páginas. Aplica el árbol de decisión de abajo. No re-leas el PDF entero.
3. **Worklist:** clasifica cada item en {gap real → acción} o {falso positivo → justificar en log}.
4. **Presenta worklist + plan de chunking y espera confirmación** (CLAUDE.md Step 4) antes de escribir.
5. **Ejecuta:** crea/fusiona chunks (escritura **atómica**: a `/tmp`, mover, **re-leer** para confirmar persistencia sin truncar/NUL/`## Cross-Re` cortado). Provenance limpia.
6. **Re-cribado:** vuelve a correr el script; confirma que no queda ningún cluster ≥100w sin cubrir **ni justificar**.
7. **Cierre:** validador 0 errores → regenera `_index.md` desde disco con script → entrada en `_processing_log.md` ("pasada retroactiva de cobertura: …") → actualiza coverage en `_source_inventory.md`.

## Árbol de triaje (NO re-leer PDFs completos)
**Cluster de páginas no cubiertas (≥3 consecutivas, ≥100w):**
- Cabecera con "Learning Assessment" / opciones A·B·C·D / "Choose the correct answer" → **skip legítimo**; justifícalo en el log; NO crear chunk.
- Cover / TOC / "Course Overview" / solo objetivos de unidad → **skip legítimo**.
- Contenido funcional real (definiciones, pasos de proceso, customizing) → **GAP REAL**. Regla workshop/merge: si ya existe un chunk para ese concepto, **fusiona** el detalle ahí (cross-ref + `last_updated`); si no existe y supera 300 palabras autónomas, crea un chunk propio. **Nunca** un chunk-workshop multi-tema.

**Outlier de extraction-ratio:**
- `<0.5` (sub-extracción) → abre el chunk y re-lee SUS páginas citadas; si omitió contenido sustancial, expándelo (fiel, en tus palabras).
- `>1.5` → mira si las páginas citadas son figura/tabla (texto escaso, contenido rico). Si la prosa **describe** lo que muestra la figura/tabla → legítimo (el protocolo de rasterización lo espera); anótalo. Si la prosa añade afirmaciones **que no están en la fuente** → recorta o marca `<!-- inferred -->`. **Solo** revisa outliers extremos (>3); ignora 1,5–2,5 salvo sospecha.

## Worklist sembrada (cribado 2026-06-08 — punto de partida; VERIFICA, no confíes)
- **S4610** (cobertura 49/89): CANDIDATO REAL p.19-23 ("Maintaining Organizational Units for Delivery" — shipping point detail; verifica si está cubierto por `enterprise-structure-shipping-point-loading-point-001` (cita p.13) o si se perdió detalle → fusiona). Verifica también cluster p.66-68. Resto: esperar muchas páginas de Learning Assessment.
- **S4605** (145/169): GAP REAL Unit 13 p.154-165 (BOM en ventas + venta a empleados + material-determination scenario). Detalle en `docs/audit/prompt_sonnet_unit13_coverage.md` — **incorpóralo aquí**, no lo corras por separado para evitar doble sesión.
- **S4615** (71/132): clusters 36-39, 71-74 verificados = Learning Assessment (skip, justificar). 119-121 verifica. Ratios altos = chunks de figuras; **solo** mira los extremos (billing-document-integration ~6,3; document-table-structure ~4,1; flexible-billing ~5,9) para confirmar que la prosa es descripción de figura, no invención.
- **S4620** (106/129): limpio; sin outliers de ratio. Verifica/justifica clusters 116-118 y 123-126 (probable Learning Assessment). Esperado: 0 chunks nuevos.

## Restricciones duras
Provenance literal (`transactions`/`tables` solo tokens del texto; lo demás en `<!-- inferred -->`). Páginas físicas. Escritura atómica + re-lectura (watcher trunca). Sin pérdida de contenido. Una sesión. Cross-References con IDs reales sin backticks. Calidad ganada (densidad + banda de ratio). `last_updated` a hoy en todo chunk tocado.

## Criterio de "hecho" (los 4 documentos)
Validador 0 errores **y** cada cluster ≥100w o bien chunkeado o bien **justificado en el log con motivo** **y** outliers de ratio triados **y** `_processing_log.md` con una entrada de pasada por documento **y** coverage registrada en `_source_inventory.md`.

## El procedimiento ya es skill
Este cribado+triaje+cierre está codificado en **`docs/skills/6-coverage-review.md`** (gate de cierre estándar). Síguela como referencia canónica; este prompt solo añade la worklist sembrada y el orden de los 4 documentos. A partir de ahora, Skill 6 corre como paso de cierre de cada documento futuro, así que esta pasada retroactiva es de una sola vez.
