def random_chosing():
    import turtle as t
    import random


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

        if n>=2:
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
            return

        t.penup()
        t.goto(-300, 200)
        t.pendown()

        if n>=2:
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

        if a>= goal:
            print('\n1st place:Number 1')
            if b>c:
                print('2nd place:Number 2')
                if n==3:
                    print('3rd place:Number 3')
            
            elif b==c:
                print('2nd place:Number(2,3)')

            
            elif c>b:
                print('2nd place:Number 3')
                print('3rd place:Number 2')
        
            


        

        elif b>= goal:
            print('\n1st place:Number 2')
            if a>c:
                print('2nd place:Number 1')
                if n==3:
                    print('3rd place:Number 3')
            
            elif a==c:
                print('2nd place:Number(1,3)')

            
            elif c>a:
                print('2nd place:Number 3')
                print('3rd place:Number 1')






        elif c>= goal:
            print('\n1st place:Number 3')
            if a>b:
                print('2nd place:Number 1')
                print('3rd place:Number 2')
            
            elif a==b:
                print('2nd place:Number(1,2)')

            
            elif a>b:
                print('2nd place:Number 2')
                print('3rd place:Number 1')


    # ========== Program Start ================

    while True:

        n = input("How many are the player's? Write 2~3:")

        if is_int(n) == True:
            n = int(n)
            pass
        elif is_int(n) == False:
            print('Error: "%s" is not a integer' %n)
            break

        DrawBackground(n)

        randomize(n)

        a = input('\nDo you want to choose again? \nPrint yes or no:')
        a = a.lower()

        if a == 'yes':
            screen = t.Screen()
            screen.reset()
            # random()
        elif a == 'no':
            print('program ended')
            break
        else:
            print('Unknown string detected')
            print('program ended')
            break




random_chosing()



