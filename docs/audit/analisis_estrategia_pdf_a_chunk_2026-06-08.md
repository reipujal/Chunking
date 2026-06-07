# Análisis empírico de estrategia: PDF→chunk (S4605 como caso)

> 2026-06-08. Validación que faltaba en el análisis inicial: cómo un documento SAP real se transforma en chunks, y si la estrategia es óptima para los dos objetivos (chunks óptimos + proceso industrializado).

## Caso medido: S4605 (Sales Processes), 168 páginas, 23.315 palabras, 18 chunks

### Cobertura fuente→chunk
- **145 de 168 páginas físicas** quedan dentro de algún rango citado por un chunk.
- **13 páginas con contenido (≥100 palabras) NO cubiertas.** Dos son front-matter (p.2, p.5, aceptable). **Las otras 11 (p.154-165) son el Unit 13 — Sales Workshop**: escenarios *Sales-to-Employee* y *Bill of Material (BOM) en ventas*.
- El log dice que el chunk `sales-workshop-scenarios-001` se "disolvió" por la regla anti-workshop. Pero la disolución **eliminó el contenido** en lugar de fusionarlo en chunks existentes, como exige la propia regla. Resultado: **BOM en ventas y venta a empleados quedaron sin cobertura** — una regresión de cobertura causada por una "corrección". Mismo anti-patrón que cash-sales: una corrección que degrada.

### Ratio de extracción (palabras del chunk / palabras del PDF en su rango)
Rango observado: **0,48 a 2,98**.
- **Baja (0,48-0,61):** `sales-order-source-of-data` (0,48), `value-contracts` (0,53), `sd-partner-functions` (0,61). Posible sub-extracción: el chunk capturó <60% del volumen de la fuente.
- **Alta (2,98):** `sales-document-technical-tables` (524 palabras de chunk vs 176 en la fuente — apéndice de tablas). Una fuente terса expandida 3x: riesgo de prosa no respaldada/inflación.

## Diagnóstico de estrategia

**1. La métrica de calidad mide lo que no toca.** El gate usa densidad interna del chunk (palabras/página). Pero un chunk puede pasar el gate con (a) 48% de extracción de su fuente, o (b) 3x el volumen de la fuente. **Ni la cobertura del documento ni la fidelidad al volumen de la fuente se miden.** Para un RAG generado *desde documentos*, esas dos señales son más relevantes que w/p. → Corregido: nueva regla 6 en CLAUDE.md + fase 6c en skill 5 (coverage-map + extraction-ratio).

**2. "0 errores" no significa "documento completo".** S4605 pasa el validador con 11 páginas de contenido funcional perdidas. El concepto de "completado" en el inventario era prematuro.

**3. Las correcciones degradan en silencio.** Dos casos confirmados (workshop → pérdida de contenido; cash-sales → token contradiciendo la fuente). Sin un check de preservación de contenido, "arreglar" puede empeorar.

## Por qué no estamos más cerca del objetivo 2 (proceso industrializado)

Los artefactos (chunks) avanzaron; el **proceso** apenas. Evidencia:
- ~40% del esfuerzo es re-trabajo (ROL 12), y esta sesión añadió la reparación de 18 archivos corruptos por concurrencia.
- Cada defecto se cazó **reactivamente** (revisión adversaria), no se previno: hasta hoy, los hallazgos no actualizaban CLAUDE.md/skills, así que las clases de error reaparecían (truncación, correcciones fantasma, pérdida de contenido).
- El gate medía lo incorrecto (densidad, no cobertura/fidelidad), dando falsa sensación de "completo".
- Estado manual no derivado (índice a mano, dedup por grep) que se desincroniza y no escala.
- El coste en tokens por documento no se controla: re-lecturas completas, múltiples rondas de corrección y re-validación lo multiplican.

Conclusión: hemos estado **artesaneando chunks y parcheando defectos**, no construyendo y endureciendo un proceso repetible. Por eso 4 documentos no nos acercan al pipeline industrial: el objetivo 1 (chunks) progresa lineal; el objetivo 2 (proceso) solo progresa si cada defecto endurece las reglas — que es lo que se ha incorporado ahora.
