# SAP SD Knowledge Base — Chunking Agent

## Rutas del proyecto

| Variable | Valor |
|---|---|
| **Workspace** | `c:\Users\aranu\Desktop\IA\Chunking` |
| **Carpeta fuente PDFs** | `c:\Users\aranu\Desktop\IA\Chunking\docu sap` |
| **Chunks output** | `c:\Users\aranu\Desktop\IA\Chunking\chunks\` |
| **Shell preferida** | PowerShell (Windows) — usar Bash tool para comandos POSIX |

> En comandos bash del protocolo, el directorio de trabajo es siempre el workspace.
> Las rutas `chunks/` son relativas al workspace.

---

## Arranque obligatorio de cada sesión

Ejecuta esto en orden. No saltes pasos.

### 1. Orientación en el filesystem

```bash
pwd
ls -la
cat chunks/_processing_log.md 2>/dev/null | tail -40 || echo "Log vacío"
cat chunks/_index.md 2>/dev/null | head -40 || echo "Índice vacío"
```

### 2. Localizar carpeta fuente

```bash
mapfile -t ROOTS < <(find . -maxdepth 5 -type d -name "docu sap" 2>/dev/null | sort -u)
printf '%s\n' "${ROOTS[@]}"
echo "Total encontrados: ${#ROOTS[@]}"
```

Busca solo dentro del directorio de trabajo actual. No sale del proyecto.
Si los PDFs no están dentro del workspace, el usuario debe moverlos
antes de continuar.

Interpreta el resultado:
- 0 resultados: detente. Informa al usuario y pide que confirme la ruta
  o que mueva los ficheros dentro del workspace.
- 1 resultado: muéstralo al usuario y pide confirmación antes de asignar.
- Más de 1: muéstralos todos, pide al usuario que elija explícitamente.

No asignes SOURCE_ROOT hasta tener confirmación explícita del usuario.
No continúes sin SOURCE_ROOT confirmado.

```bash
# Solo después de confirmación:
SOURCE_ROOT="[ruta confirmada por el usuario]"

# Verificar que la ruta es resoluble en este shell (forward slashes)
# En Git Bash/WSL usar /c/Users/... no C:\Users\...
[ -d "$SOURCE_ROOT" ] || { echo "ERROR: ruta no resoluble — usa forward slashes (/c/Users/...) no backslashes"; exit 1; }
echo "SOURCE_ROOT: $SOURCE_ROOT"

# Garantizar que chunks/ existe antes de escribir estado
mkdir -p chunks
touch chunks/_index.md chunks/_processing_log.md chunks/_source_inventory.md

# Persistir en Bash puro — sin dependencia de Python en este paso crítico
printf "source_root: '%s'\nconfirmed_at: '%s'\n" "$SOURCE_ROOT" "$(date +%Y-%m-%d)" > chunks/_project_state.md
echo "SOURCE_ROOT guardado en chunks/_project_state.md"
cat chunks/_project_state.md
```

Al arrancar una sesión nueva, si existe `chunks/_project_state.md`:
```bash
# Leer SOURCE_ROOT guardado
python3 -c "
import yaml
state = yaml.safe_load(open('chunks/_project_state.md'))
print('SOURCE_ROOT previo:', state.get('source_root'))
print('Confirmado el:', state.get('confirmed_at'))
" 2>/dev/null || grep "source_root:" chunks/_project_state.md
```
Muestra el SOURCE_ROOT guardado, propón reutilizarlo al usuario y espera
confirmación explícita antes de continuar. No lo asumas automáticamente.

### 3. Verificar herramientas

```bash
for tool in pdfinfo pdftotext pdffonts; do
  command -v "$tool" >/dev/null 2>&1 && echo "OK: $tool" || echo "FALTA: $tool"
done
command -v pdftoppm >/dev/null 2>&1 && echo "OK: pdftoppm" || echo "OPCIONAL FALTA: pdftoppm"
command -v python3 >/dev/null 2>&1 && echo "OK: python3" || echo "OPCIONAL FALTA: python3"
```

- Si falta `pdfinfo`, `pdftotext` o `pdffonts`: detente. Explica qué falta y para qué sirve.
- Si falta `pdftoppm`: puedes procesar texto, pero no documentos Tipo B visuales.
- Si falta `python3`: el script de regeneración de índice no estará disponible.

### 4. Inventariar fuentes

```bash
find "$SOURCE_ROOT" -type f -iname "*.pdf" | sed "s|$SOURCE_ROOT/||" | sort
find "$SOURCE_ROOT" -type f -iname "*.pdf" | wc -l
```

### 5. Presentar propuesta al usuario

Después de los pasos anteriores presenta:
- Cuántos PDFs hay en SOURCE_ROOT y su listado
- Qué documentos ya están procesados según el log
- Una propuesta concreta: "Propongo procesar [documento] porque [motivo]. ¿Confirmas?"

No hagas preguntas abiertas. Una propuesta específica, espera confirmación.

---

## Reglas absolutas

**Lectura permitida:**
- `$SOURCE_ROOT` y sus subcarpetas
- `chunks/`
- `/tmp/` solo para temporales generados por el agente

**Escritura permitida:**
- `chunks/`
- `/tmp/` solo para temporales

**Prohibido:**
- Modificar, mover, renombrar ni borrar documentos fuente
- Sobrescribir chunks existentes sin confirmación explícita
- Inventar contenido no soportado por la fuente
- Copiar texto literal extenso de documentación SAP
- Crear chunks duplicados sobre el mismo tema
- Escribir outputs finales fuera de `chunks/`

---

## Estructura de output

Crear estructura de directorios (mkdir -p es idempotente — seguro en cualquier sesión):

```bash
for area in enterprise-structure master-data order-management pricing shipping billing credit-management configuration integration special-processes; do
  mkdir -p "chunks/$area"
