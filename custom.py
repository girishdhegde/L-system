import math
import pygame as pg 
import pygame_objects as pgo
import numpy as np 
import colorsys


class system:
    def __init__(self, axiom, rules_fn, var, const=None, store_states=False):
        self.variables  = var
        self.axiom      = axiom
        self.rules      = rules_fn
        self.seq        = None
        self.store      = store_states

        if const:
            self.constants = list(const)
        else:
            self.constants = []

    def generate(self, iterations):
        if self.store:
            self.seq = []
            self.seq.append(self.axiom)

        prev = list(self.axiom).copy()
        for i in range(1, iterations+1):
            nxt = []
            for pos, symbol in enumerate(prev):
                if symbol in self.constants:
                    nxt.append(symbol)
                else:                
                    nxt.extend(self.rules(symbol))
            prev = nxt.copy()

            if self.store:
                self.seq.append(''.join(prev))
        
        if not self.store:
            self.seq = ''.join(prev)
            self.final = self.seq
        
        else:
            self.final = self.seq[-1]

        return self.seq

    def fill(self, surf, clr=(255,255, 255)):
        self.clr = clr
        for symb in self.final:
            self.draw(surf, symb)
        self.surf = surf

    
def draw_line(surf, pos, angle=0, l=100, clr=(0, 0, 0), yl=800):
    x2 = pos[0] + l * math.cos(angle)
    y2 = pos[1] + l * math.sin(angle)
    pg.draw.line(surf, clr, [pos[0], yl - pos[1]], (x2, yl - y2), 1)
    return x2, y2

class koch_curve(system):

    variables = 'F'
    constants = '+-'
    start     = 'F--F--F'
    def __init__(self, store_states=False, pos=(0, 0), ln=3):
        super().__init__(self.start, self.rules_fn, self.variables, self.constants, store_states=False)
        self.pos   = pos
        self.theta = math.pi / 3
        self.angle = math.pi / 3
        self.ln = ln
        self.o_pos = pos

    @staticmethod
    def rules_fn(symbol):
        return list('F+F--F+F') if symbol == 'F' else ''

    def draw(self, surf, symbol, clr=None):
        if clr:
            self.clr = clr
        if symbol in ['F']:
            new = draw_line(surf, self.pos, self.angle, self.ln, self.clr)
            self.pos = new

        elif symbol == '+':
            self.angle += self.theta

        elif symbol == '-':
            self.angle -= self.theta



def main():


    #Koch snowflake
    pos   = (650, 380)
    ln    = 1

    KC = koch_curve(False, pos, ln)
    kcsq = KC.generate(5)
    # print(kcsq)



################################################################################################################################################################################################################
###############################################################################GRAPHICS#########################################################################################################################
    pg.init()

    width = 1500
    height = 800

    fps = 144
    

    background = (0, 0, 0) #(r, g, b)
    anti_alias = False
    font_size = 15
    font = pg.font.Font(None, font_size)
    #setup
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('Koch snowflake')
    clock = pg.time.Clock()
    
    kc_surf = pg.Surface((width, height))
    kc_surf.fill(background)
    KC.fill(kc_surf, clr=(255, 120, 0))
 
    ###############################################################################
    crash = False
    while not crash:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crash = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    crash = True

        screen.fill((255, 255, 0))
        screen.blit(KC.surf, (0, 0))

        cur_fps = font.render(str(int(clock.get_fps())), anti_alias, (255, 0, 0))
        screen.blit(cur_fps, (10, 10))
        pg.display.update()
        clock.tick(fps)

    pg.quit()

if __name__ == '__main__':

    main()