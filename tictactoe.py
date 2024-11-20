from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Game state
game_state = {
    "board": [["" for _ in range(3)] for _ in range(3)],  # 3x3 grid
    "current_player": 1,  # Player 1 starts
    "winner": None  # Winner is None until someone wins
}

def check_winner(board):
    """Check if a player has won the game."""
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0]
    return None

def computer_move():
    """Simple AI for the computer to make a move."""
    for r in range(3):
        for c in range(3):
            if game_state["board"][r][c] == "":
                return r, c
    return None

@app.route("/")
def index():
    return render_template("index.html", game_state=game_state)

@app.route("/make_move", methods=["POST"])
def make_move():
    data = request.get_json()
    row, col = data["position"]
    player_symbol = "X" if game_state["current_player"] == 1 else "O"

    if game_state["board"][row][col] != "" or game_state["winner"] is not None:
        return jsonify({"error": "Invalid move!"}), 400

    game_state["board"][row][col] = player_symbol
    game_state["winner"] = check_winner(game_state["board"])

    if game_state["winner"] is None:
        game_state["current_player"] = 2
        comp_row, comp_col = computer_move()
        if comp_row is not None:
            game_state["board"][comp_row][comp_col] = "O"
            game_state["winner"] = check_winner(game_state["board"])
        if game_state["winner"] is None:
            game_state["current_player"] = 1

    return jsonify({"success": True, "game_state": game_state})

@app.route("/new_round", methods=["POST"])
def new_round():
    """Reset the game state for a new round."""
    game_state["board"] = [["" for _ in range(3)] for _ in range(3)]
    game_state["current_player"] = 1
    game_state["winner"] = None
    return jsonify({"success": True, "game_state": game_state})

if __name__ == "__main__":
    app.run(debug=True)
