# Agent Skills標準への移行計画

## 背景・目的

### 現状の課題

1. **ツール依存性の問題**
   - 現在の `.ai/agents/`, `.ai/commands/` 構造はClaude Code CLI専用
   - Cursor, VS Code等の他ツールでは互換性がない
   - プロジェクトの目標「複数AIアシスタント対応」が達成できていない

2. **Agent Skills標準化の進展**
   - 2024年12月18日にAnthropicがagentskills.ioで仕様を公開
   - Microsoft (VS Code), Cursor, Goose等が既に採用
   - 業界標準として確立されつつある

3. **コンテキスト構造の複雑化**
   - Commands (7ファイル、11,989トークン)
   - Agents (2ファイル、3,387トークン)
   - References (15ファイル、18,129トークン)
   - 依存関係が複雑で、references参照が多重化

### 移行の目的

1. **ツール非依存性の実現** - Cursor, Claude Code, VS Code等で動作
2. **標準準拠** - agentskills.io仕様への準拠
3. **保守性の向上** - Skills単位での自己完結性
4. **後方互換性** - 既存ユーザーへの影響を最小化

---

## 現状分析

### 現在のディレクトリ構造

```
template/.ai/
├── context.md          # 1,679トークン (warning)
├── agents/             # 2ファイル、3,387トークン
│   ├── architect.md
│   └── researcher.md
├── commands/           # 7ファイル、11,989トークン
│   ├── breakdown.md
│   ├── code-review.md
│   ├── context-update.md
│   ├── critical-think.md
│   ├── debug.md
│   ├── implement.md
│   └── review-update.md
├── references/         # 15ファイル、18,129トークン
│   ├── checklists/code-review/*.md (5ファイル)
│   ├── guides/*.md (4ファイル)
│   ├── patterns/*.md (1ファイル)
│   └── templates/*.md (5ファイル)
└── scripts/
    └── measure-context.py

.claude/skills/
└── context-advisor/    # このリポジトリ固有の開発用Skill
    ├── SKILL.md
    └── references/
```

### 依存関係マップ

