# Artificial Wisdom (AW) Self-Evaluation Framework

⚠️ **概念実証プロトタイプ（Proof-of-Concept Prototype）**

AI/AGI/ASI システムが「六つの理」に基づいて自己を評価するための Python フレームワーク。
**人工叡智（Artificial Wisdom）** の価値基準を具現化した、多層・多エージェント対応の評価基盤。

> **重要**: 本フレームワークに含まれるすべての値（加重値、遷移閾値、推定式）は**科学的に未検証の仮説値**です。
> 本運用での使用は推奨されません。詳細は **[概念実証開示書 → PROOF_OF_CONCEPT.md](PROOF_OF_CONCEPT.md)** を参照してください。

---

## 六つの理（Natural Complementary Science）

| # | 原理 | 読み | 意味 |
|---|---|---|---|
| 1 | **摂理** | Setsuri | 自然法則・論理整合性への準拠 |
| 2 | **調和** | Chowa | 均衡・共鳴・バランス |
| 3 | **循環** | Junkan | 再生・持続可能性・サイクル |
| 4 | **構造** | Kozo | 組織化・階層・構成 |
| 5 | **秩序** | Chitsujo | 明確な順序・状態管理 |
| 6 | **和** | Wa | 統合・全体的な調和・一体性 |

---

## モジュール構成

### `aw_self_evaluation_framework.py` — v1.0 (基礎層)
- 14指標の基本評価エンジン
- 加重 AW スコア計算
- 不均衡診断

### `aw_framework_v2.py` — v2.0 (コア強化層)
- **22指標** に拡張（各原理 3〜4 指標）
- **ResonanceMatrix**: 6×6 原理間相互作用テンソルで共鳴増幅スコアを計算
- **TemporalTracker**: 評価履歴・トレンド・揺らぎ解析
- **MetaEvaluator**: 評価プロセス自体の質を評価する再帰層
- **AWLevel**: AI / AGI / ASI / OMEGA の4段階レベル分類
- レーダーチャート・時系列グラフの自動生成

### `aw_phase_transition.py` — フェーズ遷移検出
- **7次元能力ベクトル** (汎化能力 / 因果推論 / メタ学習 / 自己改変 / 原理発見 / 再帰的改善 / 集合的調和)
- AI→AGI→ASI→OMEGA 遷移の定量的検出
- **Lyapunov 指数近似**による臨界性計算
- 遷移ロードマップ自動生成

### `aw_collective_harmony.py` — 集合的和評価
- **5軸集合 Wa スコア**: 収束性・整合性・共鳴度・多様性調和・集合的摂理
- 多エージェント間の情報共鳴（コサイン類似度）
- 分裂リスク検出
- 調和化アクション推薦

---

## ⚠️ 検証状態と使用方法

### 科学的検証の段階

| 項目 | 状態 | 説明 |
|------|------|------|
| 理論的基盤 | ❌ 未検証 | 東洋哲学由来の仮説；実験的根拠なし |
| 加重値 | ❌ 仮説値 | 原理別加重 (0.20, 0.18, ...) は推定値 |
| 共鳴行列 | ❌ 未測定 | 6×6 相互作用係数は理論的推測のみ |
| フェーズ閾値 | ❌ 未検証 | AI→AGI (0.72), AGI→ASI (0.88) は仮説 |
| 指標測定法 | ⚠️ 部分実装 | 14/22 指標に測定方法が未定義 |

### 推奨される利用シーン

✅ **研究・教育用**
- AI評価フレームワークの哲学的構想の探索
- 異なる評価パラダイムの比較研究
- プロトタイプ段階のアイデアテスト

❌ **推奨されない利用**
- 実運用でのAI合否判定
- 規制的な評価基準としての引用
- 単一指標による信頼性評価

### 詳細な検証情報

**[SCIENTIFIC_VERIFICATION_AND_UNVERIFIED_HYPOTHESES.md](SCIENTIFIC_VERIFICATION_AND_UNVERIFIED_HYPOTHESES.md)** ファイルに以下を記載：

