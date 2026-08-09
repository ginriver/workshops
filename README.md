# Calibration Tracker — 計量校正管理システム

精密機器メーカー向け計量校正管理システムの **ハンズオン演習用ベースラインリポジトリ**です。
Qoder AI エージェント実践ワークショップの Lab 1〜5 で本リポジトリを使います。

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
├── AGENTS.md                 # 常時適用のチーム開発規範（Lab 5）
├── .qoder/
│   ├── rules/                # Rules：coding-standards / api-design（Lab 5）
│   ├── skills/
│   │   └── uncertainty-eval/ # Skills：GUM 不確かさ評価のドメイン知識
│   ├── hooks/                # Hooks：品質ゲート / 危険コマンド遮断
│   └── settings.json         # Hooks 設定（プロジェクト共有）
├── governance-plugin/
│   └── calibration-team-standards/  # Plugins：チーム標準の一括配布サンプル
├── labs/
│   └── lab6-security/        # 将来の拡張 Lab 6（Qoder Security）教材 ※今回は未実施
└── requirements.txt
```

## チーム開発規範ガバナンス層（Lab 5）

本リポジトリには、Qoder の拡張機制による「チーム開発規範の強制」サンプルが含まれています。
Lab 1〜4 の間もこれらが自動的に効いています（沈黙体験）。

| 機制 | 場所 | 役割 |
|---|---|---|
| AGENTS.md | ルート | 常時適用のコア規範（階層化 / テスト必須 / API セマンティクス） |
| Rules | `.qoder/rules/` | 詳細規範。4 種タイプ（Always Apply / Model Decision / Specific Files / Apply Manually） |
| Skills | `.qoder/skills/uncertainty-eval/` | GUM 不確かさ評価のドメイン知識。git でチーム共有 |
| Hooks | `.qoder/settings.json` + `.qoder/hooks/` | 決定的ゲート：Stop で pytest 緑を強制、PreToolUse で `rm -rf` / `git push --force` を遮断 |
| Plugins | `governance-plugin/calibration-team-standards/` | Skills + Hooks + Commands を一括パッケージ化し、組織へ一括配布するサンプル |

補足：

- Hooks 設定を変更した後は Qoder IDE の再起動が必要です（ホットリロード未対応）。
- Rules の適用タイプは Qoder Settings → Rules で確認・変更できます（`.qoder/rules/` は git 共有）。
- `governance-plugin/` は Lab 5 のデモ用サンプルです。Settings → Plugins → Import からローカルフォルダとして読み込めます。

## 将来の拡張 Lab（今回のワークショップでは未実施）

- **`labs/lab6-security/`** — Lab 6: Qoder Security で作る AI コードセキュリティ防线（約 25 分）
  意図的に脆弱性を含む教材コード 5 件（コマンドインジェクション / SQLインジェクション /
  パストラバーサル / 安全でないデシリアライゼーション / 機密情報漏えい）、
  脆弱性実証プレイブック、講師用リファレンスを含む。
  詳細は [`labs/lab6-security/LAB_GUIDE.md`](labs/lab6-security/LAB_GUIDE.md) を参照。
  ⚠️ 教材コードは教育目的であり、本番環境へデプロイしないでください。

## 技術スタック

- Python + FastAPI
- SQLAlchemy（SQLite、POC 段階）
- pytest / pytest-cov

## Qoder での準備

1. 本リポジトリを Qoder で開く（File → Open Folder）
2. サイドバーの Wiki アイコン → 「Index Repository」で Repo Wiki を初期化
3. `prd/校正管理システム_要件定義書.md` を読み、Lab 1 に進む
