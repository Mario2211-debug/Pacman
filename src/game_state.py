from src.config import Config


class GameState:
    """Score, lives, level and timer of one game. No rendering here."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.score = 0
        self.lives = config.lives
        self.level = 0
        self.time_left = float(config.level_max_time)
        self.victory = False

    @property
    def level_number(self) -> int:
        return self.level + 1

    @property
    def total_levels(self) -> int:
        return len(self.config.level)

    @property
    def game_over(self) -> bool:
        return self.lives <= 0

    @property
    def finished(self) -> bool:
        return self.game_over or self.victory

    def _add_points(self, points: int) -> None:
        # The score never decreases
        if not self.finished and points > 0:
            self.score += points

    def eat_pacgum(self) -> None:
        self._add_points(self.config.points_per_pacgum)

    def eat_super_pacgum(self) -> None:
        self._add_points(self.config.points_per_super_pacgum)

    def eat_ghost(self) -> None:
        self._add_points(self.config.points_per_ghost)

    def lose_life(self) -> None:
        if self.lives > 0:
            self.lives -= 1

    def complete_level(self) -> None:
        if self.finished:
            return
        if self.level_number >= self.total_levels:
            self.victory = True
            return
        self.level += 1
        self.time_left = float(self.config.level_max_time)

    def tick(self, dt: float) -> None:
        """Running out of time costs a life and restarts the level timer."""
        if self.finished:
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self.lose_life()
            self.time_left = float(self.config.level_max_time)
