---
schema_version: 1
id: order-management-sales-monitoring-analytics-001
title: "Sales Monitoring and Analytics in SAP S/4HANA — Fulfillment App, Sales Plans, and CDS Analytics"
area: order-management
process_tags: [order-to-cash]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "149-161"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - Sales Order Fulfillment App
  - app cumplimiento pedidos de cliente
  - SAP Smart Business
  - sales monitoring S4HANA
  - monitoreo de ventas S4HANA
  - Sales Performance Plan Actual
  - Manage Sales Plans
  - planes de ventas SAP
  - CDS views analytics
  - Core Data Services analytics
  - real-time analytics S4HANA
  - analítica en tiempo real SAP S4HANA
  - qué es el Sales Order Fulfillment en SAP
level: functional
status: draft
quality: medium
created: 2026-06-16
last_updated: 2026-06-16
---

# Sales Monitoring and Analytics in SAP S/4HANA — Fulfillment App, Sales Plans, and CDS Analytics

## Operational Summary
SAP S/4HANA provides integrated tools for monitoring sales order fulfillment, managing sales targets, and analyzing sales performance in real time. The *Sales Order Fulfillment* app surfaces orders that cannot be fulfilled and guides users to resolve impediments. *SAP Smart Business* provides KPI-driven exception management with direct action links. The *Manage Sales Plans* app enables target planning by customer, material, and organizational dimension. Real-time analytics are powered by *Core Data Services* (CDS) views on the live transactional database, eliminating the need for a separate analytical system.

## Questions This Chunk Answers
- What does the Sales Order Fulfillment app show and how does a sales representative use it?
- What is SAP Smart Business and how does it connect KPI dashboards to actionable transactions?
- How are sales plans created and tracked against actuals in SAP S/4HANA?
- How does SAP S/4HANA provide real-time analytics without a separate OLAP system?
- What are Core Data Services (CDS) and what role do they play in S/4HANA reporting?

## When It Applies and Context
These tools are used by internal sales representatives (fulfillment monitoring), sales managers (plan vs. actual tracking), and analysts (ad-hoc exploration). They represent the monitoring and analytics layer of the order-to-cash cycle, operating on the same transactional data used by operational SD transactions.

## Process Flow

The typical sequence for monitoring and acting on fulfillment issues in SAP S/4HANA:
1. A sales order is blocked, incomplete, or cannot be fulfilled (backorder, missing stock, credit block)
2. The *Sales Order Fulfillment* app surfaces the order in the prioritized exception list
3. The sales representative reviews the issue type and selects a resolution option directly from the app
4. If the issue is a KPI-level exception (for example, revenue gap vs. plan), *SAP Smart Business* tiles alert the manager with a red indicator
5. The manager clicks the tile to drill down to the underlying data and navigates to the transaction to act
6. For planning cycles, the manager uses *Manage Sales Plans* to update targets and tracks results in *Sales Performance — Plan/Actual*

## Sales Order Fulfillment App

### Traditional Approach vs. S/4HANA Approach
In traditional SAP ERP, employees had to check multiple reports separately to identify fulfillment issues. Because no single screen showed all open impediments for a sales order, exceptional situations could remain undetected. Communication and decisions about problems could not be tracked in the system.

In SAP S/4HANA, the *Sales Order Fulfillment* app provides internal sales representatives with a unified view of the current fulfillment situation. The app shows a prioritized list of sales orders that cannot be fulfilled, allowing users to focus on the highest-priority issues first.

### Features of the Sales Order Fulfillment App
The app offers:
- **Highlights impediments**: identifies the specific issue type for each sales order (billing block, incompletion, credit limit exceeded, backorder)
- **Supporting information**: provides context about the relevant document and the impacted business objects
- **Resolution options**: offers specific actions available directly from the app (for example, remove billing block, edit payment terms, navigate to Change Sales Order)

