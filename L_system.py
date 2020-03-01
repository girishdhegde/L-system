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


class fractal_tree(system):
 
    variables = '01'
    constants = '[]'
    start     = '0'

    def __init__(self, store_states=False, pos=(0, 0), ln=3):
        super().__init__(self.start, self.rules_fn, self.variables, self.constants, store_states)
        self.stack = []
        self.pos = pos
        self.theta = math.pi/2
        self.angle = math.pi/2
        self.ln = ln
        self.o_pos = pos
 
    @staticmethod
    def rules_fn(symbol):
        return list('11') if symbol == '1' else list('1[0]0')

    
    def draw(self, surf, symbol, clr=None):
        if clr:
            self.clr = clr
        if symbol in ['0', '1']:
            new = draw_line(surf, self.pos, self.angle, self.ln, self.clr)
            self.pos = new

        elif symbol == '[':
            self.stack.append([self.pos, self.angle])
            self.angle += math.pi / 4

        elif symbol == ']':
            self.pos, self.angle = self.stack.pop()
            self.angle -= math.pi / 4

class fractal_plant(system):
 
    variables = 'XF'
    constants = '+-[]'
    start     = 'X'

    def __init__(self, store_states=False, pos=(0, 0), ln=3):
        super().__init__(self.start, self.rules_fn, self.variables, self.constants, store_states)
        self.stack = []
        self.pos = pos
        self.theta = 25 * (math.pi / 180)
        self.angle = 45 * (math.pi / 180)
        self.ln = ln
        self.o_pos = pos

    @staticmethod 
    def rules_fn(symbol):
        return list('F+[[X]-X]-F[-FX]+X') if symbol == 'X' else list('FF')
    
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
        elif symbol == '[':
            self.stack.append([self.pos, self.angle])
        elif symbol == ']':
            self.pos, self.angle = self.stack.pop()

class sierpinski_triangle(system):

    variables = 'FG'
    constants = '+-'
    start     = 'F-G-G'

    def __init__(self, store_states=False, pos=(0, 0), ln=3):
        super().__init__(self.start, self.rules_fn, self.variables, self.constants, store_states)
        self.pos   = pos
        self.theta = 2 * math.pi / 3
        self.angle = 2 * math.pi / 3
        self.ln = ln
        self.o_pos = pos

    @staticmethod
    def rules_fn(symbol):
        return list('F-G+F+G-F') if symbol == 'F' else list('GG')

    def draw(self, surf, symbol, clr=None):
        if clr:
            self.clr = clr
        if symbol in ['F', 'G']:
            new = draw_line(surf, self.pos, self.angle, self.ln, self.clr)
            self.pos = new

        elif symbol == '+':
            self.angle += self.theta

        elif symbol == '-':
            self.angle -= self.theta


class  sierpinski_arrowhead_curve(system):

    variables = 'AB'
    constants = '+-'
    start     = 'A'

    def __init__(self, store_states=False, pos=(0, 0), ln=3):
        super().__init__(self.start, self.rules_fn, self.variables, self.constants, store_states)
        self.pos   = pos
        self.theta = math.pi / 3
        self.angle = math.pi / 3
        self.ln    = ln
        self.o_pos = pos

    @staticmethod
    def rules_fn(symbol):
        return list('B-A-B') if symbol == 'A' else list('A+B+A')

    def draw(self, surf, symbol, clr=None):
        if clr:
            self.clr = clr
        if symbol in ['A', 'B']:
            new = draw_line(surf, self.pos, self.angle, self.ln, self.clr)
            self.pos = new

        elif symbol == '+':
            self.angle += self.theta

        elif symbol == '-':
            self.angle -= self.theta

class  dragon_curve(system):

    variables = 'XY'
    constants = 'F+-'
    start     = 'FX'

    def __init__(self, store_states=False, pos=(0, 0), ln=3):
        super().__init__(self.start, self.rules_fn, self.variables, self.constants, store_states)
        self.pos   = pos
        self.theta = math.pi / 2
        self.angle = math.pi / 2
        self.ln = ln
        self.o_pos = pos

    @staticmethod
    def rules_fn(symbol):
        return list('X+YF+') if symbol == 'X' else '-FX-Y'

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


