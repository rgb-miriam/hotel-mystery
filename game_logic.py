#Gasttypen, Gäste und Zimmer modellieren
#Jeder Gast besitzt einen Gasttyp und genau zwei Anforderungen
#Jedes Zimmer besitzt eine Nummer und mindestens ein Merkmal

from dataclasses import dataclass, field 
from enum import Enum


class GuestType(Enum):
    VAMPIR = "Vampir"
    GEIST = "Geist"
    WERWOLF = "Werwolf"
    HEXE = "Hexe"
    TROLL = "Troll"

REQUIREMENTS = {
    GuestType.VAMPIR: (
        "kein Fenster",
        "kein Spiegel",
    ),
    GuestType.GEIST: (
        "kein Spiegel",
        "Schallschutz",
    ),
    GuestType.WERWOLF: (
        "Schallschutz",
        "kein Fenster",
    ),
    GuestType.HEXE: (
        "Balkon",
        "Fenster",
    ),
    GuestType.TROLL: (
        "verstärkter Boden",
        "großes Bett",
    ),
}

@dataclass(frozen=True)
class Guest:
    id: int
    guest_type: GuestType
    requirements: tuple[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.guest_type, GuestType):
            raise ValueError(
                "Der Gasttyp muss einer der fünf Gasttypen entsprechen."
            )

        if len(self.requirements) != 2:
            raise ValueError(
                "Ein Gast benötigt genau zwei Anforderungen."
            )

        if len(set(self.requirements)) != 2:
            raise ValueError(
                "Die beiden Anforderungen müssen unterschiedlich sein."
            )


@dataclass(frozen=True)
class Room:
    number: int
    features: frozenset[str]

    def __post_init__(self) -> None:
        if not self.features:
            raise ValueError(
                "Ein Zimmer benötigt mindestens ein Merkmal."
            )

@dataclass(frozen=True)
class NightScenario:
    number: int
    guests: tuple[Guest, Guest, Guest]

    def __post_init__(self) -> None:
        if len(self.guests) != 3:
            raise ValueError(
                "Eine Nacht benötigt genau drei Gäste."
            )

        guest_ids = {
            guest.id
            for guest in self.guests
        }

        if len(guest_ids) != 3:
            raise ValueError(
                "Jeder Gast benötigt eine eigene Kennung."
            )


@dataclass
class GameSession:
    current_night: int = 1
    hotel_rating: int = 0
    chaos_value: int = 0
    state: str = "START"

    assignments: dict[int, int] = field(
        default_factory=dict
    )

    concierge_used: bool = False

    def start_game(self) -> None:
        self.current_night = 1
        self.hotel_rating = 0
        self.chaos_value = 0
        self.state = "PLANNING"
        self.assignments.clear()
        self.concierge_used = False

    

# current_night bedeutet: aktuelle Nacht = 1
#state bedeutet aktueller Spielabschnitt - "MENU"
# rating bedeutet Gesamte Hotelbewertung - 0
# chaos bedeutet gesamter Chaoswert - 0
# concierge_used bedeutet Concierge bereits eingesetzt - False
# assignments bedeutet Verbindung zwischen Gästen und Zimmern - {}





gast = Guest(
    id=1,
    guest_type=GuestType.VAMPIR,
    requirements=("kein Fenster", "kein Spiegel"),
)

ROOMS = (
    Room(
        number=1,
        features=frozenset({
            "Fenster",
            "Spiegel",
        }),
    ),
    Room(
        number=2,
        features=frozenset({
            "kein Fenster",
            "Spiegel",
            "verstärkter Boden",
            "großes Bett",
        }),
    ),
    Room(
        number=3,
        features=frozenset({
            "Fenster",
            "kein Spiegel",
            "Balkon",
        }),
    ),
    Room(
        number=4,
        features=frozenset({
            "kein Fenster",
            "kein Spiegel",
            "Schallschutz",
        }),
    ),
    Room(
        number=5,
        features=frozenset({
            "Fenster",
            "Spiegel",
            "großes Bett",
        }),
    ),
    Room(
        number=6,
        features=frozenset({
            "kein Fenster",
            "kein Spiegel",
            "verstärkter Boden",
        }),
    ),

)

