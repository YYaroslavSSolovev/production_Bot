from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config import ADMIN_ID, COMPANY_INFO
from database.db import add_application, get_user_applications
from keyboards.kb import (
    BTN_ABOUT_COMPANY,
    BTN_CANCEL,
    BTN_MY_APPLICATIONS,
    BTN_NEW_APPLICATION,
    app_decision_kb,
    cancel_kb,
    user_main_kb,
)

router = Router(name="user")


class ApplicationForm(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_description = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=(
            f"👋 <b>Welcome!</b>\n\n"
            f"I am a demo bot for <b>{COMPANY_INFO['name']}</b>.\n"
            f"This project is built with aiogram 3, FSM, PostgreSQL and Redis.\n\n"
            f"Choose an action:"
        ),
        reply_markup=user_main_kb(),
    )


@router.message(F.text == BTN_CANCEL, StateFilter("*"))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Nothing to cancel.", reply_markup=user_main_kb())
        return

    await state.clear()
    await message.answer("Action cancelled.", reply_markup=user_main_kb())


@router.message(F.text == BTN_NEW_APPLICATION)
async def start_application(message: Message, state: FSMContext):
    await state.set_state(ApplicationForm.waiting_name)
    await message.answer(
        "Step 1/3. Enter your name:",
        reply_markup=cancel_kb()
    )


@router.message(ApplicationForm.waiting_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Name is too short. Try again.")
        return

    await state.update_data(name=name)
    await state.set_state(ApplicationForm.waiting_phone)
    await message.answer("Step 2/3. Enter your phone number:", reply_markup=cancel_kb())


@router.message(ApplicationForm.waiting_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if len(phone) < 6:
        await message.answer("Phone number is too short. Try again.")
        return

    await state.update_data(phone=phone)
    await state.set_state(ApplicationForm.waiting_description)
    await message.answer("Step 3/3. Describe your request:", reply_markup=cancel_kb())


@router.message(ApplicationForm.waiting_description)
async def process_description(message: Message, state: FSMContext, bot: Bot):
    description = message.text.strip()
    if len(description) < 5:
        await message.answer("Description is too short. Try again.")
        return

    data = await state.get_data()
    name = data["name"]
    phone = data["phone"]
    username = message.from_user.username or "no_username"

    app_id = await add_application(
        user_id=message.from_user.id,
        username=username,
        name=name,
        phone=phone,
        description=description,
    )

    await state.clear()

    await message.answer(
        text=(
            f"✅ Request #{app_id} created.\n\n"
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Description: {description}"
        ),
        reply_markup=user_main_kb(),
    )

    try:
        await bot.send_message(
            ADMIN_ID,
            text=(
                f"🔔 <b>New request #{app_id}</b>\n\n"
                f"👤 {name}\n"
                f"📱 {phone}\n"
                f"📝 {description}\n"
                f"🆔 <code>{message.from_user.id}</code>\n"
                f"📎 @{username}"
            ),
            reply_markup=app_decision_kb(app_id),
        )
    except Exception:
        pass


@router.message(F.text == BTN_MY_APPLICATIONS)
async def show_my_applications(message: Message):
    applications = await get_user_applications(message.from_user.id)

    if not applications:
        await message.answer("You have no requests yet.", reply_markup=user_main_kb())
        return

    status_display = {
        "new": "🆕 New",
        "accepted": "✅ Accepted",
        "rejected": "❌ Rejected",
    }

    text = f"📋 <b>Your requests ({len(applications)}):</b>\n\n"
    for app in applications:
        short_desc = app.description[:50] + "..." if len(app.description) > 50 else app.description
        text += (
            f"#{app.id}\n"
            f"Status: {status_display.get(app.status, app.status)}\n"
            f"Date: {app.created_at}\n"
            f"Description: {short_desc}\n\n"
        )

    await message.answer(text, reply_markup=user_main_kb())


@router.message(F.text == BTN_ABOUT_COMPANY)
async def show_about_company(message: Message):
    await message.answer(
        text=(
            f"🏢 <b>{COMPANY_INFO['name']}</b>\n\n"
            f"📞 {COMPANY_INFO['phone']}\n"
            f"📍 {COMPANY_INFO['address']}\n"
            f"🕐 {COMPANY_INFO['hours']}"
        ),
        reply_markup=user_main_kb(),
    )