import pygame
from .render import Render


class Menu:
    def __init__(self, render: Render) -> None:
        self.render = render
        self.w, self.h = self.render.screen.get_size()

    def main_menu(self):
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

    def pause_menu(self):
        self.render.screen.fill(0)
        size = (int(self.w * 0.2), int(self.w * 0.2 * 248 / 1179))
        btns = [
            pygame.transform.smoothscale(
                pygame.image.load(f"images/buttons/btn{i}.png")
                .convert_alpha(), size) for i in range(3)
        ]
        btn_w, btn_h = btns[0].get_size()
        bloc_size = btn_h * 6
        pad_w = (self.w - 0) // 2
        pad_h = (self.h - bloc_size) // 2
        play = btns[0].get_rect(center=(pad_w, pad_h))
        param = btns[1].get_rect(center=(pad_w, pad_h + btn_h * 2))
        quit = btns[2].get_rect(center=(pad_w, pad_h + btn_h * 4))
        btns_rect = [play, param, quit]
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
