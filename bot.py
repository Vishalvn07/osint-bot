"""

Bot developed by @Lawxsz credits if you want to redistribute or make new bots with this base please. 
Recommendations or code improvements are accepted

For log analysis we use https://github.com/Lawxsz/log-finder/ C++ version, open source and secure! 

To get Wordlist look for Cloudlogs on telegram or forums, they are free or paid! any of them works fine!

"""


from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import sqlite3
import shutil
from datetime import datetime

TOKEN = 'BOT_TOKEN'
admin_id = 1468758771  # your admin ID
db_path = 'settings/osint_bot.db'
scanned_files_folder = 'scanned_files'

def init_db():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            tokens INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            user_id INTEGER,
            search_term TEXT,
            timestamp TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            count INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def count(update: Update, context: CallbackContext):
    if update.message.from_user.id != admin_id:
        update.message.reply_text("⛔ You are not authorized to use this command.")
        return

    try:
        if len(context.args) != 1 or not context.args[0].isdigit():
            update.message.reply_text("⚠️ Please provide a valid number. Usage: /count NUMBERS")
            return
        
        param_count = int(context.args[0])
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        c.execute('INSERT INTO Parameters (count) VALUES (?)', (param_count,))
        conn.commit()
        
        conn.close()
        
        update.message.reply_text(f"✅ Parameters updated successfully! 🎉 New count: {param_count}")

    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {str(e)}")


def add_tokens(user_id, tokens):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, tokens) VALUES (?, ?)', (user_id, 0))
    cursor.execute('UPDATE users SET tokens = tokens + ? WHERE user_id = ?', (tokens, user_id))
    conn.commit()
    conn.close()

