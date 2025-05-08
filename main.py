# importing Libraries
import pyvisgraph as vg
import pygame
from regex import P

# Initializing Pygame
pygame.init()

# Dimensions of the screen
display_width, display_height = 1280, 720
# KEYS
LEFT, RIGHT = 1, 3

# ---- COLORS ----
black = (0, 0, 0)
white = (175, 175, 175)  # light grey
red = (223, 17, 17)
gray = (169, 169, 169)
green = (0, 128, 0)
yellow = (204, 204, 0)
blue = (28, 84, 239)


# ----------------------
# ---- INITIALIZING ----
# ----------------------
Display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Path Finder")
clock = pygame.time.Clock()

# ----------------------
# ---- DRAWING MODE ----
# ----------------------
def HelpScreen():
    rectw = 550
    recth = 500
    rectwi = rectw - 10
    recthi = recth - 10
    startx = display_width * 0.5 - rectw / 2
    starty = display_height * 0.5 - recth / 2
    startxi = display_width * 0.5 - rectwi / 2
    startyi = display_height * 0.5 - recthi / 2
    helping = True
    while helping:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_h:
                    helping = False

        pygame.draw.rect(Display, blue, (startx, starty, rectw, recth))
        pygame.draw.rect(Display, yellow, (startxi, startyi, rectwi, recthi))
        DrawText(
            ">>- PATH FINDER -<<",
            red,
            30,
            startxi + 180,
            startyi + 20,
        )
        DrawText(
            "Press Keys to Perform Operations", black, 25, startxi + 10, startyi + 50
        )
        DrawText(">H - START DRAWING POLYGON", black, 25, startxi + 10, startyi + 200)
        DrawText(">C - CLEAR", black, 25, startxi + 10, startyi + 250)
        DrawText(">S - START & FINISH", black, 25, startxi + 10, startyi + 300)
        DrawText(">Q - QUIT", red, 25, startxi + 10, startyi + 350)
        pygame.display.update()
        clock.tick(10)


# ----------------------
# ---- DRAWING MODE ----
# ----------------------
def DrawPolygon(polygon, color, size, complete=True):
    if complete:
        polygon.append(polygon[0])
    p1 = polygon[0]
    for p2 in polygon[1:]:
        pygame.draw.line(Display, color, (p1.x, p1.y), (p2.x, p2.y), size)
        p1 = p2


def DrawVertices(edges, color, size):
    for edge in edges:
        pygame.draw.line(
            Display, color, (edge.p1.x, edge.p1.y), (edge.p2.x, edge.p2.y), size
        )


def DrawText(mode_txt, color, size, x, y):
    font = pygame.font.SysFont(None, size)
    text = font.render(mode_txt, True, color)
    Display.blit(text, (x, y))


class Simulator:
    def __init__(self):
        self.polygons = []
        self.work_polygon = []
        self.mouse_point = None
        self.start_point = None
        self.end_point = None
        self.shortest_path = []

        self.g = vg.VisGraph()
        self.built = False
        self.mode_draw = True
        self.mode_path = False

    def drawing_mode(self):
        self.mode_draw = not self.mode_draw
        self._clear_shortest_path()
        self.mode_path = False

    def close_polygon(self):
        if len(self.work_polygon) > 1:
            self.polygons.append(self.work_polygon)
            self.work_polygon = []
            self.g.build(self.polygons, status=False)
            self.built = True

    def shortest_path_mode(self):
        if self.mode_path:
            self._clear_shortest_path()
        self.mode_path = not self.mode_path
        self.mode_draw = False

    def clear_all(self):
        self.__init__()

    def _clear_shortest_path(self):
        self.shortest_path = []
        self.start_point = []
        self.end_point = []


def game_loop():
    simulator = Simulator()
    status = False
    while not status:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_h:
                    HelpScreen()
                elif event.key == pygame.K_d:
                    simulator.drawing_mode()
                elif event.key == pygame.K_s:
                    simulator.shortest_path_mode()

            if simulator.mode_draw:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_c:
                        simulator.clear_all()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == LEFT:
                        simulator.work_polygon.append(vg.Point(pos[0], pos[1]))
                    elif event.button == RIGHT:
                        simulator.close_polygon()

            if simulator.mode_path and simulator.built:
                if event.type == pygame.MOUSEBUTTONUP or any(
                    pygame.mouse.get_pressed()
                ):
                    if pygame.mouse.get_pressed()[LEFT - 1] or event.button == LEFT:
                        simulator.start_point = vg.Point(pos[0], pos[1])
                    elif pygame.mouse.get_pressed()[RIGHT - 1] or event.button == RIGHT:
                        simulator.end_point = vg.Point(pos[0], pos[1])
                    if simulator.start_point and simulator.end_point:
                        simulator.shortest_path = simulator.g.shortest_path(
                            simulator.start_point, simulator.end_point
                        )

        Display.fill(white)

        if len(simulator.work_polygon) > 1:
            DrawPolygon(simulator.work_polygon, black, 3, complete=False)

        if len(simulator.polygons) > 0:
            for polygon in simulator.polygons:
                DrawPolygon(polygon, black, 3)
        if len(simulator.shortest_path) > 1:
            DrawPolygon(simulator.shortest_path, red, 3, complete=False)

        if simulator.mode_draw:
            DrawText("DRAWING MODE", black, 25, 5, 5)
        elif simulator.mode_path:
            DrawText("DRAW PATH", black, 25, 5, 5)
        else:
            DrawText("HELP", black, 25, 5, 5)

        pygame.display.update()
        clock.tick(20)


# Driver Code

Display.fill(white)
HelpScreen()
game_loop()
pygame.quit()
quit()