done
touch chunks/_index.md chunks/_processing_log.md chunks/_source_inventory.md
```

```
chunks/
├── _index.md
├── _processing_log.md
├── _source_inventory.md
├── _project_state.md       ← SOURCE_ROOT confirmado y fecha de inicio
├── enterprise-structure/
├── master-data/
├── order-management/
├── pricing/
├── shipping/
├── billing/
├── credit-management/
├── configuration/
├── integration/
└── special-processes/
```

---

## Prioridad de documentos

### Alta — procesar primero
```
S4600_EN_Col17  Business Processes in SAP S4HANA Sales
S4601_EN_Col17  Business Processes in SAP S4HANA Supply Chain Execution
S4605_EN_Col17  Sales Processes in SAP S4HANA Sales
S4610_EN_Col17  Delivery Processing in SAP S4HANA
S4615_EN_Col17  Billing in SAP S4HANA Sales
S4620_EN_Col17  Pricing in SAP S4HANA Sales
S4650_EN_Col17  Cross-Functional Topics in SAP S4HANA Sales
S4680_EN_Col17  Cross-Application Processes in SAP S4HANA Sales and Procurement
SD - Shipment.pdf
Variant Configuration with SAP.pdf
SAP FI-MM-SD INTEGRATION A SPECIAL REPORT
Transportation Management with SAP TM
```

### Media — procesar después
```
S4F30_EN_Col12 Order to Cash Optimizations
TSCM60, TSCM62 y sus partes   → marcar sap_release: "ECC 6.0"
Diagramas de proceso (Tipo B): BD6, BDD, BKA, BDA, BKL, BDQ, BJE, BKZ, BD9
```

### Baja — solo si no duplica contenido de prioridad alta
```
__SAP SD.pdf
SD - User Manual.pdf
sap_sd_tutorial / sap-sd-training-tutorial
Sales and Distribution in SAP ERP Practical Guide
```

### Omitir por defecto (salvo instrucción expresa del usuario)
```
certification questions / material
dumps / sample certification
pdfcoffee certification
sap-s-4hana-sales-dumps
```

---

## Paso 1 — Clasificar el documento

> ⚠️ **Contexto de shell**: Si `$SOURCE_ROOT` está vacía (nuevo subproceso), recupérala antes de continuar:
> ```bash
> SOURCE_ROOT=$(python3 -c "import yaml; print(yaml.safe_load(open('chunks/_project_state.md'))['source_root'])" 2>/dev/null || grep "source_root:" chunks/_project_state.md | awk -F"'" '{print $2}')
> [ -d "$SOURCE_ROOT" ] || { echo "ERROR: SOURCE_ROOT no resoluble — confirma con el usuario"; exit 1; }
> ```

```bash
DOC="$SOURCE_ROOT/[nombre].pdf"

pdfinfo "$DOC"
pdffonts "$DOC" | head -10
pdftotext -f 1 -l 4 "$DOC" - 2>/dev/null | head -120

# Ratio palabras/página — muestrea desde p.30 para evitar portada, copyright e índice
# Los manuales SAP tienen 15-20 páginas de preámbulo con densidad muy baja
pages=$(pdfinfo "$DOC" 2>/dev/null | awk '/^Pages:/{print $2}')
[ -z "$pages" ] && { echo "ERROR: pdfinfo no devuelve nº de páginas — PDF cifrado, dañado o export inválido"; exit 1; }
sample_start=$(( pages > 30 ? 30 : (pages > 10 ? 10 : 1) ))
sample_end=$(( pages < (sample_start + 15) ? pages : (sample_start + 15) ))
sample_words=$(pdftotext -f "$sample_start" -l "$sample_end" "$DOC" - 2>/dev/null | wc -w)
sample_pages=$(( sample_end - sample_start + 1 ))
echo "Ratio muestra (págs $sample_start-$sample_end): $((sample_words / sample_pages)) palabras/página"
```

| Tipo | Nombre | Criterio | Estrategia |
|---|---|---|---|
| A | Curso oficial SAP | Prefijo S4600-S4680, TSCM60/62; >200 palabras/página | Extraer por capítulos/unidades |
| A* | Documento mixto | 80-200 palabras/página → tratar como Tipo A con detección de páginas visuales activada (sección mixtos en Paso 2) | Extraer texto + rasterizar páginas visuales |
| B | Slide deck visual | "Process Diagrams" en nombre, o <80 palabras/página | Rasterizar con pdftoppm |
| C | Manual comunidad | "User Manual", "tutorial", "training", BBP | Extraer, validar calidad antes |
| D | Especializado | "Shipment", "Variant Config", "FI-MM-SD", "Transportation" | Igual que Tipo A |
| E | Certificación/dumps | "certification", "dumps", "sample questions" | Omitir por defecto |

**Nota para corpus HTML→PDF (exports de Edge/Chromium):**
`pdfinfo` mostrará `Producer: Skia/PDF` u otro engine de Chromium.
En ese caso, las heurísticas de palabras/página son indicios, no criterios definitivos.
Confirma el tipo visualmente rasterizando 2-3 páginas representativas antes de proceder.
Documenta el origen en `_source_inventory.md` (Producer del pdfinfo).

Comunica al usuario antes de continuar:
```
Documento: [nombre]
Tipo: [A/B/C/D/E]
Páginas: N
Ratio: N palabras/página
Texto extraíble: alto/medio/bajo
Propuesta: procesar [sección/rango] porque [motivo]. ¿Confirmas?
```

---

## Paso 2 — Extraer contenido

> ⚠️ **Contexto de shell**: Si `$SOURCE_ROOT` está vacía (nuevo subproceso), recupérala antes de continuar:
> ```bash
> SOURCE_ROOT=$(python3 -c "import yaml; print(yaml.safe_load(open('chunks/_project_state.md'))['source_root'])" 2>/dev/null || grep "source_root:" chunks/_project_state.md | awk -F"'" '{print $2}')
> [ -d "$SOURCE_ROOT" ] || { echo "ERROR: SOURCE_ROOT no resoluble — confirma con el usuario"; exit 1; }
> ```

### Tipo A, C, D — Documentos con texto

**Regla de extracción**: nunca más de 30 páginas en una sola llamada.
Extraer bloques mayores satura el contexto y degrada las decisiones
de chunking (efecto "Lost in the Middle").

**Primera vez con cualquier documento Tipo A, C o D: mapear el índice**
```bash
pdftotext -f 1 -l 12 "$DOC" - | head -250
```
Identifica capítulos, títulos y páginas. Anota el mapa antes de continuar.
Este paso no aplica a documentos Tipo B — tienen estructura visual, no textual.
Para Tipo B, pasa directamente a la sección de rasterización.

**Extracción por bloques de máximo 30 páginas**
```bash
pdftotext -layout -f [inicio] -l [fin] "$DOC" /tmp/bloque.txt
wc -w /tmp/bloque.txt
head -80 /tmp/bloque.txt
```

**Ruido a ignorar:** cabeceras/pies ("© SAP SE", números de página),
marcas de agua ("For Internal Use Only"), referencias a diapositivas
("As shown in the figure above").

**Si el texto tiene encoding roto** (señales: `Ã©`, `â€™`):
```bash
pdftoppm -jpeg -r 150 -f [pagina] -l [pagina] "$DOC" /tmp/pagina_rota
ls /tmp/pagina_rota-*.jpg
```
Si el entorno permite inspección visual, lee la imagen.
Si no permite inspección visual: no inventes el contenido.
Registra la página como no procesada en el log y márcala para
revisión posterior. No crees el chunk hasta poder revisar visualmente.

### Tipo B — Slide decks visuales

```bash
# Limpiar y crear carpeta específica para este documento
DOC_SLUG="$(basename "$DOC" .pdf | tr ' ' '-' | tr -cd '[:alnum:]-_')"
rm -rf "/tmp/slides-$DOC_SLUG"
mkdir -p "/tmp/slides-$DOC_SLUG"

