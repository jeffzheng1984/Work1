
# --- 新版RPG游戏 ---
import pygame
import random

TILE_SIZE = 48
MAP_WIDTH = 10
MAP_HEIGHT = 8
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

# 道具类型
ITEMS = [
	{"name": "鱼干", "color": (180, 220, 255), "effect": "heal"},
	{"name": "猫薄荷", "color": (120, 255, 120), "effect": "atk"},
	{"name": "铃铛", "color": (255, 255, 120), "effect": "spd"}
]

# 敌人动物，带属性
ANIMALS = [
	{"name": "猴子", "color": (200, 180, 80), "hp": 8, "atk": 2, "defn": 1},
	{"name": "狮子", "color": (255, 180, 0), "hp": 12, "atk": 4, "defn": 2},
	{"name": "大象", "color": (120, 120, 200), "hp": 15, "atk": 3, "defn": 3},
	{"name": "长颈鹿", "color": (255, 230, 120), "hp": 10, "atk": 2, "defn": 2},
	{"name": "熊猫", "color": (220, 220, 220), "hp": 10, "atk": 2, "defn": 2},
	{"name": "老虎", "color": (255, 120, 80), "hp": 11, "atk": 3, "defn": 2},
	{"name": "斑马", "color": (180, 180, 180), "hp": 9, "atk": 2, "defn": 1},
	{"name": "河马", "color": (150, 100, 200), "hp": 13, "atk": 3, "defn": 3}
]

class Cat:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.hp = 15
		self.atk = 3
		self.spd = 2
		self.collected = set()

class Animal:
	def __init__(self, name, color, x, y, hp, atk, defn):
		self.name = name
		self.color = color
		self.x = x
		self.y = y
		self.hp = hp
		self.atk = atk
		self.defn = defn
		self.found = False

class Item:
	def __init__(self, name, color, x, y, effect):
		self.name = name
		self.color = color
		self.x = x
		self.y = y
		self.effect = effect
		self.taken = False

def draw_text(screen, text, x, y, size=28, color=(0,0,0)):
	font = pygame.font.SysFont('SimHei', size)
	img = font.render(text, True, color)
	screen.blit(img, (x, y))

def battle(cat, animal, screen):
	# 简单回合制战斗，速度高者先手
	log = []
	chp, ahp = cat.hp, animal.hp
	cat_turn = cat.spd >= animal.defn
	while chp > 0 and ahp > 0:
		if cat_turn:
			dmg = max(1, cat.atk - animal.defn + random.randint(0,1))
			ahp -= dmg
			log.append(f"小猫攻击{animal.name}造成{dmg}伤害")
		else:
			dmg = max(1, animal.atk - 1 + random.randint(0,1))
			chp -= dmg
			log.append(f"{animal.name}攻击小猫造成{dmg}伤害")
		cat_turn = not cat_turn
	win = chp > 0
	if win:
		log.append(f"你打败了{animal.name}！")
	else:
		log.append(f"你被{animal.name}打败了！")
	# 战斗结果展示
	show_battle_log(screen, log)
	return win, chp

def show_battle_log(screen, log):
	# 简单弹窗显示战斗过程
	pygame.draw.rect(screen, (255,255,255), (60, 100, SCREEN_WIDTH-120, SCREEN_HEIGHT-200))
	for i, line in enumerate(log):
		draw_text(screen, line, 80, 120+i*32, 24, (0,0,0))
	draw_text(screen, "按任意键继续...", 120, SCREEN_HEIGHT-120, 24, (100,100,100))
	pygame.display.flip()
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				waiting = False
			elif event.type == pygame.QUIT:
				pygame.quit()
				exit()

