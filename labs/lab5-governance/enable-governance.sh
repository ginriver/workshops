#!/bin/bash
# Lab 5: チーム開発規範ガバナンス層を復元する（Before/After 対比デモ用）
#
# Lab 1〜4 はガバナンス層「なし」で体験し、Lab 5 で本スクリプトを実行して
# .qoder/（Rules / Skills / Hooks）と AGENTS.md をリポジトリルートへ復元します。
#
# 用法: bash labs/lab5-governance/enable-governance.sh
# 注意: 復元後は Qoder IDE を再起動（または新規チャットを開始）してください。
#       Hooks はホットリロードされません。

set -euo pipefail

# リポジトリルートへ移動（スクリプトは labs/lab5-governance/ に配置）
cd "$(dirname "$0")/../.."

SRC="labs/lab5-governance/governance-pack"

if [ ! -d "$SRC/qoder-config" ]; then
  echo "ERROR: $SRC/qoder-config が見つかりません。" >&2
  exit 1
fi

if [ -d .qoder ]; then
  echo ".qoder/ は既に存在します（ガバナンス層は既に有効です）。"
else
  cp -R "$SRC/qoder-config" .qoder
  echo "OK: .qoder/ を復元しました（Rules / Skills / Hooks）。"
fi

if [ -f AGENTS.md ]; then
  echo "AGENTS.md は既に存在します（スキップ）。"
else
  cp "$SRC/AGENTS.md" AGENTS.md
  echo "OK: AGENTS.md を復元しました。"
fi

echo ""
echo "復元完了。次の手順で続けてください："
echo "  1. Qoder IDE を再起動（Hooks はホットリロード未対応）"
echo "  2. 新規チャットを開始し、Lab 2 と同じようなプロンプトで前後比較を実施"