# Rasterizar en bloques de 30 páginas máximo — igual que la extracción de texto
# Nunca rasterices todo el documento de golpe
pages=$(pdfinfo "$DOC" | awk '/^Pages:/ {print $2}')
echo "Total páginas: $pages — rasterizar en bloques de 30"

# Primer bloque (ajusta [inicio] y [fin] según el bloque a procesar):
pdftoppm -jpeg -r 150 -f [inicio] -l [fin] "$DOC" "/tmp/slides-$DOC_SLUG/page"
ls "/tmp/slides-$DOC_SLUG/"
```

Procesa un bloque, analiza las imágenes, extrae el conocimiento,
luego avanza al siguiente bloque. Mismo principio que la extracción de texto.

Si el entorno permite inspección visual, lee cada imagen extrayendo:
- Transacciones SAP visibles
- Campos clave en pantallas SAP GUI
- Anotaciones textuales superpuestas
- Flujo implícito entre pantallas

Si no permite inspección visual: registra el documento como
`bloqueado` en `_source_inventory.md` y consulta al usuario.

Un documento Tipo B se divide por proceso o subproceso funcional,
no por documento ni por slide:
- No crees un chunk por slide.
- No fuerces un único chunk por documento.
- Crea un chunk por flujo funcional continuo y coherente.
- Si el deck contiene varios procesos distintos, crea varios chunks.

Agrupa las slides que compongan un subproceso operativo completo en
un único chunk de tipo `proceso`.

**Documentos mixtos (Tipo A/C/D con páginas visuales):**

`pdftotext` separa páginas con el carácter de control `\f` (form feed).
Para detectar páginas visuales dentro de un bloque extraído, parsea
ese carácter explícitamente:

```bash
# Extraer bloque y evaluar densidad por página
pdftotext -layout -f [inicio] -l [fin] "$DOC" /tmp/bloque.txt

# Contar palabras por página usando  como separador
python3 - << 'PY'
import sys
text = open("/tmp/bloque.txt", encoding="utf-8", errors="replace").read()
pages = [p for p in text.split("\f") if p.strip()]
BUTTON_SET = {"save","cancel","execute","ok","back","enter","help",
              "display","change","create","delete","post","check",
              "continue","exit","refresh","print","previous","next"}
for i, page in enumerate(pages, start=[inicio]):
    tokens = page.lower().split()
    words = len(tokens)
    all_buttons = len(tokens) > 0 and set(tokens).issubset(BUTTON_SET)
    status = "VISUAL" if (words < 40 or all_buttons) else "texto"
    print(f"  Página {i}: {words} palabras — {status}")
PY
```

Si una página aparece como VISUAL o contiene solo nombres de botones
("Save", "Cancel", "Execute", "OK", "Back", "Enter", "Help"):
1. Descarta ese texto plano — no lo uses para chunkear
2. Anota el número de página
3. Rasteriza solo esa página:
```bash
pdftoppm -jpeg -r 150 -f [numero_pagina] -l [numero_pagina] "$DOC" /tmp/visual
ls /tmp/visual-*.jpg
```
4. Lee la imagen visualmente para extraer la información relevante

No rasterices todo el documento — solo las páginas que activen estas señales.

---

## Paso 3 — Detectar duplicados y gestionar versiones SAP

Los términos de búsqueda deben ser específicos al tema que estás
procesando. Construye la búsqueda usando los T-codes, tablas, términos
SAP en inglés, aliases en español y objetos de negocio identificados
en el texto fuente:

```bash
grep -RniE "TERM1|TERM2|TCODE|TABLE|alias_español" chunks/ --include="*.md" || true
```

Ejemplo para un tema de Pricing:
```bash
grep -RniE "pricing procedure|esquema de precios|condition type|clase de condicion|access sequence|secuencia de acceso|V/08|VK11|KONV|KONP" chunks/ --include="*.md" || true
```

Ejemplo para un tema de Delivery:
```bash
grep -RniE "outbound delivery|entrega de salida|\bVL01N\b|\bVL10E\b|\bLIKP\b|\bLIPS\b|shipping point|punto de expedicion" chunks/ --include="*.md" || true
```

El `|| true` evita que el script falle si no hay resultados (grep
devuelve código 1 cuando no encuentra nada).

### Caso 1 — Mismo tema, misma versión SAP, fuente diferente
No modifiques el chunk directamente. Presenta un plan de actualización:

```
Chunk existente: [id]
Nueva fuente: [fichero], p. [N-M]
Cambios propuestos:
  - [sección que se amplía o corrige]
  - añadir fuente al frontmatter
¿Confirmas la actualización?
```

Solo después de confirmación explícita: actualiza el chunk, añade la
fuente al array `sources`, documenta en el log: "actualizado con [fuente]".
No crees un chunk nuevo.

### Caso 2 — Mismo tema, versiones SAP distintas (S/4HANA vs ECC)

¿La diferencia es significativa funcionalmente?
(pantallas distintas, T-codes distintos, lógica diferente)
→ Crea dos chunks separados por versión:
  `shipping/goods-issue-s4hana-001.md`  → sap_release: "S/4HANA 2020"
  `shipping/goods-issue-ecc-001.md`     → sap_release: "ECC 6.0"
→ Añade en cada uno una sección `## Diferencias con [otra versión]`.

