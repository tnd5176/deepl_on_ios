# coding: utf-8

import json
import requests
import urllib
import appex
from html2text import html2text
import console


def get_text_input_with_appex():
    text = appex.get_text()
    if not text:
        print('No text input found.')
        return
    text = html2text(text)
    text = text.replace("\n", " ")
    return text


def post_to_deepl_api(text, target_lang="JA", auth_key_path="auth_key.json"):
    """
    DeepLのAPIにテキストを送信して翻訳を実行する関数。
    
    text : str
        翻訳したいテキスト。
        
    target_lang : str
        どの言語に翻訳するか。デフォルトはJA(日本語)。
        選べる言語は以下のドキュメントの target_lang を参照してください。
        https://www.deepl.com/docs-api/translating-text/request/
    """
    # アクセスキーの読み込み
    with open(auth_key_path) as f:
        auth_dict = json.load(f)
        auth_key = auth_dict["auth_key"]

    # リクエストヘッダーの指定
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": "DeepL-Auth-Key {}".format(auth_key)
    }

    # 送信するパラメータを指定し、コンテンツタイプに合うようにエンコードする
    params = {"text": text, "target_lang": target_lang}
    params = urllib.parse.urlencode(params)

    # DeepLのAPIにリクエストを送信する
    response = requests.post(
        url="https://api-free.deepl.com/v2/translate",
        headers=headers,
        data=params)

    return response


def main():
    if not appex.is_running_extension():
        print('This script is intended to be run from the sharing extension.')
        return

    text = get_text_input_with_appex()

    # DeepLのAPIにリクエストを送信する
    target_lang = "JA"
    response = post_to_deepl_api(text, target_lang=target_lang)

    # 翻訳結果を表示
    try:
        response.raise_for_status()  # ステータスコードが200以外の場合はエラー

        r_content = response.json()["translations"][0]
        translation = r_content["text"]
        detected_lang = r_content["detected_source_language"]
        console.alert(
            title="翻訳結果",
            message=f"入力した言語: {detected_lang}\n"
            f"翻訳した言語: {target_lang}\n"
            "\n入力した文章:\n" + text + "\n\n"
            "訳:\n" + translation,
            button1="OK",
            hide_cancel_button=True)

    except requests.exceptions.RequestException as e:
        # ステータスコードが200以外の場合はエラーを表示する
        console.alert(
            title="サーバーへリクエストを送信した際にエラーが発生しました。\n",
            message=f"ステータスコード: {response.status_code}\n"
            "エラー内容: \n" + str(e),
            button1="OK",
            hide_cancel_button=True)


if __name__ == '__main__':
    main()

