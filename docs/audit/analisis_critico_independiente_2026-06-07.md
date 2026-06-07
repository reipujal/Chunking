# Análisis crítico independiente — Proyecto Chunking SAP SD

> Estado capturado: 2026-06-07, 74 chunks en disco.
> Metodología: evidencia directa (validador, grep, lectura de archivos). Realizado **antes** de usar el framework de audit del proyecto, para no heredar sus puntos ciegos.
> Postura: adversarial. El objetivo es romper el proyecto, no validarlo.

---

## 0. Veredicto en una línea

El corpus *parece* sano —el índice y el inventario reportan "0 errores"— pero esa señal es **falsa**: el gate de calidad es frágil y se evalúa de memoria, el estado del repositorio está roto en este momento, y el proceso genera defectos a un ritmo comparable al que los corrige. La presentación supera a la sustancia.

Clasificación de severidad: `(Inmediata)` bloquea la siguiente sesión · `(Corto)` antes del próximo milestone · `(Largo)` antes de producción.

---

## 1. Integridad operacional — BLOQUEANTE `(Inmediata)`

Esta capa no la cubre el audit del proyecto y es la más grave **ahora mismo**.

**1.1 El validador está roto.** `validate_chunks.py` en el working-tree termina truncado a media instrucción (`failed = len(results`, línea 559) → `SyntaxError`. El **único gate automático del proyecto no ejecuta**. Cualquier "0 errores" reportado en este estado es ficción. La versión de `HEAD` sí parsea; el árbol de trabajo quedó a medio reescribir.

**1.2 Repositorio en estado inconsistente.** Existe un `.git/index.lock` que no se puede liberar (`Operation not permitted`) y ~70 archivos sin commitear. El `git diff --stat` muestra churn casi **simétrico** (6.611 inserciones / 6.705 eliminaciones) en archivos que esta sesión no debía tocar (chunks de S4610/S4615). Eso es la firma de una **normalización masiva** (line-endings/encoding) que entierra los cambios reales bajo ruido — el historial de git deja de ser auditable.

**1.3 Las tres fuentes de verdad del estado se contradicen entre sí:**

| Fuente | Dice | Realidad |
|---|---|---|
| disco | 74 chunks | — |
| `_index.md` | 64–65 filas (cambiaba mientras corría) | desincronizado |
| `_source_inventory.md` | S4620 "not started" | 10 chunks de S4620 ya en disco |
| `audit_context_shared.md` | S4615 "~18 chunks" | son 31 |

Ningún artefacto de estado es fiable como referencia.

**1.4 Concurrencia sin control.** Lanzar un segundo proceso en paralelo corrompió simultáneamente el validador, el índice y dejó el git-lock. No hay convención de "una sesión a la vez" ni locking. Esto **volverá a pasar**: es un fallo estructural, no un accidente.

---

## 2. Fidelidad y provenance — CRÍTICO `(Inmediata)`

**2.1 Contradicción factual entre dos chunks sobre el mismo proceso.** Cash sales está descrito en dos chunks con tokens divergentes y sin la sección `## Differences from [version]` que el propio CLAUDE.md exige (Caso 2/3):

- `special-processes/cash-sales-process-001.md` (fuente S4615): order type **CS**, output **RD03**, billing update **BV**, cancelación **SV**.
- `special-processes/sales-special-business-transactions-001.md` (fuente S4605): cash sale con delivery type **BV** y billing type **BV**.

Esto viola la *golden rule* "un concepto = un chunk por versión SAP". Un consultor que recupere uno u otro obtiene historias distintas.

**2.2 El Caso 3b (confusión de rol de token) sigue vivo.** En `cash-sales-process-001.md`, CS se introduce como *order type* (línea 39) pero en Common Errors (líneas 71 y 74) se le llama **"the CS billing type"**. CLAUDE.md prohíbe esto explícitamente (order type ≠ billing type). El defecto que su propia regla nombra como ejemplo está presente en el corpus.

