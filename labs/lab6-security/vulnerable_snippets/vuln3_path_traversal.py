"""⚠️ Lab 6 教材 — 意図的に脆弱性を含むコード（パストラバーサル）。

本ファイルは Qoder Security の検出能力を体験するための教材です。
絶対に本番環境へデプロイしないでください。ローカルの演習環境でのみ使用すること。

機能   : 校正証明書ファイルのダウンロード。
脆弱性 : ユーザー指定のファイル名が検証なしにベースディレクトリへ連結される
         → パストラバーサル（任意ファイル読み取り）。
想定検出: Qoder Security L2 軽量スキャン / L3 深度スキャン。

事前準備（LAB_GUIDE.md Step 0）:
    mkdir -p certificates
    cp labs/lab6-security/sample_data/sample-cert-0001.txt certificates/

使い方（LAB_GUIDE.md Step 3）:
    本ファイルを app/routes/ にコピーし、app/main.py にマウントする。
"""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(tags=["lab6-security"])

CERTIFICATE_DIR = Path("certificates")


@router.get("/security-lab/certificates/{filename:path}")
def download_certificate(filename: str):
    """証明書ディレクトリ内のファイルをダウンロードする。"""
    # ⚠️ 脆弱性: パスの正規化・基底ディレクトリ検証がない → パストラバーサル
    target = CERTIFICATE_DIR / filename
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Certificate file not found")
    return FileResponse(target, filename=target.name)
