import os

from aiogram import Router, F, Bot
from aiogram.filters import BaseFilter, Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import ADMIN_ID
from database.db import (
    get_all_applications,
    get_application_by_id,
    get_new_applications,
    get_statistics,
    update_application_status,
)
from keyboards.kb import (
    BTN_ALL_NEW_APPS,
    BTN_EXPORT_EXCEL,
    BTN_STATISTICS,
    BTN_USER_MENU,
    admin_main_kb,
    user_main_kb,
)
from utils.export import export_to_excel

router = Router(name="admin")


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ADMIN_ID


class IsAdminCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.from_user.id == ADMIN_ID


@router.message(Command("admin"), IsAdmin())
async def cmd_admin(message: Message):
    await message.answer(
        "🔐 <b>Admin panel</b>\n\nChoose an action:",
        reply_markup=admin_main_kb(),
    )


@router.message(Command("admin"))
async def cmd_admin_denied(message: Message):
    await message.answer("⛔ Access denied.")


@router.message(F.text == BTN_ALL_NEW_APPS, IsAdmin())
async def show_new_applications(message: Message):
    applications = await get_new_applications()

    if not applications:
        await message.answer("No new requests.", reply_markup=admin_main_kb())
        return

    text = f"📊 <b>New requests ({len(applications)}):</b>\n\n"
    for app in applications:
        short_desc = app.description[:50] + "..." if len(app.description) > 50 else app.description
        text += (
            f"📌 <b>Request #{app.id}</b>\n"
            f"👤 {app.name}\n"
            f"📱 {app.phone}\n"
            f"📝 {short_desc}\n"
            f"📅 {app.created_at}\n\n"
        )

    await message.answer(text, reply_markup=admin_main_kb())


@router.message(F.text == BTN_STATISTICS, IsAdmin())
async def show_statistics(message: Message):
    stats = await get_statistics()
    await message.answer(
        text=(
            f"📈 <b>Statistics</b>\n\n"
            f"Total: <b>{stats['total']}</b>\n"
            f"New: {stats['new']}\n"
            f"Accepted: {stats['accepted']}\n"
            f"Rejected: {stats['rejected']}\n"
            f"Today: {stats['today']}\n"
            f"Last 7 days: {stats['week']}"
        ),
        reply_markup=admin_main_kb(),
    )


@router.message(F.text == BTN_EXPORT_EXCEL, IsAdmin())
async def export_excel_handler(message: Message):
    applications = await get_all_applications()

    if not applications:
        await message.answer("No data for export.", reply_markup=admin_main_kb())
        return

    wait_message = await message.answer("Generating Excel file...")

    try:
        filepath = await export_to_excel(applications)
        document = FSInputFile(filepath)
        await message.answer_document(document=document, caption="Export completed")

        if os.path.exists(filepath):
            os.remove(filepath)

        await wait_message.delete()
    except Exception as e:
        await wait_message.edit_text(f"Export error: {e}")


@router.message(F.text == BTN_USER_MENU, IsAdmin())
async def back_to_user_menu(message: Message):
    await message.answer("User menu opened.", reply_markup=user_main_kb())


@router.callback_query(F.data.startswith("accept_"), IsAdminCallback())
async def accept_application(callback: CallbackQuery, bot: Bot):
    app_id = int(callback.data.split("_")[1])
    app = await get_application_by_id(app_id)

    if not app:
        await callback.answer("Request not found", show_alert=True)
        return

    await update_application_status(app_id, "accepted")

    try:
        await bot.send_message(
            app.user_id,
            f"✅ Your request #{app_id} has been accepted."
        )
    except Exception:
        pass

    await callback.message.edit_text(
        f"✅ <b>Request #{app_id} accepted</b>\n\n"
        f"👤 {app.name}\n"
        f"📱 {app.phone}\n"
        f"📝 {app.description}"
    )
    await callback.answer("Accepted")


@router.callback_query(F.data.startswith("reject_"), IsAdminCallback())
async def reject_application(callback: CallbackQuery, bot: Bot):
    app_id = int(callback.data.split("_")[1])
    app = await get_application_by_id(app_id)

    if not app:
        await callback.answer("Request not found", show_alert=True)
        return

    await update_application_status(app_id, "rejected")

    try:
        await bot.send_message(
            app.user_id,
            f"❌ Your request #{app_id} has been rejected."
        )
    except Exception:
        pass

    await callback.message.edit_text(
        f"❌ <b>Request #{app_id} rejected</b>\n\n"
        f"👤 {app.name}\n"
        f"📱 {app.phone}\n"
        f"📝 {app.description}"
    )
    await callback.answer("Rejected")


@router.callback_query(F.data.startswith(("accept_", "reject_")))
async def callback_access_denied(callback: CallbackQuery):
    await callback.answer("⛔ Access denied", show_alert=True)