¿La diferencia es solo cosmética? (misma lógica, UI ligeramente distinta)
→ Un solo chunk con `sap_release: generico`
→ Añade sección `## Notas de versión`.

¿No sabes si la diferencia es significativa?
→ Crea chunks separados por versión. Es más seguro que fusionar.

### Caso 3 — Misma versión, fuentes contradictorias
→ Fuente Tipo A tiene prioridad sobre B, C, D.
→ Entre dos Tipo A: la más reciente tiene prioridad.
→ Documenta la contradicción en el log.

### Caso 4 — Duplicado puro
→ Omite. Documenta en el log: "omitido — duplicado de [id]".

**Regla de oro**: un concepto = un chunk (por versión SAP si hay
diferencias significativas). El chunk debe ser completo: sintetiza
todas las fuentes disponibles. Un funcional no debería encontrar
información sobre el mismo tema repartida en varios chunks.

---

## Paso 4 — Decidir cómo chunkear

### Principio fundamental
Un chunk es correcto si puede responder una intención de búsqueda
funcional concreta sin necesitar leer ningún otro chunk.

### Cuándo crear un chunk nuevo
- Cambio de proceso de negocio (Delivery Creation ≠ Goods Issue)
- Cambio de audiencia: concepto funcional vs configuración SPRO
- Cambio de área de customizing (Output Determination ≠ Partner Determination)
- El tema supera 1500 palabras → subdivide por subtemas coherentes

### Cuándo agrupar en un solo chunk
- Contenido inseparable conceptualmente
- Resultado sería menor de 150 palabras
- Solo listas de transacciones sin contexto funcional

### Ejemplo de división — Pricing
```
pricing/condition-types-001.md      → qué son, estructura, categorías
pricing/access-sequences-001.md     → cómo busca el sistema el precio
pricing/pricing-procedures-001.md   → esquema de cálculo, rutinas, V/08
pricing/condition-records-001.md    → dónde se mantienen precios, VK11
```

### Ejemplo de agrupación — Shipping Point y Loading Point
Relacionados en configuración y uso. Un chunk es más útil que dos que
se requieren mutuamente.

### Antes de escribir: presentar plan al usuario
```
Sección: Unit 1 — Delivery Processing (p. 12-67)
Chunks identificados:
  1. shipping/delivery-creation-individual-001
     tipo: proceso | p. 15-28
     intención: "¿Cómo se crea una entrega individual?"
  2. shipping/delivery-creation-collective-001
     tipo: proceso | p. 29-41
     intención: "¿Cómo se crean entregas masivas con VL10E?"
  3. shipping/delivery-types-concept-001
     tipo: concepto | p. 12-14
     intención: "¿Qué tipos de entrega existen en SAP SD?"
¿Procedo?
```
Espera confirmación antes de escribir nada en disco.

---

## Paso 5 — Escribir el chunk

### Idioma y terminología
Redacta en español neutro. Los términos oficiales SAP van en inglés
en cursiva en el cuerpo del texto. Incluye equivalentes en español
en el campo `aliases` para mejorar el recall del RAG.

Correcto: "El *Pricing Procedure* utiliza una *Access Sequence* para
buscar los *Condition Records*."
Incorrecto: mezclar español e inglés sin criterio, o traducir T-codes.

Los `aliases` deben incluir tanto el término inglés como el español:
```yaml
aliases:
  - pricing procedure
  - esquema de precios
  - access sequence
  - secuencia de acceso
  - condition record
  - registro de condición
```

### Convención de ID y path — crítico

```
Path físico:  chunks/{area}/{slug}-{NNN}.md
ID lógico:    {area}-{slug}-{NNN}

Ejemplos:
  Path: chunks/shipping/delivery-creation-individual-001.md
  ID:   shipping-delivery-creation-individual-001

  Path: chunks/pricing/condition-types-001.md
  ID:   pricing-condition-types-001
```

El ID nunca contiene `/`.
El ID siempre incluye el área como prefijo.
El área del ID siempre coincide con la carpeta donde vive el fichero.
Comprueba el índice antes de asignar número secuencial.

### Formato obligatorio del frontmatter

