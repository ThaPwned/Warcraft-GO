"""Debug items for WCGO testing."""

# Source.Python
from listeners.tick import Delay, TickRepeat

# Warcraft: GO
from wcgo.cooldown import cooldown, cooldownf
from wcgo.entities import Item


# ======================================================================
# >> Regeneration Suit
# ======================================================================
class Regeneration_Suit(Item):
    "Regenerate health up to 100 when out of combat for 5 seconds."
    authors = 'Mahi',
    category = 'DEBUG'
    cost = 2500
    limit = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repeat = TickRepeat(self._tick)
        self._delay = None

    def _tick(self, player):
        if player.health < 100:
            player.health = min(player.health + 3, 100)

    def player_spawn(self, player, **eargs):
        self._repeat.args = (player,)
        self._repeat.start(1, 0)

    def player_death(self, **eargs):
        if self._delay is not None:
            self._delay.cancel()
            self._delay = None
        self._repeat.stop()

    def player_attack(self, **eargs):
        if self._delay is not None:
            self._delay.cancel()
        self._repeat.pause()
        self._delay = Delay(5, self._cancel_pause)

    def player_victim(self, **eargs):
        if self._delay is not None:
            self._delay.cancel()
        self._repeat.pause()
        self._delay = Delay(5, self._cancel_pause)

    def _cancel_pause(self):
        self._repeat.resume()
        self._delay = None

    
# ======================================================================
# >> Adrenaline Shot
# ======================================================================
class Adrenaline_Shot(Item):
    "Inject yourself with adrenaline for a 2 second speed boost and godmode."
    authors = 'Mahi',
    category = 'DEBUG'
    cost = 4000

    def item_purchase(self, player, **eargs):
        player.shift_property('speed', 0.7, duration=2)
        self._effect = player.godmode(2)