NIGHT_1 = NightScenario(
    number=1,
    guests=(
        Guest(
            id=11,
            guest_type=GuestType.VAMPIR,
            requirements=REQUIREMENTS[
                GuestType.VAMPIR
            ],
        ),
        Guest(
            id=12,
            guest_type=GuestType.HEXE,
            requirements=REQUIREMENTS[
                GuestType.HEXE
            ],
        ),
        Guest(
            id=13,
            guest_type=GuestType.TROLL,
            requirements=REQUIREMENTS[
                GuestType.TROLL
            ],
        ),
    ),
)

NIGHT_2 = NightScenario(
    number=2,
    guests=(
        Guest(
            id=21,
            guest_type=GuestType.GEIST,
            requirements=REQUIREMENTS[
                GuestType.GEIST
            ],
        ),
        Guest(
            id=22,
            guest_type=GuestType.VAMPIR,
            requirements=REQUIREMENTS[
                GuestType.VAMPIR
            ],
        ),
        Guest(
            id=23,
            guest_type=GuestType.WERWOLF,
            requirements=REQUIREMENTS[
                GuestType.WERWOLF
            ],
        ),
    ),
)


NIGHT_3 = NightScenario(
    number=3,
    guests=(
        Guest(
            id=31,
            guest_type=GuestType.WERWOLF,
            requirements=REQUIREMENTS[
                GuestType.WERWOLF
            ],
        ),
        Guest(
            id=32,
            guest_type=GuestType.WERWOLF,
            requirements=REQUIREMENTS[
                GuestType.WERWOLF
            ],
        ),
        Guest(
            id=33,
            guest_type=GuestType.WERWOLF,
            requirements=REQUIREMENTS[
                GuestType.WERWOLF
            ],
        ),
    ),
)


NIGHTS = (
    NIGHT_1,
    NIGHT_2,
    NIGHT_3,
)

def count_matching_requirements(
    guest: Guest,
    room: Room,
) -> int:
    matches = 0

    for requirement in guest.requirements:
        if requirement in room.features:
            matches += 1

    return matches

def calculate_guest_score(
    matches: int,
) -> tuple[int, int]:
    if matches not in (0, 1, 2):
        raise ValueError(
            "Die Trefferzahl muss zwischen 0 und 2 liegen."
        )

    rating = matches * 5
    chaos = (2 - matches) * 5

    return rating, chaos

def find_room(
    room_number: int,
) -> Room:
    for room in ROOMS:
        if room.number == room_number:
            return room

    raise ValueError(
        f"Zimmer {room_number} existiert nicht."
    )

def validate_assignments(
    scenario: NightScenario,
    assignments: dict[int, int],
) -> None:
    expected_guest_ids = {
        guest.id
        for guest in scenario.guests
    }

    if set(assignments) != expected_guest_ids:
        raise ValueError(
            "Ordne alle drei Gäste einem Zimmer zu."
        )

    assigned_rooms = list(
        assignments.values()
    )

    if len(set(assigned_rooms)) != 3:
        raise ValueError(
            "Ein Zimmer darf nur einen Gast aufnehmen."
        )

    for room_number in assigned_rooms:
        find_room(room_number)

def evaluate_night(
    scenario: NightScenario,
    assignments: dict[int, int],
) -> tuple[int, int]:
    validate_assignments(
        scenario,
        assignments,
    )

    total_rating = 0
    total_chaos = 0

    for guest in scenario.guests:
        room_number = assignments[guest.id]
        room = find_room(room_number)

        matches = count_matching_requirements(
            guest,
            room,
        )

        rating, chaos = calculate_guest_score(
            matches
        )

        total_rating += rating
        total_chaos += chaos

        print(
            guest.guest_type.value,
            "in Zimmer",
            room.number,
            ":",
            matches,
            "von 2 Anforderungen erfüllt.",
        )

    return total_rating, total_chaos

def calculate_final_result(
    total_rating: int,
    total_chaos: int,
) -> tuple[int, str]:
    score = max(
        0,
        total_rating - total_chaos,
    )

    if score <= 29:
        ending = "Kritischer Endzustand"
    elif score <= 59:
        ending = "Stabiler Endzustand"
    else:
        ending = "Erfolgreicher Endzustand"

    return score, ending

