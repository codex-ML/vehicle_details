import os
import telebot
import requests
import json
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        bot.reply_to(message, "Howdy, how are you doing?  \n Commands :- /vc <vehicle_id>")
    except Exception as e:
        handle_error(message, e)

@bot.message_handler(commands=['vc'])
def tell_vehicle_info(message):
    try:
        # Extract the vehicleId from the command
        vehicle_id = message.text.split(' ')[1]

        # Make the API request
        response = requests.get(f"https://lol.game-quasar.com/?vehicle_id={vehicle_id}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract specific fields from the header
            title_car = data.get("data", {}).get("header", {}).get("title", "Unknown")
            ownership = data.get("data", {}).get("header", {}).get("ownership", "N/A")
            owner_name = data.get("data", {}).get("header", {}).get("ownerName", "N/A")
            vehicle_num = data.get("data", {}).get("header", {}).get("vehicleNum", "N/A")

            # Extract tabs data
            tabs = data.get("data", {}).get("tabs", [])

            # Create a formatted message with the extracted information
            formatted_message = f"Title: {title_car}\nOwnership: {ownership}\nOwner Name: {owner_name}\nVehicle Number: {vehicle_num}"

            # Append information from tabs
            for tab in tabs:
                formatted_message += f"\n{tab.get('title', 'Unknown')}: {tab.get('id', 'Unknown')}"

            # Reply to the user with the formatted information
            bot.reply_to(message, f"Vehicle Information for {vehicle_id}:\n{formatted_message}")
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
