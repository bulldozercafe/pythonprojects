import pygame
import random

pygame.init()

background = pygame.display.set_mode((900, 950))
pygame.display.set_caption('Shoot!')

x_pos = 450
y_pos = 870

to_x = 0
to_y = 0


right = False
left = False

play = True

enemies = []
bullet = []

frame = 0
second = 0

gravity = 0.5
BONUS_SCORE = 30

item_list = []
last_item_score = 0
SCORE = 0

item = False



# ===================플레이어 체력, 점수=================
PLAYER_H = 5
player_health = PLAYER_H
score = 0
coll_frame = 0
game_over = False
# ======================================================

# ===================== 그림 불러오기 ===================
enemy_image = pygame.image.load("ufo2.png").convert_alpha() # 그림 불러오기  빠르게(convert.alpha())
enemy_image = pygame.transform.scale(enemy_image, (50, 50)) # 크기 조정

player_image = pygame.image.load("spaceship3.png").convert_alpha() # 그림 불러오기  빠르게(convert.alpha())
player_image = pygame.transform.scale(player_image, (50, 50)) # 크기 조정

background_image = pygame.image.load("ocean.png").convert_alpha() # 그림 불러오기 빠르게(convert.alpha())
background_image = pygame.transform.scale(background_image, (900, 950)) # 크기 조정

item_red_image = pygame.image.load("redCristal.png").convert_alpha() # 그림 불러오기  빠르게(convert.alpha())
item_red_image = pygame.transform.scale(item_red_image, (50,60)) # 크기 조정
item_green_image = pygame.image.load("greenCristal.png").convert_alpha() # 그림 불러오기  빠르게(convert.alpha())
item_green_image = pygame.transform.scale(item_green_image, (50,60)) # 크기 조정
item_blue_image = pygame.image.load("blueCristal.png").convert_alpha() # 그림 불러오기  빠르게(convert.alpha())
item_blue_image = pygame.transform.scale(item_blue_image, (50,60)) # 크기 조정
item_white_image = pygame.image.load("whiteCristal.png").convert_alpha() # 그림 불러오기  빠르게(convert.alpha())
item_white_image = pygame.transform.scale(item_white_image, (50,60)) # 크기 조정
item_img_list = [item_red_image, item_green_image, item_blue_image, item_white_image]
# ======================================================


item_random_list = [item_red_image, item_green_image, item_blue_image, item_white_image]


# ==================== 음악 불러오기 =======================
# 효과음 로드
boom_sound = pygame.mixer.Sound("boom.mp3")  # WAV 파일 경로
bullet_sound = pygame.mixer.Sound("lazer.mp3")  # WAV 파일 경로
laser_sound = pygame.mixer.Sound("LASER_LONG.mp3")  # WAV 파일 경로
bonus_sound = pygame.mixer.Sound("bonus.mp3")  # WAV 파일 경로
bullet_sound.set_volume(0.2) # 30% 볼륨으로 재생
# ===========================================================


def playMusic():
    music_list = []
    # 배경 음악 로드 및 재생
    music_list.append("Electroman Adventures.mp3")
    music_list.append("Theory of Everything (GD Cut).mp3")
    music_list.append("Clubstep (GD Cut).mp3")
    music_list.append("Electrodynamix.mp3")
    music_list.append("Time Machine.mp3")
    music_list.append("Hexagon Force.mp3")
    
    pygame.mixer.music.load(music_list[random.randint(0,len(music_list) - 1)])  # MP3 파일 경로
    pygame.mixer.music.set_volume(0.7)    
    pygame.mixer.music.play(-1)  # -1은 무한 반복을 의미합니다.



def enemies_list(enemies, frame):
    x = random.randint(1,2)
    if frame % 50 == 0:
        if x==1:
            x_pos = 0   # --> 방향
            x_vel = random.randint(1,5)
            y_vel = 0
        else:
            x_pos = 850 # <-- 방향                           
            x_vel = -random.randint(1,5)
            y_vel = 0
        enemies.append([x_pos, 200, x_vel,y_vel , 3])    # [1.x_pos, 2.y_pos, 3.x_vel, y_vel, 4.health]


def gunshots(x_pos, y_pos, bullet, frame):
    if frame % 20 == 0:
            bullet.append([x_pos + 20, y_pos])    # [1.x_pos, 2.y_pos]
            bullet_sound.play()

