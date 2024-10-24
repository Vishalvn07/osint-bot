# **OSINT Bot Telegram** 🌐

![OSINT Bot](https://i.imgur.com/OKZubqZ.png) 
![OSINT Bot](https://i.imgur.com/WNXscmd.png) 

This bot is designed for OSINT (Open Source Intelligence) tasks, providing efficient capabilities through Telegram. With features like wordlist searches, token management, and log analysis, it integrates powerful C++ log parsing to deliver fast results. User activities and search logs are automatically saved in a SQLite database for further review.

To add the Logs you must leave the .txt in the “cloud” folder, there the logs.txt will go. You can get free CLOUDLOGS in telegram, forums or paid, that's up to you!
---

## 🚀 **Features**
- 🔍 **Search using wordlists**: Perform searches across multiple wordlists to find critical information.
- 🔑 **Token Management**: Control access and usage limits via token systems.
- 📊 **Stats and Results**: Retrieve detailed stats on search performance and results found.
- 🛠️ **Admin Commands**: Add tokens, manage users, and configure bot settings.
- ⚡ **C++ Log Parsing**: Leverages a [C++ Log Finder Tool](https://github.com/Lawxsz/log-finder) for rapid log processing.
- 🧑‍💻 **User Data**: Stores user activities and search results in an integrated SQLite database.

---

## 🛠️ **Technologies Used**
- **Python**: Main language for the bot's logic and interaction with Telegram.
- **Telegram Bot API**: Interface to communicate with users on Telegram.
- **SQLite**: Database system to store user data, tokens, and search logs.
- **C++**: Fast processing tool for log analysis, linked with the bot to speed up search functions.

---

## 📋 **Commands Overview**
### **User Commands**
| Command                               | Description                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------|
| `/start`                              | Displays a welcome message and available commands.                          |
| `/search <wordlist_number> <term>`    | Search within a specific wordlist for the provided term.                    |
| `/me`                                 | Shows your stats: ID, token balance, searches performed, and results found. |
| `/wordlist`                           | Lists all available wordlists along with their sizes.                       |
| `/help`                               | Displays help with available commands and usage instructions.               |

---

### **Admin Commands**
| Command                               | Description                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------|
| `/addtoken <token> <usage_limit>`     | Adds a new token with a specific usage limit.                               |
| `/adduser <user_id>`                  | Adds a user to the system with a specific token.                            |
| `/count <1000>`                       | Adds to database numbers of parameters                                      |
| `/dcount <1000>`                      | Remove to database numbers of parameters                                    |

---

## 📝 **How to Use**

1. **Start the Bot**:  
   Type `/start` to see a welcome message and available commands.

2. **Search with a Wordlist**:  
   Use `/search <wordlist_number> <term>` to search a specific wordlist for the given term.  
   Example: `/search 2 password123`

3. **Check Stats**:  
   Use `/me` to view your personal search stats, token balance, and results found.

4. **Admin Actions**:  
   Admins can manage tokens and users by using commands like `/addtoken` and `/adduser` to control access.

---

## 🗂️ **Wordlists**
Wordlists are essential to the bot's functionality. Use the `/wordlist` command to see available wordlists with their sizes and choose the one best suited for your task.

### **Example Wordlists**
- **Wordlist 1**: Contains 100,000 lines.
- **Wordlist 2**: Contains 500,000 lines.
- **Wordlist 3**: Contains 1,000,000 lines.

---
## 📦 **Installing Requirements**

1. Clone the repository:
   ```bash
   git clone https://github.com/Lawxsz/OSINT-Bot.git

2. Go to Folder:
   ```bash
   cd OSINT-Bot
3. Install Requirements:
   ```bash
   pip3 install -r requirements.txt
   
4. Run Script
   ```bash
   python3 bot.py


## 🛡️ **Security**
The bot is secured using a token system. Tokens ensure that only authorized users can perform searches. Admins can generate, add, or remove tokens as needed.

---

## 🧑‍💻 **Contributing**
Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request.

---

## 💬 **Contact**
For any questions or issues, feel free to reach out to [@Lawxsz](https://github.com/Lawxsz) on GitHub or Telegram.

---

## 📄 **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
