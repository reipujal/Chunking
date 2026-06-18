---
schema_version: 1
id: credit-management-credit-check-sd-integration-001
title: "Credit Check in the SD Order-to-Cash Process: Integration and Release"
area: credit-management
process_tags: [order-to-cash, credit-management]
chunk_type: process
sap_release: S/4HANA 1909
sources:
  - file: "S4F30_EN_Col12 Order to Cash Optimizations with SAP Receivables Management in SAP S4 HANA.pdf"
    relative_path: "S4F30_EN_Col12 Order to Cash Optimizations with SAP Receivables Management in SAP S4 HANA.pdf"
    pages: "23, 30-38"
    source_type: A
    role: primary
  - file: "Basic Credit Management (BD6)_ Process Diagrams.html.pdf"
    relative_path: "scope_items/Basic Credit Management (BD6)_ Process Diagrams.html.pdf"
    pages: "1-2, 5"
    source_type: B
    role: secondary
transactions: []
tables: ["UKM_ITEM"]
aliases:
  - credit check sales order SAP
  - bloqueo de crédito pedido SAP
  - liberación de crédito pedido SAP
  - automatic credit control SAP SD
  - control automático de crédito
  - Documented Credit Decision DCD
  - decisión documentada de crédito
  - credit group document type SD
  - grupo de crédito tipo de documento SD
  - credit limit request case SAP
  - UKM_ITEM commitment types
  - credit block release SD order
level: functional
status: draft
quality: high
created: 2026-06-18
last_updated: 2026-06-18
---

# Credit Check in the SD Order-to-Cash Process: Integration and Release

## Operational Summary

When a sales order, delivery, or goods issue is created or changed in SAP SD, an automatic credit check is triggered in SAP Credit Management. The check evaluates the business partner's credit limit utilisation and other criteria in the relevant credit segment. If the check fails and the SD configuration entry specifies a block, the sales document is blocked and a *Documented Credit Decision* (DCD) is created in Credit Management for structured review and release. Commitment data flows from SD to Credit Management in real time, keeping the credit exposure current throughout the O2C process.

## Questions This Chunk Answers

- At which points in the SD process is the credit check triggered?
- How does SAP SD determine which check rule to apply to a specific sales document?
- What commitment types does SAP SD write to the Credit Management system, and at which process steps?
- What is a Documented Credit Decision (DCD), and what does it contain?
- How is a blocked sales document released or rejected via the DCD?
- How does the Credit Limit Request Case process work?
- What is the difference between a direct-read credit exposure update and a transfer-report-based update?

## When It Applies and Context

The credit check in SD is triggered whenever a sales order is created or changed, when a delivery is created, and when a goods issue is posted — provided that *automatic credit control* is configured in the SD system for the relevant combination of credit control area, credit group, and risk class.

SAP Credit Management and SAP FI-AR feed two types of information into the credit segment:
- **Exposure data** (from SD and FI-AR): open order values, open delivery values, unposted billing documents, open FI items, and special liabilities
- **Payment history** (from FI-AR): updated periodically by the program `UKM_TRANSFER_VECTOR`

## Process Flow

**1. Risk class query:** When creating or changing a sales order, a delivery, or posting a goods issue, SAP SD queries the current risk class of the business partner from the credit profile in SAP Credit Management. The risk class reflects the business partner's creditworthiness and drives the selection of the applicable automatic credit control configuration.

**2. Credit check trigger:** The credit check is called if automatic credit control is configured in SAP SD for the applicable combination of: *credit control area* assigned to the sales document + *credit group* of the sales document type + *risk class* queried in step 1. This configuration entry specifies the check rule to be applied and whether a failed check results in a block or only a warning.

**3. Credit check execution:** SAP Credit Management executes the credit check using the check rule stored in the business partner's credit profile. The check evaluates credit limit utilisation in the relevant credit segment (and in the main credit segment, if the sub-segment contributes to segment 0000), as well as other criteria defined in the check rule (such as payment history thresholds).

**4. Credit status assignment:** If the check result is negative and the automatic credit control entry specifies a block, SAP SD sets the credit status of the sales document to *blocked*.

**5 + 6. DCD creation and review:** When a sales document is blocked due to a failed credit check, SAP Credit Management automatically and immediately creates a *Documented Credit Decision* (DCD). The DCD acts as a virtual case file containing:
- Sales order and business partner numbers, order status, priority, and order amounts
- Reason codes and the identity of the responsible credit analyst
- A snapshot of the credit account at the time of the block (credit status, values)
- A full credit check log showing every check step executed for every credit segment per the check rule
- Notes, attachments, and links to the sales document and BP master data

