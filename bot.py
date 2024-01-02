from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging
import uuid
import requests
from io import BytesIO
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

ORDER_INFO = {}

LOCATION, DATE, TIME, SIZE, DESIGN, TITLE = range(6)

def start(update: Update, context: CallbackContext) -> int:
    # Generate a random orderid using uuid
    orderid = str(uuid.uuid4())
    ORDER_INFO['orderid'] = orderid

    update.message.reply_text(f"Hi! I'm your StarMap Generator bot. Your order ID is: {orderid}.\n\n Let's get started. \nPlease enter the location of the event:")
    return LOCATION

def get_location(update: Update, context: CallbackContext) -> int:
    ORDER_INFO['location'] = update.message.text
    update.message.reply_text("Great! Now, enter the date of the event in YYYY-MM-DD format:")
    return DATE

def get_date(update: Update, context: CallbackContext) -> int:
    ORDER_INFO['date'] = update.message.text
    update.message.reply_text("Awesome! Now, enter the time of the event in HH:MM:SS format:")
    return TIME

def get_time(update: Update, context: CallbackContext) -> int:
    ORDER_INFO['time'] = update.message.text
    update.message.reply_text("Perfect! Now, choose the size of the chart (A3/A4):")
    return SIZE

def get_size(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.upper()

    if user_input in ['A3', 'A4']:
        ORDER_INFO['size'] = user_input
        update.message.reply_text("Great choice! Now, choose the chart design (CWB/CBB/SWB/SBB):")
        return DESIGN
    else:
        update.message.reply_text("Invalid size. Please choose A3 or A4.")
        return SIZE

def get_design(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.upper()

    if user_input in ['CWB', 'CBB', 'SWB', 'SBB']:
        ORDER_INFO['chart_type'] = user_input
        update.message.reply_text("Excellent! Now, enter the title text (max 20 characters):")
        return TITLE
    else:
        update.message.reply_text("Invalid chart design. Please choose CWB, CBB, SWB, or SBB.")
        return DESIGN


API_KEY = "Kill"  
RECEIVE_DATA_ENDPOINT = "http://34.142.123.91:5000/receive_data"
SERVER_URL = "http://34.142.123.91:5000"


def send_order_info(order_info):
    headers = {"Authorization": f"{API_KEY}", "Content-Type": "application/json"}
    response = requests.post(RECEIVE_DATA_ENDPOINT, json=order_info, headers=headers)

    if response.status_code == 200:
        print("Order info sent successfully.")
        return response.json()  # Assuming the response contains a JSON with image_url
    else:
        print(f"Failed to send order info. Status code: {response.status_code}, Response: {response.text}")
        return None

def send_image_to_telegram(update: Update, image_url):
    # Send the image to the Telegram user (adjust as needed)
    update.message.reply_photo(image_url, caption="Here is your generated chart!")


def get_title(update: Update, context: CallbackContext) -> int:
    ORDER_INFO['title_text'] = update.message.text
    ORDER_INFO['chart_font'] = "NewFont"

    # Send the order info to the /receive_data endpoint
    response_data = send_order_info(ORDER_INFO)
    
    if response_data and 'image_url' in response_data:
        relative_image_url = response_data['image_url']

        # Prepend the server address to the relative image_url
        full_image_url = f"{SERVER_URL}{relative_image_url}"

        # Send a GET request to the full_image_url to receive the image
        image_response = requests.get(full_image_url)

        if image_response.status_code == 200:
            # Assuming you have a file-like object with the image data
            image_file = BytesIO(image_response.content)
            # Send the image to the Telegram user
            send_image_to_telegram(update, image_file)

            # Return a success message
            update.message.reply_text("Order received successfully! Image sent to Telegram.")
        else:
            print(f"Failed to fetch the image. Status code: {image_response.status_code}")
            update.message.reply_text("Failed to fetch the image. Please try again later.")
    else:
        update.message.reply_text("Failed to receive order information. Please try again later.")

    # Clear order info for the next request
    ORDER_INFO.clear()

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Order canceled. If you want to start again, type /generate.")
    ORDER_INFO.clear()
    return ConversationHandler.END

def main() -> None:
    updater = Updater("6788634968:AAF8F4ZxJYCuvyzRjBTwnQ2Yy8NFo0t1rMU")  # Replace with your actual bot token
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('generate', start)],
        states={
            LOCATION: [MessageHandler(Filters.text & ~Filters.command, get_location)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, get_date)],
            TIME: [MessageHandler(Filters.text & ~Filters.command, get_time)],
            SIZE: [MessageHandler(Filters.text & ~Filters.command, get_size)],
            DESIGN: [MessageHandler(Filters.text & ~Filters.command, get_design)],
            TITLE: [MessageHandler(Filters.text & ~Filters.command, get_title)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

