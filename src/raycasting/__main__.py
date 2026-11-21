import math

import pygame

RAW_MAP = [
    "################",
    "#......#.......#",
    "#.####.#.#####.#",
    "#.#....#.....#.#",
    "#.#.######.#.#.#",
    "#..........#...#",
    "###.####.#####.#",
    "#........#.....#",
    "#.###..#...#.#.#",
    "#...#........#.#",
    "###.#..#...#.#.#",
    "#......#.......#",
    "#.######.#####.#",
    "#.#..........#.#",
    "#...######.....#",
    "################",
]

MAP = [[1 if cell == "#" else 0 for cell in row] for row in RAW_MAP]

WINDOW_START_SIZE = (800, 600)
WINDOW_TITLE = "Raycasting"

GROUND_COLOR = (139, 69, 19)
SKY_COLOR = (70, 130, 180)
WALL_COLOR = (255, 255, 0)

FPS = 60
PLAYER_SPEED = 1
PLAYER_ANGLE_SPEED = 90
VIEW_DISTANCE = 100


class Player:
    def __init__(
        self,
        x: float = 1.5,
        y: float = 1.5,
        fov: int = 60,
        angle: float = 0.0,
        speed: float = 1.0,
        angle_speed: float = 1.0,
    ) -> None:
        self.x = x
        self.y = y
        self.fov = fov
        self.speed = speed
        self.angle_speed = angle_speed
        self.angle = angle

    def set_angle(self, angle: int) -> None:
        self.angle = math.radians(angle if angle < 359 else 0)

    def rotate(self, direction: int) -> None:
        self.angle = (
            self.angle + math.radians(self.angle_speed / FPS) * direction
        ) % math.radians(360)

    def _can_move_to(self, future_x: float, future_y: float) -> bool:
        map_x = int(future_x)
        map_y = int(future_y)

        if (
            (future_x <= 0)
            or (future_x >= len(MAP[0]))
            or (future_y <= 0)
            or (future_y >= len(MAP))
        ):
            return False

        return MAP[map_y][map_x] != 1

    def _move(self, angle_offset: float) -> None:
        move_angle = self.angle + angle_offset

        future_x = self.x + math.cos(move_angle) * (self.speed / FPS)
        future_y = self.y + math.sin(move_angle) * (self.speed / FPS)

        if self._can_move_to(future_x, future_y):
            self.x = future_x
            self.y = future_y

    def move_forward(self) -> None:
        self._move(0)

    def move_backward(self) -> None:
        self._move(math.pi)

    def move_left(self) -> None:
        self._move(-math.pi / 2)

    def move_right(self) -> None:
        self._move(math.pi / 2)


class Controller:
    def __init__(self, player: Player) -> None:
        self.player = player

    def check(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_w]:
            self.player.move_forward()
        if keys[pygame.K_s]:
            self.player.move_backward()
        if keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_LEFT]:
            self.player.rotate(-1)
        if keys[pygame.K_RIGHT]:
            self.player.rotate(1)


def render_scene(screen: pygame.Surface, player: Player) -> None:
    screen_width, screen_height = screen.get_size()
    pygame.draw.rect(
        screen, SKY_COLOR, (0, 0, screen_width, screen_height / 2), width=0
    )
    pygame.draw.rect(
        screen,
        GROUND_COLOR,
        (0, screen_height / 2, screen_width, screen_height / 2),
        width=0,
    )

    ray_count = screen_width

    focal_length = screen_width / (2 * math.tan(math.radians(player.fov / 2)))

    for column in range(ray_count):
        camera_x = 2 * column / ray_count - 1
        offset = math.degrees(
            math.atan(camera_x * math.tan(math.radians(player.fov / 2)))
        )
        fov_angle = player.angle + math.radians(offset)

        dir_x = math.cos(fov_angle)
        dir_y = math.sin(fov_angle)

        map_x = int(player.x)
        map_y = int(player.y)

        delta_dist_x = abs(1 / dir_x) if abs(dir_x) > 1e-10 else 1e30
        delta_dist_y = abs(1 / dir_y) if abs(dir_y) > 1e-10 else 1e30

        step_x = 1 if dir_x > 0 else -1
        side_dist_x = (
            ((map_x + 1 - player.x) * delta_dist_x)
            if dir_x > 0
            else ((player.x - map_x) * delta_dist_x)
        )

        step_y = 1 if dir_y > 0 else -1
        side_dist_y = (
            ((map_y + 1 - player.y) * delta_dist_y)
            if dir_y > 0
            else ((player.y - map_y) * delta_dist_y)
        )

        side = 0
        hit = False

        for _ in range(VIEW_DISTANCE):
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if not (0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0])):
                break

            if MAP[map_y][map_x] == 1:
                hit = True
                break

        if hit:
            ray_distance = (
                ((side_dist_y - delta_dist_y) * 1)
                if side
                else ((side_dist_x - delta_dist_x) * 1)
            )

            corrected_distance = ray_distance * math.cos(math.radians(offset))

            rect_height = focal_length / max(corrected_distance, 0.001)

            shade = 1 / (1 + ray_distance**2 * 0.02)
            rect_color = [int(i * shade) for i in WALL_COLOR]

            rect_top = (screen_height - rect_height) / 2

            rect_start = column * screen_width // ray_count
            rect_end = (column + 1) * screen_width // ray_count

            pygame.draw.rect(
                screen,
                rect_color,
                (rect_start, rect_top, rect_end - rect_start, rect_height),
                width=0,
            )


def main() -> None:
    pygame.init()

    window_size = WINDOW_START_SIZE
    is_fullscreen = False

    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    player = Player(8.5, 8.5, 90, speed=PLAYER_SPEED, angle_speed=PLAYER_ANGLE_SPEED)
    controller = Controller(player)

    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.VIDEORESIZE:
                    if not is_fullscreen:
                        window_size = (event.w, event.h)
                case pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        is_fullscreen = not is_fullscreen
                        if is_fullscreen:
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(
                                window_size, pygame.RESIZABLE
                            )

        controller.check(pygame.key.get_pressed())
        render_scene(screen, player)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