def laser(second, laser_sound, x_pos, y_pos):
    if second % 10 == 0:
        hitbox = pygame.draw.rect(background, ('red'), (x_pos + 18, y_pos - 1000, 10, 1000))
        laser_sound.play()
        return hitbox
    return None


         


playMusic()




# =========================================================================== START ====================================================================================
# =========================================================================== START ====================================================================================



while play:
    # 키보드나 마우스를 눌렀는지 확인 (무조건 맨처음 있어야 함)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            play = False
        
    # ==============   게임오버 화면 표시 ==============================
    if game_over == True:
        # 게임 오버 화면 표시
        #pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(0.1)    
        background.fill((0, 0, 0))  # 검정색 배경
        small_font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
        click_text = small_font.render("Click to start!!", True, (255, 255, 255))
        
        # 텍스트 위치 설정
        game_over_rect = game_over_text.get_rect(center=(450, 250))
        score_rect = score_text.get_rect(center=(450, 350))
        click_rect = click_text.get_rect(center=(450, 600))
        
        # 텍스트 그리기
        background.blit(game_over_text, game_over_rect)
        background.blit(score_text, score_rect)
        background.blit(click_text, click_rect)
        
        # 게임오버 화면 업데이트
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONUP:
            # 마우스를 클릭하면 1초 후에 게임 시작
            pygame.time.delay(1000)
            score = 0
            last_item_score = 0
            game_over = False
            player_health = PLAYER_H
            enemies.clear()
            bullet.clear()  
            playMusic()
        else:
            continue
            
    # =============================================================================

    


    

    # 키로 동작
    '''
    if event.type == pygame.KEYDOWN:  
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            left = False
            right = True
            to_x = 10
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            right = False
            left = True
            to_x = -10
    else:
        right = False
        left = False
        to_x = 0

    
    x_pos += to_x
    if x_pos < 0:  # 왼쪽 경계
        x_pos = 0
    elif x_pos > 850:  # 오른쪽 경계 (900 - 50)
        x_pos = 850
    '''


    # ===============마우스 위치 가져오기 ================
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x > 850:
        mouse_x = 850

    x_pos = mouse_x # 마우스 위치로 플레이어 이동
    # ===================================================

    
    
    # ===================================================

    # 화면에 그리기 시작
    # background.fill('blue')
    background.blit(background_image, (0, 0))
    
    #====================================================

    # 아이템 생성========================================

    # list에 값이 있는지 확인
    if len(item_list) > 0:
        background.blit(item_random_list[item_list[2]], (item_xpos, item_ypos))
        item_ypos += 5
        if item_ypos > 1000:
            item_list.clear()
        
    else:     # [x_pos, y_pos, {index(item_random_list)} = type]        
        if score - SCORE >= 1:                                                         
            item_list.append(random.randint(75, 825))  
            item_list.append(0)
            item_list.append(random.randint(0, 2))
            item_xpos = item_list[0]
            item_ypos = 0
            item_type = item_list[2]
            SCORE = score
    

    # 총알 생성
    gunshots(x_pos, y_pos, bullet, frame)
    
    # 총알 그리기
    for gun in bullet:
        gun[1] -= 20
        if gun[1] < -100:   # 총알이 화면 밖으로 사라지면 없애기            
            bullet.remove(gun)
            continue

        pygame.draw.rect(background, ('yellow'), (gun[0], gun[1], 10, 20))

    # LASER==================================================================
    laser_hitbox = laser(second, laser_sound, x_pos, y_pos)


    # =======================================================================
    # 플레이어 그리기    
    # pygame.draw.rect(background, ('white'), (x_pos, y_pos, 50, 50))
    background.blit(player_image, (x_pos, y_pos, 50, 50))  # 그림으로 그리기
    # =======================================================================


    # 적 새로 만들기
    enemies_list(enemies, frame)

    # 적 그리기
    for en in enemies:        
        # X속도
        if en[0] > 850 or en[0] < 0:
            en[2] = -en[2]        
        
        # Y속도
        if en[1] > 850:
            en[3] = -en[3] - 0.5
        
        en[3] += gravity
           
        # X위치 변경
        en[0] += en[2]
        # Y위치 변경
        en[1] += en[3]

        # =======================================================================
        # pygame.draw.rect(background, ('red'), (en[0], en[1], 50, 50)) # 사각형으로 그리기
        background.blit(enemy_image, (en[0], en[1], 50, 50))  # 그림으로 그리기
        # =======================================================================

        # 폰트 설정 (폰트 이름, 크기)
        font = pygame.font.Font(None, 36)  # 기본 폰트 사용, 크기 36
        text = font.render(str(en[4]), True, (255, 255, 255))  # 흰색 글씨
        background.blit(text, (en[0], en[1], 50, 50))
    

    # BULLET 충돌 확인================================================================================
    for e in enemies:
        for b in bullet:
            if b[1] < -50:
                bullet.remove(b)
                continue

            enemy_rect = pygame.Rect(e[0], e[1], 50, 50)  # 적 사각형 데이터 만들기
            bullet_rect = pygame.Rect(b[0], b[1], 10, 20)     # 총알 사각형 데이터 만들기

            # 충돌 확인
            if bullet_rect.colliderect(enemy_rect):   # 서로 겹쳤는지 검사 -> 겹쳤으면 처리                                
                bullet.remove(b)
                pygame.draw.rect(background, ('yellow'), (e[0], e[1], 50, 50), 5) # 번쩍 효과
                e[4] -= 1  # 적 체력 1 깎기
                if(e[4] < 1): # 적 체력이 1보다 작으면 삭제하기
                    if e in enemies:
                        enemies.remove(e)
                        score += 1    # 적이 죽으면 점수 + 1
                        if score % BONUS_SCORE == 0:
                            player_health += 1
                            bonus_sound.play()
                        boom_sound.play()

    # Laser 충돌 확인================================================================================
    if laser_hitbox != None:
        for e in enemies:
            enemy_rect = pygame.Rect(e[0], e[1], 50, 50)  # 적 사각형 데이터 만들기

            # 충돌 확인
            if laser_hitbox.colliderect(enemy_rect):   # 서로 겹쳤는지 검사 -> 겹쳤으면 처리                                
                pygame.draw.rect(background, ('yellow'), (e[0], e[1], 50, 50), 5) # 번쩍 효과
                e[4] -= 1  # 적 체력 1 깎기
                if(e[4] < 1): # 적 체력이 1보다 작으면 삭제하기
                    if e in enemies:
                        enemies.remove(e)
                        score += 1    # 적이 죽으면 점수 + 1
                        if score % BONUS_SCORE == 0:
                            player_health += 1
                            bonus_sound.play()
                        boom_sound.play()
    


    # PLAYER 충돌 확인============================================================================
    player_rect = pygame.Rect(x_pos, y_pos, 50, 50)
    for e in enemies:
        enemy_rect = pygame.Rect(e[0], e[1], 50, 50)  # 적 사각형 데이터 만들기        
        
        # 충돌 확인
        if frame > coll_frame + 100: 
            if player_rect.colliderect(enemy_rect):   # 서로 겹쳤는지 검사 -> 겹쳤으면 처리
                pygame.draw.rect(background, ('yellow'), (x_pos, y_pos, 50, 50), 10) # 번쩍 효과
                coll_frame = frame
                player_health -= 1
                background.fill((255, 0, 0))  # 빨간색 배경
                if player_health < 1:
                    game_over = True


    if len(item_list) > 0:
        item_rect = pygame.Rect(item_xpos, item_ypos, 50, 60)  # 아이템 사각형 데이터 만들기
    
        if player_rect.colliderect(item_rect):
            pass
        




    font = pygame.font.Font(None, 60)  # 기본 폰트 사용, 크기 36
    
    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))  # 흰색 글씨
    background.blit(score_text, (0, 0, 100, 100)) # 화면에 그리기

    health_text = font.render('Health : ' + str(player_health), True, (255, 255, 255))  # 흰색 글씨
    background.blit(health_text, (650, 0, 100, 100)) # 화면에 그리기
            

    
    

    # UPDATE frame
    frame +=1
    if frame % 60 == 0:
        second +=1

    pygame.time.Clock().tick(60)
    pygame.display.update()  

pygame.quit()

# =========================================================================== END ====================================================================================
# =========================================================================== END ====================================================================================
