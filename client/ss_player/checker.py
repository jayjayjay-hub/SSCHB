from PlayerClient import PlayerClient

class Checker:
	def __init__(self, bord, player_number, command):
		self.bord = bord
		self.player_number = player_number
		self.command = command

		def check_out_of_range():
			if self.command[0] < 0 or self.command[0] >= len(self.bord):
				return True
			if self.command[1] < 0 or self.command[1] >= len(self.bord[0]):
				return True
			return False
