# Database and Structured Data Source Integration

## Concept

Engram Mesh may connect to structured data sources such as relational databases, historians, data warehouses, APIs, and other data platforms.

The primary purpose is **not to copy or replace the source system**. Instead, Engram Mesh can discover its structure and maintain a **semantic model describing what the source contains, what its entities mean, how they relate, and how they can be accessed**.

```text
Database / Historian / Data Platform
              │
       read-only discovery
              │
              ▼
      Physical Structure
              │
              ▼
       Semantic Mapping
              │
              ▼
       Engram Mesh Graph
          ┌───┴───┐
          ▼       ▼
         MCP     Phase
          │
          ▼
          AI
```

## Example

A database may physically contain:

```text
customers
orders
order_items
products
```

Engram Mesh could represent this semantically as:

```text
Customer
   │ PLACES
   ▼
Order
   │ CONTAINS
   ▼
Product
```

The semantic model should retain traceability to the source:

```yaml
entity: Customer
type: SemanticEntity

source:
  system: CRM
  object: customers

relationships:
  - type: PLACES
    target: Order
    derived_from: orders.customer_id -> customers.id
```

This allows Engram Mesh to distinguish between:

* **discovered facts** — such as tables, foreign keys, tags or metadata;
* **semantic mappings** — what those structures represent;
* **inferred information** — interpretations proposed by AI or other tooling.

Where appropriate, inferred mappings should retain provenance and confidence information.

## Historian Example

The same approach can apply to an industrial historian.

Engram Mesh might discover structures such as:

```text
Historian
├── Sites
├── Assets
├── Tags
├── Measurements
└── Metadata
```

and represent them semantically:

```text
Site
 └── CONTAINS → Compressor
                   ├── HAS_MEASUREMENT → Discharge Pressure
                   ├── HAS_MEASUREMENT → Temperature
                   └── HAS_STATE       → Running
```

The underlying time-series data can remain in the historian.

Engram Mesh therefore does not need to store millions or billions of historical values to provide useful context about **what data exists and what it means**.

## MCP and AI Use

The semantic model can provide an MCP client or AI agent with context needed to interact correctly with another data system.

For example:

```text
                 Engram Mesh
                Semantic Model
                     │
                     ▼
AI ────────── understands ──────────┐
                                   │
      "Discharge Pressure is       │
       historian tag PT_102.PV"    │
                                   ▼
                            Database / Historian
                              query interface
```

An AI could use Engram Mesh to understand:

* which system contains the required information;
* which entities, tables, tags or measurements are relevant;
* relationships between those entities;
* terminology and business meaning;
* identifiers and source addresses;
* appropriate query structures;
* known constraints or access requirements.

The AI may then query the source using another MCP server, API, database tool or application integration.

**Engram Mesh therefore does not need to serve the underlying database data itself to provide significant value.**

Its immediate role can be:

> **Provide the semantic context required to understand and correctly use external data sources.**

## Progressive Access Model

Database integrations could support progressively greater capabilities:

| Level              | Capability                                                |
| ------------------ | --------------------------------------------------------- |
| Schema discovery   | Tables, columns, keys, tags, structures                   |
| Metadata discovery | Descriptions, types, relationships, statistics            |
| Semantic modelling | Business/domain entities and relationships                |
| Limited inspection | Approved samples or filtered records                      |
| Query assistance   | Semantic context used to construct queries                |
| Query proxy        | Engram Mesh provides controlled read access               |
| Indexed data       | Selected source information is incorporated into the mesh |

The initial specification should not require Engram Mesh to implement the later levels.

## Existing Technologies

Implementations should reuse existing technologies where appropriate rather than creating proprietary database-to-graph mechanisms unnecessarily.

Potential technologies and approaches include:

* **Ontop / Virtual Knowledge Graphs** — maps relational databases to semantic knowledge graphs without requiring the underlying data to be copied.
* **R2RML** — W3C standard for mapping relational databases to RDF datasets.
* **RDF / OWL** — established standards for representing semantic entities, relationships and ontologies.
* **Neo4j relational-to-graph tooling** — useful reference for transforming relational structures into property graphs.
* **Data catalog and lineage platforms** such as OpenMetadata — useful reference for automated metadata discovery, lineage and source modelling.
* Database-native schema metadata such as `INFORMATION_SCHEMA`, system catalogs and foreign-key definitions.

Engram Mesh should favour compatibility with established semantic and mapping standards where they satisfy the requirement.

## Architectural Principle

A source system should normally remain authoritative for its own data.

```text
SOURCE SYSTEM
Authoritative data
      │
      │ described/referenced by
      ▼
ENGRAM MESH
Semantic model + provenance + relationships
      │
      ├── MCP / AI context
      ├── discovery
      ├── navigation
      └── visualisation
```

This allows Engram Mesh to become a semantic layer across heterogeneous information systems without requiring those systems to migrate their data into Engram Mesh.

The same model can extend beyond databases to historians, APIs, repositories, document systems, file stores and other structured information sources.

> **Engram Mesh can understand and describe information without needing to own it.**
