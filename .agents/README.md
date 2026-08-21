# .agents - AI Agent 開発基盤 ＆ スキルインデックス

本ディレクトリは、AI アシスタントおよび開発チームが遵守するコーディング規約、協働プロトコル（[AGENTS.md](AGENTS.md)）、および再利用可能な専門スキル群（`skills/`）を管理・提供する汎用開発基盤です。

---

## 📚 スキルカタログ (Skill Catalog)

### 🌟 Core Skills (汎用基盤スキル - 横展開可能 10 種)

| スキル名 | バージョン | 概要・適用場面 |
| :--- | :---: | :--- |
| [`architecture-decision-records`](skills/architecture-decision-records/SKILL.md) | `v1.0.0` | 重要設計・技術選定の意思決定を ADR (`docs/adr/`) として自動記録 |
| [`requirements-to-spec`](skills/requirements-to-spec/SKILL.md) | `v1.0.0` | 曖昧な要望やアイデアから高精度な機能仕様書を構造化作成 |
| [`self-audit-and-regression-prevention`](skills/self-audit-and-regression-prevention/SKILL.md) | `v1.0.0` | 水平展開監査・冪等性・回帰防止の自己監査プロトコル |
| [`large-scale-code-refactoring`](skills/large-scale-code-refactoring/SKILL.md) | `v1.0.0` | 後方互換性を担保した大規模モジュール分割・ファサードパターン |
| [`release-review`](skills/release-review/SKILL.md) | `v1.0.0` | バージョン固定（リリース）前の品質・セキュリティ・耐障害性レビュー |
| [`design-and-plan`](skills/design-and-plan/SKILL.md) | `v1.0.0` | テーブル追加・機能拡張時の設計手順・計画策定基準 |
| [`implementation-and-refactor`](skills/implementation-and-refactor/SKILL.md) | `v1.0.0` | 実装・リファクタリング規約（DRY原則、統一ロガー、環境変数分離） |
| [`testing-and-verification`](skills/testing-and-verification/SKILL.md) | `v1.0.0` | ユニットテスト・結合テスト・コンテナ動作検証の標準手順 |
| [`performance-tuning-and-caching`](skills/performance-tuning-and-caching/SKILL.md) | `v1.0.0` | クエリチューニング、複合インデックス設計、インメモリTTLキャッシュ |
| [`template-generalization-and-audit`](skills/template-generalization-and-audit/SKILL.md) | `v1.0.0` | 汎用テンプレートへの昇華手順 ＆ Microsoft 400 自立性監査チェックリスト |

---

## 🔄 テンプレートの初期化 ＆ 同期

新規プロジェクトへの配備や、マスターとの同期は `scripts/sync_agent_template.py` を使用します。
詳細な運用方法は [AGENT_TEMPLATE_LIFECYCLE.md](../docs/guides/AGENT_TEMPLATE_LIFECYCLE.md) を参照してください。

```bash
# 新規プロジェクトへ Core テンプレートを一括配備
python3 scripts/sync_agent_template.py -Init -TargetPath "/path/to/new-project"

# テンプレートの自己整合性スモークテスト
python3 scripts/sync_agent_template.py -Test
```
