# Tarea para agente (Sonnet): cerrar el gap de cobertura del Unit 13 de S4605

## Contexto
Eres el agente de chunking del proyecto SAP SD. Antes de tocar nada, **lee en este orden**: `AGENTS.md`, `CLAUDE.md` (completo — presta atención a las *Preventive Rules*), `docs/skills/2-extract.md`, `docs/skills/5-validate-log.md` y `docs/examples.md`.

Estás corrigiendo un **defecto de pérdida de contenido**, no procesando un documento nuevo. En una sesión previa, el chunk `sales-workshop-scenarios-001` se creó y luego se "disolvió" por la regla anti-workshop, pero la disolución **eliminó el contenido en vez de fusionarlo**. El análisis de cobertura (`docs/audit/analisis_estrategia_pdf_a_chunk_2026-06-08.md`) confirma que las páginas físicas **154-165** de S4605 quedaron sin cobertura.

No repitas el error: el objetivo es **recuperar** ese contenido funcional, no volver a crear un chunk-workshop prohibido.

## Fuente
- PDF: `docu sap/processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf`
- Offset: etiqueta impresa = página física − 8. **Cita siempre páginas FÍSICAS.**
- Unit 13 — Sales Workshop, físicas **p.153-165**, con tres escenarios:
  1. **Sales-to-Employee** (~p.154-158): cuenta colectiva de cliente único (one-time customer), pedidos solo con valor neto, descuento de empleado ~15%, sin ATP ni transferencia de necesidades, factura como recibo.
  2. **Bill of Material (BOM) en ventas** (~p.159-164): explosión de BOM en el pedido, componentes como sub-ítems del ítem principal, determinación de item category por sub-ítem, determinación de schedule line dependiente del item category.
  3. **Material Determination** (~p.165): ya existe `master-data-material-determination-001`.

## Decomposición recomendada (propónla y AJÚSTALA tras leer la fuente; aplica Step 4 de CLAUDE.md)
- **BOM en ventas** → **nuevo chunk** (es un tema SD sustancial sin cobertura). Área probable `order-management` o `configuration`, `chunk_type: process` o `concept`. Solo si el cuerpo supera 300 palabras con extracción completa; si no, fusiónalo en `configuration-sales-item-category-control-001` (sub-ítems/item category) con cross-ref.
- **Sales-to-Employee** → fusionar el contexto funcional en `special-processes-sales-special-business-transactions-001` (mismo carácter de "proceso especial"). Crea chunk propio solo si supera 300 palabras de forma coherente y autónoma.
- **Material Determination (p.165)** → fusiona cualquier contexto útil del escenario en `master-data-material-determination-001`; **no** crees un chunk nuevo.

## Restricciones duras (NO negociables)
1. **Provenance.** `transactions`/`tables` solo con tokens que aparezcan literalmente en el texto extraído. El Unit 13 es conceptual: lo esperable es `transactions: []` y `tables: []`. Lo relevante-pero-no-nombrado va en comentario `<!-- inferred -->` en el body, nunca en el campo.
2. **Sin pérdida de contenido.** Estás reparando exactamente ese fallo. Cada hecho funcional de p.154-165 debe acabar en un chunk o quedar justificado en el log.
3. **Write-integrity (crítico en este workspace).** Un file-watcher trunca escrituras in-place. **Escribe atómico**: genera el contenido en `/tmp`, muévelo a `chunks/...`, y **re-lee** el archivo para confirmar que persistió completo (sin truncar, sin bytes NUL, con la sección `## Cross-References` cerrada).
4. **Una sola sesión.** No lances procesos en paralelo sobre este workspace.
5. **Calidad ganada, no por defecto.** Calcula densidad (w/p); aplica la banda de extraction-ratio (0,5–1,5) de la nueva fase 6c.
6. **Cross-References** obligatorias y con IDs reales (sin backticks/comillas). En cualquier chunk que modifiques, actualiza `last_updated` a la fecha de hoy.

## Flujo
1. Extrae p.153-165 con `pdftotext -layout -f 153 -l 165`. Detecta páginas VISUAL (skill 2) y rasteriza solo esas si hace falta.
2. **Presenta el plan de chunking** (qué chunk nuevo, qué fusiones, páginas e intención de búsqueda) y **espera confirmación** antes de escribir (CLAUDE.md Step 4).
3. Escribe/actualiza los chunks (atómico + re-lectura).
4. **Cierre (Skill 6 — `docs/skills/6-coverage-review.md` + Skill 5):**
   - `python3 validate_chunks.py chunks/` → **0 errores** obligatorio.
   - Ejecuta el coverage-map (Step 6c) sobre S4605 y confirma que **ya no quedan páginas ≥100w sin cubrir** en 154-165 (salvo justificación explícita).
   - Regenera `chunks/_index.md` desde disco con el script (no a mano).
   - Añade entrada a `chunks/_processing_log.md` (qué se recuperó, decisiones de fusión, páginas, por qué).
   - Actualiza la nota de S4605 en `chunks/_source_inventory.md` (gap Unit 13 cerrado).
5. **Resumen final:** chunks creados/actualizados, cobertura antes/después, y validación en 0 errores.

## Criterio de "hecho"
Validador en 0 errores **y** coverage-map sin páginas de contenido sin justificar en 154-165 **y** ningún hecho funcional del Unit 13 perdido.
