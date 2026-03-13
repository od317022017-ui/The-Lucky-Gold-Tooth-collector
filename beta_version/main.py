import pygame
from random import randint
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

window_size = (800, 600)
def Menuframe():
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("The Lucky Gold-Tooh collector")
    font = pygame.font.SysFont(None, 40)

    # кнопки
    play_rect = pygame.Rect(300, 200, 200, 60)
    exit_rect = pygame.Rect(300, 300, 200, 60)

    # попытка загрузить фон из файла
    bg_image = None
    try:
        bg_image = pygame.image.load(resource_path("background.png")).convert()
        bg_image = pygame.transform.scale(bg_image, window_size)
    except pygame.error:
        bg_image = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(event.pos):
                    Gameframe()
                elif exit_rect.collidepoint(event.pos):
                    running = False

        # рисуем фон
        if bg_image:
            window.blit(bg_image, (0, 0))
        else:
            window.fill((255, 255, 255))

        # рисуем кнопки
        pygame.draw.rect(window, (0, 150, 0), play_rect)
        pygame.draw.rect(window, (150, 0, 0), exit_rect)

       

        # подписи
        play_surf = font.render("Play", True, (255, 255, 255))
        exit_surf = font.render("Exit", True, (255, 255, 255))
        window.blit(play_surf, play_surf.get_rect(center=play_rect.center))
        window.blit(exit_surf, exit_surf.get_rect(center=exit_rect.center))


        pygame.display.flip()

    pygame.quit()

