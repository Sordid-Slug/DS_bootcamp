NUM_OF_STEPS = 5

LOGGING_CONFIG = {
    "filename" : "analytics.log",
    "level" : "INFO",
    "format" : "%(asctime)s %(message)s",
    "datefmt" : "%Y-%m-%d %H:%M:%S"
}

REPORT_TEMPLATE = """Report

We have made {total} observations from tossing a coin: {tails} of them were tails and {heads} of
them were heads. The probabilities are {tails_percentage:.2f}% and {heads_percentage:.2f}%, respectively. Our
forecast is that in the next {steps} observations we will have: {predicted_tails} tail and {predicted_heads} heads."""

BOT_TOKEN = "7820431039:AAEOO_uQlDz0mj_q8-MlXbV1IzPmObdvzEs"

CHAT_ID = 417638847

TELEGRAM_WEBHOOK_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"