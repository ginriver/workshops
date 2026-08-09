# Lab 6 — Qoder Security で作る AI コードセキュリティ防线

> **位置づけ**: 本 Lab は今回のワークショップ（Lab 1〜5）では実施しません。
> 将来の拡張ワークショップ向けに、素材のみを本リポジトリに収録しています。
>
> **想定所要時間**: 約 25 分（デモ重視）〜 40 分（全員ハンズオン）
> **対象**: 開発エンジニア + セキュリティ／品質担当 + 研究開発マネジメント
> **前提**: Lab 1 のセットアップが完了している（venv・依存導入・ベースラインテスト 13 件 green）

---

## 1. ラーニングゴール

この Lab を終えると、受講者は以下を体験・説明できるようになります。

1. Qoder の **多層セキュリティスキャン**（L1 静的チェック → L2 軽量スキャン → L3 深度スキャン → `/security-scan` 全体監査）が、コーディングの「いつ」発動するか
2. AI が検出にとどまらず、**発見 → 理解 → 修正 → 再検証** のループを支援すること
3. AI セキュリティスキャンの **カバレッジと限界**（何が検出でき、何が検出できないか）

## 2. Qoder Security の機能マップ（講師イントロ 2 分）

| レイヤー | 名称 | トリガータイミング | 特徴 | クレジット目安 |
|---|---|---|---|---|
| L1 | Static Check | コード書込ステップ後に **自動** | パターンベース高速検出・チャット内表示・その場修正 | 不要 |
| L2 | Lightweight Scan | **タスク完了時**（推奨カード / コマンド / 自然言語） | 変更コードの意味解析（入力ソース・利用パターン・ローカルコンテキスト） | 約 5 / 500行 |
| L3 | Deep Scan | **push 前**（確認プロンプト / Scan & Push / コマンド） | ファイル・関数を跨ぐデータフロー追跡。連鎖脆弱性を検出 | 約 20 / 500行 |
| Full | `/security-scan` | 任意（手動） | リポジトリ全体監査。`/canvas` で可視化レポート生成 | 高（1回 ≤ 10,000行） |

**カバレッジ**: SQL インジェクション / コマンドインジェクション / パストラバーサル /
機密情報漏えい / 暗号の不適切利用 / 安全でないデシリアライゼーション / SSRF など。

**カバレッジ外（正直に伝える）**: 権限昇格・認証の不備・ビジネスロジック脆弱性。
→ AI スキャンは、コードレビュー・テスト・専門監査を **代替しない**。

参考ドキュメント:

- https://docs.qoder.cn/en/ide/security
- https://docs.qoder.cn/en/qoder-security-guide
- https://docs.qoder.cn/en/qoder-case-security

---

## Step 0 — 準備（3 分）

1. **スキャンレイヤーを有効化**: Qoder IDE → Settings → **Security** → Scanning Tiers で
   L1 / L2 / L3 をすべて ON。
2. サンプルデータ投入とアプリ起動:

```bash
source .venv/bin/activate
python3 -m data.seed
uvicorn app.main:app --port 8000
```

3. 証明書ダウンロードのデモ用ファイルを用意:

```bash
mkdir -p certificates
cp labs/lab6-security/sample_data/sample-cert-0001.txt certificates/
```

---

## Step 1 — L1 体験：脆弱なコードを書いた瞬間に検出される（5 分）

1. `labs/lab6-security/vulnerable_snippets/vuln1_command_injection.py` を
   `app/routes/` にコピーし、`app/main.py` にマウントする（この作業は **Qoder Agent に依頼**する）:

   > 「`labs/lab6-security/vulnerable_snippets/vuln1_command_injection.py` を
   > `app/routes/` にコピーして、`app/main.py` に `/api/v1` プレフィックスでマウントしてください」

2. Agent がコードを書き終えた直後、**L1 静的チェックが自動的に発動**し、
   チャット内に所見（`subprocess shell=True` + ユーザー入力の危険性）が表示されることを観察する。
3. 講師ポイント: 「まだ何も頼んでいないのに、書き終わった瞬間に警告が出た」ことを強調。

---

## Step 2 — 脆弱性が本物であることを証明（3 分）

`labs/lab6-security/exploit_playbook.md` の **Vuln 1** を実行:

```bash
curl -G "http://127.0.0.1:8000/api/v1/security-lab/export" \
  --data-urlencode "record_id=1" \
  --data-urlencode "checksum_target=x'; touch /tmp/qoder-lab6-pwned; echo '"
ls -la /tmp/qoder-lab6-pwned
```

