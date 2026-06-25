# AGENTS.md — SAP SD Knowledge Base (Chunking)

> Gobierno de ESTE proyecto. Antigravity lo lee de forma nativa (lo aplica cualquier
> modelo). Sustituye al antiguo par AGENTS.md → "lee CLAUDE.md primero": el núcleo ya
> no se carga por una instrucción que el agente puede ignorar, sino por `@import`,
> para que esté siempre presente. Las cinco no-negociables van además inline.

## Reglas globales que aplican

Este proyecto hereda las reglas universales de `biblio_skills/rules/` (instaladas en el
`GEMINI.md` global). No se repiten aquí. Instancias críticas en este proyecto:

- **03 (código sobre docs)** → el **validador es la única fuente de verdad** de la salud
  del corpus. Nunca reportar "0 errores" de memoria; correrlo.
- **06 (disciplina de razonamiento)** → **todo defecto es defecto de proceso**: al corregir
  un chunk, endurece el validador / la skill de fase / este AGENTS para que la clase de
  error no pueda recurrir. Un fix que no endurece el proceso está incompleto.
- **05 (cierre)** → además de commit + push, actualizar `chunks/_processing_log.md`.

## Núcleo del proyecto

```
@docs/PROJECT_RULES.md
```

(Antiguo `CLAUDE.md`, renombrado: objetivos, reglas preventivas root-cause, esquema de
chunk y frontmatter, provenance de campos de extracción, convención de placeholders,
arranque de sesión, densidad/rasterización, límites de sesión.)

> Si tu versión de Antigravity no resuelve el `@import`, el agente DEBE abrir
> `docs/PROJECT_RULES.md` en su totalidad antes de procesar cualquier chunk.

## Cinco reglas que no se saltan (no-negociables, inline)

1. **Provenance**: `transactions` y `tables` solo contienen identificadores que aparecen
   literalmente en el texto fuente o son legibles en una figura rasterizada. Nunca desde
   conocimiento de entrenamiento.
2. **Páginas físicas**: usar siempre el número físico de página del PDF, no la etiqueta
   del pie. Detectar el offset en el Paso 1 (`docs/playbooks/1-classify.md`).
3. **Mínimo 300 palabras**: cuerpo por debajo de 300 → fusionar con el chunk relacionado
   más cercano.
4. **Cross-references**: solo el ID del chunk en texto plano — sin backticks, comillas ni
   sintaxis de enlace markdown.
5. **Apéndice de back-matter**: escanear siempre las últimas 10–15 páginas de cualquier
   curso SAP buscando apéndices de T-codes/tablas antes de concluir que `transactions: []`
   es correcto (`docs/playbooks/2-extract.md`).

## Skills por fase

Tras leer el núcleo, lee la skill de la fase actual antes de ejecutarla:

| Fase | Fichero |
|---|---|
| Clasificar documento | `docs/playbooks/1-classify.md` |
| Extraer contenido del PDF | `docs/playbooks/2-extract.md` |
| Duplicados + decisión de chunking | núcleo (Pasos 3 y 4) |
| Validar chunk + actualizar estado | `docs/playbooks/5-validate-log.md` |
| Cerrar documento (gate de cobertura) | `docs/playbooks/6-coverage-review.md` |
| Primer chunk de una sesión nueva | además `docs/examples.md` |

## Validador (gate duro — ya alineado con biblio_skills/ci-templates)

Tras escribir cualquier chunk:

```bash
python3 validate_chunks.py chunks/<area>/<slug>-<NNN>.md
```

Cero ERRORs antes de actualizar el índice; los WARNINGs son advisory.

| Capa | Mecanismo | Bypass |
|---|---|---|
| Pre-commit local | `.githooks/pre-commit` | `--no-verify` (loguea bypass; CI lo caza igual) |
| GitHub Actions | `.github/workflows/validate.yml` (cada push/PR) | ninguno |

Bootstrap por clon (una vez): `git config core.hooksPath .githooks`.
Contrato: ERROR → exit 1 → commit bloqueado.

## Auditoría

`/audit-board docs/audit/audit_board_profile.md` ante los triggers de abajo. Proponer la
ejecución sin esperar a que el usuario la pida. La skill `audit-board` ahora es **global**
(en `biblio_skills`), no específica de este repo.

| Trigger | Tier |
|---|---|
| Tras cada documento procesado | Quick (ROL 2, 4, 6, 10) |
| ≥ 3 documentos nuevos o mensual | Standard (ROL 1, 2, 4, 5, 6, 7, 9, 10) |
| Trimestral / antes de integrar en RAG de producción | Full (ROL 1–12 + síntesis) |

Antes de ejecutar: actualizar `docs/audit/audit_context_shared.md`.

## Memoria y reproducibilidad (estándar biblio_skills)

- **`chunks/_processing_log.md`**: fuente de verdad del estado — documento actual, página pendiente, decisiones abiertas. Actualizar al cerrar cada sesión. Es la capa portable que un auditor externo lee desde GitHub.
- **`requirements.lock`** (nuevo): congelar el entorno Python. Las herramientas de sistema
  (`pdfinfo`, `pdftotext`, `pdffonts`, `pdftoppm` de poppler-utils) se documentan en
  Comandos.

## Comandos / restauración de entorno

```bash
# 1. Clonar
git clone <remote> && cd Chunking
git config core.hooksPath .githooks        # activar el gate local
# 2. Herramientas de sistema (Windows: instalar poppler; Linux: apt)
#    pdfinfo, pdftotext, pdffonts, pdftoppm
# 3. Entorno Python
python -m venv .venv && . .venv/Scripts/activate   # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.lock
# 4. Verificar
python3 validate_chunks.py chunks/   # o sobre un fichero concreto
```

## Paths

**Workspace-relativos.** No hardcodear rutas absolutas de una máquina (`c:\Users\...`):
rompen en otro PC. El `SOURCE_ROOT` se confirma y persiste en `chunks/_project_state.md`
(mecanismo de arranque de sesión del núcleo). Shell preferida: PowerShell; usar el bash
tool para POSIX.

## Límite de sesión

Primeras dos sesiones (calibración): máx. una unidad lógica o 5 chunks → parar y pedir
validación. Después: máx. un documento completo (o un bloque lógico en documentos >300
páginas). Registrar siempre la siguiente página pendiente en el log.