The DCD supports an approval workflow: the case can be routed to a credit analyst or manager for investigation and approval. From the DCD, the credit manager can release or reject the blocked document. When the block is resolved, the DCD is closed automatically.

**7 + 8. Commitment update:** After the sales document is stored in the database (as released), commitment data is updated in SAP Credit Management. All SD-side commitments are stored at detail level in table **UKM_ITEM**, using the following commitment types:
- **100** — Open Orders (sales order schedule lines)
- **400** — Open Delivery Value (delivery documents)
- **500** — Unposted Billing Documents (billing documents not yet posted to FI)
- **200** — Open Items from FI (posted accounting documents)
- **300** — Exposure from Special Liabilities

The amounts are stored in document currency and converted to credit segment currency at runtime.

### Exposure Update Methods

Three variants exist for updating credit exposure from FI-AR into SAP Credit Management:
- **Triggered manually** via the report `UKM_TRANSFER_ITEMS`: transfers either all FI items not yet transported (normal mode) or all current FI items (rebuild mode). Not recommended for delta updates.
- **Automatic update**: corresponding to the SD commitment update mechanism.
- **Direct read** (S/4HANA only): available when SAP Credit Management and SAP FI-AR reside on the same system. No batch transfer required.

The payment history (key figures such as DSO, oldest open item) is updated separately by running the program `UKM_TRANSFER_VECTOR` on a daily basis.

### Credit Limit Request Case

When a business partner exceeds their credit limit, the credit analyst can request an increase through a structured Credit Limit Request Case. Typical process flow:

1. Credit limit is exceeded.
2. An SD employee creates a Credit Limit Request Case. The case is pre-populated from the BP master record with the current credit limit, risk class, notes, and attachments relevant for the approval decision.
3. The credit analyst assigns the case to the approving credit manager; it appears in the credit manager's *Credit Case Organiser*.
4. If additional information is needed, the credit manager reassigns the case to the analyst.
5. Once information is complete, the credit manager decides whether to approve the new limit.
6. If approved: the credit manager enters the approved amount and approves the request. The credit limit is automatically updated in the BP master record and the case is closed.
7. If rejected: the case is closed without changes to the credit account.

The Credit Limit Request Case is part of *Advanced Credit Management* and is not available in Basic Credit Management.

## Conditions and Restrictions

- The credit check is only triggered when an automatic credit control configuration entry exists for the combination of credit control area + credit group + risk class. If no entry exists, no check is performed.
- The credit group is assigned to SD document types (order type, delivery type, goods issue posting) in Customizing. Different document types may trigger different check rules.
- A re-check of previously blocked orders can be triggered manually from the DCD or automatically via a batch program when the business partner's credit situation improves.
- The DCD is also created proactively by Credit Management when triggered by a credit event (for example, blocking the BP master record, or a change in credit limit or risk class).
- The Credit Limit Request Case is an Advanced Credit Management feature (not in Basic CM).

## Common Errors

| Symptom | Cause | Solution |
|---|---|---|
| Sales order not credit-checked at all | No automatic credit control entry for the credit control area + credit group + risk class combination | Verify configuration in Customizing for automatic credit control |
| Order blocked even though customer has sufficient limit | Stale exposure data — SD commitments not transferred to Credit Management | Verify automatic commitment update; run UKM_TRANSFER_ITEMS in rebuild mode to resync |
| DCD not created on block (only when Credit Management runs on a separate/distributed system) | Central Credit Management unreachable or WS-RM connection not configured | Check WS-RM partner profile and connectivity; not applicable to single-system S/4HANA |
| Payment history not current | UKM_TRANSFER_VECTOR not scheduled | Schedule the program to run daily |

## Cross-References

Prior step: order-management-sales-distribution-process-001 (standard O2C baseline; credit check is triggered at sales order creation)
See also: credit-management-credit-master-data-001 (BP role UKM000, credit profile, credit segment — the master data queried in steps 1-3 above)
See also: credit-management-credit-rules-engine-001 (check rule configuration that defines which credit check steps are executed in step 3)
See also: order-management-sales-order-special-features-001 (sales order special processing including credit-relevant document types)
