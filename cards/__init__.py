from PIL import Image

from collections import defaultdict

SUITS = ['Крести', 'Буби', 'Черви', 'Пики']
VALUES = [str(i) for i in range(11)] + ['Валет', 'Дама', 'Король', 'Туз']

CARDS_PATH = 'cards/cards.png'
CARD_WIDTH = 79
CARD_HEIGH = 123


cards_images: dict[int, dict[int, Image.Image]] = defaultdict(dict)

with Image.open(CARDS_PATH) as cards_image:
    for suit in range(len(SUITS)):
        upper = suit*CARD_HEIGH
        lower = upper + CARD_HEIGH
        left = 0
        for value in range(1, 14):
            right = left + CARD_WIDTH
            card_image = cards_image.crop((left, upper, right, lower))
            left += CARD_WIDTH
            cards_images[suit][value] = card_image

    shirt_upper = 4*CARD_HEIGH
    shirt_lower = upper + CARD_HEIGH
    shirt_left = 2*CARD_WIDTH
    shirt_right = left + CARD_WIDTH
    card_shirt = cards_image.crop(
        (shirt_left, shirt_upper, shirt_right, shirt_lower)
    )
