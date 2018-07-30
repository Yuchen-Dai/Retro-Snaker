
import pygame, copy
import machanics as mc


class Gui:

    def __init__(self):
        self._running = True
        self.fps = 60
        self._load_images()
        
        self.lm = False
        self.um = False
        self.rm = False
        self.dm = False

    def run(self):
        pygame.init()
        self._resize_surface((600,600))
        self._restart()
        clock = pygame.time.Clock()

        while self._running:
            clock.tick(self.fps)
            try:
                self._handle_events()
                self.gamestate.move_snake(1/self.fps)
                self._change_dirc()
                self._check_collide()
                self._redraw()
            except mc.GameOverError:
                pass
        pygame.quit()

    def _redraw(self):
        surface = pygame.display.get_surface()

        surface.fill((255,255,255))
        self._draw_board()

        pygame.display.flip()

    def _draw_board(self):
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()


        fracw, frach = self.gamestate.get_pos()
        angle = self.gamestate.get_snake_angle()
        posw = fracw * width - 15
        posh = frach * height - 15

        rsnake = pygame.transform.rotate(self.images['snake'], -angle)
        record = Block(self.images['snake'])
        record.update_pos(posw, posh)
        record.image = rsnake
        
        self.records[str(self.count)] = record
        self.count += 1
        
        self.body.empty()
        body_length = self.gamestate.get_length()
        for i in range(1, body_length + 1):
            place = self.count - i * 12
            if place < 0:
                place = 0
            self.body.add(self.records[str(place)])
            
        self.body.draw(surface)
        
        self.candy.draw(surface)

        self.snake.update_pos(posw, posh)
        self.snake.image = rsnake
        surface.blit(self.snake.get_image(), (posw, posh))


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event.key)

    def _handle_keydown(self,key):
        if key == 276:
            self.lm = True
        elif key == 273:
            self.um = True
        elif key == 275:
            self.rm = True
        elif key == 274:
            self.dm = True
        elif key == 27:
            self._end_game()
        elif key == 114:
            self._restart()

    def _handle_keyup(self, key):
        if key == 276:
            self.lm = False
        elif key == 273:
            self.um = False
        elif key == 275:
            self.rm = False
        elif key == 274:
            self.dm = False

    def _change_dirc(self):
        time = 1/self.fps
        if self.lm:
            self.gamestate.left(time)
        if self.um:
            self.gamestate.up(time)
        if self.rm:
            self.gamestate.right(time)
        if self.dm:
            self.gamestate.down(time)

    def _check_collide(self):
        collide_list = pygame.sprite.spritecollide(self.snake, self.candy, dokill = True)
        num = len(collide_list)
        self.gamestate.eat_candy(num)
        self._create_candy(num)

        if len(pygame.sprite.spritecollide(self.snake, self.body, dokill = False)) > 2:
            raise mc.GameOverError

    def _end_game(self):
        self._running = False
    
    def _load_images(self):
        self.images = {}
        snake = pygame.image.load('1.JPG')
        candy = pygame.image.load('2.JPG')
        self.images['snake'] = snake
        self.images['candy'] = candy

    def _restart(self):
        self.count = 0
        self.gamestate = mc.Board()
        
        self.snake = Block(self.images['snake'])

        self.records = {}
        
        self.body = pygame.sprite.Group()
        
        self.candy = pygame.sprite.Group()
        self._create_candy(10)

    def _create_candy(self, num):
        
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        
        candies = []
        for i in range(num):
            candies.append(self.gamestate.get_candy())
            
        for c in candies:
            candy = Block(self.images['candy'])
            fracw, frach = c.get_pos()
            candy.update_pos(fracw * width - 15, frach * height - 15)
            self.candy.add(candy)

    def _resize_surface(self, size):
        
        pygame.display.set_mode(size)

        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        for name in self.images:
            self.images[name] = pygame.transform.scale(self.images[name], (int(0.05*width), int(0.05*height)))


class Block(pygame.sprite.Sprite):
    
    def __init__(self, image, body = 0):
        super(Block, self).__init__()
        self.image = image
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.body = body
        
    def update_pos(self, width, height):
        self.rect = self.image.get_rect().move(width, height)

    def transform(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        
    def print_rect(self):
        print(self.rect)
        
    def get_image(self):
        return self.image

if __name__ == '__main__':
    Gui().run()
