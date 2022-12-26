import telebot
import config
from telebot import types
import random
import os
from PIL import Image, ImageDraw, ImageFont

bot = telebot.TeleBot(config.TOKEN)
# логика работы бота
def image(nums):
    number = nums
    numbers = []
    rub = Image.open("img/rub.png")
    for n in str(number):
        numbers.append(int(n))

        def numswidth(nums):
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
    with Image.open("img/org.png").convert("RGBA") as base:
        imagewidth = base.size[0]
        # numswidth = len(numbers) * 53  + 74
        numsw = numswidth(numbers) + 74
        x_end = int(imagewidth / 2 - numsw / 2 + numsw - 74)
        x = int(imagewidth / 2 - numsw / 2)
        x_end = x + numsw - 74
        y = 717
        # меняем дату
        first = random.choice(range(1, 3))

        def second(first):
            if int(first) == 2:
                return random.choice(range(1, 3))
            else:
                return random.choice(range(1, 10))
        timetext = f"{first}{second(first)}:{random.choice(range(1, 6))}{random.choice(range(1, 10))}"
        time = ImageDraw.Draw(base)
        font = ImageFont.truetype("fonts/SofiaBold.ttf", 36)
        time.text((70, 27), timetext, "#a7a7a7", font=font)
        # меняем зарядку
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
        return base


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет!\nЭтот бот сделает тебе нужный скриншотик <b>из числа, которое ты введешь!</b>\n\n<i>~Чтобы начать - просто введи число <b>без пробелов и лишних знаков</b> и бот отправит тебе то, что тебе надо~</i>", parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def sending_photo(message):
    print(message.from_user.id)
    try:
        image(int(message.text))
    except ValueError:
        bot.send_message(message.chat.id, "Нужно вводить число без лишних знаков!")
    else:
        if '0' in message.text and len(message.text) != 1:
            bot.send_message(message.chat.id, "Бот обрабатывает фотографию...\nПодождите пару секунд..")
            bot.send_photo(message.chat.id, image(int(message.text)), "К сожалению, цифра ноль пока что не получила такой загар как другие цифры, поэтому она белая")
            bot.send_message(message.chat.id, "Замечательно!\nЧтобы продолжить, введи число")
        elif int(message.text) == 0:
            bot.send_message(message.chat.id, "Ну кто переводит 0 рублей?? Введите другое число!")
        else:
            bot.send_message(message.chat.id, "Бот обрабатывает фотографию...\nПодождите пару секунд..")
            bot.send_photo(message.chat.id, image(int(message.text)))
            bot.send_message(message.chat.id, "Замечательно!\nЧтобы продолжить, введи число")




if __name__ == '__main__':
    bot.infinity_polling()

