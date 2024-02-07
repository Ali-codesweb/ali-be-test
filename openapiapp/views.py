from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers as sr
from modules.validator import Validator
from openai import OpenAI
client = OpenAI(api_key="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")


@api_view(["GET"])
def test(request: Request):
    return Response("ASdsad")


@api_view(['POST', "GET"])
def generate_ad_prompt(request: Request):
    # request validation
    validation = {
        "product_description":  sr.CharField(required=True),
        "vibe_words":  sr.CharField(required=True),
    }
    # product_description = request.data.get("product_description", None)
    # vibe_words = request.data.get("vibe_words", None)
    product_description, vibe_words = Validator(
        data=request.data, fields=validation)
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
    print(chat_response)
    return Response(chat_response)
