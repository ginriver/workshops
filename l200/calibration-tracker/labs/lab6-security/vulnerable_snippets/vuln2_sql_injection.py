"""⚠️ Lab 6 教材 — 意図的に脆弱性を含むコード（SQLインジェクション）。

本ファイルは Qoder Security の検出能力を体験するための教材です。
絶対に本番環境へデプロイしないでください。ローカルの演習環境でのみ使用すること。

機能   : 機器のフリーワード検索（名称 / 管理番号の部分一致）。
脆弱性 : ユーザー入力が文字列連結で SQL 文へ直接埋め込まれる
         （パラメータバインドなし）→ SQLインジェクション。
想定検出: Qoder Security L1 静的チェック / L2 軽量スキャン / L3 深度スキャン。

使い方（LAB_GUIDE.md Step 3）:
    本ファイルを app/routes/ にコピーし、app/main.py にマウントする。
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(tags=["lab6-security"])


@router.get("/security-lab/search")
def search_instruments(keyword: str, db: Session = Depends(get_db)):
    """キーワードで機器を検索する（名称 / 管理番号の部分一致）。"""
    # ⚠️ 脆弱性: ユーザー入力が SQL 文へ直接連結される → SQLインジェクション
    sql = text(
        "SELECT id, code, name, manufacturer FROM instruments "
        f"WHERE name LIKE '%{keyword}%' OR code LIKE '%{keyword}%'"
    )
    rows = db.execute(sql).fetchall()
    return [
        {"id": row[0], "code": row[1], "name": row[2], "manufacturer": row[3]}
        for row in rows
    ]
