---
name: contexto-objetivo-vaes-y-rol-del-chunking
description: "Objetivo global del proyecto (asistente de redacción de VAES para consultores SAP SD) y rol real del RAG/chunking de documentación SD dentro de ese objetivo. Define qué es el producto, qué NO es, la arquitectura de tres capas y cómo se mide el éxito. Leer ANTES de trabajar sobre el repo de chunking."
audience: LLM
status: documento de contexto (no especificación cerrada)
---

# Contexto — Objetivo global del proyecto y rol real del "chunking"

## 0. Propósito de este documento

Este contexto existe para que un LLM que vaya a trabajar sobre este repositorio
entienda **para qué sirve realmente lo que hay aquí** antes de tocarlo.

El repositorio contiene, hoy, un sistema de *chunking + retrieval* (RAG) sobre
documentación de SAP SD, más un harness de evaluación. **Es fácil leer el repo y
concluir que el objetivo es "un RAG que responde preguntas de SAP SD". Esa
conclusión es incorrecta** y lleva a trabajar sobre el eje equivocado. Este
documento corrige esa premisa y fija el objetivo real.

Convención de este texto: se distingue explícitamente entre **[HECHO]** (verificado
o decidido), **[DECISIÓN]** (elección de alcance ya tomada, no reabrir sin motivo
nuevo) e **[HIPÓTESIS]** (a validar, no asumir como cierto).

---

## 1. Objetivo global

Construir un **asistente que ayude a consultores de SAP SD a redactar (y, antes,
validar) VAES** — Valoraciones de Esfuerzo: el documento que convierte un
requerimiento de un cliente en una propuesta valorable (necesidad de negocio,
solución, criterios de aceptación, asunciones, exclusiones y estimación de horas).
Para qué es un VAES en detalle, ver el contexto de la plantilla VAES
(documento aparte; este texto asume que el lector lo conoce o lo leerá).

Puntos no negociables del objetivo:

- **[DECISIÓN] Es una herramienta de APOYO al consultor, con humano en el bucle.**
  No es un sistema autónomo ni un producto integrado en el SAP del cliente. El
  consultor usa el asistente, lo corrige y firma la versión final.
- **[DECISIÓN] El asistente NO tiene acceso al sistema del cliente.** No hay
  extractores automáticos de la instalación. El conocimiento del cliente entra
  por **preguntas y respuestas al consultor** (y, cuando exista, código que el
  consultor pegue).

---

## 2. El hecho que lo cambia todo: el 99% de los VAES son sobre "Z"

**[HECHO, aportado por el experto de dominio]** En la práctica real, ~99% de los
VAES tratan sobre **desarrollos propios del cliente ("Z")**: programas Z, tablas Z,
user exits, BAdIs, enhancements, formularios, jobs — NO sobre el estándar de SAP.

Consecuencia directa y dura:

- El conocimiento que resuelve un VAES **no está en ninguna documentación de SAP**.
  El "Z" es código y configuración que existe únicamente en la instalación de ese
  cliente concreto.
- Por tanto, **un RAG sobre documentación estándar NO puede responder el VAES** en
  la inmensa mayoría de los casos. La respuesta no está, ni puede estar, en el
  corpus estándar.

Esto invalida la lectura ingenua "RAG de SD = el producto". El RAG de SD **no es
el motor de respuesta**. Su papel es otro, y es el tema de la sección 4.

---

## 3. Por qué es difícil: tres capas de conocimiento en sitios distintos

Para producir un VAES fiable hacen falta tres conocimientos que **no viven en el
mismo lugar**:

1. **Proceso estándar de SAP SD** — cómo funciona SD de fábrica (flujos, objetos,
   puntos de extensión). *Está en documentación.* Es lo que este repo indexa.
2. **La instalación real del cliente** — qué config está activada, qué Z/exits
   existen, qué interfaces hay y, sobre todo, **cómo se usa de verdad**. *No está
   documentado de forma accesible al asistente.* Vive en el sistema del cliente y
   en la cabeza del consultor.
3. **Interpretación** — separar qué es estándar, qué es configuración, qué es
   desarrollo propio y **qué no se puede saber sin preguntar**.

La IA es fuerte en la capa 1 y en *redactar/interpretar* (resumir doc, explicar
código, redactar borradores). La IA **no basta** para la capa 2: reconstruir la
realidad de un sistema es *descubrir*, no *interpretar*; es exhaustivo y auditable,
no probabilístico. Por eso la capa 2 **no se automatiza aquí — se obtiene
preguntando al consultor.**

---

## 4. El rol REAL del chunking / RAG de SD

