from tkinter import *
from random import *
from math import *
from PIL import *
from PIL import ImageTk
import time

# Создаем окно программы
root = Tk()
root.title("Добро пожаловать")
# Создаем область для рисования + фон
c = Canvas(root, width=600, height=600, bg="white")
c.pack(expand = YES, fill = BOTH)
image = ImageTk.PhotoImage(file = "kv.png")
c.create_image(10, 10, image = image, anchor = NW)


c.pack()

# Для движущейся точки создадим класс
class Dot:
	def __init__(self, canvas, center, dist):
		self.direct = 'right' # Направление right- по часовой, left - против
		self.angle = 0		# текущий угол
		self.radius = 20	# радиус кружка
		self.canvas = canvas    # ссылка на рисовалку для удобства
		self.center = center	# центр окружности
		self.dist = dist	# расстояние до центра
		self.x, self.y = self.p2c()	# преобразуем угол в координаты. 
		# Рисуем начальное положение
		self.shape = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill='#ffd152')
		# Запускаем анимацию
		self.update()

	def update(self):
		# Вычисляем новые координаты
		new = self.p2c()
		# Двигаем кружок на дельту
		self.canvas.move(self.shape, new[0]-self.x, new[1]-self.y)
		# Сохраняем новые кординаты как текущие
		(self.x, self.y) = new
		# Через 20мс  повторяем
		self.canvas.after(20, self.update)
		# Увеличиваем скорость
		self.angle += 0.025

	# направление круга if - влево, else - вправо.
	def p2c(self):
		if self.direct == 'left': 
			return sin(self.angle) * self.dist + self.center[0], cos(self.angle) * self.dist + self.center[1]
		else:
			return cos(self.angle) * self.dist + self.center[0], sin(self.angle) * self.dist + self.center[1]

# Статичные элементы рисовать легко
c.create_oval(100, 100, 500, 500)

# Содаем экземпляр точки
dot = Dot(c, (300, 300), 200)

# Запускаем главный цикл
root.mainloop()
