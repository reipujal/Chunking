---
schema_version: 1
id: shipping-delivery-document-concept-001
title: "Documento de entrega en SAP SD — concepto y tipos"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concepto
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "9-12"
    source_type: A
    role: primary
transacciones: []
tablas: []
aliases:
  - delivery document
  - documento de entrega
  - outbound delivery
  - entrega de salida
  - inbound delivery
  - entrega de entrada
  - Logistics Execution
  - LE
nivel: funcional
status: draft
quality: alta
created: 2026-06-05
last_updated: 2026-06-05
---

# Documento de entrega en SAP SD — concepto y tipos

## Resumen operativo
El *delivery document* es el objeto central de *Logistics Execution* (LE) en SAP S/4HANA. Representa la ejecución física de un movimiento de mercancía — tanto salidas hacia clientes como entradas desde proveedores o traslados entre centros propios. Existen tres tipos principales según el proceso de negocio al que dan soporte.

## Preguntas que responde este chunk
- ¿Qué es *Logistics Execution* en SAP S/4HANA?
- ¿Qué es un documento de entrega y para qué sirve?
- ¿Qué diferencia hay entre una entrega de salida, una de entrada y una de traslado?
- ¿En qué procesos se usa un documento de entrega?

## Definición
*Logistics Execution* (LE) proporciona las funciones necesarias para ejecutar todos los procesos logísticos — recepción y expedición de mercancías — con independencia del sector o industria. LE conecta los procesos de aprovisionamiento y distribución, ya sean internos o con terceros (proveedores, clientes, prestadores de servicios).

El *delivery document* es el documento que SAP crea para gestionar estos movimientos. Sirve de base para actividades de almacén (picking, embalaje, colocación en stock, creación de *warehouse order*) y para el registro contable del movimiento de mercancía (*Goods Issue* o *Goods Receipt*).

> El *warehouse order* es el documento que ejecuta todos los movimientos físicos de material en el almacén en EWM.

## Para qué sirve en el proceso SD
Los documentos de entrega permiten gestionar los procesos de expedición (salida) y recepción (entrada) de mercancía. Dependiendo del proceso de negocio, el documento adopta un tipo distinto.

## Estructura y variantes

### Entrega de salida (*Outbound Delivery*)
Referenciada a un pedido de ventas. Representa el proceso de expedición de mercancía a un cliente. Sirve de base para picking, embalaje, impresión de documentación y registro del *Goods Issue*.

### Entrega de entrada (*Inbound Delivery*)
Referenciada a uno o varios pedidos de compra (total o parcialmente). Representa la recepción de mercancía de un proveedor. Sirve de base para embalaje, colocación en stock, creación del *warehouse order* y registro del *Goods Receipt*.

### Entrega para traslado entre centros (*Stock Transfer Order*)
Cuando una empresa transfiere stock entre dos centros propios, el centro receptor crea un pedido de compra al centro suministrador. El centro suministrador crea un documento de entrega con referencia a ese pedido de compra. La entrega sirve de base para picking, embalaje y *Goods Issue*.

## Relación con otros objetos SAP SD

| Objeto | Relación |
|---|---|
| Pedido de ventas | Referencia para la entrega de salida |
| Pedido de compra | Referencia para la entrega de entrada o traslado |
| *Warehouse Order* (EWM) | Se crea a partir de la entrega para ejecutar movimientos en almacén |
| *Goods Issue* / *Goods Receipt* | Se registra con referencia a la entrega; reduce o aumenta el stock |
| Factura | Se crea con referencia a la entrega de salida tras el *Goods Issue* |

## Nota sobre EWM
A partir de SAP S/4HANA 1610, las funciones de *SAP Extended Warehouse Management* (EWM) están disponibles en el sistema central. El *Warehouse Management* (WM) clásico sigue disponible, pero el desarrollo futuro se concentra exclusivamente en EWM.

## Referencias cruzadas
- Estructura interna del documento: shipping-delivery-document-structure-001
