# Lab 5 ガバナンス層パッケージ（講師向け説明）

## なぜ `.qoder/` がルートにないのか

**Before / After の対比**を明確にするための意図的な設計です。

- クローン直後のリポジトリには `.qoder/` も `AGENTS.md` もありません。
  → **Lab 1〜4 は「開発規範なし」の状態**で Qoder を体験します（フリー開発）。
- Lab 5 で `enable-governance.sh` を実行し、ガバナンス層をルートへ復元します。
  → **同じようなプロンプトを再実行**して、規範あり/なしの振る舞いの差を体感します。

## 構成

```
labs/lab5-governance/
├── README.md                    # 本ファイル
├── enable-governance.sh         # 復元スクリプト（Lab 5 で実行）
└── governance-pack/
    ├── AGENTS.md                # 常時適用のコア規範（復元先: ルート）
    └── qoder-config/            # 復元先: ルートの .qoder/
        ├── settings.json        # Hooks 設定（Stop 品質ゲート / PreToolUse 危険コマンド遮断）
        ├── hooks/               # ゲート実装スクリプト
        ├── rules/               # coding-standards / api-design
        └── skills/
            └── uncertainty-eval/  # GUM 不確かさ評価のドメイン知識
```

## Lab 5 の流れ

1. `bash labs/lab5-governance/enable-governance.sh` を実行
2. **Qoder IDE を再起動**（Hooks はホットリロード未対応）→ 新規チャット開始
3. `AGENTS.md` / `.qoder/rules/` / `.qoder/skills/` / `.qoder/settings.json` を開いて仕組みを説明
4. Lab 2 と同じようなプロンプトを再実行 → 前後比較（階層化の遵守、pytest 自動実行、テスト必須）
5. Hooks の体験：`rm -rf` を Agent に依頼（PreToolUse で遮断）/ テストを壊して完了させる（Stop ゲートで拒否）
6. Plugins：Settings → Plugins → Import で `governance-plugin/calibration-team-standards` を読み込み

## 補足

- 復元された `.qoder/` と `AGENTS.md` は git 上 untracked として表示されます（問題ありません）。
- Rules の適用タイプは Qoder Settings → Rules で確認・変更できます。
- 元の状態（規範なし）に戻す場合は、`.qoder/` と `AGENTS.md` を別フォルダへ移動し、IDE を再起動してください。
