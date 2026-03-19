import pytest
from playwright.sync_api import Page, expect

# テストデータの定義
# (ユーザー名, パスワード, 期待する結果のキーワード)
test_data = [
    ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"), # 正常系
    ("wrong_user", "SuperSecretPassword!", "Your username is invalid!"),   # 異常系（ユーザー間違い）
    ("tomsmith", "wrong_password", "Your password is invalid!"),           # 異常系（パスワード間違い）
]

@pytest.mark.parametrize("username, password, expected_msg", test_data)
def test_form_login(page: Page, username, password, expected_msg):
    # 1. サイトを開く
    page.goto("https://the-internet.herokuapp.com/login")

    # 2. ログイン操作
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type='submit']")

    # 3. アサーション（結果の検証）
    #    アサーションの後に5秒止める（目視確認用）
    page.wait_for_timeout(5000)
    # メッセージが表示されるまで待機し、内容をチェック
    expect(page.locator("#flash")).to_contain_text(expected_msg)
