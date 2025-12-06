# visualizer.py
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import consts
from board import MultiBallBoard

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import consts
# וודא שהייבוא הזה תואם לשמות הקבצים שלך
from board import MultiBallBoard


class DynamicVisualizer:
    def __init__(self, board):
        self.board = board
        self.fig, self.ax = plt.subplots(figsize=(8, 6))

        # הגדרות הלוח
        self.ax.set_xlim(0, consts.BOARD_WIDTH)
        self.ax.set_ylim(0, consts.BOARD_HEIGHT)
        self.ax.set_title("Real-Time Simulation: Launchers & Balls")

        # קווים קבועים
        self.ax.axvline(x=consts.BORDER_X, color='red', linestyle='-', alpha=0.5, label='Defense Line')

        # --- אלמנטים גרפיים ---

        # 1. הכדורים (Scatter) - כאן אין בעיה לעדכן גדלים משתנים
        self.scat_balls = self.ax.scatter([], [], c='blue', s=50, label='Balls')

        # 2. החיצים (Quiver) - נאתחל כ-None וניצור אותם מחדש כל פריים
        self.quiver = None

        # 3. ציור המשגרים (קבועים)
        launcher_x = [l.pos[0] for l in self.board.launchers]
        launcher_y = [l.pos[1] for l in self.board.launchers]
        self.ax.scatter(launcher_x, launcher_y, c='green', marker='s', s=100, label='Launchers')

        self.ax.legend(loc='upper left')
        self.ax.grid(True, alpha=0.3)

    def update(self, frame):
        """פונקציה שנקראת בכל פריים של האנימציה"""

        # 1. קידום המשחק
        self.board.step()

        # 2. איסוף נתונים
        ball_positions = []
        ball_velocities_x = []
        ball_velocities_y = []

        for ball in self.board.balls:
            if not ball['done']:
                ball_positions.append(ball['pos'])
                ball_velocities_x.append(ball['velocity'][0])
                ball_velocities_y.append(ball['velocity'][1])

        # 3. עדכון הכדורים (Scatter תומך בשינוי גודל מערך)
        if ball_positions:
            data = np.array(ball_positions)
            self.scat_balls.set_offsets(data)
        else:
            self.scat_balls.set_offsets(np.empty((0, 2)))

        # 4. עדכון החיצים (מחיקה ויצירה מחדש - פותר את השגיאה)
        # אם יש חיצים ישנים - נמחק אותם
        if self.quiver is not None:
            self.quiver.remove()

        # אם יש כדורים - נצייר חיצים חדשים
        if ball_positions:
            self.quiver = self.ax.quiver(
                data[:, 0], data[:, 1],  # X, Y
                ball_velocities_x, ball_velocities_y,  # U, V
                color='red', scale=1, scale_units='xy', angles='xy'
            )
        else:
            self.quiver = None  # אין כדורים, אין חיצים

        return self.scat_balls, self.quiver

    def animate(self):
        # blit=False חשוב כאן כדי לאפשר מחיקה ויצירה של אובייקטים
        anim = animation.FuncAnimation(self.fig, self.update, frames=200, interval=50, blit=False)
        plt.show()


# --- בדיקה ---
if __name__ == "__main__":
    game_board = MultiBallBoard()
    viz = DynamicVisualizer(game_board)
    viz.animate()

class GameVisualizer:
    def __init__(self, width, height, border):
        self.width = width
        self.height = height
        self.border = border

    def show(self, balls, rocks, title="Simulation Result"):
        plt.figure(figsize=(8, 8))
        plt.title(title)
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

        # ציור הקווים
        plt.axvline(x=self.border, color='red', linewidth=2, label='Target Line')
        plt.axvline(x=self.width, color='green', linestyle='--', label='Start Line')

        # הגדרת צבעים (בדיוק כמו בקוד שלך)
        colors_balls = plt.cm.jet(np.linspace(0, 1, len(balls)))
        colors_rocks = plt.cm.plasma(np.linspace(0, 1, len(rocks)))

        # ציור כדורים
        for ball, color in zip(balls, colors_balls):
            traj = np.array(ball['trajectory'])
            plt.plot(traj[:, 0], traj[:, 1], '.-', color=color, alpha=0.6)
            plt.plot(traj[-1, 0], traj[-1, 1], 'x', color=color, markersize=10, markeredgewidth=2)
            # זווית
            plt.text(traj[0, 0], traj[0, 1], f"{ball['angle']}°", fontsize=8, color=color)

        # ציור אבנים
        for rock, color in zip(rocks, colors_rocks):
            pos = np.array(rock['pos'])
            # בקוד המקורי השתמשת ב-pos[1] שזה ה-Y. ה-X הוא 0.
            plt.plot(pos[0], pos[1], 'o', color=color, markersize=10, markeredgewidth=2)

        plt.grid(True, alpha=0.3)
        plt.show()