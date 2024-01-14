import os
import telebot
import requests
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        bot.reply_to(message,
                     "Howdy, how are you doing?  \n Commands :- /vc <vehicle_id>")
    except Exception as e:
        handle_error(message, e)


@bot.message_handler(commands=['vc'])
def tell_vehicle_info(message):
    try:
        # Extract the vehicleId from the command
        vehicle_id = message.text.split(' ')[1]

        # Make the API request
        response = requests.get(
            f"https://lol.game-quasar.com/?vehicleId={vehicle_id}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract relevant information for display
            info_to_display = {
                "License Plate": data.get("license_plate", "N/A"),
                "Owner Name": data.get("owner_name", "N/A"),
                "Vehicle Model": data.get("brand_model", "N/A"),
                "Fuel Type": data.get("fuel_type", "N/A"),
                "Registration Date": data.get("registration_date", "N/A"),
                "Insurance Expiry": data.get("insurance_expiry", "N/A"),
                "RC Status": data.get("rc_status", "N/A"),
            }

            # Create a formatted message with the extracted information
            formatted_message = "\n".join([f"{key}: {value}" for key, value in info_to_display.items()])

            # Reply to the user with the formatted information
            bot.reply_to(message, f"Vehicle Information for {vehicle_id}:\n{formatted_message}")
        else:
            bot.reply_to(
                message,
                f"Error: Unable to fetch information for vehicle {vehicle_id}")
    except IndexError:
        bot.reply_to(message, "Error: Please provide a vehicleId after /vc")
    except Exception as e:
        handle_error(message, e)


def handle_error(message, error):
    # Log the error or take appropriate action
    print(f"Error: {error}")
    bot.reply_to(message, "An error occurred. Please try again later.")


bot.infinity_polling()
