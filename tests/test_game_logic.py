import pytest

from game_logic import (
    GameController,
    GameSession,
    NIGHTS,
    ROOMS,
    calculate_guest_score,
)

def create_controller() -> GameController:
    """Erzeugt einen neuen Spielcontroller."""

    session = GameSession()

    controller = GameController(
        session=session,
        nights=NIGHTS,
        rooms=ROOMS,
    )

    controller.start_game()

    return controller

def test_scorce_for_two_matches():
    """Zwei Treffer ergeben zehn Bewertungspunkte."""

    rating, chaos = calculate_guest_score(2)

    assert rating == 10
    assert chaos == 0

def test_score_for_one_match():
    """Ein Treffer ergibt fünf Punkte und fünf Chaos."""

    rating, chaos = calculate_guest_score(1)

    assert rating == 5
    assert chaos == 5

def test_score_for_zero_matches():
    """Kein Treffer ergibt zehn Chaospunkte."""

    rating, chaos = calculate_guest_score(0)

    assert rating == 0
    assert chaos == 10

def test_room_cannot_be_assigned_twice():
    """Ein Zimmer darf nur einen Gast aufnehmen."""

    controller = create_controller()

    controller.assign_room(
        guest_id=11,
        room_number=4,
    )

    with pytest.raises(
        ValueError,
        match="bereits belegt",
    
    ):
        controller.assign_room(
            guest_id=12,
            room_number=4,
        )

def test_night_requires_three_assignments():
    """Eine Nacht benötigt drei Zimmerzuordnungen."""

    controller = create_controller()

    controller.assign_room(
        guest_id=11,
        room_number=4,
    )

    with pytest.raises(
        ValueError,
        match="alle drei Gäste",
    ):
        controller.finish_night()


def test_concierge_can_only_be_used_once():
    """Der Concierge darf pro Nacht nur einmal helfen."""

    controller = create_controller()

    recommendation = controller.recommend_room(
        guest_id=11,
    )

    assert recommendation.number == 4

    with pytest.raises(
        ValueError,
        match="bereits eingesetzt",
    ):
        controller.recommend_room(
            guest_id=12,
        )


def test_complete_game():
    """Die Partie endet nach drei ausgewerteten Nächten."""

    controller = create_controller()

    assignments_by_night = {
        1: {
            11: 4,
            12: 3,
            13: 2,
        },
        2: {
            21: 4,
            22: 6,
            23: 2,
        },
        3: {
            31: 4,
            32: 2,
            33: 6,
        },
    }

    for night_number in (1, 2, 3):
        assignments = assignments_by_night[
            night_number
        ]

        for guest_id, room_number in (
            assignments.items()
        ):
            controller.assign_room(
                guest_id=guest_id,
                room_number=room_number,
            )

        controller.finish_night()

    assert controller.session.state == "FINISHED"
    assert controller.session.hotel_rating == 75
    assert controller.session.chaos_value == 15

    final_score, ending = (
        controller.final_result()
    )

    assert final_score == 60
    assert ending == "Erfolgreicher Endzustand"