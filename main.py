import telebot
from telebot import types

# Replace 'YOUR_API_TOKEN' with your Bot's API token from BotFather
API_TOKEN = '6417942588:AAGW_OC6fa8vAmAJ5jExWzRJnKIOVdloJQI'

# Create a new bot instance
bot = telebot.TeleBot(API_TOKEN)

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Instructions message
    instructions = (
        "Welcome to the bot! Here's how you can use it:\n\n"
        "1. Click the button below to open the web app.\n"
        "2. Enjoy browsing the content.\n\n"
        "Feel free to contact us if you need help!"
    )
    
    # Create an inline button that opens the web app URL
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Open Web App", url="http://lodemon.ct.ws/?i=1")
    markup.add(button)
    
    # Send the message with the button
    bot.send_message(message.chat.id, instructions, reply_markup=markup)

# Run the bot
bot.polling()
