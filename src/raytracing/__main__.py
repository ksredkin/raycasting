import math
import pygame

MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Player:
    def __init__(self, x: int, y: int, fov: int = 60, angle: float = 0.0, speed: float = 0.01) -> None:
        self.x = x
        self.y = y
        self.fov = fov
        self.speed = speed
        self._angle = angle

    def set_angle(self, angle: int) -> None:
        self._angle = math.radians(angle if angle < 359 else 0)

    def angle(self, angle: int) -> None:
        self._angle = (self._angle + math.radians(angle if angle < 359 else 0)) % math.radians(360)

    def _check_and_move(self, future_x: int, future_y: int) -> None:
        map_x = int(future_x)
        map_y = int(future_y)
        
        if (future_x <= 0) or (future_x >= len(MAP[0])) or (future_y <= 0) or (future_y >= len(MAP)):
            return
                                        
        if not (MAP[map_y][map_x] == 1):
            self.x = future_x
            self.y = future_y

    def move_forward(self) -> None:
        future_x = self.x + (math.cos(self._angle) * self.speed)
        future_y = self.y + (math.sin(self._angle) * self.speed)

        self._check_and_move(future_x, future_y)

    def move_backward(self) -> None:
        future_x = self.x - (math.cos(self._angle) * self.speed)
        future_y = self.y - (math.sin(self._angle) * self.speed)
        
        self._check_and_move(future_x, future_y)

    def move_left(self) -> None:
        future_x = self.x + (math.sin(self._angle) * self.speed)
        future_y = self.y - (math.cos(self._angle) * self.speed)
            
        self._check_and_move(future_x, future_y)

    def move_right(self) -> None:
        future_x = self.x - (math.sin(self._angle) * self.speed)
        future_y = self.y + (math.cos(self._angle) * self.speed)
                
        self._check_and_move(future_x, future_y)
    

class Ray:
    RAY_STEP = 0.1

    def __init__(self, x: int, y: int, angle: float) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.walled = False
        self.mimo = False
        self.steps = 0

    def move_forward(self) -> None:
        self.steps += 1
        
        self.x += math.cos(self.angle) * self.RAY_STEP
        self.y += math.sin(self.angle) * self.RAY_STEP
        
        map_x = int(self.x)
        map_y = int(self.y)

        if ((self.x <= 0) or (self.x >= len(MAP[0])) or (self.y <= 0) or (self.y >= len(MAP))):
            self.mimo = True
        elif (MAP[map_y][map_x] == 1):
            self.walled = True

COLOR_SHADE = 0.97

GROUND_COLOR = (139, 69, 19)
SKY_COLOR = (70, 130, 180)

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
            self.player.angle(-1)
        if keys[pygame.K_RIGHT]:
            self.player.angle(1)

def main():
    pygame.init()
    
    window_size = (800, 600)

    is_fullscreen = False

    player = Player(1, 1, 90)

    controller = Controller(player)

    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    pygame.display.set_caption("Raytracing")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                window_size = (event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

        keys = pygame.key.get_pressed()
        controller.check(keys)

        screen_width, screen_height = screen.get_size()
        pygame.draw.rect(screen, SKY_COLOR, (0, 0, screen_width, screen_height), width=0)
        pygame.draw.rect(screen, GROUND_COLOR, (0, screen_height/2, screen_width, screen_height), width=0)

        half_fov = int(player.fov / 2)
        ray_count = half_fov * 2
        
        for column, offset in enumerate(range(-half_fov, half_fov)):
            fov_angle = player._angle + math.radians(offset)
            ray = Ray(x=player.x, y=player.y, angle=fov_angle)

            while (not ray.walled) and (not ray.mimo):
                ray.move_forward()
            
            if not ray.mimo:
                focal_length = screen_width / (
                    2 * math.tan(math.radians(player.fov / 2))
                )

                ray_distance = ray.steps * ray.RAY_STEP

                corrected_distance = ray_distance * math.cos(
                    math.radians(offset)
                )

                rect_height = focal_length / max(corrected_distance, 0.001)

                rect_color = [255, 255, 0]
                for _ in range(ray.steps-1):
                    for col in range(len(rect_color)):
                        rect_color[col] = rect_color[col]*COLOR_SHADE

                rect_top = (screen_height - rect_height)/2

                rect_start = column*screen_width//ray_count
                rect_end = (column+1)*screen_width//ray_count

                pygame.draw.rect(screen, rect_color, (rect_start, rect_top, rect_end-rect_start, rect_height), width=0)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