def Gameframe():
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("The Lucky Gold-Tooh collector")
    font = pygame.font.SysFont(None, 40)

    game = True
    loses = 0
    toothes_collected = 0
    toothe_speed = 0.1
    lose_surf = None
    max_speed = 0.80
    skin_level = 0  # добавляем переменную для уровня скина
    evelius_grade = 0
    evelius_start_time = pygame.time.get_ticks()  # время начала отображения картинки evelius
    combo = 0  # счетчик комбо за подряд собранные зубы
    last_collect_time = 0  # время последнего сбора
    show_good = False  # флаг для отображения GOOD
    good_text = ""  # текст для отображения
    good_start_time = 0  # время начала отображения GOOD

    player_pos = [300, 500]
    
    # загружаем фон
    bg_image = None
    try:
        bg_image = pygame.image.load(resource_path("background2.png")).convert()
        bg_image = pygame.transform.scale(bg_image, window_size)
    except pygame.error:
        bg_image = None
    
    # загружаем картинку игрока
    player_image = None
    try:
        player_image = pygame.image.load(resource_path("player.png")).convert_alpha()
        player_image = pygame.transform.scale(player_image, (100, 100))  # масштабируем
    except pygame.error:
        player_image = None

    object_pos = [randint(0, window_size[0] - 50), 100]  # позиция объекта для сбора
    object_image = None
    try:
        object_image = pygame.image.load(resource_path("object.png")).convert_alpha()
        object_image = pygame.transform.scale(object_image, (50, 50))
    except pygame.error:
        object_image = None
    
    # evelius badge image (shown when grade >= 1)
    evelius_image = None
    try:
        evelius_image = pygame.image.load(resource_path("evelius3.png")).convert_alpha()
        # scale to a reasonable size for corner display
        evelius_image = pygame.transform.scale(evelius_image, (150, 100))
    except pygame.error:
        evelius_image = None
    movement = True  # флаг для разрешения движения игрока
    running = True
    while running:
        collected = False  # флаг, собран ли объект в этом кадре
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if movement == True:
        # "слушаем" нажатые клавиши постоянно
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player_pos[0] -= 0.4
            if keys[pygame.K_d]:
                player_pos[0] += 0.4
            # ограничиваем движение игрока в пределах окна
            if player_pos[0] < 0:
                player_pos[0] = 0
            elif player_pos[0] > window_size[0] - 80:
                player_pos[0] = window_size[0] - 80
 

        if bg_image:
            window.blit(bg_image, (0, 0))
        else:
            window.fill((200, 200, 255))
    
        # рисуем игрока
        if player_image:
            window.blit(player_image, player_pos)
        else:
            pygame.draw.rect(window, (0, 150, 0), (player_pos[0], player_pos[1], 80, 80))

        # проверяем столкновение игрока и объекта перед рисованием
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 80, 80)
        object_rect = pygame.Rect(object_pos[0], object_pos[1], 50, 50)
        if player_rect.colliderect(object_rect):
            toothes_collected += 1
            object_pos = [randint(0, window_size[0] - 50), -50]  # новый объект сверху
            if toothe_speed >= max_speed:
                toothe_speed = max_speed
            else:
                toothe_speed += 0.01  # увеличиваем скорость объекта
            evelius_grade = 1  # увеличиваем оценку evelius за каждый собранный зуб
            evelius_start_time = pygame.time.get_ticks()
        elif object_pos[1] > window_size[1]:  # если объект упал вниз
            loses += 1
            object_pos = [randint(0, window_size[0] - 50), -50]
            evelius_grade = -1
            evelius_start_time = pygame.time.get_ticks()

        # рисуем обьект только если не собран
        if running :
            if object_image:
                window.blit(object_image, object_pos)
            else:
                pygame.draw.circle(window, (255, 215, 0), object_pos, 25)

        if game == True:
            object_pos[1] += toothe_speed  # движение объекта вниз
            if loses >= 3:
                lose_surf = pygame.Rect(300, 200, 200, 60)
                lose_surf = font.render("You lost! Press R to restart", True, (255, 255, 255))
                window.blit(lose_surf, lose_surf.get_rect(center= (400, 300)))
                game = False
                if keys[pygame.K_r]:
                    running = False
                    Gameframe()
            # отображаем счет
            score_surf = font.render(f"score: {toothes_collected}", True, (255, 255, 255))
            window.blit(score_surf, (10, 10))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                game = False
                movement = False
                Menuframe()
            if toothes_collected >= 10 and skin_level < 1:
                player_image = None
                try:
                    player_image = pygame.image.load(resource_path("player_skin2.png")).convert_alpha()
                except pygame.error:
                    player_image = None
                if player_image:
                    player_image = pygame.transform.scale(player_image, (100, 100))  # масштабируем
                skin_level = 1
            if toothes_collected >= 30 and skin_level < 2:
                player_image = None
                try:
                    player_image = pygame.image.load(resource_path("player_skin3.png")).convert_alpha()
                except pygame.error:
                    player_image = None
                if player_image:
                    player_image = pygame.transform.scale(player_image, (100, 100))  # масштабируем
                skin_level = 2
            if toothes_collected >= 60 and skin_level < 3:
                player_image = None
                try:
                    player_image = pygame.image.load(resource_path("player_skin4.png")).convert_alpha()
                except pygame.error:
                    player_image = None
                if player_image:
                    player_image = pygame.transform.scale(player_image, (100, 100))  # масштабируем
                skin_level = 3
            # display evelius badge in the top-right when unlocked
            current_time = pygame.time.get_ticks()

            # choose correct evelius image based on grade and time
            if evelius_grade == -1:
                # show bad rating for 5 seconds
                if (current_time - evelius_start_time) / 1000 < 5:
                    evelius_image = None
                    try:
                        evelius_image = pygame.image.load(resource_path("evelius1.png")).convert_alpha()
                        evelius_image = pygame.transform.scale(evelius_image, (150, 100))
                    except pygame.error:
                        evelius_image = None
                else:
                    evelius_grade = 0
                    evelius_start_time = current_time
            elif evelius_grade == 1:
                # show good rating for 5 seconds
                if (current_time - evelius_start_time) / 1000 < 5:
                    evelius_image = None
                    try:
                        evelius_image = pygame.image.load(resource_path("evelius2.png")).convert_alpha()
                        evelius_image = pygame.transform.scale(evelius_image, (150, 100))
                    except pygame.error:
                        evelius_image = None
                else:
                    evelius_grade = 0
                    evelius_start_time = current_time
            else:
                # default evelius image
                evelius_image = None
                try:
                    evelius_image = pygame.image.load(resource_path("evelius3.png")).convert_alpha()
                    evelius_image = pygame.transform.scale(evelius_image, (150, 100))
                except pygame.error:
                    evelius_image = None

            if evelius_image:
                x = window_size[0] - evelius_image.get_width() - 10
                y = 10
                window.blit(evelius_image, (x, y))
        if toothes_collected == 1000:  # easter egg для 1000 зубов
            win_surf = font.render("You are a true collector! You win!Press r to restart or q to quit", True, (255, 255, 0))
            window.blit(win_surf, win_surf.get_rect(center=(400, 300)))
            movement = False
            if keys[pygame.K_r]:
                game = False
                Gameframe()
            elif keys[pygame.K_q]:
                running = False
                Menuframe()



                

            

        



        pygame.display.flip()



if __name__ == "__main__":
    Menuframe()