def show_choice(screen, animal):
	# 弹窗选择挑战/绕行
	pygame.draw.rect(screen, (255,255,255), (60, 100, SCREEN_WIDTH-120, 180))
	draw_text(screen, f"遇到{animal.name}！", 100, 120, 32, (0,0,0))
	draw_text(screen, "按C键挑战，按S键绕行", 100, 180, 28, (0,0,0))
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					return "challenge"
				elif event.key == pygame.K_s:
					return "skip"
			elif event.type == pygame.QUIT:
				pygame.quit()
				exit()

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+80))
	pygame.display.set_caption("小猫探险记：动物园大冒险")
	clock = pygame.time.Clock()

	# 地图障碍
	obstacles = set()
	for _ in range(15):
		ox, oy = random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1)
		obstacles.add((ox, oy))

	# 初始化动物
	animal_objs = []
	animal_positions = set()
	for animal in ANIMALS:
		while True:
			ax, ay = random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1)
			if (ax, ay) not in animal_positions and (ax, ay) not in obstacles and (ax, ay) != (0,0):
				animal_positions.add((ax, ay))
				animal_objs.append(Animal(animal["name"], animal["color"], ax, ay, animal["hp"], animal["atk"], animal["defn"]))
				break

	# 初始化道具
	item_objs = []
	item_positions = set()
	for item in ITEMS:
		for _ in range(2):
			while True:
				ix, iy = random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1)
				if (ix, iy) not in animal_positions and (ix, iy) not in obstacles and (ix, iy) not in item_positions and (ix, iy) != (0,0):
					item_positions.add((ix, iy))
					item_objs.append(Item(item["name"], item["color"], ix, iy, item["effect"]))
					break

	# 小猫初始位置
	cat = Cat(0, 0)

	running = True
	win = False
	msg = ""
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN and not win:
				dx, dy = 0, 0
				if event.key == pygame.K_LEFT:
					dx = -1
				elif event.key == pygame.K_RIGHT:
					dx = 1
				elif event.key == pygame.K_UP:
					dy = -1
				elif event.key == pygame.K_DOWN:
					dy = 1
				nx, ny = cat.x + dx, cat.y + dy
				if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and (nx, ny) not in obstacles:
					cat.x, cat.y = nx, ny

		# 检查是否遇到动物
		for animal in animal_objs:
			if not animal.found and animal.x == cat.x and animal.y == cat.y:
				choice = show_choice(screen, animal)
				if choice == "challenge":
					win_battle, new_hp = battle(cat, animal, screen)
					if win_battle:
						animal.found = True
						cat.collected.add(animal.name)
						cat.hp = new_hp
						msg = f"你收集了{animal.name}！"
					else:
						cat.hp = max(1, new_hp)
						msg = f"挑战失败，生命剩余{cat.hp}"
				else:
					msg = f"你选择绕行{animal.name}"
				break

		# 检查是否拾取道具
		for item in item_objs:
			if not item.taken and item.x == cat.x and item.y == cat.y:
				if item.effect == "heal":
					cat.hp += 5
					msg = "吃到鱼干，生命+5！"
				elif item.effect == "atk":
					cat.atk += 1
					msg = "吃到猫薄荷，攻击+1！"
				elif item.effect == "spd":
					cat.spd += 1
					msg = "摇到铃铛，速度+1！"
				item.taken = True

		if len(cat.collected) == len(ANIMALS):
			win = True

		# 绘制
		screen.fill((180, 220, 255))
		# 绘制网格
		for x in range(MAP_WIDTH):
			for y in range(MAP_HEIGHT):
				rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
				pygame.draw.rect(screen, (220, 240, 255), rect, 0)
				pygame.draw.rect(screen, (180, 200, 220), rect, 1)
		# 绘制障碍
		for ox, oy in obstacles:
			pygame.draw.rect(screen, (100, 100, 100), (ox*TILE_SIZE, oy*TILE_SIZE, TILE_SIZE, TILE_SIZE))
		# 绘制动物
		for animal in animal_objs:
			if not animal.found:
				pygame.draw.circle(screen, animal.color, (animal.x*TILE_SIZE+TILE_SIZE//2, animal.y*TILE_SIZE+TILE_SIZE//2), TILE_SIZE//2-6)
				draw_text(screen, animal.name, animal.x*TILE_SIZE+8, animal.y*TILE_SIZE+TILE_SIZE//2-12, 18, (0,0,0))
		# 绘制道具
		for item in item_objs:
			if not item.taken:
				pygame.draw.rect(screen, item.color, (item.x*TILE_SIZE+12, item.y*TILE_SIZE+12, TILE_SIZE-24, TILE_SIZE-24))
				draw_text(screen, item.name, item.x*TILE_SIZE+10, item.y*TILE_SIZE+TILE_SIZE//2-10, 16, (0,0,0))
		# 绘制小猫
		pygame.draw.ellipse(screen, (255, 180, 220), (cat.x*TILE_SIZE+6, cat.y*TILE_SIZE+10, TILE_SIZE-12, TILE_SIZE-20))
		draw_text(screen, "🐱", cat.x*TILE_SIZE+12, cat.y*TILE_SIZE+8, 28)

		# 信息栏
		pygame.draw.rect(screen, (40, 60, 100), (0, SCREEN_HEIGHT, SCREEN_WIDTH, 80))
		draw_text(screen, f"生命:{cat.hp} 攻击:{cat.atk} 速度:{cat.spd}", 20, SCREEN_HEIGHT+10, 24, (255,255,255))
		draw_text(screen, f"已收集动物: {len(cat.collected)}/{len(ANIMALS)}", 20, SCREEN_HEIGHT+40, 24, (255,255,255))
		if msg:
			draw_text(screen, msg, 320, SCREEN_HEIGHT+20, 24, (255,255,0))
		if win:
			draw_text(screen, "通关成功！你找到了所有动物！", SCREEN_WIDTH//2-120, SCREEN_HEIGHT+30, 28, (255,255,0))

		pygame.display.flip()
		clock.tick(30)

	pygame.quit()

if __name__ == "__main__":
	main()