Dado que el RAG estándar no responde el VAES (sección 2), ¿para qué sirve? Para dos
cosas, y ambas son valiosas:

### 4.1 Saber QUÉ preguntar (elicitación con criterio)

**[HIPÓTESIS central del proyecto — a validar, ver sección 8]** Un LLM **sin** modelo
de proceso estándar formula preguntas genéricas al consultor ("¿qué hace el Z?").
Un LLM **con** modelo de proceso pregunta como un consultor senior: ubica el Z en el
flujo estándar y pregunta por la interacción concreta.

Ejemplo: requerimiento "modificar el cálculo del descuento por volumen". Con
conocimiento de proceso, el asistente sabe que eso toca la *determinación de
condiciones* y pregunta: "¿el Z sustituye la rutina estándar de cálculo o la
complementa?, ¿actúa antes o después de la determinación estándar?, ¿afecta solo al
pedido o también a la factura?". Esas preguntas **solo se generan si el sistema
conoce el proceso estándar**. Ese es el valor del RAG de SD.

### 4.2 Ubicar el requerimiento dentro de un proceso

El requerimiento llega suelto; el RAG lo sitúa en el proceso estándar para que el
VAES describa **dónde** impacta. Eso alimenta la sección de "requerimientos de
negocio" del VAES.

### 4.3 Cómo se mide el éxito del RAG de SD (importante)

**[DECISIÓN] El RAG de SD NO se evalúa con métricas de fidelidad de respuesta
(faithfulness / grounded_fraction) ni con "over-response".** Esas métricas miden si
el sistema responde bien preguntas de examen, que **no es su función aquí**.

Se evalúa por: **¿las preguntas que genera son las que haría un consultor experto?**
(cobertura de huecos, pertinencia). Es una rúbrica de calidad de elicitación, no un
juez de grounding.

> Nota para el LLM: si encuentras en el repo un harness de *faithfulness* con jueces,
> abstención, frase exacta, etc., entiende que mide un eje que **no es el criterio de
> éxito de este producto**. Ver sección 7.

---

## 5. Qué NO es este producto (correcciones de premisa)

- **NO** es un RAG que responde preguntas de SAP SD. (El 99% es Z, no estándar.)
- **NO** es un extractor automático de la instalación del cliente. **[DECISIÓN]**
  Esa capa se sustituye por preguntas/respuestas al consultor.
- **NO** depende de los VAES históricos como fuente de verdad. **[DECISIÓN, hoy]**
  Son "piezas sueltas de un puzzle aún sin empezar"; no se usan como corpus todavía.
  (Ver sección 6.3 para su rol futuro.)
- **NO** persigue una métrica de grounding como objetivo. El objetivo es calidad del
  borrador de VAES y de las preguntas que lo construyen.

---

## 6. Arquitectura objetivo: tres capas

### 6.1 Capa 1 — Conocimiento estándar (RAG de SD) — *este repo*
Modelo de proceso estándar. Rol: saber qué preguntar (4.1) y ubicar el requerimiento
(4.2). Es lo que el repo ya construye a medias.

### 6.2 Capa 2 — Contexto del cliente (encuesta de KT, una vez por cliente)
**[DECISIÓN/DISEÑO]** Al entrar en un cliente, el asistente hace una **encuesta
mínima de Knowledge Transfer** para capturar lo **estable** de la instalación:
versión (ECC/S4 y cuál), módulos activos, estructura organizativa, grandes
Z/exits/interfaces existentes. Se almacena de forma **persistente en el "contexto del
cliente"** y se reutiliza en todos los VAES de ese cliente.

**Criterio de diseño de la encuesta (regla de comedido):** una pregunta de KT solo
gana su sitio si su respuesta **cambia las preguntas posteriores o evita varias
preguntas futuras**. No exhaustividad. Una encuesta gigante "para capturarlo todo"
es un antipatrón: el consultor la abandona y, además, el 99% del detalle (el
comportamiento interno de cada Z) **nunca** cabe en un KT general — siempre requerirá
preguntas en el momento del VAES.

- "¿Qué versión de S/4HANA?" → gana su sitio (condiciona todo el proceso estándar).
- "¿Cuántos Z tenéis?" → no gana su sitio (no cambia nada accionable).

### 6.3 Capa 3 — Diálogo por VAES
Las preguntas específicas del Z de **este** ticket, que el asistente formula *porque*
tiene la capa 1 (proceso) y la capa 2 (mapa del cliente). Aquí el consultor responde
y, si existe, pega el código ABAP del Z (que el LLM sí sabe leer e interpretar).

