"""Conference room and equipment scheduler."""
import json
from datetime import datetime

EQUIPMENT_STOCK = {"projector": 2, "microphone": 4, "webcam": 1}


class Scheduler:
    """Books rooms, allocates equipment and records double bookings."""

    def __init__(self):
        self.reservations = {}
        self.equipment_pool = dict(EQUIPMENT_STOCK)
        self.conflicts = []
        self.next_reservation = 1

    @staticmethod
    def slot_hours(time_slot):
        """Return the length in hours of a 'HH-HH' slot."""
        start, end = str(time_slot).split("-")
        hours = int(end) - int(start)
        if hours <= 0:
            raise ValueError(
                f"Invalid slot '{time_slot}': end must be after start")
        return hours

    def schedule_room(self, room_id, time_slot, equipment_list=None):
        """Book a room; return the reservation id, or None if rejected."""
        equipment_list = equipment_list or []
        try:
            self.slot_hours(time_slot)
        except ValueError as err:
            print("Rejected:", err)
            return None
        for item in equipment_list:
            if self.equipment_pool.get(item, 0) < 1:
                print(f"Rejected: '{item}' unavailable for {room_id}")
                return None
        for booked in self.reservations.values():
            if booked["room"] == room_id and booked["slot"] == time_slot:
                self.conflicts.append(
                    f"{room_id} double-booked at {time_slot}")
        for item in equipment_list:
            self.equipment_pool[item] -= 1
        res_id = self.next_reservation
        self.reservations[res_id] = {
            "room": room_id,
            "slot": time_slot,
            "equipment": equipment_list,
        }
        self.next_reservation += 1
        return res_id

    def cancel_reservation(self, reservation_id):
        """Cancel a reservation and return its equipment to the pool."""
        booking = self.reservations.pop(reservation_id, None)
        if booking is None:
            print("Reservation", reservation_id, "not found.")
            return
        for item in booking["equipment"]:
            self.equipment_pool[item] += 1

    def export_schedule(self, file="schedule.json"):
        """Write all reservations to a JSON file."""
        with open(file, "w", encoding="utf-8") as handle:
            json.dump(self.reservations, handle)

    def log_conflicts(self, file="conflicts.log"):
        """Append conflicts to a log file and print the log."""
        with open(file, "a", encoding="utf-8") as handle:
            for conflict in self.conflicts:
                handle.write(f"{datetime.now()} {conflict}\n")
        with open(file, "r", encoding="utf-8") as handle:
            print(handle.read(), end="")


def main():
    """Run the demo."""
    sched = Scheduler()
    sched.schedule_room("Board-1", "09-11")
    sched.schedule_room("Board-1", "09-11")
    sched.schedule_room("Huddle-3", "14-12")
    sched.schedule_room("Huddle-3", 1530)
    sched.cancel_reservation(77)
    slot = input("Slot for Board-2, like 10-12 (Enter for 10-12): ") or "10-12"
    sched.schedule_room("Board-2", slot, ["projector", "webcam"])
    sched.export_schedule()
    sched.log_conflicts()
    print("Equipment left:", sched.equipment_pool)
    print("Reservations:", sched.reservations)


if __name__ == "__main__":
    main()
