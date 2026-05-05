import random
import streamlit as st
from logic_utils import GameConfig, GameState, Game

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# Initialize game config and state
config = GameConfig(difficulty)
attempt_limit = config.get_attempt_limit()
low, high = config.get_range()

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Initialize or retrieve game from session state
if "game" not in st.session_state:
    secret = random.randint(low, high)
    state = GameState(
        secret=secret,
        attempts=0,
        score=0,
        history=[],
        status="playing",
    )
    st.session_state.game = Game(config=config, state=state)

game = st.session_state.game

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - game.state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", game.state.secret)
    st.write("Attempts:", game.state.attempts)
    st.write("Score:", game.state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", game.state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # Reset game state
    secret = random.randint(low, high)
    new_state = GameState(
        secret=secret,
        attempts=0,
        score=0,
        history=[],
        status="playing",
    )
    st.session_state.game = Game(config=config, state=new_state)
    st.success("New game started.")
    st.rerun()

if game.state.status != "playing":
    if game.state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    success, outcome, message = game.process_guess(raw_guess)
    
    if not success:
        st.error(message)
    else:
        if show_hint:
            st.warning(message)
        
        st.write(f"Score: {game.state.score}")
        
        if outcome == "Win":
            st.balloons()
            st.success(
                f"You won! The secret was {game.state.secret}. "
                f"Final score: {game.state.score}"
            )
        else:
            if game.state.attempts >= attempt_limit:
                game.state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {game.state.secret}. "
                    f"Score: {game.state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
