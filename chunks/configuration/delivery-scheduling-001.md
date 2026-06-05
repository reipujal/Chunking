---
schema_version: 1
id: configuration-delivery-scheduling-001
title: "Delivery and Transportation Scheduling in SAP SD"
area: configuration
process_tags: [order-to-cash, delivery-processing, transportation]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "49-52"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - backward scheduling
  - programación hacia atrás
  - forward scheduling
  - programación hacia adelante
  - precise scheduling
  - programación exacta
  - daily scheduling
  - programación diaria
  - route schedule
  - plan de ruta
  - material availability date
  - fecha de disponibilidad de material
  - transit time
  - tiempo de tránsito
  - pick pack time
  - tiempo de picking y embalaje
  - loading time
  - tiempo de carga
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Delivery and Transportation Scheduling in SAP SD

## Operational Summary
SAP S/4HANA calculates delivery-related dates by working backwards from the customer's requested delivery date (backward scheduling) or forward from today when the backward result falls in the past (forward scheduling). Scheduling considers four timeframes pulled from the shipping point and the route. The precision of scheduling (to the minute vs. date-only) depends on whether working times are maintained for the shipping point.

## Questions This Chunk Answers
- How does backward scheduling work and what timeframes does it consider?
- When does the system switch to forward scheduling?
- What is the difference between precise scheduling and daily scheduling?
- What is a route schedule and when should it be used?

## What This Configuration Controls
Scheduling determines the material availability date (when stock must be ready for picking), the pick/pack start date, the loading date, and the goods issue date. Incorrect configuration of lead times leads to unrealistic ATP results and customer delivery date errors.

## SPRO Path or Direct T-code
- Scheduling per shipping point: LE → Shipping → Basic Shipping Functions → Scheduling → Define Scheduling by Shipping Point
- Route lead times: LE → Shipping → Routes → Define Routes → Define Routes and Stages
- Route schedules: LE → Shipping → Routes → Route Schedules

## Key Parameters

### Timeframes Used in Scheduling

| Timeframe | Source |
|---|---|
| Transit time | Route |
| Transportation lead time | Route |
| Loading time | Shipping point |
| Pick/pack time | Shipping point |

The system works backwards from the **requested delivery date**:
```
Requested delivery date
  − Transit time           → Goods issue date
  − Loading time           → Loading start date
  − Pick/pack time         → Picking start date
  − Transport lead time    → Material availability date
```

### Backward Scheduling
The standard scheduling mode. Starting from the customer's requested delivery date, the system subtracts each timeframe in sequence to calculate the material availability date. If the material availability date falls in the past, the system automatically switches to forward scheduling.

### Forward Scheduling
Triggered when:
- Backward scheduling produces a material availability date in the past
- The material is not available on the backward-scheduled availability date
- The outbound delivery is created after the original material availability date

Forward scheduling confirms a **new, later delivery date** based on the current date plus the scheduling lead times. Whether rescheduling occurs during delivery creation is configurable per delivery type.

### Precise Scheduling vs. Daily Scheduling
The scheduling mode is configured per shipping point:

| Mode | Trigger | Precision | Pick/pack time unit |
|---|---|---|---|
| **Precise scheduling** | Working times (shift sequence) maintained for shipping point | Results displayed to the minute | Hours and minutes |
| **Daily scheduling** | No working times maintained | Results displayed as date only | Days (hours/minutes used internally) |

Both modes use the factory calendar of the route to determine when the route is operational.

### Route Schedules
A route schedule organises regular outbound deliveries from one shipping point to multiple ship-to parties along a fixed route with a fixed departure pattern.

A route schedule contains:
- A route
- A weekday as departure date and departure time
- A list of ship-to parties
- An itinerary (optional)

Route schedules can be used in sales orders, stock transfer orders, and outbound deliveries — determined automatically by the system. Configurable per shipping point / order type / purchasing document type / delivering plant / delivery type.

> For detailed route schedule configuration, see SAP Note 146829.

## Configuration Impact
- Shipping point working times (shift sequence) must be maintained to enable precise scheduling.
- Route transit times and transportation lead times must be maintained on route master data.
- Delivery type must allow rescheduling for forward scheduling to take effect during delivery creation.
- Route schedules reduce manual effort in regular delivery lanes but require upfront maintenance of itineraries and departure calendars.

## Common Configuration Errors
- Pick/pack time = 0 in shipping point → scheduling collapses, all dates set to the same day.
- Route transit time not maintained → transit time = 0, delivery confirmed earlier than physically possible.
- Shift sequence not aligned with factory calendar → precise scheduling produces incorrect results.

## Cross-References
- Shipping point and loading point: enterprise-structure-shipping-point-loading-point-001
- Route and shipping point determination: configuration-delivery-field-determination-001
- Delivery creation process: shipping-outbound-delivery-creation-process-001
