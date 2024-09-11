import os
import telebot
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import nltk

nltk.download('vader_lexicon')
load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
sia = SentimentIntensityAnalyzer()


@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = f"Hi {message.from_user.first_name}, I'm a sentiment analysis bot!\n" \
                        "Send me a message, and I'll analyze its emotional tone.\n" \
                        "Try sending something positive, negative, or neutral."
    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    sentiment = sia.polarity_scores(text)

    if sentiment['compound'] >= 0.05:
        overall_sentiment = 'positive'
    elif sentiment['compound'] <= -0.05:
        overall_sentiment = 'negative'
    else:
        overall_sentiment = 'neutral'

    response = f"Sentiment analysis results:\n\n" \
               f"Positive: {sentiment['pos']:.2f}\n" \
               f"Negative: {sentiment['neg']:.2f}\n" \
               f"Neutral: {sentiment['neu']:.2f}\n\n" \
               f"Overall sentiment: {overall_sentiment}"

    bot.send_message(message.chat.id, response)

bot.polling()
