from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

BTN_NEW_APPLICATION = "📝 Create request"
BTN_MY_APPLICATIONS = "📋 My requests"
BTN_ABOUT_COMPANY = "ℹ️ About"
BTN_CANCEL = "❌ Cancel"

BTN_ALL_NEW_APPS = "📊 New requests"
BTN_STATISTICS = "📈 Statistics"
BTN_EXPORT_EXCEL = "📤 Export to Excel"
BTN_USER_MENU = "👤 User menu"

BTN_ACCEPT = "✅ Accept"
BTN_REJECT = "❌ Reject"


def user_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_NEW_APPLICATION)],
            [KeyboardButton(text=BTN_MY_APPLICATIONS)],
            [KeyboardButton(text=BTN_ABOUT_COMPANY)],
        ],
        resize_keyboard=True,
    )


def admin_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ALL_NEW_APPS)],
            [KeyboardButton(text=BTN_STATISTICS)],
            [KeyboardButton(text=BTN_EXPORT_EXCEL)],
            [KeyboardButton(text=BTN_USER_MENU)],
        ],
        resize_keyboard=True,
    )


def cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_CANCEL)]],
        resize_keyboard=True,
    )


def app_decision_kb(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=BTN_ACCEPT, callback_data=f"accept_{app_id}"),
                InlineKeyboardButton(text=BTN_REJECT, callback_data=f"reject_{app_id}"),
            ]
        ]
    )