class GameController:
    def __init__(
        self,
        session: GameSession,
        nights: tuple[NightScenario, ...],
        rooms: tuple[Room, ...],
    ) -> None:
        self.session = session
        self.nights = nights
        self.rooms = rooms

    @property
    def current_scenario(self) -> NightScenario:
        """Liefert das Szenario der aktuellen Nacht."""

        index = self.session.current_night - 1

        if index < 0 or index >= len(self.nights):
            raise ValueError(
                "Die aktuelle Nacht ist ungültig."
            )

        return self.nights[index]

    def start_game(self) -> None:
        """Startet eine neue Partie."""

        self.session.start_game()

    def assign_room(
        self,
        guest_id: int,
        room_number: int,
    ) -> None:
        """Ordnet einem Gast ein freies Zimmer zu."""

        if self.session.state != "PLANNING":
            raise ValueError(
                "Zimmer lassen sich nur während der Planung zuordnen."
            )

        valid_guest_ids = {
            guest.id
            for guest in self.current_scenario.guests
        }

        if guest_id not in valid_guest_ids:
            raise ValueError(
                "Der Gast gehört nicht zur aktuellen Nacht."
            )

        valid_room_numbers = {
            room.number
            for room in self.rooms
        }

        if room_number not in valid_room_numbers:
            raise ValueError(
                "Das ausgewählte Zimmer existiert nicht."
            )

        for other_guest_id, assigned_room in (
            self.session.assignments.items()
        ):
            if (
                assigned_room == room_number
                and other_guest_id != guest_id
            ):
                raise ValueError(
                    "Dieses Zimmer ist bereits belegt."
                )

        self.session.assignments[
            guest_id
        ] = room_number

    def remove_assignment(
        self,
        guest_id: int,
    ) -> None:
        """Entfernt die Zimmerzuordnung eines Gastes."""

        if self.session.state != "PLANNING":
            raise ValueError(
                "Zuordnungen lassen sich nur während der Planung entfernen."
            )

        valid_guest_ids = {
            guest.id
            for guest in self.current_scenario.guests
        }

        if guest_id not in valid_guest_ids:
            raise ValueError(
                "Der Gast gehört nicht zur aktuellen Nacht."
            )

        self.session.assignments.pop(
            guest_id,
            None,
        )

    def recommend_room(
        self,
        guest_id: int,
    ) -> Room:
        """Empfiehlt das beste freie Zimmer für einen Gast."""

        if self.session.state != "PLANNING":
            raise ValueError(
                "Der Concierge ist nur während der Planung verfügbar."
            )

        if self.session.concierge_used:
            raise ValueError(
                "Der Concierge wurde in dieser Nacht bereits eingesetzt."
            )

        selected_guest = None

        for guest in self.current_scenario.guests:
            if guest.id == guest_id:
                selected_guest = guest
                break

        if selected_guest is None:
            raise ValueError(
                "Der Gast gehört nicht zur aktuellen Nacht."
            )

        occupied_room_numbers = set(
            self.session.assignments.values()
        )

        free_rooms = [
            room
            for room in self.rooms
            if room.number not in occupied_room_numbers
        ]

        if not free_rooms:
            raise ValueError(
                "Es ist kein freies Zimmer verfügbar."
            )

        best_room = free_rooms[0]

        best_match_count = (
            count_matching_requirements(
                selected_guest,
                best_room,
            )
        )

        for room in free_rooms[1:]:
            match_count = (
                count_matching_requirements(
                    selected_guest,
                    room,
                )
            )

            if match_count > best_match_count:
                best_room = room
                best_match_count = match_count

        self.session.concierge_used = True

        return best_room

    def finish_night(
        self,
    ) -> tuple[int, int]:
        """Wertet die aktuelle Nacht aus."""

        if self.session.state != "PLANNING":
            raise ValueError(
                "Die Nacht kann derzeit nicht ausgewertet werden."
            )

        night_rating, night_chaos = evaluate_night(
            self.current_scenario,
            self.session.assignments,
        )

        self.session.hotel_rating += night_rating
        self.session.chaos_value += night_chaos

        if self.session.current_night == len(
            self.nights
        ):
            self.session.state = "FINISHED"
        else:
            self.session.current_night += 1
            self.session.assignments.clear()
            self.session.concierge_used = False

        return night_rating, night_chaos

    def final_result(
        self,
    ) -> tuple[int, str]:
        """Berechnet das Endergebnis der Partie."""

        if self.session.state != "FINISHED":
            raise ValueError(
                "Das Spiel ist noch nicht beendet."
            )

        return calculate_final_result(
            self.session.hotel_rating,
            self.session.chaos_value,
        )

