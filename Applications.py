import pygame
import time
import turtle as t
import random
import math

# round 함수의 오류 수정 함수
def round2(f):
    f=math.ceil(f+0.5)
    return f



#===================Random_Chosing.py===================#

def random_chosing():
    print("\nWelcome to 'Random Chosing'\nIt chooses randomly\n")

    def is_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def DrawBackground(n):
        t.bgcolor('black')
        t.speed(10)
        t.pensize(3)

        if n >= 2:
            t.pencolor('white')
            t.penup()
            t.goto(-200, -200)
            t.pendown()
            t.circle(10)
            t.penup()
            t.forward(20)
            t.pendown()
            t.write('Number 1')

            t.pencolor('yellow')
            t.penup()
            t.goto(0, -200)
            t.pendown()
            t.circle(10)
            t.penup()
            t.forward(20)
            t.pendown()
            t.write('Number 2')

        if n == 3:
            t.pencolor('violet')
            t.penup()
            t.goto(200, -200)
            t.pendown()
            t.circle(10)
            t.penup()
            t.forward(20)
            t.pendown()
            t.write('Number 3')

        if n != 2 and n != 3:
            print('Please write it properly')
            time.sleep(1)
            exit()

        t.penup()
        t.goto(-300, 200)
        t.pendown()

        if n >= 2:
            t.pencolor('white')
            t.forward(200)

            t.pencolor('yellow')
            t.forward(200)
        if n == 3:
            t.pencolor('violet')
            t.forward(200)

        t.pencolor('lightgreen')

        a = -300
        t.right(90)
        for i in range(n + 1):
            t.penup()
            t.goto(a, 200)
            t.pendown()
            t.forward(20)
            a += 200

    def randomize(n):
        t.right(180)
        t.pensize(5)

        a = -177
        b = -177
        c = -177

        goal = 197

        while a < goal and b < goal and c < goal:
            r = random.randint(1, n)
            if r == 1:
                t.penup()
                t.goto(-200, a)

                a2 = random.randint(5, random.randint(10, 20))
                a3 = a + a2

                t.pendown()
                t.goto(-200, a3)
                a = a3

            elif r == 2:
                t.penup()
                t.goto(0, b)

                b2 = random.randint(5, random.randint(10, 20))
                b3 = b + b2

                t.pendown()
                t.goto(0, b3)
                b = b3

            elif r == 3:
                t.penup()
                t.goto(200, c)

                c2 = random.randint(5, random.randint(10, 20))
                c3 = c + c2

                t.pendown()
                t.goto(200, c3)
                c = c3

        if a >= goal:
            print('\n1st place: Number 1')
            if b > c:
                print('2nd place: Number 2')
                if n == 3:
                    print('3rd place: Number 3')
            elif b == c:
                print('2nd place: Number 2 and 3')
            elif c > b:
                print('2nd place: Number 3')
                print('3rd place: Number 2')
        elif b >= goal:
            print('\n1st place: Number 2')
            if a > c:
                print('2nd place: Number 1')
                if n == 3:
                    print('3rd place: Number 3')
            elif a == c:
                print('2nd place: Number 1 and 3')
            elif c > a:
                print('2nd place: Number 3')
                print('3rd place: Number 1')
        elif c >= goal:
            print('\n1st place: Number 3')
            if a > b:
                print('2nd place: Number 1')
                print('3rd place: Number 2')
            elif a == b:
                print('2nd place: Number 1 and 2')
            elif b > a:
                print('2nd place: Number 2')
                print('3rd place: Number 1')

    # Program Start
    while True:
        n = input("How many are the players? Write 2 or 3: ")

        if is_int(n):
            n = int(n)
        else:
            print(f'Error: "{n}" is not an integer')
            time.sleep(1)
            exit()

        DrawBackground(n)
        randomize(n)

        a = input('\nDo you want to choose again? \nPrint yes or no: ')
        a = a.lower()

        if a == 'yes':
            t.Screen().reset()
        elif a == 'no':
            print('program ended')
            time.sleep(1)
            exit()
        else:
            print('Unknown input detected')
            print('program ended')
            time.sleep(1)
            exit()

#====================END====================#



#====================Typing_Practice===================#