class  hilbert_curve(system):

    variables = 'AB'
    constants = 'F+-'
    start     = 'A'

    def __init__(self,store_states=False, pos=(0, 0), ln=3):
        super().__init__(self.start, self.rules_fn, self.variables, self.constants, store_states)
        self.pos   = pos
        self.theta = math.pi / 2
        self.angle = math.pi / 2
        self.ln = ln
        self.o_pos = pos
        self.hue = 0
        self.sign = 1

    @staticmethod
    def rules_fn(symbol):
        return list('-BF+AFA+FB-') if symbol == 'A' else '+AF-BFB-FA+'


    @staticmethod
    def hsv2rgb(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


    def draw(self, surf, symbol, clr=None):
        if symbol in ['F']:
            clr = self.hsv2rgb(self.hue/360.0, 1, 1)
            new = draw_line(surf, self.pos, self.angle, self.ln, clr)
            self.pos = new
            if self.hue > 358:
                self.sign *= -1
            self.hue += (self.sign * .021)

        elif symbol == '+':
            self.angle += self.theta

        elif symbol == '-':
            self.angle -= self.theta

def main():

    # #Algae
    # var = 'AB'
    # const = None
    # axiom = 'A'

    # def rules(symbol):
    #     return list('AB') if symbol == 'A' else 'A'

    # algae = system(axiom, rules, var, const, store_states=False)
    # alg_s = algae.generate(10)
    # print(alg_s)
    # print(list(map(len, alg_s)))

########################################################################
    #Fractal tree
    pos   = (600, 0)
    ln    = 3

    FT = fractal_tree(False, pos, ln)
    ftsq = FT.generate(8)
    # print(sq)

########################################################################
    #Fractal plant
    pos   = (200, 100)
    ln    = 3

    FP = fractal_plant(False, pos, ln)
    fpsq = FP.generate(7)
    # print(fpsq)

########################################################################

    # Sierpinski triangle
    ln    = 10
    pos   = (600, 160)

    ST    = sierpinski_triangle(False, pos, ln)
    stsq  = ST.generate(6)
    # print(stsq)


######################################################################

    #  Sierpiński arrowhead curve
    ln    = 3
    pos   = (600, 115)

    SAC   = sierpinski_arrowhead_curve(False, pos, ln)
    sacsq  = SAC.generate(8)
    # print(sacsq)


######################################################################

    #Dragon curve
    ln    = 5
    pos   = (330, 550)

    DC    = dragon_curve(False, pos, ln)
    dcsq  = DC.generate(14)
    # print(dcsq)

#####################################################################

    #Hilbert curve
    ln    = 4
    pos   = (350, 175)

    HC    = hilbert_curve(False, pos, ln)
    hcsq  = HC.generate(7)
    # print(dcsq)

#####################################################################






################################################################################################################################################################################################################
###############################################################################GRAPHICS#########################################################################################################################
    pg.init()

    width = 1500
    height = 800

    w = 1210
    h = 710


    fps = 144
    

    background = (0, 0, 0) #(r, g, b)
    anti_alias = False
    font_size = 15
    font = pg.font.Font(None, font_size)
    #setup
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('L-system')
    clock = pg.time.Clock()
    
    ft_surf = pg.Surface((w, h))
    ft_surf.fill(background)
    pg.draw.rect(ft_surf, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    FT.draw_surf = ft_surf
    FT.clr  = (0, 0, 0)
 
    fp_surf = pg.Surface((w, h))
    fp_surf.fill(background)
    pg.draw.rect(fp_surf, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    FP.draw_surf = fp_surf
    FP.clr  = (0, 255, 180)
    
    st_surf = pg.Surface((w, h))
    st_surf.fill(background)
    pg.draw.rect(st_surf, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    ST.draw_surf = st_surf
    ST.clr  = (255, 255, 0)

    sac_surf = pg.Surface((w, h))
    sac_surf.fill(background)
    pg.draw.rect(sac_surf, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    SAC.draw_surf = sac_surf
    SAC.clr  = (0, 0, 0)


    dc_surf = pg.Surface((w, h))
    dc_surf.fill(background)
    pg.draw.rect(dc_surf, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    DC.draw_surf = dc_surf
    DC.clr  = (255, 50, 255)

    hc_surf = pg.Surface((w, h))
    hc_surf.fill(background)
    pg.draw.rect(hc_surf, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    HC.draw_surf = hc_surf
    HC.clr  = (255, 0, 0)


    ###############################################################################
    temp = pg.Surface((w, h))
    temp.fill(background)
    pg.draw.rect(temp, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    FT.fill(temp, [255, 255, 255])

    temp = pg.Surface((w, h))
    temp.fill(background)
    pg.draw.rect(temp, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    FP.fill(temp, [0, 150, 0])

    temp = pg.Surface((w, h))
    temp.fill(background)
    pg.draw.rect(temp, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    ST.fill(temp, [255, 255, 0])

    temp = pg.Surface((w, h))
    temp.fill(background)
    pg.draw.rect(temp, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    SAC.fill(temp, [0, 255, 255])

    temp = pg.Surface((w, h))
    temp.fill(background)
    pg.draw.rect(temp, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    DC.fill(temp, [255, 50, 255])

    temp = pg.Surface((w, h))
    temp.fill(background)
    pg.draw.rect(temp, (0, 255, 255), [(0, 0), (1210, 710)], 15)
    HC.fill(temp, [255, 0, 0])
    ###############################################################################

    lsystems = [FT, FP, ST, SAC, DC, HC]
    names    = ['Fractal Tree', 'Fractal plant', 'Sierpinski triangle', 'Sierpinski arrowhead curve', 'DRAGON CURVE', 'HILBERT CURVE']


    # itr = pgo.Slider("iterations", 10, 14, 0, (500, 720), 800)
    # sliders = [itr]

    ftb = pgo.button((150, 150), (200, 50), (220, 220, 220), (0, 255, 255), change, 'Fractal tree')
    fpb = pgo.button((150, 210), (200, 50), (220, 220, 220), (0, 255, 255), change, 'Fractal plant')
    stb = pgo.button((150, 270), (200, 50), (220, 220, 220), (0, 255, 255), change, 'Sierpinski triangle')
    sab = pgo.button((150, 330), (200, 50), (220, 220, 220), (0, 255, 255), change, 'Sierpinski curve')
    dcb = pgo.button((150, 390), (200, 50), (220, 220, 220), (0, 255, 255), change, 'Dragon curve')
    hcb = pgo.button((150, 450), (200, 50), (220, 220, 220), (0, 255, 255), change, 'Hilbert curve')
    fsl = pgo.button((150, 550), (200, 50), (220, 220, 220), (0, 255, 255), fastslow, 'Skip/Draw')
    button_list = [ftb, fpb, stb, sab, dcb, hcb, fsl]
    change_buttons = [ftb, fpb, stb, sab, dcb, hcb]


    temp = [10, 0, 0, 0, 0, 0]
    
    for curve in lsystems:
        curve.angle = curve.theta
        curve.pos   = curve.o_pos
    crash = False
    cnt = 0
    l = len(DC.final) - 1
    step = False
    current   = DC
    nth = None
    old_nth = None
    cur_sys_name = names[-2]
    while not crash:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crash = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    crash = True

            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if event.button == 1:
                    nth = click(change_buttons)
                    step = click([fsl], step)

            #     for s in sliders:
            #         if s.button_rect.collidepoint(pos):
            #             s.hit = True

            # elif event.type == pg.MOUSEBUTTONUP:
            #     for s in sliders:
            #         s.hit = False

        # for idx, s in enumerate(sliders):
        #     if s.hit:
        #         temp[idx] = s.move()


        if nth != None and old_nth != nth:
            old_nth = nth
            current = lsystems[nth]
            cur_sys_name = names[nth]
            current.angle = current.theta
            current.pos   = current.o_pos
            current.draw_surf.fill((0, 0, 0))
            pg.draw.rect(current.draw_surf, (0, 255, 255), [(0, 0), (1210, 710)], 15)
            cnt = 0
            l = len(current.final) - 1


        screen.fill((255, 255, 0))

        if step:
            if cnt != l:
                current.draw(current.draw_surf, current.final[cnt], current.clr) 
                cnt += 1
            screen.blit(current.draw_surf, (290, 0))


        else:
            screen.blit(current.surf, (290, 0))

        # for s in sliders:
        #     s.draw(screen)


        for button in button_list:
            button.draw(screen)


        t = pgo.text(cur_sys_name, (900, 750), clr=[255, 0, 0], mid=True, font="Segoe Print", font_size=25)
        t.draw(screen)

        t = pgo.text('L-System', (150, 50), clr=[255, 0, 255], mid=True, font="Segoe Print", font_size=50)
        t.draw(screen)

        cur_fps = font.render(str(int(clock.get_fps())), anti_alias, (255, 0, 0))
        screen.blit(cur_fps, (10, 10))
        pg.display.update()
        clock.tick(fps)

    pg.quit()


#pygame button callback functions

def click(buttons, *args):
    pos = pg.mouse.get_pos()
    x = None
    flag = False
    for idx, button in enumerate(buttons):
        if button.rect.collidepoint(pos):
            flag = True
            x = button.call_back(idx, *args)
    if len(args) > 0 and not flag:
        x = args[0]    
    return x

def fastslow(i, flag):
    return False if flag == True else True

def change(i):
    return i

if __name__ == '__main__':

    main()