# RoboEvaluater

オープンソースの IMM（インパクト測定・マネジメント）評価ツールです。
[Impact Management Project (IMP)](https://impactfrontiers.org/) の5次元
（What / Who / How much / Contribution / Risk）にもとづいて、プロジェクトや
団体のインパクトを評価し、レポートを生成します。

同じスコアリングロジックを2つの形で提供しています。

## 1. Webアプリ（NPO・非エンジニア向け）

インストール不要、ブラウザだけで完結するフォーム形式のツールです。データは
どこにも送信されず、すべてブラウザ内で計算されます。

```
cd webapp
python3 -m http.server 8000
# ブラウザで http://localhost:8000 を開く
```

GitHub Pages で公開する場合は、リポジトリの Settings → Pages で
`main` ブランチの `/webapp` フォルダを公開先に設定してください。

## 2. Claude スキル（エンジニア・Claude Code利用者向け）

`skill/imm-evaluator/` は Claude Code のスキルとして使えます。ご自身の
`.claude/skills/` にコピーするか、このリポジトリをスキルソースとして
参照してください。

```
cd skill/imm-evaluator
python3 scripts/evaluate.py reference/answers.example.json
```

詳細は [`skill/imm-evaluator/SKILL.md`](skill/imm-evaluator/SKILL.md) と
[`skill/imm-evaluator/reference/imp-five-dimensions.md`](skill/imm-evaluator/reference/imp-five-dimensions.md)
（スコアリングモデルの解説）を参照してください。

## ドキュメント

- [`docs/impact-frontiers-gap-analysis-2026-09.md`](docs/impact-frontiers-gap-analysis-2026-09.md)
  — 規範の管理団体である Impact Frontiers の現行規範と本ツールのギャップ分析、
  および今後の進化方針（2026-09）

## 開発

```
pip install pytest
pytest skill/imm-evaluator/tests/
```

## 注意事項

このツールは IMP の5次元フレームワークをもとにした、独自の簡略化された
オペレーショナリゼーションです。IMP による公式の認証・評価ツールでは
ありません。資金提供者向けの正式な報告に使う場合は、その旨を明記して
ください。

## ライセンス

MIT License. 詳細は [LICENSE](LICENSE) を参照してください。
