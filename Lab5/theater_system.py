"""Movie theater seat reservation system."""
import json
import hashlib


# Global state
shows = {"SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
         "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []}}


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a seat and record the result."""
    if system_logs is None:
        system_logs = []

    show = shows[show_id]
    if seat_number in show["booked"]:
        system_logs.append(
            f"Seat {seat_number} already taken for {show_id}"
        )
        return False

    show["booked"].append(seat_number)
    system_logs.append(
        f"Reserved seat {seat_number} for {show_id}"
    )
    return True


def release_seat(show_id, seat_number):
    """Release a booked seat."""
    try:
        shows[show_id]["booked"].remove(seat_number)
    except ValueError:
        return False
    return True


def ticket_code(show_id, seat_number):
    """Generate a ticket code from the show ID and seat number."""
    ticket_data = (show_id + str(seat_number)).encode("utf-8")
    return hashlib.sha256(ticket_data).hexdigest()[:8]


def dump_reservations(file="seats.json"):
    """Save seat reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(shows, f)


def load_reservations(file="seats.json"):
    """Load seat reservations from a JSON file."""
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    shows.clear()
    shows.update(data)


def print_seating_summary():
    """Print the number of free seats and booked seats for each show."""
    for show in shows.values():
        free = show["seats"] - len(show["booked"])
        print(
            f'{show["title"]}: {free} seats free, '
            f'booked = {show["booked"]}'
        )


def main():
    """Run the movie theater seat reservation workflow."""
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 25)
    reserve_seat("SHOW-2", -1)
    reserve_seat("SHOW-2", "A7")
    release_seat("SHOW-2", 3)
    print("Ticket code:", ticket_code("SHOW-1", 5))
    seat = input("Seat number to book for SHOW-2 (Enter for 4): ") or "4"
    reserve_seat("SHOW-2", seat)
    dump_reservations()
    load_reservations()
    print_seating_summary()


if __name__ == "__main__":
    main()
