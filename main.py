import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- TO'G'RI SOZLAMALAR ---
BOT_TOKEN = "8908099059:AAHgf-KtimF4hqhrkfaNCqcaWBOuxHoqBlc"
SHEET_ID = "1IF1AWRYPkUUPQaK9fPm2rUBCqK5oTo6BdLXARTk1bw4"
# --------------------------

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_builds_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
    df = pd.read_csv(url, header=None, names=['Nomi', 'Turi', 'Rasm'])
    return df

def get_promo_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet2"
    df = pd.read_csv(url, header=None)
    return df

@dp.message(Command("promokodlar"))
async def cmd_promokodlar(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🆕 Yangi o'yinchilar uchun", callback_data="p_new"))
    builder.add(types.InlineKeyboardButton(text="🔥 Eng yangi kodlar", callback_data="p_latest"))
    builder.adjust(1)
    await message.answer("Qaysi turdagi promo-kodlarni ko'rmoqchisiz?", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith("p_"))
async def show_promo_codes(callback_query: types.CallbackQuery):
    option = callback_query.data.split("_")[1]
    try:
        df = get_promo_data()
        if option == "new":
            codes = df[0].dropna().tolist() if 0 in df.columns else []
            title = "🆕 *Yangi o'yinchilar uchun promo-kodlar:*\n\n"
        else:
            codes = df[1].dropna().tolist() if 1 in df.columns else []
            title = "🔥 *Eng so'nggi chiqqan yangi promo-kodlar:*\n\n"
            
        if not codes:
            await callback_query.message.edit_text(
                "ℹ️ Hozircha bu bo'limda kodlar mavjud emas.", 
                reply_markup=InlineKeyboardBuilder().row(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_p")).as_markup()
            )
            return
            
        text = title + "_Nusxalab olish uchun kod ustiga bitta bosing:_\n\n"
        for code in codes:
            code_str = str(code).strip()
            if code_str == "" or "nan" in code_str.lower() or "http" in code_str.lower():
                continue
            text += f"🔑 `{code_str}`\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            
        builder = InlineKeyboardBuilder().row(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_p"))
        await callback_query.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    except Exception as e:
        await callback_query.message.answer("❌ Xatolik yuz berdi.")

@dp.callback_query(lambda c: c.data == "back_p")
async def back_to_promo(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🆕 Yangi o'yinchilar uchun", callback_data="p_new"))
    builder.add(types.InlineKeyboardButton(text="🔥 Eng yangi kodlar", callback_data="p_latest"))
    builder.adjust(1)
    await callback_query.message.edit_text("Qaysi turdagi promo-kodlarni ko'rmoqchisiz?", reply_markup=builder.as_markup())

@dp.message(Command("buildlar"))
async def cmd_buildlar(message: types.Message):
    builder = InlineKeyboardBuilder()
    types_list = ["Thrust", "Slash", "Strike", "Spirit"]
    for t in types_list:
        builder.add(types.InlineKeyboardButton(text=t, callback_data=f"type_{t}"))
    builder.adjust(2)
    await message.answer("Kerakli personaj turini (Type) tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith("type_"))
async def show_characters_by_type(callback_query: types.CallbackQuery):
    chosen_type = callback_query.data.split("_")[1]
    try:
        df = get_builds_data()
        df['Turi'] = df['Turi'].astype(str).str.strip()
        filtered_df = df[df['Turi'] == chosen_type]
        
        builder = InlineKeyboardBuilder()
        for index, row in filtered_df.iterrows():
            builder.add(types.InlineKeyboardButton(text=str(row['Nomi']), callback_data=f"pers_{index}"))
        builder.adjust(1)
        builder.row(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_types"))
        
        await callback_query.message.edit_text(text=f"*{chosen_type}* turidagi personajni tanlang:", reply_markup=builder.as_markup(), parse_mode="Markdown")
    except Exception as e:
        await callback_query.message.answer("Xatolik yuz berdi.")

@dp.callback_query(lambda c: c.data == "back_to_types")
async def back_to_types(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    types_list = ["Thrust", "Slash", "Strike", "Spirit"]
    for t in types_list:
        builder.add(types.InlineKeyboardButton(text=t, callback_data=f"type_{t}"))
    builder.adjust(2)
    await callback_query.message.edit_text("Kerakli personaj turini (Type) tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith("pers_"))
async def send_character_build(callback_query: types.CallbackQuery):
    row_index = int(callback_query.data.split("_")[1])
    try:
        df = get_builds_data()
        character_row = df.loc[row_index]
        name = character_row['Nomi']
        photo_url = str(character_row['Rasm']).strip()
        
        await callback_query.message.delete()
        if photo_url and photo_url.startswith("http"):
            await callback_query.message.answer_photo(photo=photo_url, caption=f"🔥 *{name}* uchun eng yaxshi build!", parse_mode="Markdown")
        else:
            await callback_query.message.answer(f"ℹ️ *{name}* uchun rasm topilmadi.", parse_mode="Markdown")
    except Exception as e:
        await callback_query.message.answer("Xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
  
