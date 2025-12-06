# board.py
import numpy as np
import random
import math
import consts
import BallsClass


class MultiBallBoard:
    def __init__(self, width=consts.BOARD_WIDTH, height=consts.BOARD_HEIGHT,
                 speed=consts.SPEED, border=consts.BORDER_X,
                 num_balls=consts.NUM_BALLS, num_rocks=consts.NUM_ROCKS):
        self.width = width
        self.height = height
        self.speed = speed
        self.border = border

        self.num_balls = num_balls
        self.balls = []
        self.ball_id_counter = 0
        self.launchers = []
        self.create_balls_lunchers()

        self.num_rocks = num_rocks
        self.rocks = []
        self.reset_rocks()

    def create_balls_lunchers(self):
        self.launchers.append(BallsClass.BallLauncher(
            x_pos=self.width,
            y_pos=self.height * 0.8,
            speed=self.speed,
            angle_mean=-20, angle_std=10, fire_prob=0.1,
            border_x=self.border, board_height=self.height))
        self.launchers.append(BallsClass.BallLauncher(
            x_pos=self.width,
            y_pos=self.height * 0.5,
            speed=self.speed,
            angle_mean=0, angle_std=25, fire_prob=0.05,
            border_x=self.border, board_height=self.height))
        self.launchers.append(BallsClass.BallLauncher(
            x_pos=self.width,
            y_pos=self.height * 0.2,
            speed=self.speed,
            angle_mean=20, angle_std=10, fire_prob=0.02,
            border_x=self.border, board_height=self.height))

    def create_rock(self, rock_id):
        """פונקציית עזר ליצירת אבן"""
        step = 10
        max_valid_y = (int(self.height) // step) * step
        start_y = random.randrange(0, max_valid_y + step, step)
        # המרה ל-float כדי שיהיה תואם לטיפוס של הכדורים
        pos = np.array([0.0, float(start_y)])
        return {
            'id': rock_id,
            'pos': pos,
        }

    def reset(self):
        self.balls = []
        self.ball_id_counter = 0
        self.rocks = []

    def reset_rocks(self):
        self.rocks = []
        for i in range(self.num_rocks):
            self.rocks.append(self.create_rock(i))
        return self.rocks

    def step(self):
        for launcher in self.launchers:
            new_ball = launcher.step()
            if new_ball is not None:
                # הוספת מזהה ייחודי לכדור
                new_ball['id'] = self.ball_id_counter
                self.ball_id_counter += 1
                self.balls.append(new_ball)

        # Updating balls locations
        all_finished = True  # בדיקה האם נשארו כדורים פעילים (פחות רלוונטי כשיש משגרים אינסופיים, אבל שיהיה)
        for ball in self.balls:
            if ball['done']:
                continue
            all_finished = False  # יש לפחות כדור אחד חי
            ball['pos'] += ball['velocity']
            ball['trajectory'].append(ball['pos'].copy())
            x, y = ball['pos']
            if x <= self.border or y >= self.height or y <= 0:  # תנאי סיום: הגיע לגבול
                ball['done'] = True
        return self.balls, all_finished

    def calc_rocks_directions(self):
        rock_ball_options = []
        for rock in self.rocks:
            for ball in self.balls:
                ball_at_border = ball['pos']
                ball_steps_to_reach_border = len(ball['trajectory']) - 1

                # חישוב מרחק אוקלידי בין האבן למיקום הסופי של הכדור
                rock_ball_dist = math.sqrt(ball_at_border[0] ** 2 + (rock['pos'][1] - ball_at_border[1]) ** 2)

                steps_for_rock_to_reach_ball_at_border = math.ceil(rock_ball_dist / self.speed)
                number_of_rock_waiting_steps_for_ball = ball_steps_to_reach_border - steps_for_rock_to_reach_ball_at_border

                # print(number_of_rock_waiting_steps_for_ball) # השארתי בהערה
                if number_of_rock_waiting_steps_for_ball >= 0:
                    rock_ball_options.append({
                        "rock_id": rock['id'],
                        "ball_id": ball['id'],
                        "spare_steps": number_of_rock_waiting_steps_for_ball
                    })
        return rock_ball_options