```yaml
---
schema_version: 1
id: {area}-{slug}-{NNN}
title: "[Título descriptivo]"
area: [enterprise-structure|master-data|order-management|pricing|
       shipping|billing|credit-management|configuration|
       integration|special-processes]
process_tags: [order-to-cash, delivery-processing]
chunk_type: [concepto|proceso|configuracion|transaccion|integracion]
sap_release: [S/4HANA 2020|ECC 6.0|generico|no especificado]
sources:
  - file: "[nombre exacto del PDF]"
    relative_path: "[ruta relativa desde SOURCE_ROOT]"
    pages: "[N-M]"       # CRÍTICO: siempre string con comillas, incluso página única (ej. "15" no 15)
    source_type: "[A|B|C|D]"
    role: "[primary|secondary]"
transacciones: [VA01, VL01N]
tablas: [VBAK, LIKP]
aliases:
  - término inglés
  - término español
  - variante española
nivel: [funcional|tecnico|ambos]
status: draft
quality: [alta|media|baja]
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

### Criterios de quality

**alta**: fuente fiable (Tipo A o D), páginas exactas identificadas,
contenido completo, sin contradicciones, sin inferencias relevantes.
Para Tipo B: solo si el flujo visual es inequívoco, las transacciones
y campos son claramente legibles, y no hay inferencias funcionales.

**media**: fuente fiable pero parcial; fuente Tipo B por defecto
(depende de interpretación visual); inferencia menor necesaria;
requiere validación funcional. Valor por defecto para Tipo B salvo
que cumpla todos los criterios de `alta`.

**baja**: fuente comunitaria (Tipo C); OCR con problemas; contenido
incompleto; contradicción no resuelta; interpretación visual incierta
o páginas no legibles.

`quality` refleja el resultado neto del chunk: combina la fiabilidad
de la fuente con la completitud del contenido resultante. Un chunk bien
construido desde una fuente parcial puede ser `media` aunque esté bien
redactado.

Todo chunk nuevo nace con `status: draft`. Ciclo de vida completo:
- `draft`: recién creado, pendiente de revisión humana
- `reviewed`: validado por el usuario — contenido correcto
- `validated`: verificado contra sistema SAP real o fuente adicional
- `deprecated`: obsoleto (versión SAP cambiada, contenido superado)

### Nota sobre sap_release

- `S/4HANA 2020`: el documento especifica explícitamente esta versión
- `ECC 6.0`: el documento es claramente de ECC (TSCM60/62, pre-2015)
- `generico`: el concepto aplica de forma estable a ECC y S/4HANA
  sin diferencias funcionales significativas
- `no especificado`: la fuente no indica versión y no es posible
  determinarlo. Usar con precaución — marcar `quality: media` como mínimo

### Valores válidos para process_tags

```
order-to-cash, delivery-processing, billing, pricing,
returns, credit-management, transportation, consignment,
third-party, free-of-charge, complaints, credit-memo,
debit-memo, invoice-correction, make-to-order,
stock-transfer, intercompany, ninguno
```

### Secciones de contenido por chunk_type

**proceso:**
```
## Resumen operativo
## Preguntas que responde este chunk
## Cuándo aplica y contexto
## Flujo del proceso  (pasos numerados con T-codes)
## Condiciones y restricciones
## Errores frecuentes  (Síntoma → Causa → Solución)
## Referencias cruzadas
```

**configuracion:**
```
## Resumen operativo
## Preguntas que responde este chunk
## Qué controla esta configuración
## Ruta SPRO o T-code directo
## Parámetros clave  (tabla: Campo | Descripción | Valores típicos)
## Impacto según configuración
## Errores de configuración frecuentes
## Referencias cruzadas
```

**concepto:**
```
## Resumen operativo
## Preguntas que responde este chunk
## Definición
## Para qué sirve en el proceso SD
## Estructura y variantes
## Relación con otros objetos SAP SD
## Referencias cruzadas
```

**transaccion:**
```
## Resumen operativo
## Preguntas que responde este chunk
## Cuándo usar esta transacción
## Objeto de negocio afectado
## Campos clave de la pantalla principal  (tabla)
## Flujo típico de uso
## Alternativas y variantes
## Restricciones
## Errores frecuentes
## Referencias cruzadas
```

**integracion:**
```
## Resumen operativo
## Preguntas que responde este chunk
## Qué integra
## Módulos o sistemas implicados
## Objetos SAP afectados
## Flujo de datos  (tabla: Origen | Objeto/dato | Destino | Momento)
## Puntos de configuración relevantes
## Impacto funcional
## Errores frecuentes de integración
## Referencias cruzadas
```

### Reglas de escritura
- Tus propias palabras. No copies texto del PDF.
- Términos SAP en inglés en cursiva en el cuerpo. Equivalentes
  españoles en `aliases`.
- Concreto: "La *selection date* determina qué *schedule lines*
  se incluyen" es útil. "La fecha es importante" no lo es.
- No inventes. Si la fuente no lo menciona, no lo incluyas.
- Omite secciones sin contenido en la fuente. Sin relleno.
- **Tablas SAP en `tablas`**: incluye solo las tablas que aparecen
  explícitamente en la fuente o que el documento asocia claramente
  al objeto técnico descrito. No añadas tablas por conocimiento
  general del dominio. Si una tabla es relevante pero no está en la
  fuente, anótala como comentario en el cuerpo del chunk y márcala
  para validación: `<!-- tabla inferida, pendiente validación: VBAK -->`.

---

## Paso 6 — Validar consistencia

Después de escribir cada chunk y antes de actualizar el índice:

Sustituye los valores reales antes de ejecutar. Asigna las variables primero:

```bash
# Sustituir con los valores reales del chunk a crear/validar
AREA="shipping"            # área real
SLUG="delivery-creation-individual"  # slug real
NNN="001"                  # número secuencial real
FILE="chunks/$AREA/$SLUG-$NNN.md"
ID="$AREA-$SLUG-$NNN"
```

**Prevalidación — ejecutar ANTES de escribir el chunk:**
```bash
# Garantizar que el directorio de área existe
mkdir -p "chunks/$AREA"

# El fichero NO debe existir (si existe, requiere plan de actualización + confirmación)
if [ -f "$FILE" ]; then
  echo "AVISO: $FILE ya existe — presentar plan de actualización y esperar confirmación"
  exit 1
fi

# El ID no debe existir en ningún chunk real
matches=$(grep -Rni "^id: ${ID}$" chunks/ --include="*.md" | wc -l)
if [ "$matches" -gt 0 ]; then
  echo "AVISO: ID $ID ya existe en $matches chunk(s) — verificar duplicado o actualización"
  grep -Rni "^id: ${ID}$" chunks/ --include="*.md"
fi
```

**Postvalidación — ejecutar DESPUÉS de escribir el chunk:**
```bash
# El fichero debe existir
ls "$FILE" || { echo "ERROR: $FILE no se escribió correctamente"; exit 1; }

# El ID debe aparecer exactamente una vez
matches=$(grep -Rni "^id: ${ID}$" chunks/ --include="*.md" | wc -l)
if [ "$matches" -ne 1 ]; then
  echo "ERROR: $ID debe aparecer exactamente una vez. Apariciones: $matches"
fi

# El área del frontmatter coincide con la carpeta
grep "^area:" "$FILE"
```

**Validación YAML (si python3 + pyyaml disponibles):**
```bash
# Exportar variables al entorno para que el heredoc protegido pueda leerlas
export AREA SLUG NNN
python3 - << 'VALIDATE'
import os, yaml, sys, pathlib

area = os.environ.get("AREA", "")
slug = os.environ.get("SLUG", "")
nnn  = os.environ.get("NNN", "")

if not area or not slug or not nnn:
    sys.exit("ERROR: AREA, SLUG o NNN no están definidos en el entorno")

path = pathlib.Path(f"chunks/{area}/{slug}-{nnn}.md")
if not path.exists():
    sys.exit(f"ERROR: fichero no encontrado en {path}")
text = path.read_text(encoding="utf-8")

