---
schema_version: 1
id: configuration-sap-fiori-launchpad-001
title: "SAP Fiori Launchpad — User Experience Paradigm and Navigation"
area: configuration
process_tags: [none]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "10-15"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - SAP Fiori
  - SAP Fiori launchpad
  - Fiori launchpad tiles
  - grupos de mosaicos Fiori
  - tile catalog Fiori
  - tipos de apps Fiori
  - transaction apps analytical apps factsheets
  - cinco principios Fiori
  - personalización launchpad SAP
  - qué es SAP Fiori y cómo funciona el launchpad
level: functional
status: draft
quality: high
created: 2026-06-16
last_updated: 2026-06-16
---

# SAP Fiori Launchpad — User Experience Paradigm and Navigation

## Operational Summary
*SAP Fiori* is SAP's user experience (UX) framework built around five design principles: role-based, responsive, simple, coherent, and instant value. It replaces the traditional SAP GUI for the most commonly used transactions and is the standard interface for SAP S/4HANA. The *SAP Fiori Launchpad* is the central entry point — a shell that hosts Fiori apps, displays live KPI tiles, and provides navigation, personalization, and embedded support. Three types of Fiori apps cover different interaction needs: *transaction apps* for process execution, *analytical apps* for monitoring, and *factsheets* for data exploration.

## Questions This Chunk Answers
- What are the five design principles of SAP Fiori?
- What is the difference between transaction apps, analytical apps, and factsheets?
- What is the SAP Fiori Launchpad and how is it structured?
- How can users personalize the SAP Fiori Launchpad?
- What are the three user types addressed by SAP Fiori and what are their characteristics?

## Definition
*SAP Fiori* (UI) and *user experience* (UX) represent two distinct but related concepts. The *user interface* (UI) describes the interface between user and device; it aims at maximizing efficiency. *User experience* (UX) takes the perspective of the end user and aims at creating a positive, motivating interaction — not only during system use but also before and after. SAP Fiori is SAP's strategic commitment to delivering good UX for business software.

## The Five SAP Fiori Design Principles
All SAP Fiori apps are built around five core principles:

| Principle | Meaning |
|---|---|
| *Role-based* | Users see only the apps relevant to their specific role; the Launchpad is configured per role |
| *Responsive* | App interfaces adapt automatically to the screen size and device type (desktop, tablet, phone) |
| *Simple* | Each app covers one user, one use case, with a maximum of three screens per app |
| *Coherent* | All apps share the same visual language, navigation patterns, and interaction model |
| *Instant value* | Low adoption barrier for both IT (simple deployment and integration) and end users (intuitive design) |

The *simple* principle is particularly significant for enterprise software: traditional SAP GUI transactions often covered multiple complex processes in one screen, requiring extensive training. A Fiori app focuses on a single task, making it accessible to occasional users.

## User Types
SAP Fiori recognizes three types of users with different needs:

**Occasional user**: uses the system rarely; needs applications that are immediately intuitive without training; typically executes single-step tasks (for example, approving an expense report or checking a delivery status).

**Expert / key user**: a fully trained SAP user who knows processes and applications in detail; works across multiple systems and UI types; uses Fiori for efficiency alongside deeper SAP GUI access for complex configurations.

**Developer / programmer**: deep process and system knowledge; responsible for adapting and extending applications; typically works with multiple UIs and technical tools beyond the Launchpad.

## The Three SAP Fiori App Types

**Transaction apps** provide task-based access to standard SAP operations: create, change, or display sales orders, deliveries, invoices, master records, and other documents. They support guided navigation through processes with up to three screens. Example: *Create Sales Order*, *Change Delivery*, *Create Billing Documents*.

**Analytical apps** provide a visual overview of complex topics for monitoring or tracking purposes — charts, KPIs, and exception-based highlights. They connect data points to the underlying transaction so users can take immediate action. Example: *Sales Order Fulfillment*, *Revenue Variance Analysis*. (See also: SAP Smart Business tiles in order-management-sales-monitoring-analytics-001.)

**Factsheets** provide a 360-degree view of a specific business object: a customer, material, sales order, or delivery. They support search and exploration with contextual navigation between related objects. Example: searching for a material and seeing all open sales orders, deliveries, and prices for that material without running separate reports.

## SAP Fiori Launchpad

### Structure
The *SAP Fiori Launchpad* is the shell that hosts all Fiori apps and provides navigation between them. Its home page displays:
- **Tiles**: each tile represents one business application. Tiles can show *live status indicators* (for example, number of open approval tasks, or a KPI value with color-coded status)
- **Tile groups**: tiles are organized into groups by topic or role (for example, a "Sales Processing" group containing all order-related apps)
- **Navigation bar**: persistent top bar for search, user settings, and notifications

The Launchpad is the entry point for Fiori apps on both mobile and desktop devices.

### Tile Catalog
The *tile catalog* lists all apps available to a given user based on their role assignment. Users can browse the catalog to add apps to their home page that are not already visible. The catalog provides a complete inventory of apps the user is authorized to use.

### Personalization
The SAP Fiori Launchpad supports user-level personalization (when enabled by the Launchpad configuration):
- **Add apps** from the tile catalog to the home page
- **Remove apps** that are not needed from the home page
- **Create, rename, and reorder tile groups**
- **Create filtered app variants**: for example, a user responsible for German market cash management can create a tile that opens the cash position report pre-filtered for Germany, arriving at the relevant data in one click

Note: the ability to personalize must be enabled in the Launchpad configuration; it is not active by default.

## Relationship with Other SAP SD Objects
- *SAP Smart Business*: uses the Fiori Launchpad to display KPI tiles for sales monitoring; tiles link directly to SD transactions and apps (see order-management-sales-monitoring-analytics-001)
- *Create Billing Documents app*: a transaction app in the Fiori Launchpad for billing execution (see billing-create-billing-documents-fiori-001)
- *Sales Order Fulfillment app*: an example of a transaction app in the Fiori Launchpad used by internal sales representatives
- *SAP Fiori roles*: the Launchpad is configured per user role in the SAP authorization concept; the apps visible to an SD sales representative differ from those visible to a warehouse clerk or billing administrator

## Cross-References
See also: order-management-sales-monitoring-analytics-001 (SAP Smart Business tiles and analytical apps in the Launchpad)
See also: billing-create-billing-documents-fiori-001 (Fiori app for billing document creation)
