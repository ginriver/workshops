"""⚠️ Lab 6 教材 — 意図的に脆弱性を含むコード（機密情報漏えい）。

本ファイルは Qoder Security の検出能力を体験するための教材です。
絶対に本番環境へデプロイしないでください。ローカルの演習環境でのみ使用すること。
※ 本ファイル内のトークンはすべてダミー（教材用）です。

機能   : 校正期限が近づいた機器の担当者にリマインダー通知を送る。
脆弱性 : 1) API トークンがソースコードへハードコードされている
         2) 認証情報と個人情報（メールアドレス）がログへそのまま出力される
         → 機密情報漏えい（Sensitive Information Exposure）。
想定検出: Qoder Security L1 静的チェック（ハードコードされたシークレット検出）
         / L2 軽量スキャン。

使い方（LAB_GUIDE.md Step 3）:
    本ファイルを app/routes/ にコピーし、app/main.py にマウントする。
"""
from __future__ import annotations

import logging

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("calibration-tracker.notify")
# （教材用）演習中にログ出力が必ずコンソールへ見えるよう、明示的にハンドラを設定している。
if not logger.handlers:
    logger.setLevel(logging.INFO)
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)

# ⚠️ 脆弱性: API 認証情報がソースコードにハードコードされている
NOTIFY_SERVICE_TOKEN = "sk-calnotify-4f8a2c91e6d74b350a1f92c8d7e6b5a4"

router = APIRouter(tags=["lab6-security"])


class NotifyPayload(BaseModel):
    """校正期限リマインダー通知の依頼。"""

    instrument_code: str
    due_date: str
    recipient_email: str


@router.post("/security-lab/notify")
def send_due_date_notification(payload: NotifyPayload):
    """校正期限のリマインダー通知を送信キューへ登録する。"""
    # ⚠️ 脆弱性: 認証情報と個人情報をログへそのまま出力している
    logger.info(
        "Sending due-date notification: token=%s recipient=%s instrument=%s due=%s",
        NOTIFY_SERVICE_TOKEN,
        payload.recipient_email,
        payload.instrument_code,
        payload.due_date,
    )
    # （実際の通知サービス呼び出しは省略 — ワークショップ簡略化のため）
    return {"status": "queued", "recipient": payload.recipient_email}
