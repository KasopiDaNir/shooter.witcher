from pygame import *
from random import randint

# фонова музика
mixer.init()
mixer.music.load('the.trail.mp3')
mixer.music.play()


# шрифти і написи
font.init()
score_text = font.Font(None, 36)
score = 0
lost_text = font.Font(None, 36)
lost = 0

lose_text = font.Font(None, 36)
win_text = font.Font(None, 36)


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

background = transform.scale(
    image.load("mountains.jpg"), 
    (win_width, win_height)
)



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        dagger = Dagger('dagger.png', self.rect.centerx, self.rect.top, 60, 50, -15) 
        daggers.add(dagger)

# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

    
# клас спрайта-кулі   
class Dagger(GameSprite): 
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

wither = Player("wither.png", 5, win_height - 100, 80, 100, 10)

daggers = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("griffin.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

run = True
game_over = False
is_win = False

while run:

    window.blit(background, (0, 0))
    
    text1 = score_text.render("Рахунок: " + str(score), 1, (0, 0, 0))
    window.blit(text1, (10, 20))
    text2 = lost_text.render("Пропущено: " + str(lost), 1, (0, 0, 0))
    window.blit(text2, (10, 50))

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if game_over == False:
                if e.key == K_SPACE:
                    wither.fire()

    if game_over == False:

        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, daggers, True, False)
        for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy('griffin.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        if sprite.spritecollide(wither, monsters, True) or lost >= 5:
            lost += 1
            game_over = True # програли, ставимо тло і більше не керуємо спрайтами.

        if score >= 100:
            game_over = True
            is_win = True

        # рухи спрайтів
        wither.update()
        monsters.update()
        daggers.update()
        
    else:
        if is_win == True:
            text4 = win_text.render("Ви перемогли", 1, (0, 0, 0))
            window.blit(text4, (200, 200))
        else:
            text3 = lose_text.render("Ви програли", 1, (0, 0, 0))
            window.blit(text3, (200, 200))

    # оновлюємо їх у новому місці при кожній ітерації циклу
    wither.reset()
    monsters.draw(window)
    daggers.draw(window)

    display.update()
    time.delay(60)