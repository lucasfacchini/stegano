from PIL import Image
from random import randint

class Stegano(object):

	def __init__(self, input_path):
		self.input_path = input_path
		self.img_input = Image.open(self.input_path)
		self.img_output = None
		self.img_output_diff = None

	def encode(self, content_str):
		self.img_output = Image.new(self.img_input.mode, self.img_input.size)
		self.img_output_diff = Image.new(self.img_input.mode, self.img_input.size)
		pixel_map = self.img_input.load()
		pixels_new = self.img_output.load()
		pixels_new_diff = self.img_output_diff.load()

		for x in range(self.img_output.size[0]):
		    for y in range(self.img_output.size[1]):
		        pixels_new_diff[x, y] = pixels_new[x, y] = pixel_map[x, y]

		sectors = self.generate_sectors(len(content_str), self.img_output.size[0])

		for i in range(0, len(sectors) - 1):
			pixel_range = (sectors[i], sectors[i+1])
			modulus_sector = self.sum_sector(pixel_range, pixels_new, self.img_output.size[1]) % 128
			char_value = ord(content_str[i])

			for j in range(0, abs(modulus_sector - char_value)):
				x, y, rgb = self.random_position(pixel_range, pixels_new, modulus_sector > char_value)
				if (modulus_sector < char_value):
					pixels_new[x, y] = (rgb[0], rgb[1], rgb[2] + 1)
				elif (modulus_sector > char_value):
					pixels_new[x, y] = (rgb[0], rgb[1], rgb[2] - 1)
				pixels_new_diff[x, y] = (255, 0, 0)

	def random_position(self, pixel_range, pixels_new, difference):
		while True:
			x, y = randint(pixel_range[0], pixel_range[1] - 1), randint(0, self.img_output.size[1]-1)
			rgb = pixels_new[x,y]
			if difference and rgb[2] == 0:
				continue
			if not difference and rgb[2] == 255:
				continue
			return x, y, rgb

	def save(self, output_path, diff_output_path=None):
		self.img_output.save(output_path, 'PNG')
		if (diff_output_path):
			self.img_output_diff.save(diff_output_path, 'PNG')

	def generate_sectors(self, len_str, img_width):
		sector_size = int((img_width-1) / len_str)
		sectors = []
		for i in range(0, len_str + 1):
			sectors.append(sector_size * i)
		return sectors

	def sum_sector(self, pixel_range, pixel_map, height):
		result = 0
		for x in range(pixel_range[0], pixel_range[1]):
			for y in range(height):
				result = result + sum(pixel_map[x, y])
		return result

	def decode(self, len_str):
		pixel_map = self.img_input.load()
		sectors = self.generate_sectors(len_str, self.img_input.size[0])
		content_str = ''
		for i in range(0, len(sectors) - 1):
			pixel_range = (sectors[i], sectors[i+1])
			content_str = content_str + (chr(self.sum_sector(pixel_range, pixel_map, self.img_input.size[1]) % 128))
		return content_str