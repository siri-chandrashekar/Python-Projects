import time
from pathlib import Path

import keyboard
import pyautogui

pyautogui.FAILSAFE = False

DEFAULT_GAME_REGION = (80, 600, 550, 245)
REFERENCE_WIDTH = 550
REFERENCE_HEIGHT = 245
STOP_KEY = "z"
JUMP_KEY = "up"
DUCK_KEY = "down"
SAVE_FRAME_KEY = "v"

BACKGROUND_SAMPLE = (100, 100)

# Reference boxes (x1, y1, x2, y2) in the default 550x245 region.
# Keep boxes to the right of the dinosaur to avoid static false positives.
CACTUS_BOX = (205, 140, 420, 222)
BIRD_BOX = (250, 55, 455, 128)

COLOR_TOLERANCE = 36
DARK_PIXEL_THRESHOLD = 140
JUMP_COOLDOWN = 0.11
DUCK_COOLDOWN = 0.35
DUCK_TIME = 0.08
BASE_JUMP_TRIGGER_X = 205
MAX_JUMP_TRIGGER_X = 300
TRIGGER_GROWTH_PER_SECOND = 0.7
DEBUG_PRINT_INTERVAL = 0.25
PREVIEW_IMAGE_PATH = Path(__file__).with_name("calibration_preview.png")
DEBUG_FRAME_PATH = Path(__file__).with_name("debug_frame.png")
CACTUS_COLUMN_MIN_PIXELS = 8
BIRD_COLUMN_MIN_PIXELS = 7
TRIPLE_CACTUS_HITS_THRESHOLD = 430
EARLY_JUMP_BOOST_X = 10
FOLLOWUP_JUMP_DELAY = 0.07
FOLLOWUP_JUMP_CLOSE_X = 40
SPEED_REACTION_START_SEC = 40
SPEED_REACTION_MAX_BOOST_X = 24
SPEED_REACTION_GROWTH_X_PER_SEC = 0.7
MIN_DYNAMIC_JUMP_COOLDOWN = 0.10


def get_pixel(image, x, y):
    pixels = image.load()
    return pixels[x, y]


def clamp(value, low, high):
    return max(low, min(value, high))


def scale_point(point, width, height):
    x, y = point
    scaled_x = int(x * width / REFERENCE_WIDTH)
    scaled_y = int(y * height / REFERENCE_HEIGHT)
    return scaled_x, scaled_y


def build_points(width, height, points):
    scaled_points = []
    for point in points:
        x, y = scale_point(point, width, height)
        x = clamp(x, 0, width - 1)
        y = clamp(y, 0, height - 1)
        scaled_points.append((x, y))
    return scaled_points


def scale_box(box, width, height):
    x1, y1, x2, y2 = box
    sx1, sy1 = scale_point((x1, y1), width, height)
    sx2, sy2 = scale_point((x2, y2), width, height)
    sx1 = clamp(sx1, 0, width - 1)
    sy1 = clamp(sy1, 0, height - 1)
    sx2 = clamp(sx2, 0, width - 1)
    sy2 = clamp(sy2, 0, height - 1)
    return min(sx1, sx2), min(sy1, sy2), max(sx1, sx2), max(sy1, sy2)


def scale_x(x, width):
    return clamp(int(x * width / REFERENCE_WIDTH), 0, width - 1)


def pixel_dark_enough(pixel, threshold=DARK_PIXEL_THRESHOLD):
    return pixel[0] < threshold and pixel[1] < threshold and pixel[2] < threshold


def changed(pixel, bg_color, tolerance=COLOR_TOLERANCE):
    color_delta = (
        abs(pixel[0] - bg_color[0]) +
        abs(pixel[1] - bg_color[1]) +
        abs(pixel[2] - bg_color[2])
    )
    bg_is_bright = (bg_color[0] + bg_color[1] + bg_color[2]) >= 600
    if color_delta > tolerance:
        return True
    # Only use "dark object" hint on bright backgrounds (day mode).
    if bg_is_bright and pixel_dark_enough(pixel):
        return True
    return False


def nearest_changed_x(image, points, bg_color):
    hits = []

    for x, y in points:
        if changed(get_pixel(image, x, y), bg_color):
            hits.append((x, y))

    if not hits:
        return None, 0

    # Smaller x is closer to the dinosaur (left side of the region).
    nearest_x = min(x for x, _ in hits)
    return nearest_x, len(hits)


def nearest_obstacle_x_in_box(image, box, bg_color, min_pixels_per_column):
    x1, y1, x2, y2 = box
    pixels = image.load()
    nearest_x = None
    hits = 0

    for x in range(x1, x2 + 1):
        column_hits = 0
        for y in range(y1, y2 + 1):
            pixel = pixels[x, y]
            if changed(pixel, bg_color):
                column_hits += 1
        if column_hits >= min_pixels_per_column:
            hits += column_hits
            if nearest_x is None or x < nearest_x:
                nearest_x = x

    return nearest_x, hits


def calibrate_region():
    print("Move your mouse to the TOP-LEFT corner of the game area and press 'c'.")
    while not keyboard.is_pressed("c"):
        time.sleep(0.05)
    left, top = pyautogui.position()
    print(f"Top-left captured at: ({left}, {top})")

    while keyboard.is_pressed("c"):
        time.sleep(0.05)

    print("Move your mouse to the BOTTOM-RIGHT corner of the game area and press 'c'.")
    while not keyboard.is_pressed("c"):
        time.sleep(0.05)
    right, bottom = pyautogui.position()
    print(f"Bottom-right captured at: ({right}, {bottom})")

    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        print("Calibration failed. Falling back to the default game region.")
        return DEFAULT_GAME_REGION

    region = (left, top, width, height)
    print(f"Using calibrated region: {region}")
    return region


