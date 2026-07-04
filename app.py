from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Welcome route
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Event Management API"
    })


# GET all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])


# POST new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({
            "error": "Title is required."
        }), 400

    new_id = max([event.id for event in events], default=0) + 1

    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required."}), 400

    for event in events:
        if event.id == id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found."}), 404

# DELETE event
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    for event in events:
        if event.id == id:
            events.remove(event)
            return "", 204

    return jsonify({"error": "Event not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)