**2.3 Corrección fantasma — el hallazgo más peligroso.** `audit_context_shared.md` registra: *"Billing type CS incorrecto en cash-sales-process-001 → CORREGIDO (→ BV)"*. **El defecto persiste.** El registro de correcciones afirma un saneamiento que no ocurrió. Esto es peor que el bug en sí: invalida la confianza en **todo** el log de correcciones. Si una corrección verificada-como-hecha no se hizo, ¿cuántas otras tampoco?

**2.4 Sospecha factual contra estándar SAP.** El cash sale estándar en SAP usa el tipo de documento **BV** (Barverkauf) como order type, delivery type y billing type; *CS* no es el order type estándar de cash sale. La versión S4605 (BV en todo) es coherente con el estándar; la versión S4615 ("order type CS") es la anómala. Acción: verificar contra el PDF S4615 físico. Si el source imprime "CS", documentar la divergencia; si no, es una **alucinación que sobrevivió a 4 rondas de revisión adversaria**.

---

## 3. Arquitectura del sistema de chunking — riesgo de diseño `(Corto)`

**3.1 La deduplicación por grep no escala y falla en silencio.** El método "grep antes de crear" depende de que el agente adivine los términos correctos. Es O(n) manual, sin garantía. Ya a 74 chunks hay solape (cash sales en 2 chunks; "free goods" tocado en 5 archivos). El propio ROL 12 del audit admite que la carga de deduplicación crece; a 150+ chunks la inconsistencia es **estructural, no accidental**.

**3.2 El paradigma "un documento = una pasada" incentiva duplicar.** El mismo proceso (cash sale) se chunkea dos veces porque aparece en S4605 y S4615, y nada fusiona ambas. El diseño premia la fragmentación por fuente en lugar de la consolidación por concepto.

**3.3 ID acoplado a la carpeta de área.** Mover un chunk de área rompe su ID lógico (`{area}-{slug}-{NNN}`) y todos los cross-refs que lo apuntan. No hay tooling de rename; la reclasificación es manual y propensa a romper el grafo.

---

## 4. Diseño RAG / retrieval `(Corto)`

**4.1 `quality` ≈ densidad (w/p) es un proxy pobre de utilidad de recuperación.** El gate optimiza palabras-por-página, no si el chunk responde la query. Riesgo de incentivo perverso: para superar el umbral de 100 w/p se "expande" el cuerpo. El log muestra `avg 262 → ~530 palabras` tras "expansión" en S4615 — hay que distinguir señal (contenido faltante recuperado del PDF) de **relleno para pasar el gate**. La métrica no puede distinguirlos; un humano tendría que muestrear.

**4.2 5 nodos aislados** (`pricing-condition-contract-*`, `pricing-special-pricing-functions-001`, `configuration-pricing-procedure-configuration-001`, …) no son referenciados por ningún hermano. Solo se alcanzan por embedding directo: si el embedding falla para esa query, el contenido es **inaccesible**.

**4.3 `_index.md` mantenido a mano** se desincroniza del disco (ya ocurrió: 74 vs 64). El índice debería *derivarse* del disco con un script, nunca editarse manualmente. Un índice que miente sobre qué existe envenena cualquier proceso downstream que lo consuma.

---

## 5. Schema y validador — punto único de fallo `(Corto)`

El validador es la única garantía de calidad del proyecto, y como tal concentra el riesgo:

**5.1 Frágil por construcción.** (a) Puede quedar roto sin que nadie lo note (§1.1); (b) se ejecuta a mano, sin CI ni pre-commit hook; (c) tiene huecos conocidos —el propio audit (`part_schema_gov`) documenta que **no** marca `quality:high` con densidad 80–99 w/p (solo <80), contradiciendo la regla explícita de CLAUDE.md.

**5.2 Mensajería contradictoria / redondeo engañoso.** En `pricing-condition-contract-settlement-001`: *"quality:high requires >=100 w/p; this chunk has 100 w/p … expand to >=100"*. El valor real es 799/8 = 99,875, redondeado a "100" en el display. El mensaje pide expandir a ≥100 mientras afirma que ya tiene 100. Calibración confusa.

