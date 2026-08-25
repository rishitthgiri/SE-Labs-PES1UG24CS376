# SE Lab — Digital Campus Library Reservation Gateway

This folder contains the three lab deliverables, in the formats required by the handout (Lab 1: Requirements Engineering & UML Use-Case Modelling). All artifacts are cross-consistent: the same 7 requirement IDs, the same use-case names, and the same `«include»`/`«extend»` relationships are used throughout.

## Deliverables (handout-required formats)
- **Requirements Table (Word/Excel):** `requirements/requirements-table.docx` and `requirements/requirements-table.xlsx` — FR-001–FR-005, NFR-001–NFR-002, each with Req ID, Type, Description, Priority, Acceptance Criteria, Rationale.
- **UML Use-Case Diagram (PDF):** `uml/use-case-diagram.pdf` — 3 actors (Student Member, Head Librarian, Campus SSO/Auth Server), ≥5 use cases, at least one `«include»` and one `«extend»`.
- **Use-Case Flow Document (Word, 1 page):** `use-case-specs/place-book-reservation-hold.docx` — Main Success Scenario + one step-anchored Alternate Flow (4a. Maximum Reservation Limit Reached), for the core use case "Place Book Reservation/Hold."

## Supplementary source files (not required, kept for convenience/editing)
- `requirements/requirements-table.md`, `requirements/requirements-table.pdf`
- `uml/use-case-diagram.puml` (editable PlantUML source), `.svg`, `.png`
- `use-case-specs/place-book-reservation-hold.md`, `.pdf`

## Traceability Summary
| Diagram Element | Requirement(s) |
|---|---|
| Search Catalog | FR-001 |
| Place Book Reservation/Hold | FR-002, FR-003 |
| View Queue Position | FR-003 |
| Send Availability Notification (`«include»`d by Reservation) | FR-004 |
| Checkout Book / Return Book | FR-005 |
| Calculate Overdue Fine (`«extend»`s Return Book) | FR-005 |
| Authenticate via Campus SSO (`«include»`d by Reservation & Checkout) | NFR-002 |
| (implicit) Response time / load handling | NFR-001 |

## Regenerating the diagram
```
java -jar plantuml.jar -tsvg docs/uml/use-case-diagram.puml
java -jar plantuml.jar -tpng docs/uml/use-case-diagram.puml
```
