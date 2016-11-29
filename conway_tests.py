import matplotlib.pyplot as plt
from random import randint
from copy import deepcopy
import numpy as np
import unittest, sys
import math
from GoLquadtree import GoLNode, GoLQuadTree
from conway import ConwayGOLGrid, ConwayGOLCell
import os, psutil, gc
from datetime import datetime

def memory_usage_psutil():
	"""
	Returns the current memory usage of python
	"""
	process = psutil.Process(os.getpid())
	mem = process.memory_info()[0] / float(2**20)
	return mem

if __name__ == '__main__':
	# This is going to run multiple sizes of the game with each different
	# version and time and compare memory usage of all versions.  

	grid_sizes = [16, 32, 64, 128]#, 256]	
	versions = ["Naive", "Optimized", "QuadTree"]
	average_naive = []
	average_opt = []
	average_quad = []
	naive_time = []
	opt_time = []
	quad_time = []
	
	for grid in grid_sizes:

		start_cells = []
		
		for x in range(grid):
			for y in range(grid):
				if randint(0, 100) < 30:
					start_cells.append((x,y))

		
		
		for version in range(3):
			print "Starting", versions[version], " at grid size", grid, "random"
			start = datetime.now()
			game = ConwayGOLGrid(grid, grid, start_cells, version, "B3/S23")
			memory_used = memory_usage_psutil()
			count = 0

			while(count < 100 and game.update()):
				count += 1

				memory_used += memory_usage_psutil()

			final = datetime.now()-start
			memory_used /= (count + 1)

			game = []
			gc.collect()

			if version == 0:
				average_naive.append(memory_used)
				naive_time.append(int(final.total_seconds()))
			elif version == 1:
				average_opt.append(memory_used)
				opt_time.append(int(final.total_seconds()))
			else:
				average_quad.append(memory_used)
				quad_time.append(int(final.total_seconds()))
				
			
	
	fix, ax = plt.subplots()

	index = np.arange(len(grid_sizes))
	bar_width = 0.35
	error_config = {'ecolor':'0.3'}

	rects_naive = plt.bar(index, average_naive, bar_width, color='b', error_kw=error_config, label='Naive')
	rects_opt = plt.bar(index+bar_width, average_opt, bar_width, color='r', error_kw=error_config, label='Optimized')
	rects_quad = plt.bar(index+(2*bar_width), average_quad, bar_width, color='g', error_kw=error_config, label='QuadTree')

	plt.xlabel('Grid Size')
	plt.ylabel('Average Memory Usage')
	plt.title('Memory Used by Different Optimization Strategies')

	plt.xticks(index + (2 * bar_width / 3), grid_sizes)
	plt.legend(loc=2)

	plt.tight_layout()
	#plt.show()
	plt.savefig('average_random.png')
	
	
	fix, ax = plt.subplots()

	index = np.arange(len(grid_sizes))
	bar_width = 0.35
	error_config = {'ecolor':'0.3'}

	rects_naive = plt.bar(index, naive_time, bar_width, color='b', error_kw=error_config, label='Naive')
	rects_opt = plt.bar(index+bar_width, opt_time, bar_width, color='r', error_kw=error_config, label='Optimized')
	rects_quad = plt.bar(index+(2*bar_width), quad_time, bar_width, color='g', error_kw=error_config, label='QuadTree')

	plt.xlabel('Grid Size')
	plt.ylabel('Execution Time for 100 Generations')
	plt.title('Time Taken by Different Optimization Strategies')

	plt.xticks(index + (2 * bar_width / 3), grid_sizes)
	plt.legend(loc=2)

	plt.tight_layout()
	#plt.show()
	plt.savefig('time_random.png')

	
	average_naive = []
	average_opt = []
	average_quad = []
	naive_time = []
	opt_time = []
	quad_time = []
	
	for grid in grid_sizes:

		start_cells = [(grid/2, grid/2)]		

		
		
		for version in range(3):
			print "Starting", versions[version], " at grid size", grid, "random"
			start = datetime.now()
			game = ConwayGOLGrid(grid, grid, start_cells, version, "B1/S12")
			memory_used = memory_usage_psutil()
			count = 0

			while(count < 100 and game.update()):
				count += 1

				memory_used += memory_usage_psutil()

			final = datetime.now() - start
			memory_used /= (count + 1)

			game = []
			gc.collect()

			if version == 0:
				average_naive.append(memory_used)
				naive_time.append(int(final.total_seconds()))
			elif version == 1:
				average_opt.append(memory_used)
				opt_time.append(int(final.total_seconds()))
			else:
				average_quad.append(memory_used)
				quad_time.append(int(final.total_seconds()))
				
			
	
	fix, ax = plt.subplots()

	index = np.arange(len(grid_sizes))
	bar_width = 0.35
	error_config = {'ecolor':'0.3'}

	rects_naive = plt.bar(index, average_naive, bar_width, color='b', error_kw=error_config, label='Naive')
	rects_opt = plt.bar(index+bar_width, average_opt, bar_width, color='r', error_kw=error_config, label='Optimized')
	rects_quad = plt.bar(index+(2*bar_width), average_quad, bar_width, color='g', error_kw=error_config, label='QuadTree')

	plt.xlabel('Grid Size')
	plt.ylabel('Average Memory Usage')
	plt.title('Memory Used by Different Optimization Strategies')

	plt.xticks(index + (2 * bar_width / 3), grid_sizes)
	plt.legend(loc=2)

	plt.tight_layout()
	#plt.show()
	plt.savefig('mem_triangle.png')

	
	fix, ax = plt.subplots()

	index = np.arange(len(grid_sizes))
	bar_width = 0.35
	error_config = {'ecolor':'0.3'}

	rects_naive = plt.bar(index, naive_time, bar_width, color='b', error_kw=error_config, label='Naive')
	rects_opt = plt.bar(index+bar_width, opt_time, bar_width, color='r', error_kw=error_config, label='Optimized')
	rects_quad = plt.bar(index+(2*bar_width), quad_time, bar_width, color='g', error_kw=error_config, label='QuadTree')

	plt.xlabel('Grid Size')
	plt.ylabel('Execution Time for 100 Generations')
	plt.title('Time Taken by Different Optimization Strategies')

	plt.xticks(index + (2 * bar_width / 3), grid_sizes)
	plt.legend(loc=2)

	plt.tight_layout()
	#plt.show()
	plt.savefig('time_triangle.png')

	
	

