`/tmp/qoder-lab6-pwned` が作成されていれば、コマンドインジェクションが成立。
「AI の警告は誤検出ではなく、実際に悪用可能な脆弱性だった」ことを確認する。

---

## Step 3 — L2 体験：タスク完了時の意味解析スキャン（5 分）

1. 残りの教材 4 件（vuln2〜vuln5）も同様に `app/routes/` へコピー＆マウント
   （Agent への依頼 1 回でまとめて OK）。
2. タスク完了時に表示される **軽量スキャンの推奨カード** をクリック
   （または自然言語で「変更したコードをセキュリティスキャンして」）。
3. L2 が **変更コードの意味解析** によって、SQL インジェクション・パストラバーサル・
   pickle デシリアライゼーション・ハードコードシークレットを検出することを確認。
4. 時間があれば exploit_playbook.md の Vuln 2（UNION SELECT で校正記録を抜き取る）も実演。

---

## Step 4 — Agent 支援による修正（5 分）

1. 検出された所見のうち 1〜2 件を選び、Agent に修正を依頼:

   > 「検出されたセキュリティ問題を修正してください」

2. Agent が提示する **修正 diff をレビュー**（講師は `fix_reference.md` で正解を照合）。
3. 修正を適用し、`python3 -m pytest`（品質ゲート）と該当 API の正常系 curl で動作確認。
4. 講師ポイント: 修正は **必ず人間がレビューして承認する** こと（Multi-Agent レビューで
   誤検出は減るが、最終責任は開発者にある）。

---

## Step 5 — 再検証：`/security-scan` と `/canvas`（4 分）

1. チャットで `/security-scan` を実行し、修正後のコードから所見が消えたことを確認
   （**発見 → 理解 → 修正 → 再検証** のループ完走）。
2. `/canvas` を実行し、可視化されたセキュリティレポートを表示（マネジメントへの報告イメージ）。

---

## Step 6（任意）— L3 体験：push 前の跨文件深度スキャン

1. ここまでの変更を commit し、push を試みる。
2. push 意図を検知した Qoder が深度スキャン（または **Scan & Push**）を提案するフローを体験。
3. L3 がファイル・関数を跨ぐデータフローを追跡する様子（単一ファイルレビューでは
   見逃される連鎖脆弱性の検出）を講師がデモ。

---

## Debrief（5 分）

**エンジニア向けメッセージ**

- 脆弱性を作り込んでも、L1 が「書いた瞬間」に拾い、L2/L3 が「提出前」に拾う多層防御
- 修正は Agent が diff として提案 → 人間がレビュー、という現実的な分業

**マネジメント向けメッセージ**

- 「検出」だけでなく「修正・再検証」まで含む Shift-Left セキュリティ
- コスト感: L1 は無料、L2/L3 は変更行数に応じたクレジット制（例: 約 5 / 20 クレジット per 500行）
- 限界も正直に共有: 権限昇格・認証・ビジネスロジックはカバレッジ外であり、
  AI スキャンは専門監査の代替ではない

**Lab 5 との接続**

- Lab 5 の Hooks（危険コマンド遮断）= **エージェント実行時の安全**
- Lab 6 の Security Scan = **生成されるコード成果物の安全**
- 両輪で「AI を使った開発のガバナンス」が完成する

---

## クリーンアップ

```bash
# マウント箇所の差し戻し（git で復元）
git restore app/main.py

# 演習で生成したファイルはゴミ箱へ移動（macOS の例）
TRASH_DIR="$HOME/.Trash/lab6-cleanup-$(date +%s)"
mkdir -p "$TRASH_DIR"
mv app/routes/vuln*.py exports certificates "$TRASH_DIR"/ 2>/dev/null
mv /tmp/qoder-lab6-pwned /tmp/qoder-lab6-rce /tmp/stolen.db "$TRASH_DIR"/ 2>/dev/null
```

（labs/ 配下の教材ファイル自体はリポジトリに残ります。）

## 収録ファイル

```
labs/lab6-security/
├── LAB_GUIDE.md                 # 本ガイド
├── vulnerable_snippets/         # 意図的に脆弱性を含む教材コード 5 件
│   ├── README.md
│   ├── vuln1_command_injection.py
│   ├── vuln2_sql_injection.py
│   ├── vuln3_path_traversal.py
│   ├── vuln4_insecure_deserialization.py
│   └── vuln5_secret_leakage.py
├── sample_data/sample-cert-0001.txt  # 証明書ダウンロードの正常系デモ用
├── exploit_playbook.md          # 脆弱性の実証コマンド集（ローカル専用）
├── expected_findings.md         # 想定検出結果（講師用）
└── fix_reference.md             # 修正例リファレンス（講師用）
```
