                                                                # used by

import random                                               

from game.casting.actor import Actor
from game.casting.artifact import Artifact
from game.casting.cast import Cast

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._artifact_velosity = Point(0, 5)
        self._score = 300
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        x=1
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
            x+=1
            if x % 10 == 0:
                self._create_artifacts(cast)
        self._video_service.close_window()

    def _create_artifacts(self, cast):
        texts = ["O", "*"]
        DEFAULT_ARTIFACTS = random.randint(0,3)
        for n in range(DEFAULT_ARTIFACTS):
            text = random.choice(texts)
            x = random.randint(1, 901)
            y = 0
            position = Point(x, y)
            position = position.scale(25)  # Change understanding code
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = Color(r, g, b)
            
            artifact = Artifact()
            artifact.set_text(text)
            artifact.set_font_size(25)      #   Change understanding code
            artifact.set_color(color)
            artifact.set_position(position)
            cast.add_actor("artifacts", artifact)


    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity) 
        artifacts = cast.get_actors("artifacts")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()        
        for artifact in artifacts:
            artifact.set_velocity(self._artifact_velosity)
            artifact.move_next(max_x, max_y)

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")

        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        for artifact in artifacts:
            if artifact.get_position().get_y() == max_y:
                cast.remove_actor("artifacts", artifact)

            if robot.get_position().equals(artifact.get_position()):
                if artifact.get_text() =="*":
                    self._score += 1
                else:
                    self._score -= 1
                cast.remove_actor("artifacts", artifact)

            
        banner.set_text(f"Actual score: {self._score}")

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()