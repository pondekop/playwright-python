import pytest
from playwright.sync_api import Page, expect

# 1. テストデータの定義
test_data = [
    ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"), # 正常系
    ("wrong_user", "SuperSecretPassword!", "Your username is invalid!"),   # 異常系（ユーザー間違い）
    ("tomsmith", "wrong_password", "Your password is invalid!"),           # 異常系（パスワード間違い）
]

# 2. 定義した test_data を使ってテストを実行する
@pytest.mark.parametrize("username, password, expected_msg", test_data)
def test_form_login(page: Page, username, password, expected_msg):

    # 1. サイトを開く
    page.goto("https://the-internet.herokuapp.com/login")

    # 2. ログイン操作
    page.fill("#username", username)
    page.fill("#password", password)
    page.get_by_role("button", name="Login").click()

    # 3. 検証（アサーション）
    flash_msg = page.locator("#flash")
    expect(flash_msg).to_be_visible()
    expect(flash_msg).to_contain_text(expected_msg)

    # 4. 正常系の場合のみ、遷移後のURLもチェック
    if username == "tomsmith" and password == "SuperSecretPassword!":
        expect(page).to_have_url("https://the-internet.herokuapp.com/secure")

    # 画面を見て確認するときは以下(画面見ないときは--headed以下を削除)
    # pytest tests/test_login.py --headed --slowmo 500