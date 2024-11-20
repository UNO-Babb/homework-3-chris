document.addEventListener("DOMContentLoaded", () => {
    const boardElement = document.getElementById("board");
    const currentPlayerElement = document.getElementById("current-player");
    const winnerMessageElement = document.getElementById("winner-message");
    const newRoundButton = document.getElementById("new-round");

    function renderBoard(board) {
        boardElement.innerHTML = "";
        board.forEach((row, rIndex) => {
            row.forEach((cell, cIndex) => {
                const tile = document.createElement("div");
                tile.classList.add("tile");
                if (cell) {
                    tile.textContent = cell;
                    tile.classList.add("taken", cell);
                }
                tile.dataset.position = `${rIndex},${cIndex}`;
                boardElement.appendChild(tile);
            });
        });
    }

    async function makeMove(position) {
        const response = await fetch("/make_move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ position }),
        });

        if (response.ok) {
            const data = await response.json();
            renderBoard(data.game_state.board);
            currentPlayerElement.textContent = data.game_state.current_player;
            if (data.game_state.winner) {
                winnerMessageElement.textContent = `Player ${data.game_state.winner === "X" ? 1 : 2} wins!`;
                newRoundButton.style.display = "block";
            }
        } else {
            const error = await response.json();
            alert(error.error);
        }
    }

    async function newRound() {
        const response = await fetch("/new_round", { method: "POST" });
        if (response.ok) {
            const data = await response.json();
            renderBoard(data.game_state.board);
            currentPlayerElement.textContent = data.game_state.current_player;
            winnerMessageElement.textContent = "";
            newRoundButton.style.display = "none";
        }
    }

    boardElement.addEventListener("click", (e) => {
        if (e.target.classList.contains("tile") && !e.target.classList.contains("taken")) {
            const [row, col] = e.target.dataset.position.split(",").map(Number);
            makeMove([row, col]);
        }
    });

    newRoundButton.addEventListener("click", newRound);

    renderBoard([["", "", ""], ["", "", ""], ["", "", ""]]);
});
