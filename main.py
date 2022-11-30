import pyautogui
from PIL import ImageGrab
from random import randint


class BloodWeb:
    def __init__(self, pixel_color):
        self.pixel_color = pixel_color

        self.ready = True
        self.image = None
        self.search_size = None
        self.start_x = 0
        self.start_y = 0
        self.image_pixels = None

    def ready_to_grab(self):
        if self.ready:
            return True
        return False

    def grab_image(self):
        self.image = ImageGrab.grab()
        image_size = self.image.size
        self.search_size = tuple(int(0.7 * i) for i in image_size)
        self.start_x = int((image_size[0] - self.search_size[0]) / 2)
        self.start_y = int((image_size[1] - self.search_size[1]) / 2)
        self.image_pixels = self.image.load()

    def get_white_pixels(self):
        white_pixel_positions = []
        for y in range(self.start_y, self.search_size[1], 3):
            for x in range(self.start_x, self.search_size[0], 3):
                self.pixel_color = self.image_pixels[x, y]
                if self.pixel_color == (255, 255, 255):
                    white_pixel_positions.append((x, y))
        return white_pixel_positions[randint(0, len(white_pixel_positions) - 1)]

    def select_item(self, x, y):
        pyautogui.mouseDown(x=x, y=y, button='left')

    def deselect_item(self):
        pyautogui.mouseUp(button='left')

    def check_if_still_white(self, x, y):
        new_image = ImageGrab.grab().load()
        if new_image[x, y] != self.pixel_color:
            return False
        return True


blood_web = BloodWeb((255, 255, 255))

def main_loop():
    while True:
        blood_web.grab_image()
        tx, ty = blood_web.get_white_pixels()
        while blood_web.check_if_still_white(tx, ty):
            blood_web.select_item(tx, ty)
        blood_web.deselect_item()


if __name__ == '__main__':
    main_loop()


