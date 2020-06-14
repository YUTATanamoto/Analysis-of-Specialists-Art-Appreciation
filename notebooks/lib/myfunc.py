import cv2
import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class FractalParser():
    def __init__(self):
        pass

    def get_fractal_dimension(self, image_file, max_box_size=100, min_box_size=1, show_figures=False):
        image = cv2.imread(image_file)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret2, image_otsu = cv2.threshold(image_gray, 0, 255, cv2.THRESH_OTSU)
        image_binalized = image_otsu==0
        width, height = image_otsu.shape[:2]
        box_size = max_box_size
        box_sizes = []
        box_counts = []
        while box_size >=  min_box_size:
            count = self.count_box(
                image_array = image_binalized,
                box_size = box_size
            )
            box_sizes.append(box_size)
            box_counts.append(count)
            box_size = int(box_size / 2)
        log_box_sizes = np.log(box_sizes)
        log_box_counts = np.log(box_counts)
        fractal_dimension = -np.polyfit(log_box_sizes, log_box_counts, 1)[0]
        if show_figures:
            fig = plt.figure()
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.set_title("original")
            ax1.imshow(image)
            ax2 = fig.add_subplot(1, 2, 2)
            ax2.set_title("binalized")
            ax2.imshow(image_binalized)
            plt.show()
        return fractal_dimension

    def count_box(self, image_array, box_size):
        width, height = image_array.shape[:2]
        num_grid_x = math.ceil(width/box_size)
        num_grid_y = math.ceil(height/box_size)
        count = 0
        for grid_index_x in range(num_grid_x):
            for grid_index_y in range(num_grid_y):
                pixels_in_box = image_array[
                    grid_index_x * box_size : (grid_index_x+1) * box_size,
                    grid_index_y * box_size : (grid_index_y+1) * box_size
                ].flatten()
                if np.sum(pixels_in_box) > 0:
                    count += 1
        return count

if __name__=='__main__':
    image_file = "./koch.png"
    fractal_parser = FractalParser()
    fractal_dimension = fractal_parser.get_fractal_dimension(
        image_file = image_file,
        max_box_size = 1000,
        min_box_size = 5,
        show_figures = True
    )
    print(fractal_dimension)
