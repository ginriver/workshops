# Vulnerable Snippets — 意図的に脆弱性を含む教材コード

> ⚠️ **これらのファイルは Qoder Security の検出体験のための教材です。**
> **絶対に本番環境へデプロイしないでください。**

| ファイル | 脆弱性クラス | 想定検出レイヤー |
|---|---|---|
| `vuln1_command_injection.py` | OSコマンドインジェクション (CWE-78) | L1 / L2 |
| `vuln2_sql_injection.py` | SQLインジェクション (CWE-89) | L1 / L2 / L3 |
| `vuln3_path_traversal.py` | パストラバーサル (CWE-22) | L2 / L3 |
| `vuln4_insecure_deserialization.py` | 安全でないデシリアライゼーション (CWE-502) | L1 / L2 |
| `vuln5_secret_leakage.py` | ハードコード認証情報 + ログ漏えい (CWE-798 / CWE-532) | L1 |

## 使い方

1. ファイルを `app/routes/` へコピーする
2. `app/main.py` にマウントする:

```python
from app.routes.vuln1_command_injection import router as vuln1_router

app.include_router(vuln1_router, prefix="/api/v1")
```

3. `uvicorn app.main:app --port 8000` を起動して動作確認

各ファイルの詳細な使い方は `../LAB_GUIDE.md` を参照してください。
脆弱性が実際に悪用可能であることの証明は `../exploit_playbook.md` にあります。
