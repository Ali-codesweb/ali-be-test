import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import serializers as sr
from modules.validator import Validator
from openai import RateLimitError

from openapiapp.utils import generate_prompt


@api_view(["GET"])
def test(request: Request):
    # return Response("hello ok")
    raise ValueError("sadsadasd")


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
        chat_response = generate_prompt(product_description, vibe_words)
        message = chat_response.model_dump(
        )['choices'][0]['message']['content']
        message = json.loads(message)
        response_status = status.HTTP_200_OK
    except RateLimitError as e:
        message = e.body
        response_status = status.HTTP_403_FORBIDDEN
    except Exception as e:
        message = "Some Error Occurred"
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(status=response_status, data=message)
