---
type: creative work
aliases:
  - Topic scheme
part_of: "[[Personal ontology vault]]"
topics:
  - "[[Personal ontology vault]]"
captured_from: template, claude-personal-vault
created: 2026-10-18
updated: 2026-10-18
---

# Vault topics

The controlled list of topics the vault's index is built on. Every hub article belongs to it, and the owner approves each one.

## Details

- A hub is any article whose frontmatter has `in_scheme: "[[Vault topics]]"`. Every other article, except reviews, names 1 to 3 hubs in `topics:`, primary first. The pattern follows SKOS, where concepts join a concept scheme with `inScheme`.[^skos]
- A topic earns a hub when it has literary warrant (at least 3 articles, counting the hub) and structural warrant (its members would not fit better under another hub, and it will still matter in six months). Ideally it also has user warrant: evidence that the owner or their agents look for it.[^isko][^t]
- A hub splits when a narrower topic inside it earns warrant, never because of its size. Splitting is the owner's call.[^t]
- Agents never add or remove a hub on their own. When no hub fits a new article, capture files it under the closest hub and asks the owner whether to add one.[^t]
- Nesting with `broader:` starts with the first sub-hub the owner approves. A sub-hub is a hub that also carries `broader: "[[Parent hub]]"`.[^t]
- The vault starts with one hub, [[Personal ontology vault]]. Setup replaces it with the owner's own list.[^t]

## Sources

[^skos]: W3C, "SKOS Simple Knowledge Organization System Reference," section 4, Concept Schemes. https://www.w3.org/TR/skos-reference/
[^isko]: ISKO Encyclopedia of Knowledge Organization, "Literary warrant." https://www.isko.org/cyclo/literary_warrant
[^t]: Template default, `claude-personal-vault`, 2026-10-18.
