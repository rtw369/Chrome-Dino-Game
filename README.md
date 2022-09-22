# Chrome-Dino-Game
Velocity of the dino and obstacles increase by 0.1 as score increase by 1
Find the patterns for the obstacles spawn rate
    - larger quantity obstacles spawn more frequently as the game progresses?
    - no, make obstacles appear as random.
The image has to be split into multiple images containing each sprite image.
    - ie. dino1, dino2, dino3, bird1, bird2, cacti1 ...
Classes: Dino, Obstacles(cacti and birds), Base, Background(cloud and sun)?
    - Dino images might need fine-tuning to make sure the pixels are the same.
    - Birds will appear in 3 different spot: top, middle, bottom.
        - top: high enough to dodge without doing anything.
        - middle: high enough to dodge by jumping or ducking.
        - bottom: high enough to only be able to dodge by ducking.
    - Obstacles will have certain distance between them.
        - The original game has ~4 different lengths between the obstacles and tends to use the longest ones in the later
          part of the game where the velocity of the obstacles are high.
        - The original game has a maximum of 2 obstacles on the screen and minimum of 1 obstacles on the screen, this
          game will use latter case with 1 fixed length between the obstacles.
Screen size will be equivalent to phone screen size, two bases will move towards the dino repeatedly.

# AI
Use the configuration settings from "TechWithTim Flappy Bird AI Tutorial"

Input: obstacle.y, Distance between the obstacle and the dino, obstacle velocity
Output: jump or crouch
Fitness: Longest surviving dino, encourage to jump over the obstacle rather than jumping onto one.