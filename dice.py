# Author: Stephen Luttrell

import copy, os, pickle, pyperclip, pygame, sys, time
import lib.speech as speech
from lib.sound_pool import sound_pool
from __random import RandomOrg

def save_data(data, file='untitled'):
	with open(file, 'wb') as o:
		pickle.dump(data, o)

def retrieve_data(file):
	with open(file, 'rb') as i:
		return pickle.load(i)

def roll_for_abilities():
	# D&D character ability rolls (roll 4d6, keep highest 3)
	totals = None
	integers.get_true_random(type='integers', num=24, min=1, max=6)
	if integers.data:
		totals = []
		for i in range(0, len(integers.data), 4):
			temp = sorted([int(integers.data[i]), int(integers.data[i+1]), int(integers.data[i+2]), int(integers.data[i+3])])
			totals.append(temp[1] + temp[2] + temp[3])
	return copy.copy(totals)

if __name__ == '__main__':
	integers = RandomOrg()
	CHANGE_ITEM = 'sounds\\menu\\mChange.wav'
	ROLLBACK = 'sounds\\menu\\mRoll.wav'
	SELECT = 'sounds\\menu\\mSelect.wav'
	EXIT = 'sounds\\menu\\mCancel.wav'
	TAB = 'sounds\\menu\\mTab.wav'
	tabs = [ 'coin toss', 'roll a d4', 'roll a d6', 'roll a d8', 'roll a d10', 'roll a d12', 'roll a d20', 'roll for abilities' ]
	column = 0
	row = 0
	rolls = [ [], [], [], [], [], [], [], [] ]
	quit = False

	screen = pygame.display.set_mode((400, 400))
	pygame.display.set_caption('True Random Dice Roller')
	backgroundColor = (0, 0, 0)
	screen.fill(backgroundColor)
	pygame.display.flip()

	if os.path.isfile('settings.dat'): speech.set_rate(retrieve_data('settings.dat'))

	while not quit:
		time.sleep(.005) # Be kind to other processes

		for e in pygame.event.get(): # Query the event pool
			if pygame.key.get_pressed()[pygame.K_UP]:
				if len(rolls[column]) > 0:
					if row > 0:
						row -= 1
						sound_pool.play_stationary(CHANGE_ITEM)
					else:
						row = len(rolls[column]) - 1
						sound_pool.play_stationary(ROLLBACK)
					speech.speak('roll number ' + str(row + 1) + ': ' + rolls[column][row], True)
				else:
					speech.speak('please press enter to roll the dice')
			if pygame.key.get_pressed()[pygame.K_DOWN]:
				if len(rolls[column]) > 0:
					if row < len(rolls[column]) - 1:
						row += 1
						sound_pool.play_stationary(CHANGE_ITEM)
					else:
						row = 0
						sound_pool.play_stationary(ROLLBACK)
					speech.speak('roll number ' + str(row + 1) + ': ' + rolls[column][row], True)
				else:
					speech.speak('please press enter to roll the dice')
			if pygame.key.get_pressed()[pygame.K_LEFT]:
				if column > 0: column -= 1
				else: column = len(tabs) - 1
				sound_pool.play_stationary(TAB)
				speech.speak(tabs[column], True)
				row = len(rolls[column]) - 1
			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				if column < len(tabs) - 1: column += 1
				else: column = 0
				sound_pool.play_stationary(TAB)
				speech.speak(tabs[column], True)
				row = len(rolls[column]) - 1
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				if column == 0: # Coin toss
					integers.get_true_random(min=1, max=2)
					if int(integers.data[0]) == 1: rolls[column].append('heads')
					else: rolls[column].append('tails')
				elif column == 1: # D4
					integers.get_true_random(min=1, max=4)
					rolls[column].append(integers.data[0])
				elif column == 2: # D6
					integers.get_true_random(min=1, max=6)
					rolls[column].append(integers.data[0])
				elif column == 3: # D8
					integers.get_true_random(min=1, max=8)
					rolls[column].append(integers.data[0])
				elif column == 4: # D10
					integers.get_true_random(min=1, max=10)
					rolls[column].append(integers.data[0])
				elif column == 5: # D12
					integers.get_true_random(min=1, max=12)
					rolls[column].append(integers.data[0])
				elif column == 6: # D20
					integers.get_true_random(min=1, max=20)
					rolls[column].append(integers.data[0])
				elif column == 7: # Roll for abilities
					rolls[column].append(' '.join(map(str, roll_for_abilities())))
				row += 1
				row = len(rolls[column]) - 1
				if column == 0: sound_pool.play_stationary('sounds\\rolls\\coin.wav')
				elif 1 <= column <= 6: sound_pool.play_stationary('sounds\\rolls\\single.wav')
				else: sound_pool.play_stationary('sounds\\rolls\\multiple.wav')
				speech.speak('roll number ' + str(row + 1) + ': ' + rolls[column][row], True)
			if pygame.key.get_pressed()[pygame.K_SPACE]:
				if len(rolls[column]) > 0:
					speech.speak('roll number ' + str(row + 1) + ': ' + rolls[column][row], True)
				else:
					speech.speak('please press enter to roll the dice')
			if pygame.key.get_pressed()[pygame.K_c]:
				if len(rolls[column]) > 0:
					pyperclip.copy(rolls[column][row])
					speech.speak('copied ' + rolls[column][row] + ' to the clipboard')
			if pygame.key.get_pressed()[pygame.K_MINUS]:
				if speech.get_rate() > 0:
					speech.set_rate(speech.get_rate() - 1)
					speech.speak('speech rate decreased to: ' + str(speech.get_rate()), True)
					save_data(speech.get_rate(), 'settings.dat')
				else:
					speech.speak('speech rate at min')
			if pygame.key.get_pressed()[pygame.K_EQUALS]:
				if speech.get_rate() < 10:
					speech.set_rate(speech.get_rate() + 1)
					speech.speak('speech rate increased to: ' + str(speech.get_rate()), True)
					save_data(speech.get_rate(), 'settings.dat')
				else:
					speech.speak('speech rate is at max')
			if pygame.key.get_pressed()[pygame.K_ESCAPE]:
				quit = True

	sound_pool.play_stationary(EXIT)
	time.sleep(.5)
	sys.exit(0)