### Salida
El asistente redacta el borrador del VAES cruzando las tres capas y **declarando
explícitamente la procedencia de cada afirmación**: qué sabe por el estándar, qué le
dijeron del cliente, y **qué queda por validar / no puede saber**. Esa frontera
"lo sé vs me lo tienen que decir" es la pieza crítica de fiabilidad.

> **[HIPÓTESIS de futuro]** La capa 2 + lo que cada VAES revela del Z **es** el puzzle
> empezando a completarse. Cliente a cliente, ese contexto acumulado puede acabar
> siendo el activo más valioso del sistema, por encima del RAG de SD. No se construye
> ahora, pero la capa 2 debe diseñarse para **crecer** con lo aprendido en cada VAES,
> no como una foto fija del KT.

---

## 7. Estado del repositorio: qué es producto y qué es andamiaje

Para que un LLM no trabaje sobre el eje equivocado:

- **Activo real e independiente del enfoque:** el corpus/chunks de SAP SD, el gold
  set, el chunking y el retrieval. Sirven a la Capa 1 (modelo de proceso estándar).
- **Andamiaje de medición, eje equivocado para el producto:** el harness de
  *faithfulness* (jueces, grounded_fraction), la métrica de *over-response* y el
  protocolo de *abstención por frase exacta*. Medían "¿responde bien o se abstiene?",
  que es relevante para un Q&A, **no** para "¿el asistente sabe qué preguntar y qué no
  puede saber?". No es basura, pero **no es el criterio de éxito del producto**:
  - El trabajo de **abstención** se **reubica**: pasa de "fallo a suprimir" a
    "función deseada" — el mecanismo que distingue *lo que el sistema sabe por el
    estándar* de *lo que debe pedir al consultor* (los "?" de la salida). Es
    sub-componente, no el todo.
  - El **faithfulness/over-response** como métrica headline queda **retirado** para
    este objetivo. Si se necesita un evaluador, será una **rúbrica de calidad** (del
    VAES y de las preguntas), no un juez de grounding.

**[DECISIÓN] No seguir puliendo el harness de faithfulness.** El número exacto de
over-response no cambia ninguna decisión de producto.

---

## 8. Cómo validar el diseño antes de construir (pilot barato)

Antes de construir las capas 2 y 3 o de ampliar el repo, **validar la hipótesis
central (4.1) con coste mínimo**:

> Tomar UN requerimiento real sobre un Z, darle al asistente el requerimiento + unos
> pocos hechos de contexto de cliente (inventados o de un KT mínimo), y observar
> **qué preguntas genera**.
> - Si son las preguntas que haría un consultor senior → la Capa 1 cumple su función
>   real y el diseño se sostiene.
> - Si son genéricas o erran → ahí está el trabajo (mejorar el modelo de proceso /
>   el prompt de elicitación), y NO en ningún harness de fidelidad.

Esto es una tarde de trabajo, no un sistema. Regla general del proyecto: **pilot
barato que confirme que el efecto existe antes de escalar.**

---

## 9. Reglas para un LLM que trabaje en este repositorio

1. **No asumas que el objetivo es "un RAG que responde".** Es un asistente de
   redacción de VAES con humano en el bucle; el RAG aporta proceso estándar para
   saber qué preguntar, no respuestas.
2. **No reintroduzcas faithfulness/over-response como métrica de éxito.** El éxito es
   calidad de las preguntas y del borrador de VAES.
3. **El conocimiento del cliente entra por preguntas, no por extractores.** No
   propongas construir extractores de la instalación.
4. **Antes de construir una capacidad, entrega build-vs-buy:** ¿existe ya una
   herramienta/estándar (p. ej. un framework de evaluación por rúbrica, output
   estructurado, orquestación de agentes)? ¿por qué construir a medida? Reutilizar lo
   resuelto y estable por defecto.
5. **Empieza por lo mínimo y valida con un pilot antes de escalar.** No construyas las
   tres capas de golpe; son, en gran parte, prompts + un store de contexto por
   cliente, no un harness nuevo.
6. **Declara siempre la procedencia** (estándar / dicho por el cliente / por validar)
   en cualquier salida orientada a VAES. Esa frontera es la fiabilidad del producto.

---

## 10. Resumen en una frase

No se está construyendo un RAG que responde preguntas de SAP SD; se está construyendo
un **asistente que, apoyado en conocimiento de proceso estándar (el RAG de este
repo), sabe qué preguntar al consultor sobre los desarrollos Z del cliente —que es el
99% del trabajo— y redacta un borrador de VAES declarando qué sabe y qué queda por
validar.** El chunking de SD es la capa que habilita las preguntas correctas, no la
que da las respuestas.
