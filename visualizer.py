# visualizer.py
import matplotlib.pyplot as plt
import numpy as np

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