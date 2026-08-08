# Calibration Tracker — 計量校正管理システム

精密機器メーカー向け計量校正管理システムの **ハンズオン演習用ベースラインリポジトリ**です。
Qoder AI エージェント実践ワークショップの Lab 1〜4 で本リポジトリを使います。

## 実装済み（ベースライン）

- **機器マスタ管理** — 機器の登録・一覧・参照・更新（カテゴリ／ステータスで絞り込み）
- **校正記録管理** — 校正記録の登録・一覧（登録時に最終校正日を自動更新）
- **ヘルスチェック** — `GET /healthz`

## 未実装（ワークショップで追加する機能）

以下の機能は `prd/校正管理システム_要件定義書.md` に定義されていますが、
**意図的に未実装**です。ハンズオン中に Qoder を使って実装します。

- 校正スケジュール自動アラート（Lab 2 機能1）
- 測定不確かさ評価（Lab 2 機能2）

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# ベースラインのテストが全て pass することを確認
python3 -m pytest

# （任意）サンプルデータの投入
python3 -m data.seed

# （任意）ローカルで API サーバを起動
uvicorn app.main:app --reload
```

API ドキュメント（Swagger UI）: http://127.0.0.1:8000/docs

## ディレクトリ構成

```
calibration-tracker/
├── app/
│   ├── main.py               # FastAPI エントリポイント
│   ├── database.py           # Engine / Session 管理
│   ├── models/               # SQLAlchemy ORM モデル
│   ├── schemas/              # Pydantic スキーマ
│   ├── services/             # ビジネスロジック
│   └── routes/               # API ルート
├── tests/                    # pytest テスト（ベースライン）
├── data/
│   └── seed.py               # サンプルデータ投入スクリプト
├── prd/
│   └── 校正管理システム_要件定義書.md   # Lab 1 の入力となる PRD
└── requirements.txt
```

## 技術スタック

- Python + FastAPI
- SQLAlchemy（SQLite、POC 段階）
- pytest / pytest-cov

## Qoder での準備

1. 本リポジトリを Qoder で開く（File → Open Folder）
2. サイドバーの Wiki アイコン → 「Index Repository」で Repo Wiki を初期化
3. `prd/校正管理システム_要件定義書.md` を読み、Lab 1 に進む
