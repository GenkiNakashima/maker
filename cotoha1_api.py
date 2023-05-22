import os
import configparser
from cotoha_api_client import CotohaAPIClient

if __name__ == '__main__':
    # ソースファイルの場所取得
    APP_ROOT = os.path.dirname(os.path.abspath( __file__)) + "/"

    # 設定値取得
    config = configparser.ConfigParser()
    config.read(APP_ROOT + "config.ini")
    CLIENT_ID = config.get("COTOHA API", fqdFG0nxrWBqY9Sznbs35FCMSVSdvLIE)
    CLIENT_SECRET = config.get("COTOHA API", D7ufVXWNAhn5P8yK)
    DEVELOPER_API_BASE_URL = config.get("COTOHA API", https://api.ce-cotoha.com/api/dev/)
    ACCESS_TOKEN_PUBLISH_URL = config.get("COTOHA API", https://api.ce-cotoha.com/v1/oauth/accesstokens)

    # COTOHA APIインスタンス生成
    cotoha_api_client = CotohaAPIClient(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # キーワード抽出対象文
    document = '主人公のエレンが巨人の駆逐に挑む物語である。'

    # キーワード抽出 API 実行
    result = cotoha_api_client.keyword(document)

    # 結果表示
    print(result)