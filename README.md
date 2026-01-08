# AI Game Referee – Rock–Paper–Scissors–Plus

## Overview
This project is a simple AI referee for a Rock–Paper–Scissors–Plus game.
The bot runs the game between the user and itself, enforces the rules,
keeps track of state across rounds, and explains the result of each round.

The focus of this assignment is on clear logic, proper state handling,
and designing the agent in a way that would work reliably in a real system.

---

## Game Rules
- The game is played for a maximum of 3 rounds
- Valid moves are: rock, paper, scissors, and bomb
- Each player can use bomb only once in the entire game
- Bomb beats all other moves
- Bomb vs bomb results in a draw
- Invalid input wastes the round
- The game ends automatically after round 3

---

## State Model
The game maintains an explicit state object stored in code and not inside prompts.
This state persists across turns and is updated after every round.

The state includes:
- `round`: current round number
- `user_score`: number of rounds won by the user
- `bot_score`: number of rounds won by the bot
- `user_bomb_used`: whether the user has already used bomb
- `bot_bomb_used`: whether the bot has already used bomb
- `game_over`: indicates when the game has finished

Keeping the state outside prompts makes the behavior predictable and easier to debug.

---

## Agent and Tool Design
The system is designed as a single agent that controls the game flow.
The agent itself does not decide game outcomes directly. Instead, the
logic is split into small tool-style functions.

### Tools used
- **validate_move**  
  Checks whether the user input is valid and enforces constraints such as
  one-time bomb usage.

- **resolve_round**  
  Applies the Rock–Paper–Scissors–Plus rules and decides the winner of
  a single round.

- **update_game_state**  
  Updates scores, bomb usage, round count, and determines when the game
  should end.

All tools return structured dictionary outputs, which keeps the logic
deterministic and easy to reason about.

---

## Google ADK Usage
This solution follows Google ADK design principles.

- The referee is modeled as a single agent responsible for orchestration.
- Validation, rule evaluation, and state updates are handled through
  explicit tools.
- Game state is stored as structured data and not embedded in prompts.
- Tool outputs are structured dictionary values.

The code runs as a standalone script but is structured in a way that can
be easily migrated to a full Google ADK runtime.

---

## Architecture Separation
The implementation keeps different responsibilities separate:
- Input handling and flow control are managed by the agent loop
- Game rules are enforced through deterministic logic
- State is managed independently of user interaction
- User-facing responses are generated after logic decisions

This separation improves clarity and maintainability.

---

## Trade-offs
I focused more on correctness, clarity, and explicit state handling rather
than advanced UX or complex prompt design. All important game rules are
enforced in code instead of relying on probabilistic model behavior.

---

## Possible Improvements
With more time, I would:
- Add a replay option without restarting the program
- Improve handling of more natural language inputs
- Add basic tests for game logic
- Integrate a full ADK execution loop with model-driven tool selection

---

## How to Run
```bash
python game_referee.py
