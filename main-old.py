import matplotlib.pyplot as plt
import numpy as np
import random
import math


class MultiBallBoard:
    def __init__(self, width=100, height=300, speed=5, num_balls=2, num_rocks=1):
        self.width = width
        self.height = height
        self.speed = speed
        self.border = self.width / 3.0  # The border
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

        # החזרת המילון שמייצג כדור
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
        # 1. הגרלת גובה התחלה
        step = 10
        max_valid_y = (int(self.height) // step) * step
        start_y = random.randrange(0, max_valid_y + step, step)
        pos = np.array([0, start_y])
        return {
            'id': rock_id,
            'pos': pos,
        }

    def reset_balls(self):
        """מאתחל מחדש את כל הכדורים (׳גמדים׳)"""
        self.balls = []
        for i in range(self.num_balls):
            ball = self._create_ball(i)
            self.balls.append(ball)
        return self.balls

    def reset_rocks(self):
        """מאתחל את האבנים (׳ענקים׳)"""
        self.rocks = []
        for i in range(self.num_rocks):
            rock = self.create_rock(i)
            self.rocks.append(rock)
        return self.rocks

    def step(self):
        """מקדמת את כל הכדורים בצעד אחד"""
        all_finished = True

        for ball in self.balls:
            if ball['done']:
                continue  # כדור שסיים לא זז יותר

            all_finished = False  # יש לפחות כדור אחד שעדיין זז

            # עדכון מיקום
            ball['pos'] += ball['velocity']
            ball['trajectory'].append(ball['pos'].copy())

            # בדיקת תנאי עצירה לכדור הספציפי
            x, y = ball['pos']
            if x <= self.border or y >= self.height or y <= 0:
                ball['done'] = True

        return self.balls, all_finished

    def calc_rocks_directions(self):
        rock_ball_options = []
        for rock in self.rocks:
            for ball in self.balls:
                ball_at_border = ball['pos']
                ball_steps_to_reach_border = len(ball['trajectory'])-1
                rock_ball_dist = math.sqrt(ball_at_border[0]**2 + (rock['pos'][1] - ball_at_border[1])**2)
                steps_for_rock_to_reach_ball_at_border = math.ceil(rock_ball_dist/self.speed)
                number_of_rock_waiting_steps_for_ball = ball_steps_to_reach_border - steps_for_rock_to_reach_ball_at_border
                print(number_of_rock_waiting_steps_for_ball)
                if number_of_rock_waiting_steps_for_ball >=0:
                    rock_ball_options.append({"rock_id": rock['id'],"ball_id": ball['id'], "spare_steps": number_of_rock_waiting_steps_for_ball})
        return rock_ball_options

    def visualize(self):
        plt.figure(figsize=(8, 8))
        plt.title(f"Simulation with {self.num_balls} Balls and {self.num_rocks} Rocks")
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

        # ציור הקווים
        plt.axvline(x=self.border, color='red', linewidth=2, label='Target Line')
        plt.axvline(x=self.width, color='green', linestyle='--', label='Start Line')

        # לולאה לציור המסלול של כל כדור
        # נשתמש ב-colormap כדי שלכל כדור יהיה צבע קצת שונה
        colors_balls = plt.cm.jet(np.linspace(0, 1, self.num_balls))
        colors_rocks = plt.cm.plasma(np.linspace(0, 1, self.num_rocks))

        for ball, color in zip(self.balls, colors_balls):
            traj = np.array(ball['trajectory'])
            plt.plot(traj[:, 0], traj[:, 1], '.-', color=color, alpha=0.6)
            # נקודת סיום
            plt.plot(traj[-1, 0], traj[-1, 1], 'x', color=color, markersize=10, markeredgewidth=2)

            # הדפסת הזווית ליד נקודת ההתחלה (אופציונלי, עוזר לדיבאג)
            plt.text(traj[0, 0], traj[0, 1], f"{ball['angle']}°", fontsize=8, color=color)

        for rock, color in zip(self.rocks, colors_rocks):
            pos = np.array(rock['pos'])
            plt.plot(pos[1], 'o', color=color, markersize=10, markeredgewidth=2)

        plt.grid(True, alpha=0.3)
        plt.show()

# --- הרצה ---
# נגדיר 10 כדורים כדי לראות את האקשן
game = MultiBallBoard(width=100, height=300, speed=1, num_balls=3, num_rocks=3)

done = False
steps = 0
max_steps = 1000

while not done and steps < max_steps:
    balls, done = game.step()  # הפונקציה מחזירה True ב-done רק כשכולם סיימו
    steps += 1
print(f"balls: {balls}")
print(f"Rocks: {game.rocks}")
print(f"Rock-Balls: {game.calc_rocks_directions()}")

print(f"Simulation finished in {steps} steps.")

game.visualize()