import pygame
from .render import Render, collide_point

class ToggleBox:
    def __init__(self, string, size, boolean):
        self.name = string
        self.font = pygame.font.Font("font/press_start_2p.ttf", size)
        self.text = self.font.render(string, False, "#dedeff")
        self.bool_val = boolean
        self.bool = self.font.render("ON" if boolean else "OFF",
                                      False,
                                    "#0ec43c" if boolean else "#ff0000")
        self.t_size_w, self.t_size_h = self.text.get_size()
        self.b_size_w, self.b_size_h = self.bool.get_size()
        self.surf = pygame.Surface((self.t_size_w + self.b_size_w + 10, self.t_size_h))
        self.draw_box()

    def flip(self):
        self.bool_val = not self.bool_val
        self.bool = self.font.render(
            "ON" if self.bool_val else "OFF",
            False, "#0ec43c" if self.bool_val else "#ff0000")
        self.b_size_w, self.b_size_h = self.bool.get_size()

    def draw_box(self):
        self.surf.fill(0)
        self.surf.blit(self.text, (0 , 0))
        self.surf.blit(self.bool, (self.t_size_w + 10, 0))

class ParamBox:
    def __init__(self, string, size, min_v, max_v, range_size, value):
        self.name = string
        self.font = pygame.font.Font("font/press_start_2p.ttf", size)
        self.text = self.font.render(string, False, "#dedeff")
        self.font_val = self.font.render(str(value), False, "#181713")
        self.value = value
        self.t_size_w, self.t_size_h = self.text.get_size()
        self.surf = pygame.Surface((self.t_size_w + range_size + 10, self.t_size_h))
        self.range_val = max_v - min_v
        self.min = min_v
        self.max = max_v
        self.percent = (value - min_v) / self.range_val
        self.range = pygame.Surface((range_size, self.t_size_h))
        self.range.fill("#3B1D8B")
        self.range_box = pygame.Surface((range_size, self.t_size_h))
        self.range_box.fill("#dee7de")
        self.draw_box(range_size)
        self.pad_w = self.surf.get_size()[0] // 2

    def draw_box(self, range_size):
        percent = self.percent
        self.range_box.fill("#dee7de")
        self.range_box.blit(self.range, (-int(range_size * (1 - percent)) , 0))
        self.surf.blit(self.range_box, (self.t_size_w + 10 , 0))
        self.surf.blit(self.text, (0, 0))
        rect = self.font_val.get_rect(midtop=(self.t_size_w + 10 + range_size // 2, 0))
        self.surf.blit(self.font_val, rect)

class RangeBox(ParamBox):
    def __init__(self, string, size, min_v, max_v, range_size, value):
        super().__init__(string, size, min_v, max_v, range_size, value)

class Menu:
    def __init__(self, render: Render) -> None:
        self.render = render
        self.w, self.h = self.render.screen.get_size()


    def param_menu(self, config: dict, clock, fps):
        clamps = {
            "width": (6, 33),
            "height": (6, 33),
            "lives": (1, 3),
            "seed": (0, 0xffff),
            "points_per_pacgum": (1, 100),
            "points_per_super_pacgum": (1, 500),
            "fps": (30, 60),
            "points_per_ghost": (1, 1600),
            "nb_player": (1, 2)
        }
        self.render.screen.fill(0)
        toggles = ("cheat_mode", "audio_enable")
        boxes, toggle_boxes = [], []
        nb_boxes = len(clamps.keys()) + len(toggles)
        font_size = self.h // (nb_boxes * 4 + 2)
        range_size = self.render.screen.get_size()[0] // 10
        for toggle in toggles:
            toggle_boxes.append(ToggleBox(toggle, font_size, False))
        for name, (min_v, max_v) in clamps.items():
            current = config.get(name, min_v)
            boxes.append(RangeBox(name, font_size, min_v, max_v, range_size, current))
        pad_w = self.render.screen.get_rect().centerx
        pad_h = (self.render.screen.get_size()[1] - font_size * nb_boxes * 2) // 2
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return config
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    for key, val in config.items():
                        for box in boxes:
                            if box.name == key:
                                config[key] = box.value
                        for tog in toggle_boxes:
                            if tog.name == key:
                                config[key] = tog.bool_val
                    return config
                if pygame.mouse.get_pressed()[0]:
                    mx, my = pygame.mouse.get_pos()
                    j = 0
                    for box in boxes:
                        rect = box.surf.get_rect(center=((pad_w, j * (font_size * 2) + pad_h)))
                        rect.x += (box.text.get_size()[0] + 10)
                        r_box = box.range_box.get_rect()
                        r_box.x += rect.x
                        r_box.y += rect.y
                        if collide_point(r_box, mx, my):
                            len2left_edge = mx - r_box.x
                            box.percent = len2left_edge / range_size
                            val = round(box.range_val * box.percent)
                            val += box.min
                            box.value = val
                            box.font_val = box.font.render(str(val), False, "#181713")
                            box.draw_box(range_size)
                        j += 1
                    for tog in toggle_boxes:
                        rect = tog.surf.get_rect(center=((pad_w, j * (font_size * 2) + pad_h)))
                        rect.x += (tog.text.get_size()[0] + 10)
                        r_bool = tog.bool.get_rect()
                        r_bool.x += rect.x
                        r_bool.y += rect.y
                        j += 1
                        if collide_point(r_bool, mx, my):
                            tog.flip()
                            tog.draw_box()
            i = 0
            for box in (boxes):
                rect = box.surf.get_rect(center=((pad_w, i * (font_size * 2) + pad_h)))
                self.render.screen.blit(box.surf, rect)
                i += 1
            for tog in (toggle_boxes):
                rect = tog.surf.get_rect(center=((pad_w, i * (font_size * 2) + pad_h)))
                self.render.screen.blit(tog.surf, rect)
                i += 1
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
        play, param, hg, quit = btns_rect
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.run = False
                    return "start"
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
                    return "start"
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
