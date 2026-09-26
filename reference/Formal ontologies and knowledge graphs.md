---
type: concept
aliases:
  - Ontology
  - Knowledge graph
related:
  - "[[Personal knowledge management practice]]"
  - "[[Agent-readable markdown conventions]]"
captured_from: research, Claude Code, 2026-09-26
created: 2026-09-26
updated: 2026-09-26
---

# Formal ontologies and knowledge graphs

The standard vocabularies for types and relationships (schema.org, Wikidata, DBpedia, SKOS, PROV-O), researched for what this vault can borrow.

## Summary

An ontology is an agreed set of *types* of things and the *relationships* allowed between them. A knowledge graph is data stored in that shape: things connected by named relationships. The basic unit is a triple, *subject, relationship, object*, for example "Rex, owned by, Alex."

Formal ontologies are built for machines to reason over at web scale. This vault needs far less. What it can borrow is their vocabulary: well-tested names for types and relationships, so we are not inventing our own from scratch.

## schema.org

schema.org is the shared vocabulary search engines use. It is built from types and properties, arranged in "a multiple inheritance hierarchy where each type may be a sub-class of multiple types."[^schema-model] It is deliberately forgiving: "some data is better than none," and it is "not intended as a universal ontology."[^schema-model]

Everything descends from `Thing`. The direct subtypes most relevant to a personal vault are `Person`, `Organization`, `Place`, `Event`, `CreativeWork`, `Product`, `Action`, and `Intangible` (the home of ideas and concepts). Several properties defined on `Thing` map neatly to note features:[^schema-thing]

| schema.org property | Meaning | Obsidian equivalent |
| --- | --- | --- |
| `name` | The name of the item | Note title |
| `alternateName` | "An alias for the item" | `aliases` property |
| `description` | A description of the item | Opening summary |
| `sameAs` | A URL that "unambiguously indicates the item's identity" | An external link |
| `subjectOf` | A work or event about this thing | Backlinks from articles |

Relationship properties worth borrowing include `knows` (person to person), `isPartOf` / `hasPart`, `about`, `mentions`, `citation`, `memberOf`, and `location`.[^schema-props]

## Wikidata

Wikidata stores knowledge as statements: an item, a property, and a value, optionally with qualifiers, references, and ranks.[^wikidata] Its most important principle for this vault is about citations. Wikidata calls itself "not a database that stores *facts* about the world, but a secondary knowledge base that collects and links to references to such knowledge."[^wikidata] Each statement carries its own sources, so conflicting sources can sit side by side, with ranks marking which one is preferred or deprecated.[^wikidata]

This speaks directly to the question of conflicting information. Wikidata's answer is to keep both claims, each with its sources, and mark which is preferred.

Three Wikidata properties do most of the structural work across the whole graph: *instance of* (P31), *subclass of* (P279), and *part of* (P361).[^wd-props]

## DBpedia

DBpedia extracts structured data from Wikipedia. Its ontology is "a large cross-domain ontology" with 768 classes and 3,000 properties, built by "a successful crowd-sourcing effort."[^dbpedia] It shows that a broad ontology can grow over time from contributions rather than being designed up front.

## SKOS: lightweight concept schemes

SKOS (Simple Knowledge Organization System) is a W3C standard for thesauri and taxonomies. It is explicitly a "lightweight, intuitive conceptual modeling language" and avoids the formal rigor of ontology languages like OWL.[^skos] It has three core relationships between concepts:[^skos]

- `broader` / `narrower`: more general and more specific. These are not automatically transitive.
- `related`: an associative link that is neither broader nor narrower, like "birds" and "ornithology."

SKOS also separates a concept's preferred label (`prefLabel`) from alternative labels (`altLabel`). That is the same split as a note title versus Obsidian's `aliases`.[^skos]

## PROV-O: tracking where knowledge came from

PROV-O is the W3C ontology for provenance: where a piece of information came from and how it was produced.[^prov] Its core terms are `Entity`, `Activity`, and `Agent`, linked by relationships such as `wasDerivedFrom`, `wasGeneratedBy`, `wasAttributedTo`, and `hadPrimarySource`.[^prov] For this vault, provenance means recording which source, and which session or agent, produced a fact.

## What this means for the vault

These are options for the design decisions, not conclusions:

- **Entity types can come straight from schema.org's top level.** Person, Place, Organization, Event, CreativeWork, Product, and a concept type cover most of what a personal vault holds (pets, hobbies, ideas, research). A pet is a case where schema.org is thin, which is a good test for the entity-type decision.
- **A small relationship set covers a lot.** `is a` (instance of), `part of`, `related`, `knows`, `about`, and `cites` would express most links. SKOS shows that a few well-defined relationships beat many loose ones.
- **Citations belong on individual claims, not only at the end of an article.** That is the Wikidata model, and it makes conflicting sources manageable.
- **Provenance fields are cheap to add now and hard to add later.** A `source` and a `captured by` field on each article would record where facts came from.

## Sources

[^schema-model]: schema.org, "Data model." https://schema.org/docs/datamodel.html (accessed 2026-09-26).
[^schema-thing]: schema.org, "Thing." https://schema.org/Thing (accessed 2026-09-26).
[^schema-props]: schema.org property pages: https://schema.org/knows, https://schema.org/isPartOf, https://schema.org/about, https://schema.org/mentions, https://schema.org/citation, https://schema.org/memberOf (accessed 2026-09-26).
[^wikidata]: Wikidata, "Help:Statements." https://www.wikidata.org/wiki/Help:Statements (accessed 2026-09-26).
[^wd-props]: Wikidata property pages: https://www.wikidata.org/wiki/Property:P31, https://www.wikidata.org/wiki/Property:P279, https://www.wikidata.org/wiki/Property:P361 (accessed 2026-09-26).
[^dbpedia]: DBpedia Association, "DBpedia Ontology." https://www.dbpedia.org/resources/dbpedia-ontology/ (accessed 2026-09-26).
[^skos]: Antoine Isaac and Ed Summers (eds.), "SKOS Simple Knowledge Organization System Primer," W3C Working Group Note, August 18, 2009. https://www.w3.org/TR/skos-primer/ (accessed 2026-09-26).
[^prov]: Timothy Lebo, Satya Sahoo, and Deborah McGuinness (eds.), "PROV-O: The PROV Ontology," W3C Recommendation, April 30, 2013. https://www.w3.org/TR/prov-o/ (accessed 2026-09-26).
