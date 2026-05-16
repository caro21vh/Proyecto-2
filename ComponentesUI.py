"""
ComponentesUI.py — Widgets reutilizables y helpers de dibujo.
Contiene: Button, InputField y las funciones de dibujo genéricas.
Importa de Constantes para colores y fuentes.
"""

import pygame
import Constantes as C


# Dibujos

def draw_rounded_rect(surface, color, rect, radius=12, border=0, border_color=None):
    """Rect con esquinas redondeadas y borde opcional."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, width=border, border_radius=radius)


def render_text_centered(surface, font, text, color, rect):
    """Texto centrado dentro de un Rect."""
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=rect.center))


def clip_text(font, text, max_width):
    """Corta el texto con '…' si supera max_width px."""
    if font.size(text)[0] <= max_width:
        return text
    while len(text) > 1 and font.size(text + "…")[0] > max_width:
        text = text[:-1]
    return text + "…"


def draw_header(surface, title, subtitle=""):
    """Barra superior azul oscuro con título y subtítulo."""
    pygame.draw.rect(surface, C.BLUE_DARK, (0, 0, C.WIDTH, 65))
    logo = C.TITLE_FONT.render("LinProd", True, C.WHITE)
    surface.blit(logo, (30, 16))
    sep = C.HEAD_FONT.render("  |  " + title, True, (180, 200, 255))
    surface.blit(sep, (30 + logo.get_width(), 20))
    if subtitle:
        sub = C.SMALL_FONT.render(subtitle, True, (160, 180, 230))
        surface.blit(sub, (30 + logo.get_width() + sep.get_width() + 10, 26))


# Botón

class Button:
    def __init__(self, x, y, width, height, text,
                 color=None, text_color=None, radius=10, font=None, icon=None):
        self.rect   = pygame.Rect(x, y, width, height)
        self.text   = text
        self.color  = color      if color      else C.BLUE
        self.tcolor = text_color if text_color else C.WHITE
        self.radius = radius
        self.font   = font if font else C.SMALL_FONT
        self.icon   = icon

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color   = tuple(min(v + 25, 255) for v in self.color) if hovered else self.color
        draw_rounded_rect(surface, color, self.rect, self.radius)

        txt_surf = self.font.render(self.text, True, self.tcolor)
        if self.icon:
            icon_surf = self.font.render(self.icon, True, self.tcolor)
            total_w   = icon_surf.get_width() + 6 + txt_surf.get_width()
            ix = self.rect.centerx - total_w // 2
            iy = self.rect.centery - icon_surf.get_height() // 2
            surface.blit(icon_surf, (ix, iy))
            surface.blit(txt_surf,  (ix + icon_surf.get_width() + 6, iy))
        else:
            surface.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# Input Field

class InputField:
    def __init__(self, x, y, width, height, value="", max_len=25, font=None):
        self.rect    = pygame.Rect(x, y, width, height)
        self.value   = value
        self.active  = False
        self.max_len = max_len
        self.font    = font if font else C.TEXT_FONT

    def draw(self, surface):
        border_color = C.BLUE if self.active else C.LIGHT
        draw_rounded_rect(surface, C.WHITE, self.rect, 8, 2, border_color)
        txt  = clip_text(self.font, self.value, self.rect.width - 12)
        surf = self.font.render(txt, True, C.BLACK)
        surface.blit(surf, (
            self.rect.x + 8,
            self.rect.y + (self.rect.height - surf.get_height()) // 2,
        ))
        if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cx = self.rect.x + 8 + self.font.size(txt)[0] + 2
            pygame.draw.line(surface, C.BLACK,
                             (cx, self.rect.y + 6),
                             (cx, self.rect.bottom - 6), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE):
                if len(self.value) < self.max_len:
                    self.value += event.unicode
        return self.active