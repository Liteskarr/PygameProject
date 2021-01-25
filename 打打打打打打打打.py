import noise
import random
CELL_TYPES = [(0, 85, 0, 127, 't'), 
			  (0, 85, 128, 255, 'a'),
			  (86, 170, 0, 127, 'p'),
			  (86, 170, 128, 255, 's'),
			  (171, 255, 0, 255, 'd'),
			  (171, 255, 128, 255, 'r')]#Температура мин макс, влажность мин макс, буква
class Field:
    @staticmethod
    def generate_field(size):
        field = [[0 for i in range(size)] for i in range(size)]

        for y in range(size):
            for x in range(size):
                temperature = int((noise.pnoise3(float(x + 50) * 0.3, float(y + 50) * 0.3,
                                       random.randint(1, 0xffffff)) + 1) * 128)
                water = int((noise.pnoise3(float(x + 50) * 0.3, float(y + 50) * 0.3,
                                       random.randint(1, 0xffffff)) + 1) * 128)
                typ = 'r'
                for tm, tmx, wm, wmx, l in CELL_TYPES:
                    if temperature >= tm and temperature <= tmx and water >= wm and water <= wmx:
                    	typ = l
                    	break
                field[x][y] = typ
 
        return field

a = Field.generate_field(50)
for i in a:
	print(''.join(i))