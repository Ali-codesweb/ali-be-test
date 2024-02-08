from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import serializers as sr
from modules.validator import Validator
from openai import OpenAI, RateLimitError
from django.conf import settings
client = OpenAI(api_key=settings.ENV.get("GPT_KEY"))


@api_view(["GET"])
def test(request: Request):
    return Response("hello ok")


@api_view(['POST'])
def generate_ad_prompt(request: Request):
    # request validation
    validation = {
        "product_description":  sr.CharField(required=True),
        "vibe_words":  sr.CharField(required=True),
    }
    product_description, vibe_words = Validator(
        data=request.data, fields=validation)
    try:
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a product description and seed words, and your task is to generate product names."
                },
                {
                    "role": "user",
                    "content": f"Product description: {product_description}\n    Seed words: {vibe_words}."
                }
            ],
            temperature=0.8,
            max_tokens=64,
            top_p=1
        )
        message = chat_response.model_dump()
        response_status = status.HTTP_200_OK
    except RateLimitError as e:
        message = e.body
        response_status = status.HTTP_403_FORBIDDEN
    except Exception as e:
        message = "Some Error Occurred"
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(status=response_status, data=message)
