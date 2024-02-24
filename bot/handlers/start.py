
import asyncio
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from sqlalchemy import insert, select
from db.model import User
from bot.buttons.reply import *
from db.connect import session
from dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message, state : FSMContext) -> None:
    query = select(User).where(User.chat_id == message.from_user.id)
    user = session.execute(query).fetchone()
    if not user:
        await message.answer(f"Assalomu alaykum ! , {hbold(message.from_user.full_name)}!")
        query = insert(User).values(chat_id=message.from_user.id, username=message.from_user.full_name)
        session.execute(query)
        session.commit()
        await message.answer(f"Bu bo'timiz sizga kunlik qiladigan 🏋️ mashqlarni ko'rsatib beradi",
                             reply_markup=menu_btn())
    else:
        await message.answer(f"Assalomu alaykum ! , {hbold(message.from_user.full_name)}!")
        await message.answer(f"Bu bo'timiz sizga kunlik qiladigan 🏋️ mashqlarni ko'rsatib beradi",
                             reply_markup=menu_btn())



@dp.message(lambda msg : msg.text)
async def echo_handler(msg: Message):
    if msg.text == 'Start ✅':
        await msg.answer("Quydagilardan birontasini tanlang 👇🏿" , reply_markup=menu_btn_start())
    elif msg.text == 'Filial 📍':
        await msg.answer("Bizda hozircha filial yuq")
    elif msg.text == 'News':
        message = await get_info()
        for ietm in message:
            text = f"{ietm.get('date')} \n \n {ietm.get('text')}"
            await msg.answer_photo(photo=ietm.get('photo_url') , caption=text)

    elif msg.text=="Woman 🧍‍♀" or msg.text == "Men 🧍‍♂":
        await msg.answer("Quydagilardan birontasini tanlang 👇🏿" , reply_markup=woman_man_btn())
    elif msg.text == "🔙 back":
        await msg.answer("Quydagilardan birontasini tanlang 👇🏿", reply_markup=menu_btn())
    elif msg.text =="1 oy" or msg.text =="2 oy" or msg.text =="3 oy":
        await msg.answer("Quydagilardan birontasini tanlang 👇🏿", reply_markup=week_btn())





import httpx
from bs4 import BeautifulSoup

async def get_info():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://kun.uz/news/category/sport")
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    news = []
    for i in soup.find_all("div", {"class": "col-md-6"}):
        new = {}
        date = i.find('span')
        text = i.find('a',{'class': 'small-news__title'})
        photo_url = i.find("a" , {"class":"small-news__img"})
        if date: new.update({'date': date.text})
        if text: new.update({'text': text.text})
        if photo_url: new.update({'photo_url':photo_url.find("img")['src']})
        news.append(new)
    return news




