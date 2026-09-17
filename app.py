from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from game_logic import (
    GameController,
    GameSession,
    NIGHTS,
    ROOMS,
)


app = Flask(__name__)
app.secret_key = "hotel-mystery-development-key"


game_session = GameSession()

game_controller = GameController(
    session=game_session,
    nights=NIGHTS,
    rooms=ROOMS,
)


@app.route("/")
def start():
    """Zeigt die Startseite."""

    return render_template(
        "start.html",
    )


@app.route(
    "/start-game",
    methods=["POST"],
)
def start_game():
    """Startet eine neue Partie."""

    game_controller.start_game()

    return redirect(
        url_for("game")
    )


@app.route("/game")
def game():
    """Zeigt die aktuelle Nacht."""

    if game_session.state == "START":
        return redirect(
            url_for("start")
        )

    if game_session.state == "FINISHED":
        return redirect(
            url_for("result")
        )

    return render_template(
        "game.html",
        scenario=game_controller.current_scenario,
        rooms=ROOMS,
        assignments=game_session.assignments,
        hotel_rating=game_session.hotel_rating,
        chaos_value=game_session.chaos_value,
        concierge_used=game_session.concierge_used,
    )


@app.route(
    "/assign-room",
    methods=["POST"],
)
def assign_room():
    """Speichert eine Zimmerzuordnung."""

    guest_id = int(
        request.form["guest_id"]
    )

    room_number = int(
        request.form["room_number"]
    )

    try:
        game_controller.assign_room(
            guest_id=guest_id,
            room_number=room_number,
        )

        flash(
            f"Gast {guest_id} wurde Zimmer "
            f"{room_number} zugeordnet."
        )

    except ValueError as error:
        flash(str(error))

    return redirect(
        url_for("game")
    )


@app.route(
    "/remove-assignment",
    methods=["POST"],
)
def remove_assignment():
    """Entfernt eine Zimmerzuordnung."""

    guest_id = int(
        request.form["guest_id"]
    )

    try:
        game_controller.remove_assignment(
            guest_id=guest_id,
        )

        flash(
            f"Die Zuordnung von Gast "
            f"{guest_id} wurde entfernt."
        )

    except ValueError as error:
        flash(str(error))

    return redirect(
        url_for("game")
    )


@app.route(
    "/recommend-room",
    methods=["POST"],
)
def recommend_room():
    """Ruft den Concierge auf."""

    guest_id = int(
        request.form["guest_id"]
    )

    try:
        recommendation = (
            game_controller.recommend_room(
                guest_id=guest_id,
            )
        )

        flash(
            f"Der Concierge empfiehlt Gast "
            f"{guest_id} das Zimmer "
            f"{recommendation.number}."
        )

    except ValueError as error:
        flash(str(error))

    return redirect(
        url_for("game")
    )


@app.route(
    "/finish-night",
    methods=["POST"],
)
@app.route(
    "/finish-night",
    methods=["POST"],
)
def finish_night():
    """Wertet die aktuelle Nacht aus."""

    completed_night = (
        game_session.current_night
    )

    try:
        night_rating, night_chaos = (
            game_controller.finish_night()
        )

    except ValueError as error:
        flash(str(error))

        return redirect(
            url_for("game")
        )

    if completed_night == len(NIGHTS):
        game_session.state = "FINISHED"

        final_score, ending = (
            game_controller.final_result()
        )

        return render_template(
            "result.html",
            hotel_rating=game_session.hotel_rating,
            chaos_value=game_session.chaos_value,
            final_score=final_score,
            ending=ending,
        )

    flash(
        f"Nacht {completed_night} abgeschlossen. "
        f"Hotelbewertung +{night_rating}, "
        f"Chaos +{night_chaos}."
    )

    return redirect(
        url_for("game")
    )


@app.route("/result")
def result():
    """Zeigt das Endergebnis."""

    if game_session.state == "START":
        return redirect(
            url_for("start")
        )

    if game_session.state != "FINISHED":
        return redirect(
            url_for("game")
        )

    final_score, ending = (
        game_controller.final_result()
    )

    return render_template(
        "result.html",
        hotel_rating=game_session.hotel_rating,
        chaos_value=game_session.chaos_value,
        final_score=final_score,
        ending=ending,
    )

@app.route("/help")
def help_page():
    """Zeigt die Spielregeln."""

    return render_template(
        "help.html",
    )

if __name__ == "__main__":
    app.run(debug=True)

    