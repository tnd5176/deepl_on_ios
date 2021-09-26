# deepl_on_ios
iOS上で選択した文字列をDeepLで翻訳して表示するアプリです。  
pythonistaのshare extentionとして開発しました。

## 注意
このプログラムを使用するにはDeepLの認証キーが必要です。  
https://www.deepl.com/pro-api?cta=header-pro/ で登録してDeepL API Freeの認証キーを取得した後、  
`translate_with_deepl.py`と同じディレクトリに

```
{
  "auth_key": "取得した認証キー"
}
```
という内容の`auth_key.json`を作成してください。
