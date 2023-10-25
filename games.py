from aiogram.types import User, Message, InputMediaPhoto
from PIL import Image

from asyncio import sleep as aiosleep
from random import shuffle
from io import BytesIO

from utils import get_state, finish_state
from states import BJStates
from cards import VALUES, SUITS, CARD_WIDTH, CARD_HEIGH, cards_images


def deck_to_str(deck: list[tuple[int, int]]):
    text = ''
    for card in deck:
        suit, value = card
        if value == 1:
            value = 14
        text += f'{VALUES[value]} {SUITS[suit]}, '
    
    return text.rstrip(', ')


def deck_to_image(deck: list[tuple[int, int]]) -> BytesIO:
    n = len(deck)
    im = Image.new(
        'RGB',
        (
            CARD_WIDTH * min(3, n),
            CARD_HEIGH * ((n+min(3, n)-1) // min(3, n))
        )
    )

    cur_upper, cur_left = 0, 0
    for card in deck:
        suit, value = card
        card_image = cards_images[suit][value]
        im.paste(card_image, (cur_left, cur_upper))
        if cur_left + CARD_WIDTH < im.width:
            cur_left += CARD_WIDTH
        else:
            cur_left = 0
            cur_upper += CARD_HEIGH

    im_bytes = BytesIO()
    im_bytes.name = 'cards.png'
    im.save(im_bytes, 'PNG')
    im_bytes.seek(0)

    return im_bytes


def get_bj_summ(deck: list[tuple[int, int]]):
    summ = 0
    for card in deck:
        _, value = card
        if 11 <= value <= 13:
            summ += 10
        elif value == 1:
            summ += 11 if summ + 11 <= 21 else 1
        else:
            summ += value

    return summ


async def bj_process(message: Message, first_user: User, second_user: User):
    for seconds in range(5, 0, -1):
        await message.edit_text(
            f"@{first_user.username}, @{second_user.username} принял игру.\n"
            f"Начало через {seconds} секунд."
        )
        await aiosleep(1)

    for user in (first_user.id, second_user.id):
        await BJStates.bet.set(user=user)

    for seconds in range(10, 0, -1):
        await message.edit_text(
            "<b>Сделайте ставку</b>. Будет выбрана минимальная ставка.\n"
            f"Отправьте <b>целое положительное число</b> в чат. {seconds} секунд"
        )
        await aiosleep(1)
    
    await message.edit_text(
        "<b>Ставки закрыты.</b>"
    )
    
    min_bet = min([
        (await get_state(user=user).get_data()).get('bet', 0)
        for user in (first_user.id, second_user.id)
    ])
    if min_bet == 0:
        text = '<b>Игра отменена.</b>\nОдин из игроков не сделал ставку.'
    else:
        text = f'Выбрана ставка {min_bet}'
    new_message = await message.answer(text)

    if min_bet == 0:
        return
    
    await aiosleep(4)

    decks_count = 3

    deck = [
        (suit, value)
        for _ in range(decks_count)
        for suit in range(4) for value in range(1, 14)
    ]
    shuffle(deck)

    croupier_deck = [deck.pop() for _ in range(1)]
    first_player_deck = [deck.pop() for _ in range(2)]
    second_player_deck = [deck.pop() for _ in range(2)]

    text = (
        f'<b>Выпавшие карты | сумма</b>\n'
        f'<i>Крупье</i>: {deck_to_str(croupier_deck)} | {get_bj_summ(croupier_deck)}\n'
    )

    await new_message.edit_text(text)

    first_player_text = f'<i>{first_user.username}</i>\n<b>Сумма</b>: {get_bj_summ(first_player_deck)}'

    await message.answer_photo(deck_to_image(first_player_deck), first_player_text)

    second_player_text = f'<i>{second_user.username}</i>\n<b>Сумма</b>: {get_bj_summ(second_player_deck)}'

    await message.answer_photo(deck_to_image(second_player_deck), second_player_text)

    for user in (first_user.id, second_user.id):
        await finish_state(user=user)
