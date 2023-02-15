import pandas as pd
from datetime import date
import telegram
import schedule
import time
from flask import Flask

# Set the Telegram API token and chat ID
bot_token = "5639755535:AAFWlHOyhBANI0u-6GFHspbkP4h5E-aBoxY"
chat_ids = ["5891316395","1062597793"]

# Create a Telegram bot instance
bot = telegram.Bot(token=bot_token)

def send_update():
    # Get the current date
    today = date.today().strftime("%Y-%m-%d")

    # Fetch the IPO data from the website
    urlshare = "https://www.sharesansar.com/?show=home"
    htmlshare = requests.get(urlshare).content
    df_list_share = pd.read_html(htmlshare)

    # Select the IPO data for today's event
    df_share_today = df_list_share[2][df_list_share[2]['Opening Date'] == today]

    # Check if there is any event today
    if len(df_share_today) == 0:
        message = "No IPO event today"
    else:
        # Format the data to be sent
        message = f"IPOs occurring today ({today}):\n\n"
        for _, row in df_share_today[['Company', 'Units', 'Opening Date', 'Closing Date']].iterrows():
            message += f"{row['Company']}\nUnits: {row['Units']}\nOpening Date: {row['Opening Date']}\nClosing Date: {row['Closing Date']}\n\n"

    # Send the message to the Telegram chat
    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=message)

# Create the Flask app
app = Flask(__name__)

# Define a route to trigger the update
@app.route('/update')
def update():
    send_update()
    return 'Update sent!'

# Schedule the update to run every 6 hours
schedule.every(6).hours.do(send_update)

# Run the scheduled update as a background process
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Start the background thread
    import threading
    thread = threading.Thread(target=run_schedule)
    thread.start()

    # Start the Flask app
    app.run()