def typing_practice():
    print("\nWelcome to 'Typing Practice'\nYou can practice typing\n")

    def words():
        print('0%')
        f = 0
        for i in range(1, 101):
            # 리스트의 유효한 인덱스 범위에서 랜덤으로 단어를 선택
            w = words_list[random.randint(0, len(words_list) - 1)]
            w2 = input(w + '\n')
            
            if w != w2:
                f += 1
            print(f'{i}%')
            print(f'Incorrect: {f}')
        print(f'Accuracy: {100 - f}%')



    def sentences():
        print('0%')
        f = 0
        top_rate = 0
        for i in range(5, 101, 5):
            #리스트의 유효한 인덱스 범위에서 랜덤으로 문장을 선택
            s = sentences_list[random.randint(0, len(sentences_list) -1)]
            
            start_time = time.time()
            s2 = input(s + '\n')
            end_time = time.time()

            wrote_time = round2(end_time - start_time)
            
            if s != s2:
                f += 1
                # 문장이 일치하지 않을 때 타이핑 속도는 0
                tr = '-'
            else:
                # wrote_time이 0보다 큰 경우에만 타이핑 속도를 계산
                tr = round2((len(s) / wrote_time)*60) if wrote_time > 0 else 0
                
                if top_rate < tr:
                    top_rate = tr
            print(f'{i}%')

            
            print(f'Incorrect: {f}')
            print(f'Typing Rate: {tr}')
            print(f'Top Typing Rate: {top_rate}')
            

        print(f'Accuracy: {20 - f}%')
        print(f'Top Typing Rate: {top_rate}')

    words_list = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog', 'keyboard', 'practice', 'speed',
                  'accuracy', 'typing', 'letter', 'words', 'fast', 'slow', 'skill', 'hands', 'exercise']
    sentences_list = ['The cat sat on the mat', 'She loves to read books', 'Time flies when having fun',
                      'Keep calm and carry on', 'A stitch in time saves nine', 'He runs fast every morning',
                      'The sun sets in the west', 'Practice makes perfect', 'You are what you eat',
                      'They play soccer on Sundays', 'Life is short, smile often', 'I can do it by myself',
                      'The quick brown fox jumps', 'Silence is golden, talk less', 'Never give up on dreams',
                      'Work hard and stay humble', 'A picture is worth a thousand words',
                      'She sings beautifully at night', 'The early bird catches the worm',
                      'Success is the best revenge']

    ques = input("If you want to practice writing words, write 'W'\nOr if you want to practice writing sentences, write 'S': ")
    ques = ques.lower()
    
    if ques == 'w':
        words()
    elif ques == 's':
        sentences()
    else:
        print('Unknown input detected')
        print('Program ended')
        time.sleep(1)
        exit()


#====================END====================#




#====================Simple_Dino_Game====================#

def dino_game():
    # 초기화
    pygame.init()

    # 화면 크기 설정
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Game")

    # 색상 정의
    WHITE = (255, 255, 255)

    # 공룡 클래스
    class Dino(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("dino2.png")
            self.rect = self.image.get_rect()
            self.rect.x = 50
            self.rect.y = HEIGHT - 70
            self.is_jumping = False
            self.jump_speed = 10
            self.gravity = 0.5
            
            # 히트박스 줄이기
            self.rect.inflate_ip(-8, -8)  # 가로, 세로 각각 8씩 줄이기

        def update(self):
            if self.is_jumping:
                self.rect.y -= self.jump_speed
                self.jump_speed -= self.gravity
                if self.rect.y >= HEIGHT - 70:
                    self.rect.y = HEIGHT - 70
                    self.is_jumping = False
                    self.jump_speed = 10

        def jump(self):
            if not self.is_jumping:
                self.is_jumping = True

    # 장애물 클래스
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("cac.png")
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - 50

        def update(self):
            self.rect.x -= 5
            if self.rect.x < -20:
                self.kill()

    # 점수 표시 함수
    def display_score(score):
        font = pygame.font.SysFont(None, 55)
        score_text = font.render(f"{score}", True, (100, 100, 100))
        screen.blit(score_text, (10, 10))

    # 스프라이트 그룹
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    dino = Dino()
    all_sprites.add(dino)

    # 게임 루프
    running = True
    clock = pygame.time.Clock()

    nGap = 0
    score = 0
    frame_rate = 60

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        # 업데이트
        all_sprites.update()

        # 장애물 생성
        nGap += 1
        if nGap == 50:
            if random.randint(0, 100) > (100 - 50):
                obstacle = Obstacle()
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
            nGap = 0

        # 충돌 감지
        if pygame.sprite.spritecollideany(dino, obstacles):
            print("Game Over!")
            print(f"Score: {int(score/5)}")
            running = False

        # 화면 그리기
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # 점수 업데이트
        score += 1

        # 점수 표시
        display_score(int(score / 5))

        pygame.display.flip()

        # 프레임 속도 조절
        frame_rate+=0.01
        clock.tick(frame_rate)

    pygame.quit()

#====================END====================#



#========================================Program_Start========================================#


appli_ques = input('\nWelcome to "Applications.py" \
\n\nType "R" for Random Choosing, "T" for Typing Practice, or "D" for Dino Game: ')

if appli_ques.lower() == 'r':
    random_chosing()
elif appli_ques.lower() == 't':
    typing_practice()
elif appli_ques.lower() == 'd':
    dino_game()
else:
    print('Unknown input detected')
    print('program ended')
    time.sleep(1)
    exit()