if not text.startswith("---"):
    sys.exit("ERROR: falta frontmatter YAML")

meta = yaml.safe_load(text.split("---", 2)[1])

required = ["schema_version","id","title","area","process_tags",
            "chunk_type","sap_release","sources","transacciones",
            "tablas","aliases","nivel","status","quality",
            "created","last_updated"]
for field in required:
    if field not in meta:
        sys.exit(f"ERROR: campo obligatorio ausente: {field}")

valid_areas = {"enterprise-structure","master-data","order-management",
               "pricing","shipping","billing","credit-management",
               "configuration","integration","special-processes"}
valid_types = {"concepto","proceso","configuracion","transaccion","integracion"}
valid_status = {"draft","reviewed","validated","deprecated"}
valid_quality = {"alta","media","baja"}
valid_release = {"S/4HANA 2020","ECC 6.0","generico","no especificado"}
valid_nivel = {"funcional","tecnico","ambos"}
valid_source_type = {"A","B","C","D"}
valid_role = {"primary","secondary"}
valid_tags = {"order-to-cash","delivery-processing","billing","pricing",
              "returns","credit-management","transportation","consignment",
              "third-party","free-of-charge","complaints","credit-memo",
              "debit-memo","invoice-correction","make-to-order",
              "stock-transfer","intercompany","ninguno"}

if meta["area"] not in valid_areas: sys.exit(f"ERROR: area inválida: {meta['area']}")
if meta["chunk_type"] not in valid_types: sys.exit(f"ERROR: chunk_type inválido: {meta['chunk_type']}")
if meta["status"] not in valid_status: sys.exit(f"ERROR: status inválido: {meta['status']}")
if meta["quality"] not in valid_quality: sys.exit(f"ERROR: quality inválida: {meta['quality']}")
if meta["sap_release"] not in valid_release: sys.exit(f"ERROR: sap_release inválido: {meta['sap_release']}")
if meta["nivel"] not in valid_nivel: sys.exit(f"ERROR: nivel inválido: {meta['nivel']}")

invalid_tags = set(meta.get("process_tags",[])) - valid_tags
if invalid_tags: sys.exit(f"ERROR: process_tags inválidos: {invalid_tags}")

for s in meta.get("sources", []):
    for k in ["file","relative_path","pages","source_type","role"]:
        if k not in s:
            sys.exit(f"ERROR: source sin campo: {k}")
    if s.get("source_type") not in valid_source_type:
        sys.exit(f"ERROR: source_type inválido: {s.get('source_type')}")
    if s.get("role") not in valid_role:
        sys.exit(f"ERROR: role inválido: {s.get('role')}")
    if not isinstance(s.get("pages",""), str):
        sys.exit(f"ERROR: pages debe ser string con comillas, no número: {s.get('pages')}")

print("YAML OK — chunk válido")
VALIDATE
```

Si alguna comprobación falla: corrige el chunk antes de continuar.
No actualices el índice con un chunk defectuoso.

---

## Paso 7 — Actualizar estado

### `_processing_log.md` — append-only, nunca reescribir

```markdown
## YYYY-MM-DD — [nombre exacto del PDF]
- Relative path: [ruta desde SOURCE_ROOT]
- Tipo: A/B/C/D/E
- Páginas totales: N
- Rango procesado: p. X-Y
- Próxima página pendiente: p. Z  (o "ninguna — completado")
- Texto extraíble: alto/medio/bajo
- Encoding issues: [páginas problemáticas, o "ninguno"]
- Chunks creados: N
  - [id] → chunks/area/fichero.md
- Chunks actualizados:
  - [id] → motivo
- Duplicados encontrados y decisión:
  - [id existente] → [omitido/fusionado/separado por versión SAP]
- Contenido omitido: [qué y por qué, o "nada"]
- Decisiones de chunking no obvias: [decisión y justificación]
- Estado: no iniciado / parcial / completado / omitido
```

### `_index.md` — regenerar con script

```bash
python3 << 'PYEOF'
import os, sys
try:
    import yaml
except ImportError:
    print("AVISO: pyyaml no disponible en este entorno.")
    print("ACCIÓN MANUAL REQUERIDA: añade la fila directamente al final de chunks/_index.md")
    print("Formato: | {id} | chunks/{area}/{slug}-{NNN}.md | {título} | ... |")
    sys.exit(0)  # Dependencia ausente no es error de datos — permite continuar con fallback manual

import datetime
chunks_dir = "chunks"
rows = []
for root, _, files in os.walk(chunks_dir):
    for f in sorted(files):
        if not f.endswith(".md") or f.startswith("_"):
            continue
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        if not content.startswith("---"):
            continue
        try:
            parts = content.split("---", 2)
            meta = yaml.safe_load(parts[1])

            def esc(v):
                return str(v).replace("|", "\\|").replace("\n", " ")

            t_codes = esc(", ".join(str(t) for t in meta.get("transacciones", [])))
            sources = meta.get("sources", [])
            src_files = esc(", ".join(s.get("file", "") for s in sources))
            src_pages = esc(", ".join(str(s.get("pages", "")) for s in sources))
            tags = esc(", ".join(str(t) for t in meta.get("process_tags", [])))
            rows.append(
                f"| {meta.get('id','')} "
                f"| {path} "
                f"| {meta.get('title','')} "
                f"| {meta.get('area','')} "
                f"| {meta.get('chunk_type','')} "
                f"| {meta.get('sap_release','')} "
                f"| {tags} "
                f"| {src_files} "
                f"| {src_pages} "
                f"| {t_codes} "
                f"| {meta.get('status','')} "
                f"| {meta.get('quality','')} |"
            )
        except Exception as e:
            print(f"Error en {path}: {e}")

today = datetime.date.today()
header = [
    "# SAP SD Knowledge Base — Índice\n",
    f"Última actualización: {today}  |  Total chunks: {len(rows)}\n",
    "| ID | Path | Título | Área | Tipo | SAP Release | Process Tags"
    " | Fuentes | Páginas | T-codes | Status | Calidad |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|",
]
rows.sort(key=lambda r: r.lower())
# Detectar IDs duplicados antes de escribir
seen_ids = {}
for row in rows:
    parts = row.split("|")
    id_val = parts[1].strip() if len(parts) > 1 else ""
    path_val = parts[2].strip() if len(parts) > 2 else ""
    if id_val in seen_ids:
        print(f"ERROR: ID duplicado — {id_val}")
        print(f"  ya en: {seen_ids[id_val]}")
        print(f"  también en: {path_val}")
        print("Corrige los IDs duplicados antes de regenerar el índice.")
        sys.exit(1)
    else:
        seen_ids[id_val] = path_val
