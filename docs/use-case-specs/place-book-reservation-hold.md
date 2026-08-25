# Use-Case Specification: Place Book Reservation/Hold

## Use Case Name
Place Book Reservation/Hold

## Related Requirements
FR-002 (Place Reservation), FR-003 (FIFO Waiting Queue), FR-004 (Availability Notification), NFR-002 (Authentication)

## Actors
- **Primary Actor:** Student Member
- **Supporting Actors:** System (Notification Service), Head Librarian (indirect, via catalog/queue oversight)

## Preconditions
1. The Student Member is authenticated via Campus SSO (see `«include» Authenticate via Campus SSO`, NFR-002).
2. The Student Member's account has no outstanding fines exceeding ₹500 (FR-005).
3. The book (identified by ISBN) exists in the catalog and its current status is "On Loan" or "Fully Reserved" (i.e., not immediately available for checkout).
4. The Student Member has fewer than 5 currently active reservations.

## Postconditions
**Success:**
1. A new reservation record is created with a unique reservation ID, linked to the member and the ISBN.
2. The reservation is appended to the FIFO queue for that ISBN at the next available position.
3. The book's availability status reflects the updated queue (e.g., "Reserved — Queue Position 3").
4. When the reservation reaches the front of the queue and a copy becomes available, the `Send Availability Notification` use case is triggered (`«include»`), and a 48-hour pickup hold begins.

**Failure:**
1. No reservation record is created.
2. The system state (queue, member's reservation count) remains unchanged.
3. The member is shown a specific, actionable error message.

## Main Success Scenario
1. The Student Member searches for a book by ISBN, title, or author (`Search Catalog` use case) and selects a title showing status "On Loan" or "Reserved."
2. The Student Member selects "Place Reservation/Hold" on the book's detail page.
3. The system verifies the member is authenticated (`«include» Authenticate via Campus SSO`); if not, the member is redirected to Campus SSO login and returns to this flow upon success.
4. The system checks the member's account for outstanding fines (< ₹500) and active reservation count (< 5).
5. The system checks that the member does not already hold an active reservation for the same ISBN.
6. The system creates a new reservation record with a unique reservation ID, timestamp, and calculated queue position (current queue length + 1).
7. The system updates the book's availability display to reflect the member's queue position.
8. The system displays a confirmation screen to the member showing: reservation ID, book title, queue position, and estimated wait (if available).
9. The system logs the transaction for audit purposes (NFR-002).
10. (Later, asynchronously) When the reservation reaches queue position 1 and a copy is returned/added, the system triggers `Send Availability Notification` (`«include»`) and starts a 48-hour pickup window.

## Alternate Flow: A1 — Maximum Reservation Limit Reached
**Trigger:** At Step 4 of the Main Success Scenario, the system detects the member already has 5 active reservations.

1. The system halts the reservation process and does **not** create a new reservation record.
2. The system displays an error message: "You have reached the maximum limit of 5 active reservations. Please cancel an existing reservation or wait for a hold to be fulfilled before placing a new one."
3. The system presents the member's current list of active reservations with an option to cancel one (`Cancel Reservation` use case).
4. If the member cancels an existing reservation, the system re-evaluates and allows the member to retry Step 2 of the Main Success Scenario for the original book.
5. The use case ends (failure postcondition) if the member does not cancel a reservation.

*(Alternate note: the same structure applies to related exception flows — A2 "Duplicate Reservation," where Step 5 detects an existing active hold on the same ISBN and the system blocks the request with a "You already have an active reservation for this title" message; and A3 "ISBN Not Found / Book Available for Immediate Checkout," which redirects the member to the `Checkout Book` use case instead of reservation. Only A1 is detailed above per the assignment's one-alternate-flow requirement.)*

## Business Rules Referenced
- Maximum 5 active reservations per member (FR-002).
- FIFO queue ordering, no priority bypass except by Head Librarian override (FR-003, `Override Reservation Queue` extend use case).
- 48-hour pickup window after notification before the hold expires and passes to the next member (FR-004).
- Members with fines > ₹500 are blocked from new reservations (FR-005).

## Assumptions
- "Active reservation" means a reservation in status Queued or Ready-for-Pickup (not yet expired, cancelled, or fulfilled).
- Queue position is computed at creation time and only changes due to cancellations ahead of the member in the queue.
