from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# ----- Main Keyboard -----#
info_btn = KeyboardButton("📝 Инфо 📝")
login_btn = KeyboardButton("🔑 Вход 🔑")
projects_btn = KeyboardButton("📁 Мои проекты 📁")
create_ecs_btn = KeyboardButton("💻 Создать ECS 💻")

main_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(info_btn, login_btn, projects_btn, create_ecs_btn)


# ----- Cancel Login Keyboard ----- #
canlec_inl_btn = InlineKeyboardButton("Отмена", callback_data='Отмена')

cancel_buttons = InlineKeyboardMarkup().add(canlec_inl_btn)


# ----- Dynamic Buttons ----- #
def gen_markup(texts: list, prefix: list, row_width: int) -> InlineKeyboardMarkup:
	markup = InlineKeyboardMarkup(row_width=row_width)
	for i in range(len(texts)):
		markup.insert(InlineKeyboardButton(f"{texts[i]}", callback_data=f"{prefix[i]}"))
	return markup