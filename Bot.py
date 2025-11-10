import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WAITING_FOR_TEXT = 1
WAITING_FOR_FILENAME = 2

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loading_message = await update.message.reply_text("sᴛᴀʀᴛɪɴɢ ᴘʀɪᴠᴀᴄʏ ɪɴᴠᴀᴅᴇʀ 🚀....")
    for i in range(3):
        dots = "." * (i + 1)
        await loading_message.edit_text(f"ɪɴᴠᴀᴅɪɴɢ👾⚡{dots}")
        await asyncio.sleep(0.5)
    
    intro_text = """
ᴘʀɪᴠᴀᴄʏ ɪɴᴠᴀᴅᴇʀ ʙᴏᴛ 🤖 🔥

ᴡᴇʟᴄᴏᴍᴇ! ɪ ᴀᴍ ᴘʀɪᴠᴀᴄʏ ɪɴᴠᴀᴅᴇʀ ᴡʜᴏ ᴇxᴛʀᴀᴄᴛ ᴜꜱᴇʀꜱ ᴘʀɪᴠᴀᴛᴇ ᴅᴀᴛᴀ ᴀɴᴅ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ɪɴᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅᴀʙʟᴇ .ᴛxᴛ ꜰɪʟᴇꜱ.

ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ:
/ꜱᴛᴀʀᴛ - ɪɴɪᴛɪᴀᴛᴇꜱ ɪɴᴠᴀᴅɪɴɢ ᴘʀᴏᴄᴇꜱꜱ
/ɪɴᴠᴀᴅᴇ - ᴇxᴛʀᴀᴄᴛ ᴜꜱᴇʀꜱ ᴅᴀᴛᴀ
/ʜᴇʟᴘ - ɢᴇᴛ ʜᴇʟᴘ ᴀʙᴏᴜᴛ ᴜꜱɪɴɢ ᴛʜᴇ ʙᴏᴛ

ʜᴏᴡ ᴛᴏ ᴜꜱᴇ:
1. ꜱᴇɴᴅ /ꜰɪʟᴇ ᴄᴏᴍᴍᴀɴᴅ
2. ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴛᴇxᴛ
3. ᴘʀᴏᴠɪᴅᴇ ᴀ ꜰɪʟᴇɴᴀᴍᴇ
4. ʀᴇᴄᴇɪᴠᴇ ʏᴏᴜʀ .ᴛxᴛ ꜰɪʟᴇ

ꜰᴇᴀᴛᴜʀᴇꜱ:
✅ ᴘʀᴇꜱᴇʀᴠᴇꜱ ꜱᴘᴀᴄᴇꜱ ᴀɴᴅ ɪɴᴅᴇɴᴛᴀᴛɪᴏɴ
✅ ᴍᴀɪɴᴛᴀɪɴꜱ ʟɪɴᴇ ʙʀᴇᴀᴋꜱ ᴀɴᴅ ᴘᴀʀᴀɢʀᴀᴘʜꜱ
✅ ᴋᴇᴇᴘꜱ ꜱᴘᴇᴄɪᴀʟ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ
✅ ᴏʀɪɢɪɴᴀʟ ꜰᴏʀᴍᴀᴛᴛɪɴɢ ɪɴᴛᴀᴄᴛ 💾

ᴘʀɪᴠᴀᴄʏ ɪɴᴠᴀᴅᴇʀ ᴍᴀᴅᴇ ʙʏ :@peteraintyours
"""
    await loading_message.edit_text(intro_text)

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
ʜᴇʟᴘ ɢᴜɪᴅᴇ... 📖
**/file** - ꜱᴛᴀʀᴛ ᴄʀᴇᴀᴛɪɴɢ ᴀ ᴛᴇxᴛ ꜰɪʟᴇ
**/cancel** - ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴏᴘᴇʀᴀᴛɪᴏɴ
"""
    await update.message.reply_text(help_text)

# /file command
async def file_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['waiting_for'] = 'text'
    await update.message.reply_text(
        "📝 ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴛᴇxᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜱᴀᴠᴇ (max 4000 characters):"
    )
    return WAITING_FOR_TEXT

# Handle text input
async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if len(user_text) > 4000:
        await update.message.reply_text("❌ ᴛᴇxᴛ ᴛᴏᴏ ʟᴏɴɢ! ᴍᴀx 4000 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ ᴀʟʟᴏᴡᴇᴅ.")
        return WAITING_FOR_TEXT

    context.user_data['text_to_save'] = user_text
    context.user_data['waiting_for'] = 'filename'
    await update.message.reply_text(
        "✅ ᴛᴇxᴛ ʀᴇᴄᴇɪᴠᴇᴅ! ɴᴏᴡ ᴇɴᴛᴇʀ ᴀ ꜰɪʟᴇɴᴀᴍᴇ (without .txt):"
    )
    return WAITING_FOR_FILENAME

# Handle filename input
async def handle_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filename = update.message.text.strip()
    if not filename:
        await update.message.reply_text("❌ ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ꜰɪʟᴇɴᴀᴍᴇ.")
        return WAITING_FOR_FILENAME

    cleaned_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not cleaned_filename:
        await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ꜰɪʟᴇɴᴀᴍᴇ. Use letters, numbers, spaces, hyphens, underscores.")
        return WAITING_FOR_FILENAME

    text_to_save = context.user_data.get('text_to_save', '')
    full_filename = f"{cleaned_filename}.txt"
    line_count = text_to_save.count('\n') + 1
    char_count = len(text_to_save)

    try:
        with open(full_filename, 'w', encoding='utf-8') as f:
            f.write(text_to_save)

        with open(full_filename, 'rb') as f:
            # Fixed caption - removed Markdown formatting that was causing the error
            caption = (
                f"✅ File Created Successfully!\n\n"
                f"📄 Filename: {full_filename}\n"
                f"📊 Lines: {line_count}\n"
                f"📝 Characters: {char_count}\n"
                f"🎯 Formatting: Preserved exactly\n\n"
                f"All your formatting (spaces, line breaks, indentation) has been maintained!\n"
                f"File created using @Privacy_invaderbot\n"
                f"Privacy fucked by @peteraintyours ⚡"
            )
            
            await update.message.reply_document(
                document=f,
                filename=full_filename,
                caption=caption
                # Removed parse_mode to avoid Markdown parsing issues
            )

        os.remove(full_filename)
        context.user_data.clear()

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"❌ Error creating file: {e}")

    return ConversationHandler.END

# /cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
    context.user_data.clear()
    return ConversationHandler.END

# Invalid messages
async def invalid_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ʀᴇǫᴜᴇꜱᴛᴇᴅ ɪɴꜰᴏ ᴏʀ ᴜꜱᴇ /cancel."
    )
    if context.user_data.get('waiting_for') == 'text':
        return WAITING_FOR_TEXT
    else:
        return WAITING_FOR_FILENAME

# Main function
def main():
    TOKEN = "8386107439:AAHnpR9UEAEldxyt_D5xxunZHLjZv57tTTU"
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('file', file_command)],
        states={
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input),
                MessageHandler(filters.COMMAND & ~filters.Regex('^/cancel$'), invalid_message)
            ],
            WAITING_FOR_FILENAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_filename),
                MessageHandler(filters.COMMAND & ~filters.Regex('^/cancel$'), invalid_message)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(conv_handler)

    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
