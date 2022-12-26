import random
import os
from PIL import Image, ImageDraw, ImageFont


class ImageWorker:
    def __init__(self, nums):
        number = nums
        numbers = []
        rub = Image.open("img/rub.png")
        for n in str(number):
            numbers.append(int(n))
        with Image.open("img/org.png").convert("RGBA") as base:
            imagewidth = base.size[0]
            # numswidth = len(numbers) * 53  + 74
            numsw = self.numswidth(numbers) + 74
            x_end = int(imagewidth / 2 - numsw / 2 + numsw - 74)
            x = int(imagewidth / 2 - numsw / 2)
            x_end = x + numsw - 74
            y = 717

            #меняем дату
            first = random.choice(range(1, 3))
            def second(first):
                if int(first) == 2:
                    print(first)
                    return random.choice(range(1, 3))
                else:
                    return random.choice(range(1, 10))

            timetext = f"{first}{second(first)}:{random.choice(range(1, 6))}{random.choice(range(1, 10))}"
            time = ImageDraw.Draw(base)
            font = ImageFont.truetype("fonts/SofiaBold.ttf", 36)
            time.text((70, 27), timetext, "#a7a7a7", font=font)
            #меняем зарядку
            batteryimagename = random.choice(os.listdir('img/power/'))
            batteryimage = Image.open(f'img/power/{batteryimagename}')
            base.paste(batteryimage, (950, 39))

            for n in range(0, len(numbers)):
                nimage = Image.open(f"img/rubs/{numbers[n]}.png")
                base.paste(nimage, (x, y))
                cutnumbers = numbers[slice(n + 1, len(numbers))]
                if len(cutnumbers) % 3 == 0 and cutnumbers:
                    x += 22
                x += nimage.size[0]
            base.paste(rub, (x, y))
            base.show()
            return base


    def numswidth(self, nums):
        w = 0
        for n in nums:
            nsize = Image.open(f"img/rubs/{n}.png").size[0]
            w += nsize
        if len(nums) in range(4, 7):
                w += 22
        elif len(nums) in range(7, 10):
                w += 44
        elif len(nums) in range(10, 13):
                w += 66
        elif len(nums) in range(13, 16):
                w += 88

        return w
