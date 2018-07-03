#BFS宽度优先搜索走迷宫
import cv2
import numpy as np
from queue import Queue
import time

class Maze:
	def __init__(self, img_file):
		self._img_file = img_file
		self.img = cv2.imread(img_file)
		self._img = self._thresholding(img_file)
		self._xsize = self._img.shape[0]
		self._ysize = self._img.shape[1]
		self.end = (834, 1481)


	def _thresholding(self, img_file):
		img = cv2.imread(img_file, 0)
		_, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
		return img

	def _is_white(self, pixel):
		if pixel == 255:
			return True

	def _get_neighbour(self, position):
		x, y = position
		neightbours = []
		if x > 0:
			neightbours.append((x-1, y))
		if x < self._xsize-1:
			neightbours.append((x+1, y))
		if y > 0:
			neightbours.append((x, y-1))
		if y < self._ysize-1:
			neightbours.append((x, y+1))
		return neightbours

	def init_start(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
			cv2.circle(self.img, (x, y), 5, (0, 0, 255), -1)
			cv2.circle(self.img, self.end[::-1], 5, (0, 255, 0), -1)
			self.start = (y, x)

	def solve(self):
		print("Start solving...")
		pixels = self._img.copy()
		queue = Queue()
		queue.put([self.start])
		while not queue.empty():
			path = queue.get() 
			pixel = path[-1]
			if pixel == self.end:
				return path
			for adjacent in self._get_neighbour(pixel):
				x,y = adjacent
				if self._is_white(pixels[x,y]):
					pixels[x,y] = 127 # see note
					new_path = list(path)
					new_path.append(adjacent)
					queue.put(new_path)
		raise RuntimeError("Queue has been exhausted. No answer was found.")

	def restart(self):
		self.img = cv2.imread(self._img_file)
		self._img = self._thresholding(self._img_file)
A=Maze('test.jpg')
print(A._img.shape)

if __name__ == '__main__':
	M = Maze("test.jpg")
	cv2.namedWindow('maze')
	a = cv2.setMouseCallback('maze', M.init_start)

	
	print("Instruction:\n", "Press left button to select start point, then press 's' to start solving.")

	while(1):
		cv2.imshow('maze', M.img)
		k = cv2.waitKey(1)
		if k == 27:
			break
		elif k == ord('s'):
			try:
				tstart = time.time()
				path = M.solve()
				tend = time.time()
				print("Time cost:", tend - tstart)
			except RuntimeError as e:
				print("No solution found. Please try again.")
				M.restart()
				continue
			for pos in path:
				M.img[pos] = (0, 0, 255)
			print("To restart, press 'r'.")
		elif k == ord('r'):
			M.restart()
			print("Instruction:\n", "Press left button to select start point, then press 's' to start solving.")