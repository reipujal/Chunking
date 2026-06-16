"""Build chunk_topic_map.json — run from workspace root."""
import json

MAPPINGS = {
    # billing (18 chunks)
    "billing-billing-document-cancellation-001": [
        {"topic_id": "o2c.billing.complaints", "confidence": "high", "notes": "Cancellation reversal via SV; billing complaints process."}
    ],
    "billing-billing-document-creation-methods-001": [
        {"topic_id": "o2c.billing.standard", "confidence": "high", "notes": "All billing creation methods (VF01, VF04, collective)."}
    ],
    "billing-billing-document-integration-001": [
        {"topic_id": "o2c.billing.standard", "confidence": "high", "notes": "Integration of billing in the O2C chain."}
    ],
    "billing-billing-document-structure-001": [
        {"topic_id": "o2c.billing.standard", "confidence": "high", "notes": "Billing document header/item structure."}
    ],
    "billing-billing-plans-concept-001": [
        {"topic_id": "o2c.billing.special", "confidence": "high", "notes": "Periodic and milestone billing plans."}
    ],
    "billing-create-billing-documents-fiori-001": [
        {"topic_id": "o2c.billing.standard", "confidence": "high", "notes": "Fiori-based billing creation and management."},
        {"topic_id": "platform.fiori", "confidence": "medium", "notes": "Fiori app landscape for billing."}
    ],
    "billing-credit-debit-memo-process-001": [
        {"topic_id": "o2c.billing.complaints", "confidence": "high", "notes": "Credit/debit memo request to memo process."}
    ],
    "billing-document-table-structure-001": [
        {"topic_id": "o2c.billing.standard", "confidence": "medium", "notes": "Technical tables (VBRK/VBRP); structural/technical view of billing."}
    ],
    "billing-down-payment-processing-001": [
        {"topic_id": "o2c.billing.special", "confidence": "high", "notes": "Down payment billing with billing plan type A."}
    ],
    "billing-installment-payments-001": [
        {"topic_id": "o2c.billing.special", "confidence": "high", "notes": "Installment payment agreements and billing."}
    ],
    "billing-invoice-combination-and-split-001": [
        {"topic_id": "o2c.billing.settlement", "confidence": "high", "notes": "Invoice combination criteria and split logic."}
    ],
    "billing-invoice-correction-request-process-001": [
        {"topic_id": "o2c.billing.complaints", "confidence": "high", "notes": "Invoice correction request (RK) process."}
    ],
    "billing-invoice-list-001": [
        {"topic_id": "o2c.billing.settlement", "confidence": "high", "notes": "Invoice list creation and factoring discount."}
    ],
    "billing-omnichannel-convergent-billing-001": [
        {"topic_id": "o2c.billing.settlement", "confidence": "high", "notes": "Convergent billing, EBDR, omnichannel settlement."}
    ],
    "billing-preliminary-billing-documents-001": [
        {"topic_id": "o2c.billing.special", "confidence": "high", "notes": "PBD concept and processing."}
    ],
    "billing-pro-forma-invoice-001": [
        {"topic_id": "o2c.billing.special", "confidence": "high", "notes": "Pro forma invoice types (F5, F8)."}
    ],
    "billing-returns-process-001": [
        {"topic_id": "o2c.billing.complaints", "confidence": "high", "notes": "Returns order to credit memo; S4600 secondary source added."}
    ],
    "billing-value-dated-credit-memos-001": [
        {"topic_id": "o2c.billing.complaints", "confidence": "medium", "notes": "Single-page source (phys 109); specialized sub-type of credit memo."}
    ],

    # configuration (21 chunks)
    "configuration-billing-account-determination-001": [
        {"topic_id": "o2c.billing.fi", "confidence": "high", "notes": "VKOA account determination for billing."}
    ],
    "configuration-billing-copying-control-001": [
        {"topic_id": "xfunc.copy", "confidence": "high", "notes": "Billing facet of copy control (delivery->billing, order->billing)."}
    ],
    "configuration-billing-data-flow-001": [
        {"topic_id": "xfunc.copy", "confidence": "medium", "notes": "Data flow via reference documents, governed by copy control."},
        {"topic_id": "o2c.billing.standard", "confidence": "medium", "notes": "Billing-perspective view of document data flow."}
    ],
    "configuration-billing-fi-interface-controls-001": [
        {"topic_id": "o2c.billing.fi", "confidence": "high", "notes": "SD-FI interface parameter controls."}
    ],
    "configuration-billing-negative-postings-001": [
        {"topic_id": "o2c.billing.fi", "confidence": "high", "notes": "Negative posting configuration for cancellations."}
    ],
    "configuration-billing-output-management-brfplus-001": [
        {"topic_id": "xfunc.output", "confidence": "high",
         "notes": "SUPPLEMENTARY per authority_registry: billing-specific BRFplus facet. S4650 Unit 4 will become primary for the full topic."}
    ],
    "configuration-billing-relevance-item-category-001": [
        {"topic_id": "ctrl.billing_type", "confidence": "high", "notes": "Billing relevance field on item category."}
    ],
    "configuration-billing-types-sap-s4hana-001": [
        {"topic_id": "ctrl.billing_type", "confidence": "high", "notes": "Standard billing types and their controls."}
    ],
    "configuration-delivery-field-determination-001": [
        {"topic_id": "o2c.delivery.outbound", "confidence": "high",
         "notes": "Auto-determination of plant, shipping conditions, shipping point, route."}
    ],
    "configuration-delivery-item-category-001": [
        {"topic_id": "ctrl.delivery", "confidence": "high", "notes": "Delivery item category and determination."}
    ],
    "configuration-delivery-process-customizing-001": [
        {"topic_id": "xfunc.copy", "confidence": "high",
         "notes": "Delivery facet of copy control; also covers split criteria and special scenarios."}
    ],
    "configuration-delivery-scheduling-001": [
        {"topic_id": "o2c.delivery.outbound", "confidence": "high", "notes": "Delivery and transportation scheduling configuration."}
    ],
    "configuration-delivery-type-001": [
        {"topic_id": "ctrl.delivery", "confidence": "high", "notes": "Delivery type concept and configuration."}
    ],
    "configuration-flexible-billing-document-numbering-001": [
        {"topic_id": "ctrl.billing_type", "confidence": "medium", "notes": "Flexible numbering is a billing type control feature."}
    ],
    "configuration-pricing-procedure-configuration-001": [
        {"topic_id": "price.config", "confidence": "high", "notes": "Pricing procedure steps, requirements, alt calc types."}
    ],
    "configuration-sales-copying-control-001": [
        {"topic_id": "xfunc.copy", "confidence": "high", "notes": "Sales facet of copy control."}
    ],
    "configuration-sales-document-type-control-001": [
        {"topic_id": "ctrl.sales", "confidence": "high", "notes": "Sales document type (VOV8) controls."}
    ],
    "configuration-sales-incompletion-check-001": [
        {"topic_id": "xfunc.incompletion", "confidence": "high", "notes": "Incompletion log and procedure configuration."}
    ],
    "configuration-sales-item-category-control-001": [
        {"topic_id": "ctrl.sales", "confidence": "high", "notes": "Item category (VOV7) controls and determination (VOV4)."}
    ],
    "configuration-sap-fiori-launchpad-001": [
        {"topic_id": "platform.fiori", "confidence": "high", "notes": "Fiori launchpad UX paradigm; S4600 primary."}
    ],
    "configuration-schedule-line-category-control-001": [
        {"topic_id": "ctrl.sales", "confidence": "high", "notes": "Schedule line category (VOV6) controls and determination."}
    ],

    # enterprise-structure (5 chunks)
    "enterprise-structure-billing-organizational-assignment-001": [
        {"topic_id": "ent.org.sales", "confidence": "high",
         "notes": "Billing-facet org assignments; S4615 primary. Distributed authority within ent.org.sales."}
    ],
    "enterprise-structure-head-office-branch-billing-001": [
        {"topic_id": "ent.org.sales", "confidence": "medium",
         "notes": "Head-office/branch billing scenario; S4615, single-page source."}
    ],
    "enterprise-structure-sales-distribution-enterprise-structure-001": [
        {"topic_id": "ent.org.sales", "confidence": "high",
         "notes": "General SD enterprise structure (sales org, DC, division, sales area). S4605 primary."}
    ],
    "enterprise-structure-shipping-point-loading-point-001": [
        {"topic_id": "ent.org.shipping", "confidence": "high", "notes": "Shipping point and loading point; S4610 primary."}
    ],
    "enterprise-structure-warehouse-org-units-ewm-001": [
        {"topic_id": "ent.org.warehouse", "confidence": "high", "notes": "EWM/IM warehouse org structure; S4610 primary."}
    ],

    # integration (2 chunks)
    "integration-general-billing-interface-001": [
        {"topic_id": "integration.gbi", "confidence": "high", "notes": "GBI for external billing; S4615 primary."}
    ],
    "integration-sales-document-technical-tables-001": [
        {"topic_id": "o2c.order.basic", "confidence": "medium",
         "notes": "VBAK/VBAP/VBUK/VBUP table structure; technical complement to sales order processing. S4605 back-matter."}
    ],

    # master-data (5 chunks)
    "master-data-business-partner-master-data-001": [
        {"topic_id": "ent.master.bp", "confidence": "high", "notes": "Customer master in BP model; S4600 primary."}
    ],
    "master-data-material-determination-001": [
        {"topic_id": "xfunc.material_det", "confidence": "high",
         "notes": "Product substitution / material determination. Density advisory warning active (70 w/p)."}
    ],
    "master-data-material-listing-exclusion-001": [
        {"topic_id": "xfunc.material_det", "confidence": "high", "notes": "Positive/negative material listing and exclusion."}
    ],
    "master-data-material-master-sd-001": [
        {"topic_id": "ent.master.material", "confidence": "high", "notes": "Material master SD views + CMiR; S4600 primary."}
    ],
    "master-data-sd-partner-functions-001": [
        {"topic_id": "ent.master.partner", "confidence": "high", "notes": "Partner functions and determination; S4605 primary."}
    ],

    # order-management (11 chunks)
    "order-management-availability-check-atp-001": [
        {"topic_id": "o2c.order.atp", "confidence": "high", "notes": "ATP concept and configuration; S4600 primary."}
    ],
    "order-management-backorder-processing-001": [
        {"topic_id": "o2c.order.atp", "confidence": "high", "notes": "BOP and ATP scenarios; S4600 primary."}
    ],
    "order-management-collective-processing-001": [
        {"topic_id": "o2c.order.collective", "confidence": "high",
         "notes": "Collective delivery/picking/billing processing; S4600 primary."}
    ],
    "order-management-outline-agreements-scheduling-quantity-contracts-001": [
        {"topic_id": "o2c.order.outline", "confidence": "high",
         "notes": "Scheduling agreements and quantity contracts; S4605 primary."}
    ],
    "order-management-presales-additional-processes-001": [
        {"topic_id": "o2c.presales", "confidence": "high", "notes": "Inquiries and quotations; S4600 primary."},
        {"topic_id": "o2c.order.special", "confidence": "medium",
         "notes": "Also covers MTO and service products; bundled in the same chunk."}
    ],
    "order-management-sales-distribution-process-001": [
        {"topic_id": "o2c.order.basic", "confidence": "high",
         "notes": "O2C process overview and SD document types; S4605 primary."}
    ],
    "order-management-sales-document-data-flow-001": [
        {"topic_id": "xfunc.copy", "confidence": "medium",
         "notes": "Create-with-reference and document flow; governed by copy control."},
        {"topic_id": "o2c.order.basic", "confidence": "medium",
         "notes": "User-facing perspective of document flow in sales order processing."}
    ],
    "order-management-sales-monitoring-analytics-001": [
        {"topic_id": "analytics.sales", "confidence": "high",
         "notes": "Fulfillment app, sales plans, CDS analytics; S4600 primary."}
    ],
    "order-management-sales-order-source-of-data-001": [
        {"topic_id": "o2c.order.basic", "confidence": "high",
         "notes": "Data sources during order entry (master data, copy control); S4605 primary."}
    ],
    "order-management-sales-order-special-features-001": [
        {"topic_id": "o2c.order.basic", "confidence": "high",
         "notes": "Special features in sales order processing; S4605 primary."}
    ],
    "order-management-value-contracts-001": [
        {"topic_id": "o2c.order.outline", "confidence": "high",
         "notes": "Value contracts with release orders; S4605 primary."}
    ],

    # pricing (10 chunks)
    "pricing-condition-contract-maintenance-001": [
        {"topic_id": "price.ccm", "confidence": "high", "notes": "Condition contract creation and maintenance; S4620 primary."}
    ],
    "pricing-condition-contract-management-concept-001": [
        {"topic_id": "price.ccm", "confidence": "high", "notes": "CCM concept and overview; S4620 primary."}
    ],
    "pricing-condition-contract-settlement-001": [
        {"topic_id": "price.ccm", "confidence": "high", "notes": "Settlement run and document flow; S4620 primary."}
    ],
    "pricing-condition-records-001": [
        {"topic_id": "price.records", "confidence": "high",
         "notes": "Condition record creation, maintenance, reporting; S4620 primary."}
    ],
    "pricing-condition-technique-overview-001": [
        {"topic_id": "price.technique", "confidence": "high", "notes": "Condition technique mechanics; S4620 primary."}
    ],
    "pricing-free-goods-001": [
        {"topic_id": "price.free_goods", "confidence": "high",
         "notes": "Automatic free goods determination; S4605 primary."}
    ],
    "pricing-pricing-agreements-001": [
        {"topic_id": "price.agreements", "confidence": "high", "notes": "Promotions and sales deals; S4620 primary."}
    ],
    "pricing-special-condition-types-001": [
        {"topic_id": "price.special", "confidence": "high", "notes": "Special condition types; S4620 primary."}
    ],
    "pricing-special-pricing-functions-001": [
        {"topic_id": "price.special", "confidence": "high",
         "notes": "Group conditions, exclusion groups, condition supplements; S4620 primary."}
    ],
    "pricing-statistical-condition-types-001": [
        {"topic_id": "price.special", "confidence": "medium",
         "notes": "Statistical conditions and tax determination; overlaps price.config on tax. S4620 primary."}
    ],

    # shipping (8 chunks)
    "shipping-delivery-document-concept-001": [
        {"topic_id": "o2c.delivery.outbound", "confidence": "high", "notes": "Delivery document types and concept; S4610 primary."}
    ],
    "shipping-delivery-document-structure-001": [
        {"topic_id": "o2c.delivery.outbound", "confidence": "high", "notes": "Delivery document structure; S4610 primary."}
    ],
    "shipping-delivery-special-functions-001": [
        {"topic_id": "o2c.delivery.special", "confidence": "high",
         "notes": "Delivery pricing, interface, incompletion; S4610 primary."}
    ],
    "shipping-ewm-picking-process-001": [
        {"topic_id": "o2c.delivery.picking", "confidence": "high", "notes": "EWM picking process; S4610 primary."}
    ],
    "shipping-goods-issue-ewm-001": [
        {"topic_id": "o2c.delivery.picking", "confidence": "high",
         "notes": "Goods issue posting and delivery split; S4610 primary."}
    ],
    "shipping-inbound-delivery-ewm-001": [
        {"topic_id": "o2c.delivery.inbound", "confidence": "high", "notes": "Inbound delivery and GR in EWM; S4610 primary."}
    ],
    "shipping-outbound-delivery-creation-process-001": [
        {"topic_id": "o2c.delivery.outbound", "confidence": "high",
         "notes": "Delivery creation process (collective, due list, picking location); S4610 primary."}
    ],
    "shipping-outbound-delivery-monitor-001": [
        {"topic_id": "o2c.delivery.outbound", "confidence": "medium",
         "notes": "Outbound delivery monitor; also used as collective processing tool."},
        {"topic_id": "o2c.order.collective", "confidence": "medium",
         "notes": "Monitor used for collective picking and GI; overlaps collective processing topic."}
    ],

    # special-processes (2 chunks)
    "special-processes-cash-sales-process-001": [
        {"topic_id": "o2c.order.special", "confidence": "high",
         "notes": "Cash sale. CS/BV conflict documented in chunk body and authority_registry."}
    ],
    "special-processes-sales-special-business-transactions-001": [
        {"topic_id": "o2c.order.special", "confidence": "high",
         "notes": "Rush orders, cash sales (BV/BV per S4605), consignment, FoC. S4605 primary."}
    ],
}

output = {
    "built": "2026-06-16",
    "total_chunks": len(MAPPINGS),
    "note": (
        "Maps each chunk to one or more topics with confidence level. "
        "confidence=high: unambiguous; confidence=medium: multi-topic bundle or caveats worth reviewing; "
        "confidence=low: review recommended. Primary topic is listed first."
    ),
    "chunks": [
        {"chunk_id": cid, "topics": topics}
        for cid, topics in sorted(MAPPINGS.items())
    ]
}

with open("ontology/chunk_topic_map.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

n = len(output["chunks"])
medium_chunks = [c for c in output["chunks"] if any(t["confidence"] in ("medium", "low") for t in c["topics"])]
multi_topic = [c for c in output["chunks"] if len(c["topics"]) > 1]
print(f"Written: ontology/chunk_topic_map.json")
print(f"  Chunks mapped: {n}")
print(f"  Multi-topic chunks: {len(multi_topic)}")
print(f"  Chunks with medium/low confidence: {len(medium_chunks)}")
for c in medium_chunks:
    med = [t for t in c["topics"] if t["confidence"] in ("medium","low")]
    for t in med:
        print(f"    {c['chunk_id']} -> {t['topic_id']} [{t['confidence']}]")
