from flask import Blueprint, request, jsonify

user_bp = Blueprint('users', __name__)

# Default users used as initial in-memory state
_DEFAULT_USERS = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]

# In-memory storage (acts like a simple database)
users = []


def reset_users():
    """
    Reset users to default state.

    This is critical for test stability:
    - Unit tests expect a known initial state
    - Integration tests may mutate the data
    """
    global users
    users = [user.copy() for user in _DEFAULT_USERS]


# Initialize users on module load
reset_users()


@user_bp.route("/", methods=["GET"])
def get_users():
    """
    Return the list of all users.

    Status code 200 is implicit and should NOT be returned explicitly,
    otherwise unit tests that call the function directly will fail.
    """
    return jsonify(users)


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """
    Return a single user by ID.
    """
    user = next((u for u in users if u["id"] == user_id), None)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


@user_bp.route("/", methods=["POST"])
def create_user():
    """
    Create a new user and store it in memory.
    """
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    new_id = max((u["id"] for u in users), default=0) + 1
    new_user = {
        "id": new_id,
        "name": name,
        "email": email,
    }

    users.append(new_user)
    return jsonify(new_user), 201