with open(os.path.join(chunks_dir, "_index.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(header + rows) + "\n")
print(f"Índice regenerado: {len(rows)} chunks.")
PYEOF
```

Si python3/pyyaml no están disponibles, añade la fila manualmente
(toda en una línea, sin saltos):
```markdown
| {id} | chunks/{area}/{slug}-{NNN}.md | {título} | {área} | {tipo} | {sap_release} | {tags} | {fuente} | {páginas} | {t-codes} | draft | {calidad} |
```

### `_source_inventory.md`

```markdown
# Source Inventory — SAP SD Knowledge Base
Última actualización: YYYY-MM-DD

| Fichero | Relative path | Tipo | Prioridad | Páginas | Palabras/pág | Estado | Nota |
|---|---|---|---|---|---|---|---|
| S4610_EN_Col17 Delivery Processing.pdf | S4610_EN_Col17 ... | A | alta | 178 | 320 | parcial | p.68 pendiente |
```

Estados: `no iniciado` / `parcial` / `completado` / `omitido` / `bloqueado`

---

## Límite por sesión

### Primeras dos sesiones — modo calibración
- Máximo una unidad lógica (capítulo o bloque funcional cerrado)
- O máximo 5 chunks, lo que ocurra antes
- Para y pide validación humana

### Después de calibrar
- Máximo un documento completo por sesión
- O un bloque lógico completo en documentos >300 páginas
- No uses "hasta la mitad" — usa la frontera lógica del documento
- Registra siempre la próxima página pendiente en el log

### Al terminar cada sesión, presenta:
```
Chunks creados/actualizados esta sesión:
  - [id] → [path]
Pendiente de validación:
  - [qué debe revisar el usuario]
Siguiente recomendación:
  - [propuesta concreta para la próxima sesión]
```

---

## Ejemplos de referencia

Chunks validados manualmente desde `SD - Shipment.pdf` (Tipo B).
Úsalos como referencia de densidad técnica, formato y criterio.

### Ejemplo 1 — chunk_type: proceso

```markdown
---
schema_version: 1
id: shipping-delivery-creation-process-001
title: "Creación de entregas de salida en SAP SD"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: proceso
sap_release: generico
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "2-9"
    source_type: B
    role: primary
transacciones: [VL01N, VL10E, VL02N, VL03N, VL06O]
tablas: []
aliases:
  - outbound delivery
  - entrega de salida
  - crear entrega
  - delivery creation
  - creación entrega
nivel: funcional
status: draft
quality: alta
created: 2026-06-01
last_updated: 2026-06-01
---

# Creación de entregas de salida en SAP SD

<!-- tablas inferidas, pendiente validación: LIKP, LIPS, VBUK -->

## Resumen operativo
Una entrega de salida (*outbound delivery*) es el documento que inicia
el proceso físico de expedición contra un pedido de cliente. SAP permite
crearla individualmente para un pedido concreto o colectivamente para
un conjunto de pedidos pendientes. Solo se incluyen las *schedule lines*
confirmadas hasta la *selection date* indicada.

## Preguntas que responde este chunk
- ¿Cómo se crea una entrega de salida en SAP SD?
- ¿Qué diferencia hay entre crear entregas de forma individual y colectiva?
- ¿Por qué no se generan posiciones en la entrega aunque haya stock?
- ¿Qué es la *selection date* y cómo afecta a las entregas?

## Cuándo aplica y contexto
La entrega se crea después de que el pedido tiene *schedule lines*
confirmadas. Es el paso previo al picking, embalaje y *Goods Issue*.
Sin entrega no hay GI y sin GI no hay factura.

## Flujo del proceso

### Opción 1 — Entrega individual desde el pedido (VA02)
1. Entrar en el pedido con **VA02**
2. Menú: *Sales document > Deliver*
3. SAP redirige a la misma pantalla que VL01N con el pedido pre-rellenado
4. Verificar *Shipping point* y *Selection date*
5. Confirmar → entrega creada

### Opción 2 — Entrega individual directa (VL01N)
1. Ejecutar **VL01N**
2. Introducir *Shipping point*, *Selection date* y número de pedido
3. Confirmar → pantalla de overview de la entrega

### Opción 3 — Entregas colectivas (VL10E — Delivery Due List)
1. Ejecutar **VL10E**
2. Criterios: *Shipping point*, rango de fechas; opcionales: ruta,
   *ship-to*, org. ventas, canal, división, prioridad
3. El sistema muestra *schedule lines* confirmadas hasta la fecha
4. Seleccionar líneas y elegir modo:
   - **Dialog**: crea entregas manualmente, igual que VL01N
   - **Background**: crea todas automáticamente en batch

## Condiciones y restricciones
- Solo *schedule lines* confirmadas (ATP aprobado)
- La *selection date* filtra: solo líneas confirmadas hasta esa fecha
- El *Shipping point* debe estar asignado al centro del pedido

## Errores frecuentes

**"No schedule lines due for delivery up to the selected date"**
→ La *selection date* es anterior a la fecha de confirmación del pedido.
→ Ampliar la *selection date* hasta cubrir la fecha confirmada.

**El pedido no aparece en VL10E**
→ Verificar que el *Shipping point* coincide con el del pedido.
→ Verificar que las *schedule lines* no están bloqueadas.

## Referencias cruzadas
- Ver también: shipping-delivery-types-concept-001
- Siguiente paso: shipping-goods-issue-001
```

---

### Ejemplo 2 — chunk_type: concepto

```markdown
---
schema_version: 1
id: shipping-delivery-types-concept-001
title: "Entrega de salida en SAP SD — concepto y estructura"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concepto
sap_release: generico
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "2, 10"
    source_type: B
    role: primary
transacciones: [VL01N, VL02N, VL03N]
tablas: []
aliases:
  - outbound delivery
  - entrega de salida
  - delivery document
  - documento de entrega
nivel: funcional
status: draft
quality: media
created: 2026-06-01
last_updated: 2026-06-01
---

# Entrega de salida en SAP SD — concepto y estructura

<!-- tablas inferidas, pendiente validación: LIKP, LIPS -->

## Resumen operativo
La entrega de salida es el documento logístico que representa la expedición
física de mercancía contra un pedido de cliente. Tiene cabecera con datos
del destinatario y posiciones con los materiales. No tiene *schedule lines*.
Es el pivote entre la gestión de pedidos (SD) y el almacén (WM/EWM).

## Preguntas que responde este chunk
- ¿Qué es una entrega de salida en SAP SD?
- ¿Qué estructura tiene el documento de entrega?
- ¿En qué se diferencia la entrega del pedido de ventas?

## Definición
Documento SAP SD que representa la intención y ejecución de enviar
mercancía a un cliente. Se crea con referencia a un pedido de ventas
y hereda sus datos de expedición.

## Para qué sirve en el proceso SD
Permite iniciar el picking, registrar embalaje y carga, ejecutar el
*Goods Issue* (reduce stock y genera documento contable en FI), y sirve
de base para la factura.

## Estructura y variantes

| Nivel | Datos que contiene |
|---|---|
| Cabecera | *Ship-to party*, fecha de entrega, *shipping point*, peso total, bultos |
| Posición | Material, cantidad, unidad de medida, lote, estado de picking |

A diferencia del pedido, la entrega **no tiene *schedule lines***.

## Relación con otros objetos SAP SD

| Objeto | Relación |
|---|---|
| Pedido de ventas | La entrega se crea con referencia; hereda *ship-to*, materiales y cantidades confirmadas |
| *Transfer Order* (WM) | Si hay gestión de almacén, genera una *transfer order* para picking |
| *Goods Issue* | Se ejecuta sobre la entrega en VL02N |
| Factura | Se crea con referencia a la entrega después del GI |

## Referencias cruzadas
- Proceso de creación: shipping-delivery-creation-process-001
- Siguiente paso: shipping-goods-issue-001
```

---

### Ejemplo 3 — chunk_type: transaccion

```markdown
---
schema_version: 1
id: shipping-goods-issue-cancel-vl09-001
title: "Cancelación de Goods Issue con VL09"
area: shipping
process_tags: [returns, delivery-processing]
chunk_type: transaccion
sap_release: generico
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "15"
    source_type: B
    role: primary
transacciones: [VL09]
tablas: []
aliases:
  - cancelar GI
  - reverse goods issue
  - VL09
  - cancelar salida de mercancías
  - revertir GI
nivel: funcional
status: draft
quality: media
created: 2026-06-01
last_updated: 2026-06-01
---

# Cancelación de Goods Issue con VL09

<!-- tablas inferidas, pendiente validación: LIKP, MKPF -->

## Resumen operativo
**VL09** revierte un *Goods Issue* registrado por error. Deshace el
descenso de stock y anula el documento contable en FI. Solo es posible
dentro del mismo período contable en que se registró el GI original.

## Preguntas que responde este chunk
- ¿Cómo se cancela un *Goods Issue* registrado por error?
- ¿Cuándo ya no es posible usar VL09?
- ¿Qué alternativa existe si el período contable está cerrado?

## Cuándo usar esta transacción
Cuando se ha registrado un GI sobre una entrega de salida por error
y el período contable del GI aún está abierto en FI.

## Objeto de negocio afectado
Entrega de salida (*outbound delivery*) con GI registrado.

## Campos clave de la pantalla principal

| Campo | Descripción | Notas |
|---|---|---|
| *Shipping point* | Punto de expedición | Obligatorio |
| *Inbound/Outbound delivery* | Número de entrega | Introducir directamente |
| *Define date* | Fecha de reversión | Por defecto = hoy |

## Flujo típico de uso
1. Ejecutar **VL09**
2. Introducir *Shipping point* y número de entrega
3. Seleccionar la línea que aparece en el resultado
4. Ejecutar *Cancel/Reverse*
5. El sistema revierte el GI; la entrega vuelve a estado abierto

## Restricciones
Solo posible en el **mismo período contable** en que se registró
el GI original. Si el período está cerrado en FI: usar devolución
de cliente (*Returns Order* + *Return Delivery* + GR).

## Errores frecuentes

**"Reversal not possible — period already closed"**
→ Período contable cerrado. Proceder con devolución de cliente.

**La entrega no aparece en la selección**
→ Verificar que el GI está registrado y que el *Shipping point* coincide.

## Referencias cruzadas
- Proceso previo: shipping-goods-issue-001
- Alternativa si período cerrado: special-processes-customer-returns-001
```

---

## Qué observar en estos ejemplos

**Resumen operativo**: 3-5 líneas con el concepto completo. Si no puedes
escribirlo sin relleno, el chunk está mal delimitado.

**Preguntas reales**: no genéricas sino preguntas que haría un funcional
en un proyecto real.

**Sin secciones vacías**: el ejemplo 3 no incluye secciones que la fuente
no cubría. Sin relleno inventado.

**Terminología**: términos SAP en inglés en cursiva en el cuerpo.
Equivalentes en español en `aliases`. Nunca al revés, nunca mezclado.

**quality: media vs alta en Tipo B**: los tres ejemplos vienen de
`SD - Shipment.pdf` (Tipo B, slide deck). El primero tiene `alta` porque
el flujo visual era inequívoco, las transacciones y campos eran
claramente legibles, y no hubo inferencias funcionales. Los otros dos
tienen `media` porque la información era parcial o requirió interpretación.
`quality: media` es el valor por defecto para cualquier Tipo B. Solo
sube a `alta` si cumples todos los criterios descritos en la definición.

**chunk_type correcto**: VL09 es `transaccion`, no `configuracion`.
Una transacción operativa de reversión no es configuración SPRO.

---

## Contexto del proyecto

Objetivo: sistema RAG para responder preguntas de un consultor funcional SAP SD.
El usuario está aprendiendo SAP SD y técnicas RAG simultáneamente.
Calidad sobre velocidad. 20 chunks excelentes valen más que 200 mediocres.
No generes chunks si no puedes indicar fuente y páginas exactas.
Cuando dudes entre dos opciones razonables, propón ambas y espera confirmación.