### Process Flow View
The app includes a graphical *process flow* visualization that shows the complete business process for a selected sales order — from order through supply, delivery, and invoice — and displays the status of each stage using semantic colors:
- **Red circle**: stage has one or more unresolved issues
- **Green circle**: all documents in this stage are in order

The process flow allows the user to identify which stage is blocking fulfillment and to navigate directly to the relevant document to resolve the issue.

## SAP Smart Business
*SAP Smart Business* is the exception-based working model that underpins monitoring tools in SAP S/4HANA. It combines analytics with action:
- **KPI tiles in the Fiori Launchpad**: display live key performance indicators with semantic colors (red/yellow/green) based on defined targets and thresholds
- **Exception-based focus**: surfaces only deviations from targets, reducing information overload
- **Direct action link**: from any KPI chart or data point, the user can navigate directly to the relevant SAP transaction to resolve the underlying issue — without losing context
- **Configuration via Smart Business Modeler apps**: administrators define KPIs, thresholds, and visual appearance without development

SAP Smart Business follows SAP Fiori guidelines and is accessible from the Fiori launchpad, making it available on any device.

## Sales Plans

### Manage Sales Plans App
Sales plans enable sales organizations to set quantitative targets for upcoming periods (monthly, quarterly, annual). The *Manage Sales Plans* app supports:
- **Dimension selection**: plans can be defined by any combination of customer, material, sales organization, distribution channel, and division
- **Excel-based workflow**: the user selects dimensions in the app, downloads a plan layout to Microsoft Excel, fills in target values offline, and uploads the file back to the plan
- **Multiple versions**: several plan versions can coexist for the same period (for example, a conservative baseline version and an optimistic version reflecting expected market growth)

Each user can only search, display, and edit sales plans that they created.

### Sales Performance — Plan/Actual App
After a plan is created, the *Sales Performance — Plan/Actual* app tracks actual results against targets:
- **Hybrid view**: a chart shows plan vs. actual trends visually; a table below shows the detail
- **Planned and actual values** represent either incoming sales orders or sales volume, depending on the plan version definition
- **Period comparison**: by month, quarter, or year, as defined in the plan version

## Real-Time Analytics Architecture

### Problem with Separate OLTP/OLAP Systems
Traditional ERP architectures separated transactional systems (OLTP: create orders, post goods issues) from analytical systems (OLAP: reports, aggregated data). This separation caused:
- **Information delays**: analytical data required an ETL (extract, transform, load) process from OLTP to OLAP before it was available for reporting
- **Data staleness**: reports ran on data that might be hours or days old
- **Data redundancy and complexity**: maintaining two synchronized systems increased IT overhead and introduced data governance risks

### SAP S/4HANA Approach: Single In-Memory Platform
SAP S/4HANA eliminates the OLTP/OLAP separation by running both workloads on a single in-memory platform (SAP HANA). Transactional and analytical queries execute against the same live data without an ETL layer. This provides:
- **Real-time reporting**: reports and dashboards always show the latest data, including orders created seconds earlier
- **Simplified data management**: one platform, one dataset, one governance model
- **Faster decision-making**: business users can act on current data during live customer interactions

### Core Data Services (CDS)
*Core Data Services* (CDS) is the technical framework SAP S/4HANA uses to implement real-time operational reporting. Key characteristics:
- CDS views are defined and maintained in the ABAP layer of S/4HANA
- They represent a *Virtual Data Model* (VDM) built on top of the transactional and master data tables
- SAP HANA generates SQL runtime views that execute data reads and transformations inside the database layer
- CDS views reuse existing ABAP authorization checks, maintaining data security across analytics and transactions
- The same CDS/VDM underpins embedded BW analytics, SAP Smart Business cockpits, and ad-hoc multidimensional reporting (OLAP-style pivot, filtering, sorting in a Web Dynpro grid)

## Cross-References
See also: order-management-collective-processing-001 (billing due list and order fulfillment execution)
See also: order-management-availability-check-atp-001 (backorders that appear in the fulfillment app)
See also: configuration-sap-fiori-launchpad-001 (Fiori launchpad where Smart Business tiles reside)
