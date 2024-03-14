import json
from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

tools = [
    {"type": "code_interpreter"},
   {
        "type": "function",
        "function": {
            "name": "search_hotpepper_shops",
            "description": "ホットペッパーグルメAPIを利用し、キーワードや個室の有無などのオプションフィルターで飲食店を検索できます。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "飲食店を検索するためのキーワード。店名、住所、駅名、お店ジャンルなどを指定できる。ユーザーメッセージから検索キーワードとなる文字を抽出して検索クエリーにしてください。例: ###大阪駅 和食###"
                    },
                    "private_room": {
                        "type": "integer",
                        "description": "個室ありの店舗のみを検索, 0:絞り込まない, 1:絞り込む。オプション",
                        "enum": [0, 1]
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_vacant_hotels",
            "description": "楽天トラベルのAPIを使って、場所、チェックイン日、チェックアウト日、予算、大人の人数など、さまざまなフィルターで空室ホテルを検索できます。",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "ホテル検索場所の緯度(WGS84), ex:35.6065914"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "ホテル検索場所の経度(WGS84), ex:139.7513225"
                    },
                    "searchRadius": {
                        "type": "number",
                        "description": "緯度経度検索時の検索半径(単位km), 0.1 to 3.0"
                    },
                    "checkinDate": {
                        "type": "string",
                        "description": "yyyy-MM-dd 形式のチェックイン日。年の指定がない場合は2024年を指定する。"
                    },
                    "checkoutDate": {
                        "type": "string",
                        "description": "yyyy-MM-dd 形式のチェックアウト日。年の指定がない場合は2024年を指定する。"
                    },
                    "maxCharge": {
                        "type": "integer",
                        "description": "上限金額, int 0 to 999999999"
                    },
                    "adultNum": {
                        "type": "integer",
                        "description": "宿泊者数, int 1 to 99"
                    }
                },
                "required": ["latitude", "longitude", "searchRadius", "checkinDate", "checkoutDate"]
            }
        }
    }
]


def search_hotpepper_shops(keyword: str):
    print("CALL: search_hotpepper_shops()", keyword)
    # return dummy shops with json
    shops = [
        {"name": "おいしいイタリアン有楽町店", "address": "有楽町"},
        {"name": "素晴らしいイタリアン銀座店", "address": "銀座"},
    ]
    # return shops array to string
    names = [shop['name'] for shop in shops]
    names_string = '\n'.join(names)

    return names_string

def search_vacant_hotels(latitude, longitude, searchRadius, checkinDate, checkoutDate, maxCharge=50000, adultNum=1, page=1, hits=2, response_format='json'):
    print("CALL: search_vacant_hotels()", latitude, longitude, searchRadius, checkinDate, checkoutDate, maxCharge, adultNum)
    # return dummy shops with json
    hotels = [
        {"name": "東京マイクロソフトホテル", "address": "東京駅"},
        {"name": "マイクロソフトイン銀座", "address": "銀座"},
    ]
    # return shops array to string
    names = [hotel['name'] for hotel in hotels]
    names_string = '\n'.join(names)

    return names_string

tool_map = {
    "search_hotpepper_shops": search_hotpepper_shops,
    "search_vacant_hotels": search_vacant_hotels
}