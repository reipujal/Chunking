---
schema_version: 1
id: shipping-delivery-document-structure-001
title: "Estructura del documento de entrega en SAP SD"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concepto
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "13-14"
    source_type: A
    role: primary
transacciones: []
tablas: []
aliases:
  - estructura entrega
  - delivery document structure
  - cabecera entrega
  - delivery header
  - posición entrega
  - delivery item
  - shipment document
  - documento de expedición
  - freight order
  - TM freight order
nivel: funcional
status: draft
quality: alta
created: 2026-06-05
last_updated: 2026-06-05
---

# Estructura del documento de entrega en SAP SD

## Resumen operativo
El documento de entrega en SAP SD tiene dos niveles: cabecera y posiciones. La cabecera agrupa los datos comunes a toda la entrega; las posiciones contienen los materiales a entregar. La pantalla se organiza en pestañas (*tabstrips*) por tipo de actividad logística. El documento de entrega difiere del *shipment document* y del *TM Freight Order* en alcance y propósito.

## Preguntas que responde este chunk
- ¿Cómo está organizado internamente un documento de entrega?
- ¿Qué datos contiene la cabecera y qué datos contienen las posiciones?
- ¿Qué diferencia hay entre un documento de entrega y un documento de expedición (*shipment*)?
- ¿Qué es un *TM Freight Order* y cuándo se usa en lugar de la entrega?

## Definición
El documento de entrega consta de una cabecera y un número variable de posiciones. La cabecera contiene datos que aplican a toda la entrega. Las posiciones contienen la información de los materiales a entregar.

## Para qué sirve en el proceso SD
La estructura del documento soporta el flujo logístico completo: desde la determinación del punto de expedición y la ruta hasta el picking, embalaje, carga y el registro del *Goods Issue* o *Goods Receipt*. Cada fase del proceso tiene su propia pestaña en el documento.

## Estructura y variantes

### Cabecera
Contiene datos que aplican a toda la entrega:
- *Ship-to party* (destinatario)
- *Shipping point* (punto de expedición)
- Ruta (*route*)

La pantalla de resumen (*overview*) muestra una selección de datos de cabecera y posición agrupados por actividad en pestañas (*tabstrips*).

**Pestañas de cabecera:** procesamiento, picking, carga, expedición, comercio exterior/aduanas, textos, interlocutores, salida de documentos, supervisión de bultos, condiciones.

### Posiciones
Contienen información sobre los materiales a entregar. En la pantalla de detalle de posición, la información se agrupa en pestañas similares a las de la cabecera.

## Entrega vs. *Shipment Document* vs. *TM Freight Order*

| Documento | Alcance | Cuándo se usa |
|---|---|---|
| Entrega de salida | Un punto de expedición → un destinatario a lo largo de una ruta | Proceso estándar de expedición de mercancía |
| *Shipment Document* (LE-TRA) | Agrupa varias entregas en un envío | Varios destinos o puntos de carga en un mismo vehículo (WM clásico) |
| *TM Freight Order* | Agrupa varias entregas con criterios configurables (ruta, requerimiento de transporte) | Varios puntos de expedición, varios destinatarios en una misma ruta (SAP TM) |

> A partir de SAP S/4HANA 1709, *Transportation Management* está integrado en el sistema central, sustituyendo progresivamente al *LE Transportation Management* clásico.

## Referencias cruzadas
- Tipos de entrega y concepto general: shipping-delivery-document-concept-001
