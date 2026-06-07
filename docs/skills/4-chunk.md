# Skill 4 — Decide How to Chunk

**Core principle**: a chunk is correct if it answers a concrete functional search intent without needing any other chunk.

## When to Create a New Chunk
- Change of business process (Delivery Creation ≠ Goods Issue)
- Change of audience: functional concept vs. SPRO configuration
- Change of customizing area (Output Determination ≠ Partner Determination)
- Topic exceeds 1500 words → subdivide by coherent sub-topics

## When to Group in a Single Chunk
- Content that cannot be separated conceptually
- Body would be under 300 words even with full extraction — merge with nearest related topic (300w is the hard floor)
- Only transaction lists without functional context

## Division Example — Pricing
```
pricing/condition-types-001.md       → what they are, structure, categories
pricing/access-sequences-001.md      → how the system searches for prices
pricing/pricing-procedures-001.md    → calculation schema, routines, V/08
pricing/condition-records-001.md     → where prices are maintained, VK11
```

## Grouping Example
Shipping Point + Loading Point: related in configuration and usage. One chunk is more useful than two that require each other.

## Before Writing: Present Plan to User

```
Section: [Unit N — Title] (p. X-Y)
Chunks identified:
  1. area/slug-001  |  type: process  |  p. 15-28
     intent: "How is an individual delivery created?"
  2. area/slug-001  |  type: concept  |  p. 12-14
     intent: "What delivery types exist in SAP SD?"
Proceed?
```

Wait for confirmation before writing anything to disk.
