# Loss-aware graph mapping contracts

Core 0.2 graphs are **portable directed topology with optional labels and record
references**. They are not an ontology, RDF dataset, query language, layout
format, or general property-graph model.

## JSON-LD and RDF

Use a versioned adapter vocabulary rather than treating arbitrary edge relation
strings as RDF predicates. Map each graph to a graph/dataset identifier, local
node IDs to identifiers scoped by the Engram graph ID, record references to
Engram object identifiers, and directed edges to explicit edge resources carrying
edge ID, source, destination, relation label, and optional display label.

Representing an edge only as an RDF triple is lossy because Core edge identity
and labels cannot be recovered reliably. Blank nodes are also unsuitable when a
round trip must retain local node and edge IDs. RDF language tags, datatypes,
named-graph semantics, inference, reification variants, lists, and ontology
meaning have no Core equivalent and require a loss report on import.

## Property graphs

Map Core node and edge IDs to dedicated immutable properties and preserve graph
membership explicitly. Record references remain ID-valued properties, not
database-internal node keys. Relation and label map to named properties without
promoting arbitrary implementation properties into Core extensions.

Multi-valued properties, typed values, hyperedges, undirected edges, ports,
groups, nested graphs, parallel-edge restrictions, schema constraints, indexes,
and layout are implementation semantics. Export either preserves them in a
documented extension/profile or declares them lost.

## Round-trip evidence

A mapping report compares node IDs, edge IDs, direction, endpoints, relation,
labels, record IDs and scope, extension data, and graph membership after
`Engram -> target -> Engram`. It separately lists target semantics that cannot be
represented. Semantic equality is never inferred solely from equal node/edge
counts. Executable fixtures and review from experienced users of the target
format are required before the feedback item is complete.
