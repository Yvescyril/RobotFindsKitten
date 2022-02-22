import random
from game.casting.actor import Actor
from game.shared.point import Point 
from game.casting.cast import Cast
from game.shared.color import Color

class Artifact(Actor):
    """
    An item of cultural or historical interest. 
    
    The responsibility of an Artifact is to provide a message about itself.

    Attributes:
        _message (string): A short description about the artifact.
    
    def __init__(self):
        super().__init__()
        self._DEFAULT_ARTIFACTS = 3
        self._artifact = Actor()
        self._texts = ["O", "*"]
        self._CELL_SIZE = 15
        self._FONT_SIZE = 15
           
    def _create_artifacts(self, cast):

        for n in range(self._DEFAULT_ARTIFACTS):
            text = random.choice(self._texts)
            x = random.randint(1, 900)
            y = 0
            position = Point(x, y)
            position = position.scale(self._CELL_SIZE)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = Color(r, g, b)

            self._artifact.set_text(text)
            self._artifact.set_font_size(self._FONT_SIZE)
            self._artifact.set_color(color)
            self._artifact.set_position(position)
            cast.add_actor("artifacts", self._artifact)"""