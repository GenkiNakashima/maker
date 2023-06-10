import os
import urllib.request
import json
import configparser
import codecs

class CotohaApi:
    # 初期化
    def __init__(self, client_id, client_secret, developer_api_base_url, access_token_publish_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.developer_api_base_url = developer_api_base_url
        self.access_token_publish_url = access_token_publish_url
        self.getAccessToken()

    # アクセストークン取得
    def getAccessToken(self):
        # アクセストークン取得URL指定
        url = self.access_token_publish_url

        # ヘッダ指定
        headers={
            "Content-Type": "application/json;charset=UTF-8"
        }

        # リクエストボディ指定
        data = {
            "grantType": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        # リクエストボディ指定をJSONにエンコード
        data = json.dumps(data).encode()

        # リクエスト生成
        req = urllib.request.Request(url, data, headers)

        # リクエストを送信し、レスポンスを受信
        res = urllib.request.urlopen(req)

        # レスポンスボディ取得
        res_body = res.read()

        # レスポンスボディをJSONからデコード
        res_body = json.loads(res_body)

        # レスポンスボディからアクセストークンを取得
        self.access_token = res_body["access_token"]

    def ne(self, sentence):
        # 固有表現抽出API URL指定
        url = self.developer_api_base_url + "nlp/v1/ne"
        # ヘッダ指定
        headers={
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json;charset=UTF-8",
        }
        # リクエストボディ指定
        data = {
            "sentence": sentence
        }
        # リクエストボディ指定をJSONにエンコード
        data = json.dumps(data).encode()
        # リクエスト生成
        req = urllib.request.Request(url, data, headers)
        # リクエストを送信し、レスポンスを受信
        try:
            res = urllib.request.urlopen(req)
             # レスポンスボディ取得
            res_body = res.read()
        # レスポンスボディをJSONからデコード
            res_body = json.loads(res_body)
        # レスポンスボディから解析結果を取得
            return res_body
        # リクエストでエラーが発生した場合の処理
        except urllib.request.HTTPError as e:
            # ステータスコードが401 Unauthorizedならアクセストークンを取得し直して再リクエスト
            if e.code == 401:
                print ("get access token")
                self.access_token = getAccessToken(self.client_id, self.client_secret)
                headers["Authorization"] = "Bearer " + self.access_token
                req = urllib.request.Request(url, data, headers)
                res = urllib.request.urlopen(req)
            # 401以外のエラーなら原因を表示
            else:
                print ("<Error> " + e.reason)

        

def anaumeoni(sentence):
    # ソースファイルの場所取得
    APP_ROOT = os.path.dirname(os.path.abspath( __file__)) + "/"

    # 設定値取得
    config = configparser.ConfigParser()
    config.read(APP_ROOT + "config.ini")
    CLIENT_ID = config.get("COTOHA API", "Developer Client id")
    CLIENT_SECRET = config.get("COTOHA API", "Developer Client secret")
    DEVELOPER_API_BASE_URL = config.get("COTOHA API", "Developer API Base URL")
    ACCESS_TOKEN_PUBLISH_URL = config.get("COTOHA API", "Access Token Publish URL")

    # COTOHA APIインスタンス生成
    cotoha_api = CotohaApi(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # 固有表現抽出対象文
    #sentence = 'ついにアラバスタに辿り着いたルフィ達は、B・Wの扇動によって間近に迫った大反乱を防ぐため奔走する。反乱軍を説得するため反乱軍の本拠地がある町ユバに向かうが、すでに反乱軍は本拠地を移していた。ルフィの提案で反乱軍の制止ではなく、アラバスタの反乱を煽りたてた張本人であるB・W社社長にして王下七武海の一角サー・クロコダイルがいるレインベースに乗り込む。しかし、クロコダイルが発動した「ユートピア作戦」によりアラバスタ国民の暴動はさらに加速してしまう。ルフィはクロコダイルに挑むが、彼の圧倒的な力の前に敗れてしまう。首都アルバーナにて国王軍と反乱軍が衝突する最中、ゾロ達はオフィサーエージェントを撃破。そして、復活を遂げたルフィがアルバーナに到着しサイバイマン孫悟空'

    # 固有表現抽出 API 実行
    result = cotoha_api.ne(sentence)
    word_list=[]
    for i in range(len(result["result"])):
        word_list.append(result["result"][i]["form"])
    

    return ''.join([document.replace(word, '(  ' + str(i+1) + '  )') for i, word in enumerate(word_list)])

