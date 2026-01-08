"""
AI Game Referee – Rock–Paper–Scissors–Plus

This implementation follows Google ADK principles:
- Single agent orchestration
- Explicit tools for validation, logic, and state mutation
- Structured state outside prompts
- Deterministic, explainable behavior

The code runs with or without Google ADK installed.
"""

# -----------------------------
# SAFE GOOGLE ADK IMPORT
# -----------------------------
try:
    from google.adk import Agent, tool
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False

import random

# -----------------------------
# GAME CONSTANTS
# -----------------------------
VALID_MOVES = ["rock", "paper", "scissors", "bomb"]
MAX_ROUNDS = 3

# -----------------------------
# GAME STATE (STRUCTURED, PERSISTENT)
# -----------------------------
game_state = {
    "round": 1,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_over": False
}

# =====================================================
# TOOLS (VALIDATION / LOGIC / STATE MUTATION)
# =====================================================

# -----------------------------
# TOOL 1: VALIDATE MOVE
# -----------------------------
if ADK_AVAILABLE:
    @tool
    def validate_move(user_move: str, state: dict) -> dict:
        user_move = user_move.lower().strip()

        if user_move not in VALID_MOVES:
            return {"valid": False, "reason": "Invalid move"}

        if user_move == "bomb" and state["user_bomb_used"]:
            return {"valid": False, "reason": "Bomb already used"}

        return {"valid": True, "move": user_move}
else:
    def validate_move(user_move: str, state: dict) -> dict:
        user_move = user_move.lower().strip()

        if user_move not in VALID_MOVES:
            return {"valid": False, "reason": "Invalid move"}

        if user_move == "bomb" and state["user_bomb_used"]:
            return {"valid": False, "reason": "Bomb already used"}

        return {"valid": True, "move": user_move}


# -----------------------------
# TOOL 2: RESOLVE ROUND
# -----------------------------
if ADK_AVAILABLE:
    @tool
    def resolve_round(user_move: str, bot_move: str) -> dict:
        if user_move == "bomb" and bot_move == "bomb":
            return {"winner": "draw"}
        if user_move == "bomb":
            return {"winner": "user"}
        if bot_move == "bomb":
            return {"winner": "bot"}

        if user_move == bot_move:
            return {"winner": "draw"}

        if (
            (user_move == "rock" and bot_move == "scissors") or
            (user_move == "scissors" and bot_move == "paper") or
            (user_move == "paper" and bot_move == "rock")
        ):
            return {"winner": "user"}

        return {"winner": "bot"}
else:
    def resolve_round(user_move: str, bot_move: str) -> dict:
        if user_move == "bomb" and bot_move == "bomb":
            return {"winner": "draw"}
        if user_move == "bomb":
            return {"winner": "user"}
        if bot_move == "bomb":
            return {"winner": "bot"}

        if user_move == bot_move:
            return {"winner": "draw"}

        if (
            (user_move == "rock" and bot_move == "scissors") or
            (user_move == "scissors" and bot_move == "paper") or
            (user_move == "paper" and bot_move == "rock")
        ):
            return {"winner": "user"}

        return {"winner": "bot"}


# -----------------------------
# TOOL 3: UPDATE GAME STATE
# -----------------------------
if ADK_AVAILABLE:
    @tool
    def update_game_state(state: dict, user_move: str, bot_move: str, result: dict) -> dict:
        if user_move == "bomb":
            state["user_bomb_used"] = True
        if bot_move == "bomb":
            state["bot_bomb_used"] = True

        if result["winner"] == "user":
            state["user_score"] += 1
        elif result["winner"] == "bot":
            state["bot_score"] += 1

        state["round"] += 1

        if state["round"] > MAX_ROUNDS:
            state["game_over"] = True

        return state
else:
    def update_game_state(state: dict, user_move: str, bot_move: str, result: dict) -> dict:
        if user_move == "bomb":
            state["user_bomb_used"] = True
        if bot_move == "bomb":
            state["bot_bomb_used"] = True

        if result["winner"] == "user":
            state["user_score"] += 1
        elif result["winner"] == "bot":
            state["bot_score"] += 1

        state["round"] += 1

        if state["round"] > MAX_ROUNDS:
            state["game_over"] = True

        return state


# -----------------------------
# BOT MOVE LOGIC
# -----------------------------
def choose_bot_move(state: dict) -> str:
    if state["bot_bomb_used"]:
        return random.choice(["rock", "paper", "scissors"])
    return random.choice(VALID_MOVES)


# =====================================================
# AGENT ORCHESTRATION LOOP
# =====================================================
def run_game():
    print("Welcome to Rock–Paper–Scissors–Plus!")
    print("Best of 3 rounds.")
    print("You may use 'bomb' once — it beats everything.")
    print("Invalid moves waste the round.")
    print("Let’s begin!\n")

    while not game_state["game_over"]:
        print(f"--- Round {game_state['round']} ---")
        user_input = input("Your move: ")

        validation = validate_move(user_input, game_state)

        if not validation["valid"]:
            print(f"Invalid input: {validation['reason']}. Round wasted.\n")
            game_state["round"] += 1
            if game_state["round"] > MAX_ROUNDS:
                game_state["game_over"] = True
            continue

        user_move = validation["move"]
        bot_move = choose_bot_move(game_state)

        result = resolve_round(user_move, bot_move)
        update_game_state(game_state, user_move, bot_move, result)

        print(f"You played: {user_move}")
        print(f"Bot played: {bot_move}")

        if result["winner"] == "draw":
            print("Result: Draw\n")
        elif result["winner"] == "user":
            print("Result: You win this round!\n")
        else:
            print("Result: Bot wins this round!\n")

    print("=== GAME OVER ===")
    print(f"Final Score → You: {game_state['user_score']} | Bot: {game_state['bot_score']}")

    if game_state["user_score"] > game_state["bot_score"]:
        print("Final Result: You win 🎉")
    elif game_state["bot_score"] > game_state["user_score"]:
        print("Final Result: Bot wins 🤖")
    else:
        print("Final Result: Draw 🤝")


# -----------------------------
# OPTIONAL: ADK AGENT DECLARATION
# -----------------------------
if ADK_AVAILABLE:
    game_agent = Agent(
        name="RPSPlusReferee",
        description="An AI referee agent enforcing rules and tracking game state",
        tools=[validate_move, resolve_round, update_game_state],
    )

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_game()
