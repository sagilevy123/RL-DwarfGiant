import random
import math
import numpy as np


class BallLauncher:
    def __init__(self, x_pos, y_pos, speed, angle_mean, angle_std, fire_prob, border_x, board_height):
        self.pos = np.array([float(x_pos), float(y_pos)])
        self.speed = speed
        self.angle_mean = angle_mean
        self.angle_std = angle_std
        self.fire_prob = fire_prob
        self.angles_constrains(x_pos, y_pos, border_x, board_height)

    def angles_constrains(self, x_pos, y_pos, border_x, board_height):
        dist_to_border = x_pos - border_x

        # 1. חישוב גבול עליון
        dist_to_ceiling = board_height - y_pos
        if dist_to_ceiling <= 0:
            self.max_angle_up = 0
        else:
            self.max_angle_up = math.degrees(math.atan(dist_to_ceiling / dist_to_border))

        # 2. חישוב גבול תחתון
        dist_to_floor = y_pos
        if dist_to_floor <= 0:
            self.max_angle_down = 0
        else:
            self.max_angle_down = math.degrees(math.atan(dist_to_floor / dist_to_border))

    def step(self):
        if random.random() > self.fire_prob:
            return None  # לא יורים בצעד הזה
        raw_angle = random.gauss(self.angle_mean, self.angle_std)
        final_angle = max(-self.max_angle_down, min(self.max_angle_up, raw_angle))
        rad = math.radians(final_angle)
        vx = -self.speed * math.cos(rad)
        vy = self.speed * math.sin(rad)
        velocity = np.array([vx, vy])
        return {
            'pos': self.pos.copy(),  # copy!
            'velocity': velocity,
            'angle': final_angle,
            'trajectory': [self.pos.copy()],
            'done': False
        }
