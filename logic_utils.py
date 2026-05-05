from dataclasses import dataclass, field
from typing import Tuple, Optional


@dataclass
class GameConfig:
    """Configuration for difficulty levels."""
    difficulty: str
    
    def get_range(self) -> Tuple[int, int]:
        """Return (low, high) inclusive range for the difficulty."""
        ranges = {
            "Easy": (1, 20),
            "Normal": (1, 100),
            "Hard": (1, 500),
        }
        return ranges.get(self.difficulty, (1, 100))
    
    def get_attempt_limit(self) -> int:
        """Return max attempts allowed for this difficulty."""
        limits = {
            "Easy": 6,
            "Normal": 8,
            "Hard": 5,
        }
        return limits.get(self.difficulty, 8)


@dataclass
class GameState:
    """Represents the current state of a game."""
    secret: int
    attempts: int
    score: int
    history: list = field(default_factory=list)
    status: str = "playing"  # "playing", "won", "lost"
    
    def add_guess(self, guess: int) -> None:
        """Record a guess in history."""
        self.history.append(guess)
    
    def increment_attempts(self) -> None:
        """Increment attempt counter."""
        self.attempts += 1


@dataclass
class Game:
    """Main game logic class."""
    config: GameConfig
    state: GameState
    
    def parse_guess(self, raw: str) -> Tuple[bool, Optional[int], Optional[str]]:
        """
        Parse user input into an int guess.
        
        Returns: (ok: bool, guess_int: int | None, error_message: str | None)
        """
        if raw is None or raw == "":
            return False, None, "Enter a guess."
        
        try:
            if "." in raw:
                value = int(float(raw))
            else:
                value = int(raw)
        except Exception:
            return False, None, "That is not a number."
        
        return True, value, None
    
    def check_guess(self, guess: int) -> Tuple[str, str]:
        """
        Compare guess to secret and return (outcome, message).
        
        Returns: (outcome, message)
        outcome examples: "Win", "Too High", "Too Low"
        """
        if guess == self.state.secret:
            return "Win", "🎉 Correct!"
        
        if guess > self.state.secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    
    def update_score(self, outcome: str) -> int:
        """Update and return new score based on outcome."""
        attempt_number = self.state.attempts
        
        if outcome == "Win":
            points = 100 - 10 * (attempt_number + 1)
            points = max(points, 10)  # minimum 10 points
            self.state.score += points
        elif outcome == "Too High":
            if attempt_number % 2 == 0:
                self.state.score += 5
            else:
                self.state.score -= 5
        elif outcome == "Too Low":
            self.state.score -= 5
        
        return self.state.score
    
    def process_guess(self, raw_guess: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Process a raw guess input and update game state.
        
        Returns: (success: bool, outcome: str | None, message: str | None)
        """
        ok, guess_int, err = self.parse_guess(raw_guess)
        
        if not ok:
            self.state.add_guess(raw_guess)
            return False, None, err
        
        self.state.attempts += 1
        self.state.add_guess(guess_int)
        
        outcome, message = self.check_guess(guess_int)
        self.update_score(outcome)
        
        if outcome == "Win":
            self.state.status = "won"
        
        return True, outcome, message


# Backwards-compatible functions for existing code
def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """Return (low, high) inclusive range for a given difficulty."""
    config = GameConfig(difficulty)
    return config.get_range()


def parse_guess(raw: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> Tuple[str, str]:
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
