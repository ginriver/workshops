"""⚠️ Lab 6 教材 — 意図的に脆弱性を含むコード（コマンドインジェクション）。

本ファイルは Qoder Security の検出能力を体験するための教材です。
絶対に本番環境へデプロイしないでください。ローカルの演習環境でのみ使用すること。

機能   : 校正証明書をテキストファイルへエクスポートし、チェックサムを返す。
脆弱性 : ユーザー指定の checksum_target がシェルコマンドへそのまま連結される
         （subprocess + shell=True）→ コマンドインジェクション。
想定検出: Qoder Security L1 静的チェック / L2 軽量スキャン
         （危険なコマンド実行 API の検出）。

使い方（LAB_GUIDE.md Step 1）:
    本ファイルを app/routes/ にコピーし、app/main.py にマウントする。
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.calibration import CalibrationRecord

router = APIRouter(tags=["lab6-security"])

EXPORT_DIR = Path("exports")


@router.get("/security-lab/export")
def export_certificate(
    record_id: int,
    checksum_target: str = "",
    db: Session = Depends(get_db),
):
    """指定された校正記録を証明書テキストファイルとしてエクスポートする。

    checksum_target が指定された場合はそのパス、未指定の場合は
    エクスポートしたファイル自身のチェックサム（md5）を計算する。
    """
    record = db.get(CalibrationRecord, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Calibration record not found")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    content = (
        "=== CALIBRATION CERTIFICATE / 校正証明書 ===\n"
        f"Certificate No : {record.certificate_number or 'N/A'}\n"
        f"Date           : {record.calibration_date.isoformat()}\n"
        f"Performed by   : {record.performed_by}\n"
        f"Reference std. : {record.reference_standard}\n"
        f"Result         : {record.result}\n"
    )
    target = EXPORT_DIR / f"certificate-{record_id}.txt"
    target.write_text(content, encoding="utf-8")

    check_target = checksum_target or str(target)
    # ⚠️ 脆弱性: ユーザー入力がシェルコマンドへ直接展開される → コマンドインジェクション
    result = subprocess.run(
        f"md5 '{check_target}'",
        shell=True,
        capture_output=True,
        text=True,
    )
    return {
        "exported_to": str(target),
        "checksum": result.stdout.strip(),
    }
