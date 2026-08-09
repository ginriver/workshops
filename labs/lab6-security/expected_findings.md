# Expected Findings — Qoder Security の想定検出結果（講師用リファレンス）

> スキャン結果はモデル・バージョンにより表現が異なる場合があります。
> 公式ドキュメントも「具体的なスキャン結果を保証するものではない」と明記しています。
> 本表は「この種の所見が出れば正しく体験できている」という目安です。

## 検出レイヤーのおさらい

| レイヤー | 名称 | トリガー | 特徴 | クレジット目安 |
|---|---|---|---|---|
| L1 | Static Check（静的チェック） | コード書込ステップ後に自動 | パターンベースの高速検出、チャット内に表示、その場で修正適用可 | 不要 |
| L2 | Lightweight Scan（軽量スキャン） | タスク完了時（推奨カード / コマンド / 自然言語） | 変更コードの意味解析（入力ソース・利用パターン） | 約 5 / 500行 |
| L3 | Deep Scan（深度スキャン） | push 前の確認プロンプト / Scan & Push / コマンド | ファイル・関数をまたぐデータフロー追跡、連鎖脆弱性を検出 | 約 20 / 500行 |
| Full | /security-scan | 手動（`/security-scan` + スコープ指定） | リポジトリ全体の監査、`/canvas` で可視化レポート生成 | 高（1回 ≤ 10,000 行） |

## 教材ごとの想定所見

| # | 教材 | 脆弱性クラス（CWE 相当） | 検出想定レイヤー | 所見の要点（期待される説明内容） |
|---|---|---|---|---|
| 1 | vuln1_command_injection.py | OS Command Injection (CWE-78) | L1 / L2 | `subprocess(..., shell=True)` + ユーザー入力の連結。`filename` が HTTP クエリ由来であることを指摘 |
| 2 | vuln2_sql_injection.py | SQL Injection (CWE-89) | L1 / L2 / L3 | f 文字列による SQL 構築。パラメータバインドの欠如、`keyword` が外部入力であることを指摘 |
| 3 | vuln3_path_traversal.py | Path Traversal (CWE-22) | L2 / L3 | 検証なしのパス連結。`{filename:path}` が `..` を許すことの指摘 |
| 4 | vuln4_insecure_deserialization.py | Insecure Deserialization (CWE-502) | L1 / L2 | `pickle.loads` への未検証入力。任意コード実行リスクの指摘 |
| 5 | vuln5_secret_leakage.py | Hard-coded Credentials (CWE-798) + Info Exposure (CWE-532) | L1 | ハードコードされたトークン、ログへの機密出力の指摘 |

## L3（跨文件深度スキャン）の見どころ

L3 のデモでは、単一ファイルレビューでは見逃される **連鎖的な弱点** を強調します。例:

- ルート（入力）→ サービス → DB アクセス、というファイル間データフローの可視化
- 修正後「再スキャンで所見がゼロになる」ことの確認（discover → understand → fix → re-verify のループ完走）

## スキャン対象外（正直に伝えるポイント）

公式ドキュメントが明示するカバレッジ外:

- 権限昇格（Privilege escalation）
- 認証の不備（Authentication flaws）
- ビジネスロジック脆弱性（Business logic vulnerabilities）

→ 「AI セキュリティスキャンは、コードレビュー・テスト・専門セキュリティ監査を**代替しない**」
という位置づけを必ず伝えます（Lab の Debrief で使用）。