**5.3 El árbitro no es determinista.** Las dos versiones del validador (HEAD vs working-tree) emiten **veredictos distintos sobre el mismo corpus**: HEAD marca "Missing Cross-References"; el working-tree marca "DENSITY+QUALITY". Qué es un "error" depende de qué copia del validador corras.

**5.4 La salud se reporta de memoria, no del validador.** El índice/inventario publican "0 errores" mientras el corpus real tiene 5 FAIL / 6 errores ahora mismo (Cross-References ausente en 4 chunks de pricing, densidad+quality en otros). La métrica de salud está **desconectada de la herramienta que la mediría**.

---

## 6. Gobernanza y proceso `(Corto/Largo)`

**6.1 El framework de auditoría está roto en origen.** `audit_board_profile.md` declara `Framework: ~/.claude/skills/audit-board/FRAMEWORK.md`, que **no existe** en el entorno. El comando documentado `/audit-board` no es invocable tal cual. El audit funciona solo porque un LLM improvisa los roles desde el profile, no porque el framework exista.

**6.2 La última auditoría no se cerró.** Hay 2 part-files de hoy (`part_contenido_rag`, `part_schema_gov`) pero **sin síntesis ni executive summary**, y `audit_context_shared.md` no se regeneró (sigue diciendo S4615 "~18"). Un audit a medias da una falsa sensación de cobertura.

**6.3 Human-in-the-loop ficticio.** Todos los chunks están `status: draft` "pending human/revisor review", pero no hay revisor: el agente se auto-aprueba en rondas adversarias sucesivas. 4 rondas de "adversarial review" y defectos como el de §2.2 sobreviven. La revisión adversaria automatizada **no sustituye** la validación funcional humana que el propio proyecto dice necesitar.

**6.4 El proceso es parcialmente net-negative.** El ROL 12 estima que ~40% del esfuerzo es post-corrección. Hay sesiones (Codex extrayendo 30–50% del texto) que introdujeron defectos cuya corrección costó más que la generación inicial. Métrica a vigilar: defectos-corregidos / defectos-introducidos por sesión. Si se acerca a 1, el proyecto camina en círculos.

---

## 7. Cobertura `(Largo)` — confirmo el audit existente

37% en top-10 queries; `credit-management/` con 0 chunks; third-party e intercompany a 0. Ya cuantificado por ROL 10. No lo reabro: el diagnóstico de cobertura del audit es sólido y no necesita endurecerse — necesita ejecutarse contra los PDFs pendientes (S4600 para credit management primero).

---

## 8. Los tres riesgos existenciales

1. **El gate de calidad miente.** Validador que puede estar roto + métricas reportadas de memoria + correcciones fantasma (§2.3) → el corpus puede declararse "listo para producción RAG" sin estarlo. Es el riesgo más grave porque desactiva todos los demás controles.
2. **Concurrencia sin locking** → corrupción de estado recurrente y reproducible (§1.4).
3. **Dedup manual que no escala** → a 150 chunks el corpus se vuelve inconsistente por construcción (§3.1), justo cuando empieza a tener valor.

---

## 9. Acciones mínimas antes de seguir procesando

1. `(Inmediata)` Restaurar `validate_chunks.py` desde HEAD, re-validar el corpus completo, y **arreglar los 5 FAIL de pricing** (Cross-References + densidad/quality). Hasta entonces, ninguna sesión nueva.
2. `(Inmediata)` Resolver el git-lock y commitear con un diff limpio; investigar y revertir la normalización masiva de line-endings si no fue intencional.
3. `(Inmediata)` Verificar cash sales contra los PDFs S4605 **y** S4615; reconciliar en un solo chunk con `## Differences from` o corregir el token erróneo. Auditar el resto del log de correcciones por más "correcciones fantasma".
4. `(Corto)` Generar `_index.md` con un script desde el disco; prohibir su edición manual.
5. `(Corto)` Añadir al validador: detección de `quality:high` con 80–99 w/p, y un check de sincronía disco↔índice↔inventario.
6. `(Corto)` Definir política de concurrencia (lockfile de sesión) y de cierre de audit (síntesis obligatoria + regeneración de context).