| Command/Agent | 参照するReferences |
|--------------|-------------------|
| code-review.md | checklists/code-review/* (5), guides/code-review-agents.md, guides/code-review-self-reflection.md, templates/code-review-output.md |
| breakdown.md | guides/task-breakdown.md, templates/implementation.md |
| implement.md | guides/task-roles.md |
| context-update.md | templates/adr.md |
| review-update.md | checklists/code-review.md |

---

## 設計提案

### オプション1: 完全移行（推奨）

**構造**:
```
template/.ai/
├── context.md          # 既存のまま維持
├── skills/             # 新規: Agent Skills標準準拠
│   ├── architect/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── researcher/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── checklists/
│   │       ├── guides/
│   │       └── templates/
│   ├── breakdown/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── implement/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── critical-think/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── context-update/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── debug/
│   │   ├── SKILL.md
│   │   └── references/
│   └── review-update/
│       ├── SKILL.md
│       └── references/
├── scripts/            # 既存のまま維持
└── [deprecated]        # 移行後に削除予定
    ├── agents/
    ├── commands/
    └── references/

.claude/skills/
└── context-advisor/    # 既存のまま（開発用）
```

**利点**:
- ✅ 完全なツール非依存性
- ✅ Skills単位で自己完結
- ✅ 標準準拠で将来性が高い

**欠点**:
- ❌ 移行作業が大規模
- ❌ 既存ユーザーへの影響が大きい

### オプション2: ハイブリッド（段階的移行）

**構造**:
```
template/.ai/
├── context.md
├── skills/             # 新規: 優先度高いものから移行
│   ├── code-review/
│   └── architect/
├── agents/             # 残存: 移行中
│   └── researcher.md
├── commands/           # 残存: 移行中
│   ├── breakdown.md
│   └── ...
└── references/         # Skills移行済みのものは削除
```

**利点**:
- ✅ 段階的な移行が可能
- ✅ 既存ユーザーへの影響を段階化

**欠点**:
- ❌ 構造の二重管理期間が発生
- ❌ ドキュメントの複雑化

### オプション3: 並行運用（非推奨）

両方の構造を維持。

**欠点**:
- ❌ メンテナンスコスト倍増
- ❌ 混乱を招く

---

## 推奨案: オプション1（完全移行）

**理由**:
1. Agent Skills標準は既に確立しており、待つ理由がない
2. プロジェクトの規模が小さく、一括移行が実現可能
3. 長期的なメンテナンス負荷を最小化

### Agent Skills標準フォーマット

```yaml
---
name: skill-identifier          # 必須: kebab-case
description: スキルの説明        # 必須: トリガー判定に使用
version: "1.0.0"                # オプション
model: sonnet                    # オプション（Claude Code専用拡張）
allowed-tools: "Read,Grep,Bash" # オプション（Claude Code専用拡張）
---

# Skill詳細説明

Markdown形式の指示とガイドライン
```

### Skills統合マッピング

| 統合後Skill | 元ファイル | 統合するReferences |
|-----------|----------|-------------------|
| **architect** | agents/architect.md | - |
| **researcher** | agents/researcher.md | templates/report.md |
| **code-review** | commands/code-review.md | checklists/code-review/* (5), guides/code-review-*.md (2), templates/code-review-output.md, patterns/code-review-patterns.md |
| **breakdown** | commands/breakdown.md | guides/task-breakdown.md, templates/implementation.md |
| **implement** | commands/implement.md | guides/task-roles.md |
| **critical-think** | commands/critical-think.md | - |
| **context-update** | commands/context-update.md | templates/adr.md |
| **debug** | commands/debug.md | - |
| **review-update** | commands/review-update.md | - |

**汎用Templates**（複数Skillsから参照）:
- `templates/command.md` - 新規Skill作成時の参考として `docs/guides/` に移動

---

## 実装方針

### Phase 1: 基盤整備（破壊的変更なし）

1. **Skills ディレクトリ作成**
   - `template/.ai/skills/` を作成
   - README.md でSkills標準について説明

2. **移行ツール開発**
   - `scripts/migrate-to-skills.py` - 自動移行スクリプト
   - `scripts/validate-skills.py` - Skills形式の検証

3. **ドキュメント準備**
   - `docs/migration-guide.md` - 移行ガイド作成
   - CHANGELOG.md にv2.0.0予告を記載

### Phase 2: Skills移行（優先度順）

**優先度判断基準**:
- 参照の多いもの（code-review等）
- 独立性の高いもの（critical-think等）

1. **Tier 1（独立型）** - 並列実行可能
   - critical-think
   - debug
   - architect
   - researcher

2. **Tier 2（軽量参照型）**
   - context-update (templates/adr.md)
   - review-update

3. **Tier 3（重量参照型）**
   - code-review (9ファイル参照)
   - breakdown (2ファイル参照)
   - implement (1ファイル参照)

### Phase 3: 後処理

1. **非推奨化**
   - `template/.ai/agents/` → `template/.ai/[deprecated]/agents/`
   - `template/.ai/commands/` → `template/.ai/[deprecated]/commands/`
   - `template/.ai/references/` → 削除（Skills内に統合済み）

2. **CLAUDE.md 更新**
   - Agent Skills標準準拠を明記
   - ディレクトリ構造図の更新

3. **examples/ 更新**
   - 各技術スタック例をSkills形式に更新

4. **バージョンタグ**
   - `git tag v2.0.0` - 破壊的変更

---

## 考慮事項・リスク

### リスク1: 既存ユーザーへの影響

**影響**:
- Claude Code CLI: `/command-name` がそのまま動作しなくなる可能性
- Cursor: 既存の `.ai/` 構造に依存している場合、動作しない

**緩和策**:
- Phase 1で移行ガイドを事前公開
- CHANGELOG.mdで事前告知
- [deprecated] ディレクトリを1バージョン維持

### リスク2: Claude Code固有機能の喪失

**懸念**:
- `allowed-tools` はClaude Code専用拡張
- 他ツールで無視される可能性

**対策**:
- YAML frontmatterに `allowed-tools` を含める（標準外だが無害）
- ドキュメントで「Claude Code拡張」と明記

### リスク3: トークン数の増加

**懸念**:
- References統合でSkills単体のトークン数増加

**対策**:
- `measure-context.py` をSkills対応に拡張
- Skill別のトークン閾値設定（5,000トークン上限）

### リスク4: 移行スクリプトのバグ

**対策**:
- `scripts/validate-skills.py` で事前検証
- Phase 2で1Skillずつ慎重に移行
- Git履歴で簡単にロールバック可能

---

## 成功基準

1. ✅ 全9 Skills が agentskills.io 仕様に準拠
2. ✅ Cursor, Claude Code, VS Code で動作確認
3. ✅ 各Skillのトークン数が5,000以下
4. ✅ 移行ガイド・CHANGELOGが完備
5. ✅ CI/CDでSkills検証が自動実行

---

## タイムライン（概算）

| Phase | 内容 | 推定工数 |
|-------|------|---------|
| Phase 1 | 基盤整備 | 3-4h |
| Phase 2.1 | Tier 1移行（4 Skills） | 4-6h |
| Phase 2.2 | Tier 2移行（2 Skills） | 2-3h |
| Phase 2.3 | Tier 3移行（3 Skills） | 5-7h |
| Phase 3 | 後処理・文書化 | 2-3h |
| **合計** | | **16-23h** |

---

## 次のステップ

1. **決定事項の確認**
   - この計画でよいか？
   - オプション1（完全移行）で進めるか？
   - 優先度・順序に変更はないか？

2. **実装開始**
   - `/breakdown` で implementation.md 生成
   - `/implement` で自動実行
   - または手動で順次実装

3. **検証**
   - 各Phaseでの動作確認
   - 複数ツールでの互換性テスト
