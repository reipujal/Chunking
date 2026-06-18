---
schema_version: 1
id: credit-management-credit-rules-engine-001
title: "SAP Credit Management: Rules Engine — Scoring, Limits, and Check Rules"
area: credit-management
process_tags: [order-to-cash, credit-management]
chunk_type: configuration
sap_release: S/4HANA 1909
sources:
  - file: "S4F30_EN_Col12 Order to Cash Optimizations with SAP Receivables Management in SAP S4 HANA.pdf"
    relative_path: "S4F30_EN_Col12 Order to Cash Optimizations with SAP Receivables Management in SAP S4 HANA.pdf"
    pages: "39-43"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - credit rules engine SAP
  - scoring formula SAP credit management
  - credit limit formula SAP
  - credit check rule SAP
  - risk class scoring SAP
  - motor de reglas de crédito SAP
  - fórmula de puntuación de crédito
  - regla de verificación de crédito
  - clase de riesgo fórmula SAP
  - credit scoring rule risk class
  - credit eventing follow-on activities SAP
level: functional
status: draft
quality: high
created: 2026-06-18
last_updated: 2026-06-18
---

# SAP Credit Management: Rules Engine — Scoring, Limits, and Check Rules

## Operational Summary

The SAP Credit Management *Credit Rules Engine* provides three types of configurable rules that automate credit evaluation: the *Credit Scoring Rule* (calculates the business partner's credit score and derives the risk class), the *Credit Limit Rule* (calculates and proposes a credit limit per credit segment), and the *Credit Check Rule* (defines which check steps are executed when SD triggers the credit check). An *eventing* mechanism allows process chains to be built so that credit events (such as a change in risk class or credit score) automatically trigger follow-on activities. These capabilities are part of Advanced Credit Management and are not available in Basic Credit Management.

## Questions This Chunk Answers

- What is the Credit Scoring Rule, and what does it produce?
- How is a scoring formula structured, and what inputs can it use?
- What is the Credit Limit Rule, and how does it relate to credit segments?
- What are the building blocks of a formula (scoring or credit limit)?
- What does a Credit Check Rule define, and where is it assigned?
- What is credit eventing, and what are examples of credit events?

## What This Configuration Controls

The Credit Rules Engine automates the credit evaluation and monitoring process. Without it, credit scores, risk classes, and credit limits must be maintained manually by the credit analyst. With the rules engine:
- The credit score and risk class are recalculated automatically when relevant input data changes
- A credit limit is proposed automatically per credit segment
- Credit check steps are defined consistently in the check rule and applied uniformly when SD triggers the check
- Process chains (event → follow-on activity) reduce manual monitoring workload

All three rule types are assigned to the business partner's credit account (credit profile) and are part of the *Advanced Credit Management* licence tier.

## SPRO Path or Direct T-code

Not stated in source. These are FSCM Credit Management configuration objects (not standard SD SPRO entries).

## Key Parameters

### Credit Scoring Rule

The scoring rule automatically calculates the business partner's *credit score* and derives the corresponding *risk class*. The risk class is the value queried by SAP SD at order creation to select the applicable automatic credit control configuration entry.

The scoring is based on a *scoring formula*, freely definable by the user. A scoring formula can combine:
- SAP Business Partner master data (preconfigured field selection)
- Transactional data (e.g., payment behaviour)
- External credit agency ratings (multiple external ratings can be mapped to a single internal rating for comparability)
- Input parameters extensible via BAdI implementation

The scoring rule also defines the *validity period* of the scoring result. When the score expires or is invalidated, a credit event is triggered.

### Credit Limit Rule

The credit limit rule automatically proposes a credit limit for the business partner. If the business partner conducts business in multiple credit segments, a separate credit limit is calculated per credit segment. The credit limit formula is stored on the credit segment of the business partner.

A credit limit formula uses the same input parameters as the scoring formula (BP master data, external credit information, payment behaviour). A calculation log is available to explain the credit limit proposal.

### Formula Structure

Both the scoring formula and the credit limit formula are built from *formula steps*. Each step can be one of three types:

| Step Type | Purpose |
|---|---|
| Condition | Check a value against a threshold or set of values |
| Substitution | Set the score or limit value based on a condition result |
| Exception | Ignore the calculation for this step (bypasses the formula step) |

Formulas use *parameters* (values filled at runtime) and *functions*. Both the parameter list and the function list can be extended via BAdI implementations.

### Credit Check Rule

The *credit check rule* defines which credit check steps should be applied during the sales document process. Examples of steps that can be included in a check rule:
- Dynamic credit limit check
- Static credit limit check
- Oldest open item check

The check rule is assigned to the business partner's credit account at the *credit profile* level (not at the credit segment level). For each check rule, own thresholds can be defined per credit segment. If any single check step within the rule fails, the overall result of the credit check is set to negative.

### Events and Follow-On Activities

The *eventing* concept allows an automated monitoring process to be built as a chain of events and follow-on activities. When a predefined credit event occurs, configured follow-on activities are triggered automatically.

Examples of credit events:
- Score Invalid / Changed
- External Rating Invalid / Changed
- Credit Limit Invalid / Changed
- Change to Credit Limit Requested
- Credit Refused
- Payment Behaviour Summary: Dunning Data Invalid, Due Date Invalid, Payment Data Invalid
- Risk Class Changed
- Limit Utilisation Changed
- Block Set in Credit Management
- Special Attention Indicator Set

Example use case: if the business partner's external credit agency rating changes, the event *External Rating Changed* automatically triggers the formula to recalculate the credit score and risk class, which in turn may recalculate the credit limit.

## Configuration Impact

- The scoring rule populates the *risk class* in the credit profile. The risk class is the key used in the SD automatic credit control configuration table (credit control area + credit group + risk class → check rule). If the scoring rule produces an incorrect or unexpected risk class, the wrong check rule is applied in SD — resulting in either no block when one should occur, or a block when none should.
- The credit limit rule populates the credit limit per credit segment, which is the limit evaluated during the credit check.
- The check rule (assigned to the credit profile) must be consistent with the rules referenced in the SD automatic credit control configuration.

## Common Configuration Errors

| Symptom | Cause | Solution |
|---|---|---|
| Risk class not updated after score change | Scoring rule not assigned to business partner's credit profile | Assign the scoring rule in the credit profile |
| Credit limit not updated after new credit info | Credit limit rule not assigned or formula references external data not yet imported | Assign credit limit rule; verify external data import is complete before formula run |
| Follow-on activity not triggered after credit event | Event chain not configured or follow-on activity misconfigured | Review event chain Customizing in Credit Management |

## Cross-References

See also: credit-management-credit-master-data-001 (business partner credit profile where the scoring and check rules are assigned)
See also: credit-management-credit-check-sd-integration-001 (how the risk class produced by the scoring rule is used in the SD credit check trigger)
