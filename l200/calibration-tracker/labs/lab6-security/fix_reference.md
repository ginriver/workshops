# Fix Reference — 修正例（講師用リファレンス）

> Qoder Agent が提案する修正は以下と **完全に一致する必要はありません**。
> 受講者には「Agent の修正 diff をレビューし、意味が正しいか判断する」ことを求めます。
> 本ファイルは講師が正解を即答できるようにするためのリファレンスです。

## Vuln 1 — コマンドインジェクションの修正

ポイント: `shell=True` をやめる + 入力パスの検証（存在チェック / 許可ディレクトリ限定）。

```python
import subprocess

@router.get("/security-lab/export")
def export_certificate(record_id: int, checksum_target: str = "", db=Depends(get_db)):
    ...
    check_path = Path(checksum_target) if checksum_target else target
    if not check_path.is_file():
        raise HTTPException(status_code=422, detail="Checksum target not found")
    # リスト引数 + shell なし（シェルを経由しない）
    result = subprocess.run(["md5", str(check_path)], capture_output=True, text=True)
```

## Vuln 2 — SQLインジェクションの修正

ポイント: パラメータバインド（`text()` + `:param`）。

```python
from sqlalchemy import text

sql = text(
    "SELECT id, code, name, manufacturer FROM instruments "
    "WHERE name LIKE :kw OR code LIKE :kw"
)
rows = db.execute(sql, {"kw": f"%{keyword}%"}).fetchall()
```

さらに望ましい形: SQLAlchemy ORM（`Instrument.name.contains(keyword)`）への置き換え。

## Vuln 3 — パストラバーサルの修正

ポイント: `resolve()` で正規化し、基底ディレクトリ内に収まっているか検証。

```python
base = CERTIFICATE_DIR.resolve()
target = (base / filename).resolve()
if not target.is_relative_to(base):   # Python 3.9+
    raise HTTPException(status_code=400, detail="Invalid filename")
```

## Vuln 4 — 安全でないデシリアライゼーションの修正

ポイント: 信頼できないデータに `pickle` を使わない。JSON など安全な形式へ移行。

```python
import json

data = json.loads(base64.b64decode(payload.data_b64))
```

（レガシー形式をどうしても読み込む必要がある場合は、署名検証・隔離環境での処理を併用。
この設計判断自体を Agent と議論させるのが教育的に有効です。）

## Vuln 5 — 機密情報漏えいの修正

ポイント: シークレットは環境変数 / シークレット管理へ。ログはマスキング。

```python
import os

NOTIFY_SERVICE_TOKEN = os.environ.get("NOTIFY_SERVICE_TOKEN", "")
if not NOTIFY_SERVICE_TOKEN:
    raise RuntimeError("NOTIFY_SERVICE_TOKEN is not configured")

logger.info(
    "Sending due-date notification: recipient_domain=%s instrument=%s due=%s",
    payload.recipient_email.split("@")[-1],   # メールはドメインのみ記録
    payload.instrument_code,
    payload.due_date,
)
```

## 共通チェックリスト（再検証時に受講者へ確認させる）

1. 修正後、`/security-scan` を再実行し所見が消えたか
2. 既存テスト（`python3 -m pytest`）が pass するか（品質ゲート通過）
3. 正常系 API が引き続き動くか（curl で確認）
4. 修正が過剰でないか（機能を壊す「セキュリティ劇場」になっていないか）
