# main.py
from board import MultiBallBoard
from visualizer import GameVisualizer
import consts


def run_simulation():
    # יצירת האובייקטים
    # שים לב: אנחנו לא מעבירים פרמטרים, אז הוא לוקח הכל מ-consts.py כולל הגבול
    game = MultiBallBoard()
    viz = GameVisualizer(consts.BOARD_WIDTH, consts.BOARD_HEIGHT, consts.BORDER_X)

    print(f"Starting simulation with {consts.NUM_BALLS} balls and {consts.NUM_ROCKS} rocks...")

    done = False
    steps = 0

    # לולאת המשחק
    while not done and steps < consts.MAX_STEPS:
        balls, done = game.step()
        steps += 1

    print(f"Simulation finished in {steps} steps.")

    # הדפסות כפי שביקשת
    print(f"Balls: {[b['id'] for b in balls]}")  # הדפסה מקוצרת לזיהוי
    print(f"Rocks: {[r['pos'] for r in game.rocks]}")

    print("\n--- Rock-Balls Calculation ---")
    options = game.calc_rocks_directions()
    print(f"Rock-Balls Options: {options}")

    # הצגת הגרף
    viz.show(game.balls, game.rocks, f"Sim: {consts.NUM_BALLS} Balls, {consts.NUM_ROCKS} Rocks")


if __name__ == "__main__":
    run_simulation()