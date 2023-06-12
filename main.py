from PIL import Image, ImageOps
from colorama import Fore
from pathlib import Path
import glob
import os

VALUE_WARNING = 'only numbers 1 or 2 allowed...'
FORMAT_WARNING = 'only images are allowed...'
SUCCESS = 'success! check the output folder'

class Images:
    def __init__(self):
        self.pic_path = None
        self.case=None
        self.images=[]

    def create_output_dir(self):
        if not os.path.exists('output'):
            os.makedirs('output')

    def intro(self):
        print('\n1 - select a folder of pictures\n2 - select a single picture\n')

        while True:
            try:
                self.case=int(input('>>> '))
                if self.case==1:
                    return (self.folder_pics())
                elif self.case==2:
                    return (self.single_picture())
                else:
                    print(VALUE_WARNING+'\n')
            except ValueError:
                print(VALUE_WARNING+'\n')

    def folder_pics(self):
        self.images = input('folder path: ')+'\\'
        slashes=self.images[:-1]
        pics_counter = 0
        self.images=glob.glob(f"{self.images}*")

        for img in self.images[:]:
            try:
                Image.open(img)
                print(Fore.GREEN+'valid image '+img.replace(slashes,'')[1:]+Fore.RESET)
                pics_counter+=1
            except IOError:
                print(Fore.RED+'invalid image, removing '+img.replace(slashes,'')[1:]+Fore.RESET)
                self.images.remove(img)

        print(f'\nthe number of uploaded pictures: {pics_counter}\n')
        self.multiple_pictures()
    
    def single_picture(self):
        self.create_output_dir()
        image = input(r'picture path: ')
        try:
            im=Image.open(image.replace('"',''))
            filename=Path(image).stem
            im.save(f'output/{filename}_edited.png', 'png')
            print(SUCCESS)
        except IOError:
            print(FORMAT_WARNING)

    def multiple_pictures(self):
        self.create_output_dir()
        for multi_images in self.images:
            im = Image.open(multi_images)

            try:
                watermark=Image.open('watermark.png')
                print('watermark added...')
            except FileNotFoundError:
                print('no watermark.png')

            resized_watermark = ImageOps.contain(watermark, (im.size), Image.LANCZOS)
            main_img_center = (im.width // 2, im.height // 2)
            watermark_center = (resized_watermark.width // 2, resized_watermark.height // 2)
            position = (main_img_center[0] - watermark_center[0], main_img_center[1] - watermark_center[1])

            im.paste(resized_watermark, position, resized_watermark)

            filename=Path(multi_images).stem
            im.save(f'output/{filename}_edited.png', 'png')

        print('\n'+SUCCESS)

def main():
     ima=Images()
     ima.intro()

if __name__ == '__main__':
    main()