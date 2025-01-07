import pygame
import numpy as np

#Default colors for ease of programming
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (100, 65, 23)
GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)

#Sidebar elements
SIDEBAR_WIDTH = 200
SIDEBAR_COLOR = GRAY
BUTTON_COLOR = BLUE
SLIDER_COLOR = DARK_GRAY
SLIDER_BG_COLOR = WHITE

#initialize all GUI elements
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 24)

#Slider class to handle user interaction
class Slider:
    def __init__(self, label, value, x, y, min_val, max_val, step, parent):
        self.label = label
        self.value = value
        self.x = x
        self.y = y
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.slider_rect = pygame.Rect(x, y, 150, 10)
        self.handle_rect = pygame.Rect(x + (value - min_val) / (max_val - min_val) * 150 - 5, y - 5, 10, 20)
        self.is_dragging = False
        self.parent = parent
    def draw(self):
        pygame.draw.rect(self.parent, SLIDER_BG_COLOR, self.slider_rect)  # Slider background
        pygame.draw.rect(self.parent, SLIDER_COLOR, self.handle_rect)  # Slider handle
        # Draw the label and value
        label_text = font.render(f"{self.label}: {self.value:.2e}", True, BLACK)
        self.parent.blit(label_text, (self.x - 30, self.y - 20))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            mouse_x = event.pos[0]
            if self.slider_rect.collidepoint(mouse_x, self.y):
                new_value = self.min_val + (mouse_x - self.x) / 150 * (self.max_val - self.min_val)
                self.value = np.clip(new_value, self.min_val, self.max_val)
                self.handle_rect.x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * 150 - 5

def draw_sidebar(screen, height):
    pygame.draw.rect(screen, SIDEBAR_COLOR, (0, 0, SIDEBAR_WIDTH, height))
    
    # Title text
    title_text = font.render("Simulation Controls", True, BLACK)
    screen.blit(title_text, (20, 20))

#Button class to handle user interaction
class Button:
    def __init__(self, label, x, y, width, height, parent):
        self.label = label
        self.rect = pygame.Rect(x, y, width, height)
        self.parent = parent

    def draw(self):
        screen = self.parent
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)  # Button background
        button_text = font.render(self.label, True, WHITE)
        screen.blit(button_text, (self.rect.x + (self.rect.width - button_text.get_width()) // 2,
                                  self.rect.y + (self.rect.height - button_text.get_height()) // 2))

    def check_click(self, event, func):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            func()

#Nice vector graphics
def draw_vector(surface, origin, vector, color, scale=1, width=2):
    scaled_vector = scale * vector
    end = (origin[0] + scaled_vector[0], origin[1] + scaled_vector[1])
    pygame.draw.line(surface, color, origin, end, width)

    arrow_size = 10
    angle = np.arctan2(scaled_vector[1], scaled_vector[0])
    left = (end[0] - arrow_size * np.cos(angle - np.pi / 6),
            end[1] - arrow_size * np.sin(angle - np.pi / 6))
    right = (end[0] - arrow_size * np.cos(angle + np.pi / 6),
            end[1] - arrow_size * np.sin(angle + np.pi / 6))
    pygame.draw.line(surface, color, end, left, width)
    pygame.draw.line(surface, color, end, right, width)

                