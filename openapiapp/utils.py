from openai import OpenAI, RateLimitError
from django.conf import settings

client = OpenAI(api_key=settings.ENV.get("GPT_KEY"))


def generate_prompt(description, vibe_words):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with a product description and seed words, and your task is to generate only top 3 product names."
            },
            {
                "role": "user",
                "content": f"Product description: {description}\n    Seed words: {vibe_words}."
            },
            {
                "role": "user",
                "content": 'Give  transcript for 1.TV ad for the first product name aimed at young adults 2.Facebook ad for the second product name and for Radio ad for third product name aimed at parents 3.a safety warning for any name'
            },
            {
                "role": "user",
                "content": 'Give product names in an array in a separate key array and give all in json like keys  1.product_names 2.tv_ad_young_adults 3.facebook_ad_parents 4.radio_ad_parents 5.safety_warning and values as 1 line transcript'
            },
        ],
        temperature=0.8,
        max_tokens=500,
        top_p=1
    )


# {
#     "product_names": ["1", "2", "3"],
#     "tv_ad_young_adults": "",
#     "facebook_ad_parents": "",
#     "radio_ad_parents": "",
#     "safety_warning": ""
# }
