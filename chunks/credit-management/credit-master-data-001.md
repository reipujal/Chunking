---
schema_version: 1
id: credit-management-credit-master-data-001
title: "SAP Credit Management: Master Data and Organisational Concepts"
area: credit-management
process_tags: [order-to-cash, credit-management]
chunk_type: concept
sap_release: S/4HANA 1909
sources:
  - file: "S4F30_EN_Col12 Order to Cash Optimizations with SAP Receivables Management in SAP S4 HANA.pdf"
    relative_path: "S4F30_EN_Col12 Order to Cash Optimizations with SAP Receivables Management in SAP S4 HANA.pdf"
    pages: "20-29"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - SAP Credit Management master data
  - business partner role UKM000
  - credit profile SAP
  - credit segment SAP
  - crédito FSCM datos maestros
  - perfil de crédito socio comercial
  - segmento de crédito SAP
  - gestión de crédito SAP S4HANA
  - Basic Credit Management vs Advanced Credit Management
  - credit control area credit segment
level: functional
status: draft
quality: high
created: 2026-06-18
last_updated: 2026-06-18
---

# SAP Credit Management: Master Data and Organisational Concepts

## Operational Summary

SAP Credit Management (FSCM-CR) organises credit risk data through a dedicated *Business Partner* role and a two-level credit data structure: the *credit profile* (company-wide data) and the *credit segment* (area-specific credit limits and payment-history data). Two tiers of functionality are available in S/4HANA: *Basic Credit Management*, included without additional licensing, and *Advanced Credit Management*, which adds formula-based scoring and limit calculation, credit eventing, Credit Limit Requests, and external credit agency integration.

## Questions This Chunk Answers

- What Business Partner role stores credit-specific data in SAP Credit Management?
- What is the difference between the credit profile and credit segment data in the Business Partner master?
- What is a credit segment, and how does it relate to a credit control area?
- How does the main credit segment (0000) aggregate exposure across sub-segments?
- How can customer hierarchies be modelled in SAP Credit Management?
- What functional capabilities are available in Basic Credit Management that are not available in Advanced?

## Definition

SAP Credit Management is the FSCM component that enables a company to implement a company-wide credit policy, calculate and monitor credit limits, and embed credit checks into key operational processes such as sales order creation and delivery processing. It is built on the *SAP Business Partner* (BP) object: credit-specific data is maintained in the BP using the dedicated role **UKM000** (*SAP Credit Management*).

## Purpose in the SD Process

When a sales order is created, SAP SD queries the risk class of the customer from the credit profile stored in the BP credit role (UKM000) and triggers the credit check in SAP Credit Management. The check evaluates credit limit utilisation and other criteria stored in the credit segment data. The result controls whether the sales document is processed normally, blocked, or released. This integration is described in detail in the companion process chunk (see Cross-References).

## Structure and Variants

### Business Partner Credit Data

The SAP Business Partner master record stores credit-relevant data in role **UKM000**. The credit data is divided into two levels:

**Credit Profile** (valid across all credit segments for the business partner):
- The rule governing scoring and credit limit calculation
- The current credit score and, if applicable, external agency valuations
- The *risk category* (risk class) of the business partner — this value is queried first in SD at order creation and determines which automatic credit control configuration entry applies
- The *check rule* for the credit limit check, which defines which credit check steps are executed when SD calls the credit check
- Notes, negative characteristics, credit security, and collateral information

**Credit Segment Data** (specific to each credit segment in which the business partner conducts business):
- The credit limit for the segment and the total credit exposure in that segment (credit limit utilisation)
- A manually set credit block (if present)
- Payment history key figures: highest dunning level, oldest open item, last payment date, average days sales outstanding (DSO), and highest turnover in the last 12 months
- The payment history information is provided by FI-AR and summarised in the *Payment History Key Figures* tab of the credit segment

The credit segment data forms the basis for the order-related credit decision: release or block of the sales order, and the resulting payment terms.

### Credit Segment Concept

A **credit segment** represents a credit monitoring area corresponding to one or several credit control areas. Its purpose is to allow the definition of separate credit limits for a business partner in different regions or divisions.

Key properties:
- A credit control area is assigned to exactly one credit segment
- **Credit Segment 0000** is the *main credit segment*, pre-defined and not changeable. It represents the credit limit at company (portfolio) level for the business partner
- A sub-segment can be configured to contribute its exposure to Segment 0000, so that both the sub-segment limit and the company-level limit are checked during the credit check
- Sub-segments cannot have further sub-segments (maximum two levels)
- Only the main credit segment (0000) can be used to define a total company-level credit limit in addition to individual sub-segment limits

During the credit limit check (for example, at sales order creation):
1. The credit limit utilisation of the business partner in the *corresponding credit segment* is checked (sub-segment limit)
2. If that sub-segment contributes to Segment 0000, the credit limit utilisation in the *main segment* is also checked (company-level limit)

A sub-segment contributes to the main segment only when: (a) more than one credit segment exists, and (b) credit limits are maintained in Segment 0000.

### Basic vs Advanced Credit Management

In SAP S/4HANA, two tiers are available:

| Capability | Basic CM | Advanced CM |
|---|---|---|
| Business Partner in role UKM000 | ✓ | ✓ |
| Credit limit per credit segment | ✓ | ✓ |
| Manual credit score and risk class | ✓ | ✓ |
| Documented Credit Decision (DCD) | ✓ (for document blocks) | ✓ |
| Formula-based score and credit limit calculation | — | ✓ |
| Credit eventing (automated follow-on actions) | — | ✓ |
| Credit Limit Request Case | — | ✓ |
| Integration with SAP S/4HANA Cloud for credit information | — | ✓ |

Basic Credit Management is provided without additional licensing as part of the S/4HANA technical foundation. Advanced Credit Management requires a separate licence.

### Customer Hierarchies in Credit Management

The following relationship types can be maintained at the credit segment level between business partners:

- **FUKM001 / TUKM001** (*Higher-level Credit Management Account of / Lower-level Credit Management Account of*): defines parent-child credit hierarchies (up to 10 levels). The credit exposure of lower-level credit accounts rolls up into the total exposure of the higher-level account. The report `UKM_COMMITMENTS` shows how sub-account exposure consolidates to the higher-level account.
- **TUKMSB0** (*In Credit Management is managed by*): assigns the responsible credit analyst (per credit segment) to the business partner. The analyst must also exist as a Business Partner (Person) in the Employee role.
- **TUKMSBG** (*Is in credit analyst group*): organises credit analysts into groups.

## Relationship with Other SAP SD Objects

The BP credit role UKM000 is the master data source for the credit check process. The risk category (risk class) stored in the credit profile is queried at SO creation; the check rule stored in the credit profile determines which credit check steps are executed. The credit segment stores the credit limit and exposure data used for the actual check. Changes to the credit limit, risk class, or credit score do not automatically re-evaluate already-blocked sales orders — a re-check must be triggered manually or via a batch program (described in the process integration chunk).

## Cross-References

See also: credit-management-credit-check-sd-integration-001 (how SD queries this master data to execute the credit check and block/release orders)
See also: credit-management-credit-rules-engine-001 (scoring and limit calculation formulas that populate the risk class and credit limit in this master data)
See also: master-data-business-partner-master-data-001 (general BP master data including SD-specific roles; UKM000 is the credit-specific role)
