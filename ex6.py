import ex6_helper


def otsu(image):
	list_of_thre = [''] * 255
	for thresh in range(255):
		num_b = 0
		num_w = 0
		sum_b = 0
		sum_w = 0
		for row in image:
			for pixel in row:
				if pixel < thresh:
					num_b += 1
					sum_b += pixel
				else:
					num_w += 1
					sum_w += pixel
		if num_w == 0 or num_b == 0 or sum_w == 0 or sum_b == 0:
			list_of_thre[thresh] = 0
			continue
		else:
			avg_b = sum_b / num_b
			avg_w = sum_w / num_w
			current_thresh = num_b * num_w * (avg_b - avg_w) ** 2
			list_of_thre[thresh] = current_thresh
			continue
	maximal_thresh = list_of_thre.index(max(list_of_thre))
	return maximal_thresh


def otsu_loaded(image_filename):
	image = ex6_helper.load_image(image_filename)
	return otsu(image)


#print(otsu_loaded('test20.jpg'))


def threshold_filter(image):
	max_val = otsu(image)
	for row in range(len(image)):
		for pixel in range(len(image[row])):
			# current_pixel = image[row][pixel]
			if pixel < max_val:
				image[row][pixel] = 0
			else:
				image[row][pixel] = 255
	return image


# print(threshold_filter(ex6_helper.load_image('test20.jpg')))



def validity_check(i, j, image):
	if i < 0:
		return False
	if j < 0:
		return False
	if i > len(image) - 1:
		return False
	if j > len(image[0]) - 1:
		return False
	else:
		return True


def apply_filter(image, filter):
	new_image = [['' for i in range(len(image[0]))] for j in range(len(image))]
	for row in range(len(image)):
		for col in range(len(image[0])):
			new_pixel_sum = 0
			for i in range(row - 1, row + 2):
				for j in range(col - 1, col + 2):
					if not validity_check(i, j, image):
						new_pixel_sum += image[row][col] * filter[row - (i + 1)][col - (j + 1)]
					else:
						new_pixel_sum += image[i][j] * filter[row - (i + 1)][col - (j + 1)]
			if new_pixel_sum == float:
				new_image[row][col] = int(new_pixel_sum)
			elif abs(new_pixel_sum) > 255:
				new_image[row][col] = 255
			elif new_pixel_sum < 0 and new_pixel_sum > -255:
				new_image[row][col] = abs(new_pixel_sum)
			else:
				new_image[row][col] = new_pixel_sum
	return new_image


image_list = [[4,45,65,250,6,25],[170,150,40,0,52,4],[0,4,7,0,190,5]]
filter_list = [[2,-1,2],[-1,5,-1],[2,-1,2]]
#print(apply_filter(image_list, filter_list))


def detect_edges(image):
	new_image = [['' for i in range(len(image[0]))] for j in range(len(image))]
	for row in range(len(image)):
		for col in range(len(image[0])):
			pixel_neighbor_sum = 0 - image[row][col]
			for i in range(row - 1, row + 2):
				for j in range(col - 1, col + 2):
					if not validity_check(i, j, image):
						pixel_neighbor_sum += image[row][col]
					else:
						pixel_neighbor_sum += image[i][j]
			neighbor_avg = int(pixel_neighbor_sum / 8)
			new_value = image[row][col] - neighbor_avg
			if new_value < 0:
				new_image[row][col] = abs(new_value)
			else:
				new_image[row][col] = new_value
	return new_image

#print(detect_edges(image_list))


def downsample_by_3(image):
	reduced_image = [['' for i in range(0, len(image[0]), 3)] for j in range(0, len(image), 3)]
	for row in range(0, len(image), 3):
		for col in range(0, len(image[0]), 3):
			pixel_neighbor_sum = 0
			for i in range(row, row + 3):
				for j in range(col, col + 3):
					pixel_neighbor_sum += image[i][j]
			neighbors_avg = int(pixel_neighbor_sum / 9)
			reduced_image[row//3][col//3] = neighbors_avg
	return reduced_image

#print(downsample_by_3(image_list))


def calculate_diagonal(image):
	current_diagonal = ((len(image) ** 2) + (len(image[0]) ** 2)) ** 0.5
	return current_diagonal


def downsample(image, max_diagonal_size):
	slant = calculate_diagonal(image)
	while slant > max_diagonal_size:
		image = downsample_by_3(image)
		slant = calculate_diagonal(image)
		if slant > max_diagonal_size:
			continue
		else:
			return image

new_image = [[1 for i in range(9)] for j in range(9)]
#print(downsample(new_image, 2**0.5))

img = ex6_helper.load_image("test20.jpg")
# img2 = detect_edges(img)
# result_checker = []
# for i in range(len(img)):
# 	result_checker.append(img[i]+img2[i])
# ex6_helper.show(result_checker)
dots = ex6_helper.pixels_on_line(img,1,17,False)
new_img = []
for _ in range(len(img)):
	new_img.append([0]*len(img[0]))

for dot in dots:
	new_img[dot[0]][dot[1]] = 255

ex6_helper.show(new_img)
print(dots)