def start():
    last_jump_time = 0
    last_duck_time = 0
    last_debug_print = 0

    print("Type 'c' and press Enter to calibrate, or just press Enter to use the default region.")
    try:
        user_input = input().strip().lower()
    except EOFError:
        user_input = ""

    if user_input == "c":
        game_region = calibrate_region()
    else:
        game_region = DEFAULT_GAME_REGION
        print(f"Using default region: {game_region}")

    _, _, region_width, region_height = game_region
    cactus_box = scale_box(CACTUS_BOX, region_width, region_height)
    bird_box = scale_box(BIRD_BOX, region_width, region_height)
    background_sample = scale_point(BACKGROUND_SAMPLE, region_width, region_height)
    background_sample = (
        clamp(background_sample[0], 0, region_width - 1),
        clamp(background_sample[1], 0, region_height - 1),
    )

    preview = pyautogui.screenshot(region=game_region)
    preview.save(PREVIEW_IMAGE_PATH)
    print(f"Saved calibration screenshot: {PREVIEW_IMAGE_PATH}")
    try:
        PREVIEW_IMAGE_PATH.resolve().open("rb").close()
        preview.show()
    except Exception:
        pass

    print("Switch to the game window. Starting in 5 seconds...")
    time.sleep(5)
    pyautogui.press("space")
    pyautogui.press("up")
    print("Bot started. Press 'z' to stop, 'v' to save a debug frame.")
    run_started_at = time.time()
    base_jump_trigger_x = scale_x(BASE_JUMP_TRIGGER_X, region_width)
    max_jump_trigger_x = scale_x(MAX_JUMP_TRIGGER_X, region_width)

    while True:
        if keyboard.is_pressed(STOP_KEY):
            break

        image = pyautogui.screenshot(region=game_region)
        bg_color = get_pixel(image, *background_sample)

        nearest_cactus_x, cactus_hits = nearest_obstacle_x_in_box(
            image,
            cactus_box,
            bg_color,
            CACTUS_COLUMN_MIN_PIXELS,
        )
        nearest_bird_x, bird_hits = nearest_obstacle_x_in_box(
            image,
            bird_box,
            bg_color,
            BIRD_COLUMN_MIN_PIXELS,
        )

        now = time.time()
        elapsed = now - run_started_at
        jump_trigger_x = min(
            max_jump_trigger_x,
            base_jump_trigger_x + int(elapsed * TRIGGER_GROWTH_PER_SECOND * region_width / REFERENCE_WIDTH),
        )
        if elapsed > SPEED_REACTION_START_SEC:
            speed_boost = int(
                (elapsed - SPEED_REACTION_START_SEC)
                * SPEED_REACTION_GROWTH_X_PER_SEC
                * region_width
                / REFERENCE_WIDTH
            )
            max_boost = int(SPEED_REACTION_MAX_BOOST_X * region_width / REFERENCE_WIDTH)
            jump_trigger_x = min(max_jump_trigger_x, jump_trigger_x + min(speed_boost, max_boost))

        dynamic_jump_cooldown = max(
            MIN_DYNAMIC_JUMP_COOLDOWN,
            JUMP_COOLDOWN - min(0.01, elapsed / 600),
        )
        # Dense cactus groups (e.g., triple cactus) need an earlier jump window.
        if cactus_hits >= TRIPLE_CACTUS_HITS_THRESHOLD:
            boost = int(EARLY_JUMP_BOOST_X * region_width / REFERENCE_WIDTH)
            jump_trigger_x = min(max_jump_trigger_x, jump_trigger_x + boost)

        cactus_visible = (
            cactus_hits >= 80
            and nearest_cactus_x is not None
            and nearest_cactus_x < int(region_width * 0.92)
        )
        bird_visible = (
            bird_hits >= 220
            and nearest_bird_x is not None
            and nearest_bird_x > int(region_width * 0.35)
            and nearest_bird_x < int(region_width * 0.92)
        )

        if keyboard.is_pressed(SAVE_FRAME_KEY):
            image.save(DEBUG_FRAME_PATH)
            print(f"Saved debug frame: {DEBUG_FRAME_PATH}")
            time.sleep(0.25)

        if now - last_debug_print >= DEBUG_PRINT_INTERVAL:
            print(
                "debug",
                f"bg={bg_color}",
                f"cactus_hits={cactus_hits}",
                f"nearest_cactus_x={nearest_cactus_x}",
                f"bird_hits={bird_hits}",
                f"nearest_bird_x={nearest_bird_x}",
                f"jump_trigger_x={jump_trigger_x}",
                f"region_width={region_width}",
            )
            last_debug_print = now

        if (
            cactus_visible
            and nearest_cactus_x <= jump_trigger_x
            and now - last_jump_time >= dynamic_jump_cooldown
        ):
            pyautogui.press(JUMP_KEY)
            last_jump_time = now
            time.sleep(0.01)
            continue

        should_followup_jump = (
            cactus_visible
            and nearest_cactus_x <= jump_trigger_x - FOLLOWUP_JUMP_CLOSE_X
            and now - last_jump_time >= FOLLOWUP_JUMP_DELAY
        )
        if should_followup_jump:
            pyautogui.press(JUMP_KEY)
            last_jump_time = now
            time.sleep(0.005)
            continue

        should_duck = (
            bird_visible
            and nearest_bird_x <= jump_trigger_x + 15
            and not cactus_visible
            and now - last_duck_time >= DUCK_COOLDOWN
        )

        if should_duck:
            pyautogui.keyDown(DUCK_KEY)
            time.sleep(DUCK_TIME)
            pyautogui.keyUp(DUCK_KEY)
            last_duck_time = now

        time.sleep(0.01)


if __name__ == "__main__":
    start()
