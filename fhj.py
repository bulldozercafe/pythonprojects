import turtle as t

t.speed(7)
t.bgcolor('black')
t.color('yellow')
t.penup()
t.goto(-200,-200)
t.pendown()
t.forward(500)
t.left(90)
t.forward(500)

t.penup()
t.goto(-200,-200)
t.pendown()
t.speed(10)
x=-195
y=-195
for i in range(99):    #t.forward(5)  _| x=300 y=-200
    t.goto(300,y)
    x+=5
    y+=5
    t.goto(x,-200)
