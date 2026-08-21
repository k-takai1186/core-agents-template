---
name: template-generalization-and-audit
description: 個別プロジェクトのコード・規約資産から環境依存を排除し、完全自立型の汎用AIエージェントテンプレート（Microsoft 400 Capable）へ昇華・監査するための標準チェックリストプロトコル
category: core
version: 1.0.0
---

# 汎用テンプレート昇華 ＆ 自立性監査 Skill (Template Generalization & Audit)

本スキルは、個別プロジェクトで開発された AI エージェント規約・スクリプト・スキル群を、他のあらゆるプロジェクトへ即座に展開可能な **「完全自立型汎用テンプレート（Microsoft 400 Capable）」** へ昇華させるための標準チェックリストおよび検証手順を定義します。

---

## 📋 5 フェーズ・自立性監査チェックリスト

### Phase 1: 固有依存スキャン (Dependency Scan)
- [ ] **絶対パスの排除:** 環境固有の絶対パス（例: ドライブ文字直書きや `file://` スキーム）が残存していないか（相対パスで統一）。
- [ ] **固定モデル名の抽象化:** 特定モデル名が直書きされず、`.agents/agent_config.json` のロール定義（primary/review）に外出しされているか。
- [ ] **業務固有語の撤去:** 個別テーブル名や業務専門用語が Core 規約に混入していないか。

### Phase 2: Core / Domain の物理分離 (Clean Architecture)
- [ ] **規約の分離:** 汎用規約（行動規範・DoD・Dual-AI等）は `AGENTS.md`、プロジェクト固有規約は `DOMAIN.md.example` へ完全分離されているか。
- [ ] **スキルの分類:** 各スキルの Frontmatter に `category: core` または `category: domain` が明記されているか。

### Phase 3: クロスプラットフォーム適合 (POSIX & Windows)
- [ ] **ロジックの Python 一本化:** ツール本体は Python 標準ライブラリのみで実装され、OS 固有スクリプト（`.ps1`, `.sh`）は単なる 1 行ラッパーになっているか。
- [ ] **環境非依存コマンド:** `sed -i` や `grep -P` などの GNU/BSD 非互換構文を使用せず、POSIX 標準（`grep -E`）または Python 内で完結しているか。

### Phase 4: ゼロコンフィグ ＆ プレースホルダ設計 (Zero-Config)
- [ ] **未設定時の安全性:** `agent_config.json` の未設定ゲート（例: `g3_build: ""`）はエラーで落ちず、警告を出して安全にスキップされるか。
- [ ] **配備時置換配線:** `{{PROJECT_NAME}}`, `{{config_path}}` 等のプレースホルダが `sync_agent_template.py` の配備処理で正しく解決されるか。

### Phase 5: 自律スモークテスト検証 (Microsoft 400 判定)
- [ ] **スモークテスト実行:** `python3 scripts/sync_agent_template.py -Test` を実行し、全項目 PASS (exit 0) を確認。
- [ ] **ユニットテスト通過:** `python3 -m unittest discover -s tests -q` が exit 0 で通過すること。
