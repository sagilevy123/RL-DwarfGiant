# board.py
import numpy as np
import random
import math
import consts


class MultiBallBoard:
    def __init__(self, width=consts.BOARD_WIDTH, height=consts.BOARD_HEIGHT,
                 speed=consts.SPEED, border=consts.BORDER_X,
                 num_balls=consts.NUM_BALLS, num_rocks=consts.NUM_ROCKS):
        self.width = width
        self.height = height
        self.speed = speed
        self.border = border  # לוקח מהקבוע, בלי לחשב מחדש
        self.num_balls = num_balls
        self.balls = []
        self.num_rocks = num_rocks
        self.rocks = []

        self.reset_balls()
        self.reset_rocks()

    def _create_ball(self, ball_id):
        """פונקציית עזר ליצירת כדור בודד עם זווית חוקית"""
        # 1. הגרלת גובה התחלה
        start_y = random.uniform(0, self.height)
        pos = np.array([float(self.width), start_y])

        # 2. חישוב זווית מקסימלית (כדי למנוע פגיעה בתקרה לפני הקו)
        dist_to_border = self.width - self.border
        available_height = self.height - start_y

        if available_height <= 0:
            max_angle_deg = 0
        else:
            max_tan = available_height / dist_to_border
            max_angle_deg = math.degrees(math.atan(max_tan))

        # 3. בחירת זווית מהרשימה המותרת
        possible_angles = range(0, 91, 10)
        valid_angles = [a for a in possible_angles if a <= max_angle_deg + 0.1]
        if not valid_angles: valid_angles = [0]

        angle_deg = random.choice(valid_angles)
        angle_rad = math.radians(angle_deg)

        # 4. וקטור מהירות
        vx = -self.speed * math.cos(angle_rad)
        vy = self.speed * math.sin(angle_rad)
        velocity = np.array([vx, vy])

        return {
            'id': ball_id,
            'pos': pos,
            'velocity': velocity,
            'angle': angle_deg,
            'trajectory': [pos.copy()],
            'done': False
        }

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

    def reset_balls(self):
        self.balls = []
        for i in range(self.num_balls):
            self.balls.append(self._create_ball(i))
        return self.balls

    def reset_rocks(self):
        self.rocks = []
        for i in range(self.num_rocks):
            self.rocks.append(self.create_rock(i))
        return self.rocks

    def step(self):
        """מקדמת את כל הכדורים בצעד אחד"""
        all_finished = True

        for ball in self.balls:
            if ball['done']:
                continue

            all_finished = False

            # עדכון מיקום
            ball['pos'] += ball['velocity']
            ball['trajectory'].append(ball['pos'].copy())

            # בדיקת תנאי עצירה לכדור הספציפי
            x, y = ball['pos']
            if x <= self.border or y >= self.height or y <= 0:
                ball['done'] = True

        return self.balls, all_finished

    def calc_rocks_directions(self):
        """הלוגיקה המדויקת מהקוד שלך"""
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