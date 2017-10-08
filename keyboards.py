import telebot

started_keyboard = telebot.types.ReplyKeyboardMarkup(True)
started_keyboard.row("Все организации")
started_keyboard.row("Поиск по ID", "Добавить организацию")
started_keyboard.row("Другое")

orgs_keyboard = telebot.types.ReplyKeyboardMarkup(True)
orgs_keyboard.row("Школы \U0001F3EB", "Больницы\U0001F3E5", "Спортивные\U0001F3C0")
orgs_keyboard.row("Развлечения\U0001F3A4", "Парикмахерские\U0001F487", "Магазины\U0001F6CD")
orgs_keyboard.row("Такси\U0001F695", "Ремонт | Сервис\U0001F6E0", "Компании\U0001F465")
orgs_keyboard.row("Кафе | Бары\U0001F374", "Другие\u27A1\uFE0F")
orgs_keyboard.row("\u2B05\uFE0F На главную")

other_keyboard = telebot.types.ReplyKeyboardMarkup(True)
other_keyboard.row("Вопросы и предложения", "Нашли ошибку?")
other_keyboard.row("Хочу телеграм-бота!")
other_keyboard.row("\u2B05\uFE0F На главную")