def get_tokens(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT tokens FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


# get wordlist
def get_wordlists():
    wordlist_folder = 'cloud'
    return [f for f in os.listdir(wordlist_folder) if os.path.isfile(os.path.join(wordlist_folder, f))]

def get_file_size(file_path):
    size_bytes = os.path.getsize(file_path)
    if size_bytes >= 1_073_741_824:  # GB
        return f"{size_bytes / 1_073_741_824:.2f} GB"
    elif size_bytes >= 1_048_576:  # MB
        return f"{size_bytes / 1_048_576:.2f} MB"
    else:
        return f"{size_bytes} bytes"


def show_wordlists(update: Update):
    # print available wordlist to client
    wordlists = get_wordlists()
    if not wordlists:
        update.message.reply_text("🚫 *No wordlists found in the 'cloud' directory.*")
        return

    response = "📄 *Choose a wordlist:* 📄\n\n"
    for index, wordlist in enumerate(wordlists, start=1):
        file_path = os.path.join('cloud', wordlist)
        file_size = get_file_size(file_path)
        response += f"{index}: {wordlist} - {file_size}\n"
    
    update.message.reply_text(response, parse_mode='Markdown')

# save searchs on database
def save_search(user_id, search_term):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO searches (user_id, search_term, timestamp) VALUES (?, ?, ?)', 
                   (user_id, search_term, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    message = f"""
👋 *Welcome to the OSINT Bot* 🤖
*Programmed by*: @lawxsz

🆔 *Your ID*: `{user_id}`

📜 *Available Commands*:
- 🔍 `/search <term>` - *Perform a search*
- 📊 `/me` - *Check your tokens and ID*
- 📂 `/wordlist` - *View available files*
- ❓ `/help` - *View this message again*

⚙️ _Let’s get started!_
    """
    update.message.reply_text(message, parse_mode="Markdown")
def search(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    
    tokens = get_tokens(user_id)
    if tokens <= 0:
        update.message.reply_text("You have no tokens left. Please contact the admin.")
        return

    if len(context.args) < 2:
        update.message.reply_text("Usage: /search <wordlist_choice> <search_term>")
        show_wordlists(update)
        return

    wordlist_choice = context.args[0]
    search_term = context.args[1]

    wordlists = get_wordlists()


    if not wordlist_choice.isdigit() or int(wordlist_choice) < 1 or int(wordlist_choice) > len(wordlists):
        update.message.reply_text("Invalid wordlist choice. Please select a valid option.")
        show_wordlists(update)
        return

    wordlist = os.path.join('cloud', wordlists[int(wordlist_choice) - 1])

    
    #Here you run https://github.com/Lawxsz/log-finder in C++ for obvious reasons so 
    #that it parses the wordlist much faster, you can parse the executable or compile your own using the public repository!
    
    try:
        result_file = f"{search_term}_{datetime.now().strftime('%H-%M-%S')}.txt"
        
        os.system(f'apifinder.exe {wordlist} {search_term}')

        if os.path.exists(result_file):

            with open(result_file, 'r', encoding='utf-8', errors='replace') as f:
                results = f.readlines()

            if results:
                if len(results) <= 30:
                    update.message.reply_text(f"✅ Results:\n" + "".join(results))
                else:
                    context.bot.send_document(chat_id=update.message.chat_id, document=open(result_file, 'rb'),
                                              caption="📄 Results file sent.")

                save_search(user_id, search_term)
                add_tokens(user_id, -1)  # -1 token

                
                scanned_files_path = os.path.join(scanned_files_folder, result_file)
                shutil.move(result_file, scanned_files_path)
            else:
                update.message.reply_text("No results found in the file.")
        else:
            update.message.reply_text(f"No result file generated: {result_file}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def me(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    tokens = get_tokens(user_id)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM searches WHERE user_id = ?', (user_id,))
    scan_count = cursor.fetchone()[0]

    lines_found = 0
    if os.path.exists(scanned_files_folder):
        for filename in os.listdir(scanned_files_folder):
            with open(os.path.join(scanned_files_folder, filename), 'r') as f:
                lines_found += len(f.readlines())

    #here you count how many total parameters are in the cloud, you can set this with the command for example
    # /count 1000. How to count your parameters, I programmed in C++ a script that does
    # exactly that in https://github.com/Lawxsz/log-finder/. 
    
    cursor.execute('SELECT SUM(count) FROM Parameters')
    total_params = cursor.fetchone()[0] or 0


    conn.close()

    message = f"""
✨ *Your OSINT Stats* ✨

🆔 *Your ID*: `{user_id}`
🪙 *Tokens left*: `{tokens}`
🔍 *Searches done*: `{scan_count}`
📄 *Lines found*: `{lines_found}`
📊 *Parameters stored*: `{total_params}`

⚙️ _Keep up the great work!_
    """

    update.message.reply_text(message, parse_mode="Markdown")

def wordlist(update: Update, context: CallbackContext):
    
    files = os.listdir('cloud')
    
    message = "📂 *Available Wordlist Files:* 📂\n\n"

    if files:
        for file in files:
            file_path = os.path.join('cloud', file)
            file_size = get_file_size(file_path)
            message += f"🔹 {file} - *Size:* {file_size}\n"
    else:
        message += "🚫 *No files found in the 'cloud' directory.*"

    update.message.reply_text(message, parse_mode='Markdown')

def add(update: Update, context: CallbackContext):
    if update.message.from_user.id != admin_id:
        update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) < 2:
        update.message.reply_text("Usage: /add <user_id> <tokens>")
        return

    try:
        target_user_id = int(context.args[0])
        tokens = int(context.args[1])
        add_tokens(target_user_id, tokens)
        update.message.reply_text(f"Added {tokens} tokens to user {target_user_id}.")
    except ValueError:
        update.message.reply_text("Please provide valid user_id and tokens (numbers).")
def help_command(update: Update, context: CallbackContext):
    message = (
        "🆘 *Help Menu* 🆘\n\n"
        "Here are the available commands you can use:\n"
        "1. /start - Welcome message and available commands\n"
        "2. /search <term> - Perform a search based on the term provided\n"
        "3. /me - Check your tokens, ID, searches done, and lines found\n"
        "4. /wordlist - View available wordlist files with their sizes\n"
        "5. /help - Display this help message again\n\n"
        "For more assistance, feel free to reach out! 😊"
    )
    update.message.reply_text(message, parse_mode='Markdown')

def total_scans(update: Update, context: CallbackContext):
    if update.message.from_user.id != admin_id:
        update.message.reply_text("You are not authorized to use this command.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM searches')
    total_scan_count = cursor.fetchone()[0]
    conn.close()

    update.message.reply_text(f"Total number of scans performed: {total_scan_count}")


def main():
    updater = Updater(TOKEN, use_context=True)

    init_db()

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('search', search))
    updater.dispatcher.add_handler(CommandHandler('me', me))
    updater.dispatcher.add_handler(CommandHandler('wordlist', wordlist))
    updater.dispatcher.add_handler(CommandHandler('add', add))
    updater.dispatcher.add_handler(CommandHandler('count', count))
    updater.dispatcher.add_handler(CommandHandler('total_scans', total_scans))
    updater.dispatcher.add_handler(CommandHandler("help", help_command)) 

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
