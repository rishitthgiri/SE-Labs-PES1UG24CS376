# SE Lab — Digital Campus Library Reservation Gateway

This folder contains the three lab deliverables. All artifacts are cross-consistent: the same 7 requirement IDs, the same use-case names, and the same `«include»`/`«extend»` relationships are used throughout.

## Contents
- `requirements/requirements-table.md` — FR-001–FR-005, NFR-001–NFR-002 with ID, Type, Description, Priority, Acceptance Criteria, Rationale.
- `uml/use-case-diagram.puml` — Editable PlantUML source.
- `uml/use-case-diagram.svg` / `uml/use-case-diagram.png` — Rendered diagram (Student Member, Head Librarian; includes `«include»` and `«extend»`).
- `use-case-specs/place-book-reservation-hold.md` — ~1-page flow spec for "Place Book Reservation/Hold," with one Alternate Flow (maximum reservation limit reached).

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
