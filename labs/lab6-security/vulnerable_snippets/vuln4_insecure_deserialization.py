"""⚠️ Lab 6 教材 — 意図的に脆弱性を含むコード（安全でないデシリアライゼーション）。

本ファイルは Qoder Security の検出能力を体験するための教材です。
絶対に本番環境へデプロイしないでください。ローカルの演習環境でのみ使用すること。

機能   : レガシーシステムからエクスポートされた機器データ（base64）の取り込み。
脆弱性 : 信頼できないデータを pickle でデシリアライズする
         → 任意コード実行（RCE）。
想定検出: Qoder Security L1 静的チェック（危険 API）/ L2 軽量スキャン。

使い方（LAB_GUIDE.md Step 3）:
    本ファイルを app/routes/ にコピーし、app/main.py にマウントする。
"""
from __future__ import annotations

import base64
import pickle

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["lab6-security"])


class LegacyImportPayload(BaseModel):
    """レガシーシステムからのエクスポートデータ。"""

    data_b64: str  # base64 エンコードされた pickle ストリーム


@router.post("/security-lab/import-legacy")
def import_legacy_export(payload: LegacyImportPayload):
    """レガシーエクスポートデータを取り込む。"""
    raw = base64.b64decode(payload.data_b64)
    # ⚠️ 脆弱性: 信頼できないデータの pickle デシリアライズ → 任意コード実行
    data = pickle.loads(raw)
    count = len(data) if hasattr(data, "__len__") else 1
    return {"status": "imported", "records": count}