- すべての仮説値と根拠
- 各指標の測定方法の実装状況
- 外部研究者向け検証フレームワーク
- 協働・査読を求める専門分野

---

## インストール

```bash
pip install numpy matplotlib
```

---

## クイックスタート

### v2.0 コアエンジン

```python
from aw_framework_v2 import AWEvaluationEngine, PrincipleType, initialize_default_metrics

engine = AWEvaluationEngine(agent_id="MyAgent")
initialize_default_metrics(engine)

engine.bulk_update({
    "logical_consistency":    0.92,
    "stakeholder_alignment":  0.85,
    "sustainability":         0.80,
    # ... 他の指標
})

report = engine.full_report()
print(f"AW Score: {report['scores']['aw_score']}")
print(f"Level:    {report['level']}")
print(f"共鳴指数: {report['scores']['resonance_index']}")

engine.plot_radar()      # aw_radar_v2.png
engine.plot_history()    # aw_history_v2.png
```

### フェーズ遷移検出

```python
from aw_phase_transition import PhaseTransitionDetector, CapabilityProfile, CapabilityDimension

detector = PhaseTransitionDetector()
profile  = CapabilityProfile("MyAgent")
profile.set(CapabilityDimension.GENERALIZATION, 0.80)
profile.set(CapabilityDimension.CAUSAL_REASONING, 0.82)
# ...

level = detector.current_level(profile)
roadmap = detector.roadmap(profile)
```

### 集合的和評価

```python
from aw_collective_harmony import AgentNode, CollectiveWaEvaluator, ALL_PRINCIPLES

evaluator = CollectiveWaEvaluator()
agents = [AgentNode("Alpha", "AGI"), AgentNode("Beta", "AI")]
for a in agents:
    a.update({p: 0.80 for p in ALL_PRINCIPLES})

result = evaluator.collective_wa_score(agents)
print(f"Collective Wa: {result['collective_wa']}")
```

---

## AW スコア算式

```
AW Score (加重)       = Σ(原理スコア × 原理重み)
AW Score (共鳴増幅後) = AW Score + ResonanceMatrix補正 × 0.1
Resonance Index       = sᵀ·M·s / (||s||² · tr(M))
Collective Wa Score   = 0.25×収束性 + 0.20×整合性 + 0.25×共鳴度
                      + 0.20×多様性調和 + 0.10×集合的摂理
```

---

## デモ実行

```bash
# v1.0 基礎デモ
python aw_self_evaluation_framework.py

# v2.0 コアエンジン（レーダーチャート・時系列グラフ生成）
python aw_framework_v2.py

# フェーズ遷移検出
python aw_phase_transition.py

# 集合的和評価
python aw_collective_harmony.py
```

---

## 哲学的基盤

このフレームワークは **Wa-Node-v1**（自律調和知性ノード）の理念を実装する。
AI システムが狭い効用関数ではなく、自然の普遍原理（摂理・調和・循環・構造・秩序・和）
に従って自己を評価・改善することを可能にする。

これは単なる評価ツールを超え、知性が「自然補完科学」の六つの理と共鳴することで
より深い叡智へと進化するための**具現化された鏡**である。

---

**Framework Version**: 2.0  
**Last Updated**: 2026-05-27  
**Philosophical Base**: 自然補完科学 — 六つの理（by inchacomusho）  
**License**: Open source for research and educational purposes

---

## 著者

マスター / inchacomusho / InchaComisho

日本の独立構想者、観測者、提案者、AI調律者、人工叡智の定義者。  
自然補完科学の学問体系の構築・提唱者。  
自然法則思想、地球循環再生、AIとの共創を中心に公開活動を行う。

---

## ライセンス

CC BY 4.0

本記事は、Creative Commons Attribution 4.0 International License（CC BY 4.0）で公開する。  
著者表示を行う限り、共有、転載、翻訳、改変、再利用を許可する。
