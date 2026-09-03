import pygame
from .render import Render, collide_point

class ToggleBox:
    """Pour cheat_mode / audio_enable : pas de curseur, juste ON/OFF."""
 
    def __init__(self, label, value, pos, font, color="#dedeff"):
        self.value = value
        self.font = font
        self.color = color
 
        label_surf = font.render(label, False, color)
        h = label_surf.get_height()
        self.static_surf = pygame.Surface((label_surf.get_width() + 60, h))
        self.static_surf.blit(label_surf, (0, 0))
 
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1],
                                 self.static_surf.get_width(), h)
        # zone cliquable pour toggler : à droite du label
        self.toggle_rect = pygame.Rect(
            pos[0] + label_surf.get_width() + 10, pos[1], 40, h)
 
    def flip(self):
        self.value = not self.value

    def draw_toggle_box(self, screen: pygame.Surface):
        screen.blit(self.static_surf, self.pos)
        text = "ON" if self.value else "OFF"
        color = "#7CFC00" if self.value else "#FF4444"
        value_surf = self.font.render(text, False, color)
        screen.blit(value_surf, self.toggle_rect.topleft)

class ParamBox:
    def __init__(self, label: str, min_val: int, max_val: int, value: int, pos, font,
                 track_w=120, track_h=8, color="#dedeff"):
        self.min_val, self.max_val, self.value = min_val, max_val, value
        self.font = font
        self.color = color
        self.handle_w = 6

        label_surf = font.render(label, False, color)
        min_surf = font.render(str(min_val), False, color)
        max_surf = font.render(str(max_val), False, color)

        static_h = max(label_surf.get_height(), min_surf.get_height() + track_h)
        static_w = label_surf.get_width() + 10 + track_w
        self.static_surf = pygame.Surface((static_w, static_h))

        label_rect = label_surf.get_rect(midleft=(0, static_h // 2))
        track_rect = pygame.Rect(label_rect.right + 10, static_h - track_h,
                                  track_w, track_h)
        min_rect = min_surf.get_rect(bottomleft=track_rect.topleft)
        max_rect = max_surf.get_rect(bottomright=track_rect.topright)

        self.static_surf.blit(label_surf, label_rect)
        self.static_surf.blit(min_surf, min_rect)
        self.static_surf.blit(max_surf, max_rect)
        pygame.draw.rect(self.static_surf, color, track_rect, 1)

        # rect/track en coordonnées ECRAN absolues : c'est ce qui sert
        # au clic (collide_point) et au calcul du curseur, pas les
        # coordonnées locales à static_surf
        self.rect = self.static_surf.get_rect(topleft=pos)
        self.track_rect = track_rect.move(pos)

    def ratio(self) -> float:
        return (self.value - self.min_val) / (self.max_val - self.min_val)

    def handle_rect(self) -> pygame.Rect:
        x = self.track_rect.x + int(
            self.ratio() * (self.track_rect.width - self.handle_w))
        return pygame.Rect(x, self.track_rect.y, self.handle_w,
                            self.track_rect.height)

    def set_value_from_mouse_x(self, mouse_x: int):
        ratio = (mouse_x - self.track_rect.x) / self.track_rect.width
        ratio = max(0.0, min(1.0, ratio))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)


def draw_param_box(screen: pygame.Surface, box: ParamBox):
    screen.blit(box.static_surf, box.rect)

    handle = box.handle_rect()
    pygame.draw.rect(screen, "#ffcc00", handle)

    value_surf = box.font.render(str(int(box.value)), False, "#ffcc00")
    value_rect = value_surf.get_rect(midbottom=handle.midtop)
    screen.blit(value_surf, value_rect)


class Menu:
    def __init__(self, render: Render) -> None:
        self.render = render
        self.w, self.h = self.render.screen.get_size()
#self.player2 = init_player(self, 1, self.args.lives)

    def param_menu(self, config: dict, clock, fps):
        clamps = {
            "width": (6, 33),
            "height": (6, 33),
            "lives": (1, 3),
            "seed": (0, 0xffff),
            "points_per_pacgum": (1, 100),
            "points_per_super_pacgum": (1, 500),
            "fps": (30, 60),
            "nb_player": (1, 2),
            "points_per_ghost": (1, 1600),
        }
        toggles = ("cheat_mode", "audio_enable")
        boxes, toggle_boxes = [], []
        y = 80
        i = 0
        for name, (min_v, max_v) in clamps.items():
            current = config.get(name, min_v)
            boxes.append(ParamBox(name, min_v, max_v, current,
                                (100, y), self.render.font))
            y += boxes[i].font.get_linesize() * 3
            i += 1
    
        for name in toggles:
            current = config.get(name, False)
            toggle_boxes.append(ToggleBox(name, current, (100, y), self.render.font))
            y += 40
    
        dragging = None
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for name, box in zip(clamps, boxes):
                        config[name] = int(box.value)
                    for name, tbox in zip(toggles, toggle_boxes):
                        config[name] = tbox.value
                    return config
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    for name, box in zip(clamps, boxes):
                        config[name] = int(box.value)
                    for name, tbox in zip(toggles, toggle_boxes):
                        config[name] = tbox.value
                    return config
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for box in boxes:
                        if collide_point(box.track_rect, mx, my):
                            dragging = box
                            box.set_value_from_mouse_x(mx)
                    for tbox in toggle_boxes:
                        if collide_point(tbox.toggle_rect, mx, my):
                            tbox.flip()
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging = None
                if event.type == pygame.MOUSEMOTION and dragging is not None:
                    dragging.set_value_from_mouse_x(event.pos[0])
    
            self.render.screen.fill(0)
            for box in boxes:
                draw_param_box(self.render.screen, box)
            for tbox in toggle_boxes:
                tbox.draw_toggle_box(self.render.screen)
    
            pygame.display.flip()
            clock.tick(fps)

    def main_menu(self, clock, fps):
        self.render.screen.fill(0)
        nb_btn = 4
        # size = ratio w/h 248px/1179px
        size = (int(self.w * 0.2), int(self.w * 0.2 * 248 / 1179))
        btns = [
            pygame.transform.smoothscale(
                pygame.image.load(f"images/buttons/btn{i}.png")
                .convert_alpha(), size) for i in range(nb_btn)
        ]
        bloc_size = size[1] * nb_btn * 2
        pad_w = (self.w - 0) // 2
        pad_h = (self.h - bloc_size) // 2
        btns_rect = [
            btn.get_rect(center=(pad_w, pad_h + size[1] * i * 2))
            for i, btn in enumerate(btns)
        ]
        play, param, quit, hg = btns_rect
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.run = False
                    return ""
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play.collidepoint(event.pos):
                            self.render.erase(btns_rect)
                            return "play"
                        elif quit.collidepoint(event.pos):
                            # self.run = False
                            return "quit"
                        elif param.collidepoint(event.pos):
                            return "param"
            self.render.hoover_opacity70(btns, btns_rect)
            self.render.draw_obj(btns, btns_rect)
            pygame.display.flip()
            clock.tick(fps)

    def pause_menu(self, clock, fps):
        self.render.screen.fill(0)
        nb_btn = 2
        # size = ratio w/h 248px/1179px
        size = (int(self.w * 0.2), int(self.w * 0.2 * 248 / 1179))
        btns = [
            pygame.transform.smoothscale(
                pygame.image.load(f"images/buttons/pause_btn{i}.png")
                .convert_alpha(), size) for i in range(nb_btn)
        ]
        bloc_size = size[1] * nb_btn * 2
        pad_w = (self.w - 0) // 2
        pad_h = (self.h - bloc_size) // 2
        btns_rect = [
            btn.get_rect(center=(pad_w, pad_h + size[1] * i * 2))
            for i, btn in enumerate(btns)
        ]
        back2menu, resume = btns_rect
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.run = False
                    return ""
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if resume.collidepoint(event.pos):
                            self.render.erase(btns_rect)
                            return "play"
                        elif back2menu.collidepoint(event.pos):
                            # self.run = False
                            return "start"
            self.render.hoover_opacity70(btns, btns_rect)
            self.render.draw_obj(btns, btns_rect)
            pygame.display.flip()
            clock.tick(fps)
