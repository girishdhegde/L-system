import pygame

class button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None, text='', font="Segoe Print", font_size=16, font_clr=[0, 0, 0]):
        self.clr    = clr
        self.size   = size
        self.func   = func
        self.surf   = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            return self.func(*args)

class text:
    def __init__(self, msg, position, clr=[100, 100, 100], font=None, font_size=15, mid=False):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, 1, clr)

        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])

        if mid:
            self.position = self.txt_surf.get_rect(center=position)


    def draw(self, screen):
        screen.blit(self.txt_surf, self.position)


class Slider():

    pygame.init()
    font_size = 15
    font = pygame.font.Font(None, font_size)

    def __init__(self, name, val, maxi, mini, pos, size=100):
        self.val = val
        self.maxi = maxi  
        self.mini = mini  
        self.xpos = pos[0] 
        self.ypos = pos[1]
        self.surf = pygame.Surface((size, 50))
        self.hit = False  
        self.size = (size, 50)
        self.txt_surf = self.font.render(name, 1, (0, 0, 0))
        self.txt_rect = self.txt_surf.get_rect(center=(self.size[0]//2, 15))

        self.surf.fill((255, 255, 255))
        pygame.draw.rect(self.surf, (100, 255, 0), [0, self.size[1] - 20, self.size[0], 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)  

        self.button_surf = pygame.Surface((20, 20))
        self.button_surf.fill((1, 1, 1))
        self.button_surf.set_colorkey((1, 1, 1))
        pygame.draw.circle(self.button_surf, (0, 0, 0), (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, (255, 0, 255), (10, 10), 4, 0)

    def draw(self, screen):
        surf = self.surf.copy()

        pos = (int((self.val-self.mini)/(self.maxi-self.mini)*self.size[0]), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)

        screen.blit(surf, (self.xpos, self.ypos))

    def move(self, value=None):
        if value != None:
            self.val = value
        else:   
            self.val = (pygame.mouse.get_pos()[0] - self.xpos) / self.size[0] * (self.maxi - self.mini) + self.mini
            if self.val < self.mini:
                self.val = self.mini
            if self.val > self.maxi:
                self.val = self.maxi
        return self.val



def click(buttons):
    pos = pygame.mouse.get_pos()
    for idx, button in enumerate(buttons):
        if button.rect.collidepoint(pos):
            button.call_back(idx)

