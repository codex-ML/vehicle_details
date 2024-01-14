import os
import telebot
import requests

bot_token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        bot.reply_to(message, "Howdy, how are you doing?")
    except Exception as e:
        handle_error(message, e)

@bot.message_handler(commands=['vc'])
def tell_vehicle_info(message):
    try:
        # Extract the vehicleId from the command
        vehicle_id = message.text.split(' ')[1]

        # Make the API request
        response = requests.get(f"https://lol.game-quasar.com//?vehicleId={vehicle_id}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            bot.reply_to(message, f"Response: {response.text}")
        else:
            bot.reply_to(message, f"Error: Unable to fetch information for vehicle {vehicle_id}")
    except IndexError:
        bot.reply_to(message, "Error: Please provide a vehicleId after /vc")
    except Exception as e:
        handle_error(message, e)

def handle_error(message, error):
    # Log the error or take appropriate action
    print(f"Error: {error}")
    bot.reply_to(message, "An error occurred. Please try again later.")

bot.infinity_polling()
