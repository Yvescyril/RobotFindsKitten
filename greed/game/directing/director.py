                                                                # used by

import winsound

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
            self._artifact_velosity (Artifact class that inherits the Actor class): the movement and the speed for the artifact.
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
            #the variable x and the following code will set the speed of the falling artifacts (the gems and the rocks)
            if x % 10 == 0:
                self._create_artifacts(cast)
        self._video_service.close_window()

    def _create_artifacts(self, cast): #creating the falling gems and the rocks
        texts = ["H", "*"]
        DEFAULT_ARTIFACTS = random.randint(0,3) #the number of the falling artifacts
        
        for n in range(DEFAULT_ARTIFACTS):
            text = random.choice(texts)
            x = random.randint(1, 901)
            y = 0
            position = Point(x, y) #the coordinates where the artifacts will fall, y=0 because it starts at the top of the screen, x is random
            position = position.scale(25)  # refer to the point class method
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = Color(r, g, b)
            
            artifact = Artifact() #setting the artifacts with their descriptions, font_size and cell_size = 25 like the rfk game
            artifact.set_text(text)
            artifact.set_font_size(15)      #   Change understanding code
            artifact.set_color(color)
            artifact.set_position(position)
            cast.add_actor("artifacts", artifact)


    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        and an automatic fall for the artifacts
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity) 
        
        #setting the automatic fall for the artifacts, refer to the actor method since the artifact inherits the actor method
        artifacts = cast.get_actors("artifacts")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()        
        for artifact in artifacts:
            artifact.set_velocity(self._artifact_velosity)
            artifact.move_next(max_x, max_y)

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        creating a banner at the top left of the screen to show the score
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")
         
        #update the robot's position based on the keyboard input
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        #remove the artifact when t reach the bottom of the screen or the player touches the artifacts
        for artifact in artifacts:
            if artifact.get_position().get_y() == max_y:
                cast.remove_actor("artifacts", artifact)

            if robot.get_position().equals(artifact.get_position()):
                if artifact.get_text() =="*":
                    self._score += 1 #win 1 point if the player touches the gem
                    winsound.PlaySound("mixkit-winning-a-coin-video-game-2069.wav", winsound.SND_FILENAME)
                else:
                    self._score -= 1 #lose 1 point if the player touches the rock
                    winsound.PlaySound("mixkit-creature-cry-of-hurt-2208", winsound.SND_FILENAME)
                cast.remove_actor("artifacts", artifact) 

        #displaying the Actual score based on the circumstances above
        banner.set_text(f"Score: {self._score}")

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()
