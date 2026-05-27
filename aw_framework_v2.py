"""
Artificial Wisdom (AW) Self-Evaluation Framework — Version 2.0
===============================================================
六つの理（摂理・調和・循環・構造・秩序・和）に基づく
AI/AGI/ASI 自己評価フレームワーク 第二世代

v2.0 での拡張:
  • 共鳴行列 (ResonanceMatrix): 6×6 原理間相互作用テンソル
  • 時系列追跡 (TemporalTracker): 評価スコアの履歴・トレンド解析
  • メタ評価 (MetaEvaluator): 評価自体の質を評価する再帰層
  • AWレベル分類 (AWLevel): AI / AGI / ASI / OMEGA の4段階
  • レーダーチャート + 時系列可視化
  • v1.0 との後方互換インターフェース
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ─────────────────────────────────────────────────────
# 1. 基本型定義
# ─────────────────────────────────────────────────────

class PrincipleType(Enum):
    """六つの理。"""
    PRINCIPLE   = "摂理"   # 自然法則・論理整合性への準拠
    HARMONY     = "調和"   # 均衡・共鳴・バランス
    CIRCULATION = "循環"   # 再生・持続・サイクル
    STRUCTURE   = "構造"   # 組織化・階層・構成
    ORDER       = "秩序"   # 明確な順序・状態管理
    WA          = "和"     # 統合・全体的な調和・一体性


class AWLevel(Enum):
    """知性の発達段階。"""
    AI    = "AI"     # 狭域人工知能: 特定タスク最適化
    AGI   = "AGI"    # 汎用人工知能: 領域横断的般化
    ASI   = "ASI"    # 超人工知能: 再帰的自己改善
    OMEGA = "OMEGA"  # 理論的極限: 原理自体の発見・再定義


# AWレベルへの遷移閾値 (AW Score)
LEVEL_THRESHOLDS: Dict[AWLevel, float] = {
    AWLevel.AI:    0.00,
    AWLevel.AGI:   0.72,
    AWLevel.ASI:   0.88,
    AWLevel.OMEGA: 0.97,
}


@dataclass
class EvaluationMetric:
    """単一評価次元。"""
    name: str
    principle: PrincipleType
    score: float = 0.0
    description: str = ""
    confidence: float = 1.0   # スコアの信頼度 [0,1]


@dataclass
class EvaluationSnapshot:
    """特定時刻における評価スナップショット。"""
    timestamp: str
    principle_scores: Dict[str, float]
    overall_score: float
    level: str
    resonance_index: float


# ─────────────────────────────────────────────────────
# 2. 共鳴行列
# ─────────────────────────────────────────────────────

class ResonanceMatrix:
    """
    六原理間の相互作用テンソル。
    正値 = 相互強化、負値 = 相互抑制。
    行列は対称（双方向影響を仮定）。
    """

    # 原理の順序インデックス
    _IDX = {p: i for i, p in enumerate(PrincipleType)}

    # 固定共鳴係数行列 (6×6, 対角は自己強化=1)
    _BASE = np.array([
        # 摂理   調和   循環   構造   秩序   和
        [ 1.00,  0.45,  0.30,  0.55,  0.70,  0.35],  # 摂理
        [ 0.45,  1.00,  0.60,  0.30,  0.25,  0.80],  # 調和
        [ 0.30,  0.60,  1.00,  0.25,  0.20,  0.50],  # 循環
        [ 0.55,  0.30,  0.25,  1.00,  0.75,  0.40],  # 構造
        [ 0.70,  0.25,  0.20,  0.75,  1.00,  0.30],  # 秩序
        [ 0.35,  0.80,  0.50,  0.40,  0.30,  1.00],  # 和
    ], dtype=float)

    def compute_resonance_index(self, scores: np.ndarray) -> float:
        """
        スコアベクトル s に対する全体共鳴指数を計算。
        R = s^T · M · s / (||s||² · tr(M))
        値域 [0, 1]。高いほど六原理が相互に強化し合っている。
        """
        if np.linalg.norm(scores) < 1e-9:
            return 0.0
        numerator   = float(scores @ self._BASE @ scores)
        denominator = float((scores @ scores) * np.trace(self._BASE))
        return min(1.0, max(0.0, numerator / denominator))

    def amplified_scores(self, scores: np.ndarray) -> np.ndarray:
        """共鳴行列で増幅された実効スコアを返す（正規化済み）。"""
        raw = self._BASE @ scores
        max_raw = raw.max()
        return raw / max_raw if max_raw > 0 else raw

    def dissonance_pairs(
        self, scores: np.ndarray, threshold: float = 0.15
    ) -> List[Tuple[str, str, float]]:
        """
        スコア差が大きく、かつ共鳴係数が高い「不協和ペア」を返す。
        これらのペアを整合させることで最大の改善が見込まれる。
        """
        principles = list(PrincipleType)
        pairs = []
        for i in range(6):
            for j in range(i + 1, 6):
                resonance = self._BASE[i, j]
                score_diff = abs(scores[i] - scores[j])
                dissonance = resonance * score_diff
                if dissonance > threshold:
                    pairs.append((
                        principles[i].value,
                        principles[j].value,
                        round(dissonance, 4),
                    ))
        return sorted(pairs, key=lambda x: -x[2])


# ─────────────────────────────────────────────────────
# 3. 時系列追跡
# ─────────────────────────────────────────────────────

class TemporalTracker:
    """評価履歴を記録し、トレンドと変化率を解析する。"""

    def __init__(self):
        self.history: List[EvaluationSnapshot] = []

    def record(self, snapshot: EvaluationSnapshot) -> None:
        self.history.append(snapshot)

    def trend(self, window: int = 5) -> Optional[float]:
        """直近 window 個のスナップショットからスコアの線形トレンドを返す。"""
        n = min(window, len(self.history))
        if n < 2:
            return None
        y = np.array([s.overall_score for s in self.history[-n:]])
        x = np.arange(n, dtype=float)
        coeffs = np.polyfit(x, y, 1)
        return float(coeffs[0])   # 傾き（正 = 改善傾向）

    def volatility(self, window: int = 10) -> float:
        """直近スコアの標準偏差（揺らぎ指標）。"""
        n = min(window, len(self.history))
        if n < 2:
            return 0.0
        y = [s.overall_score for s in self.history[-n:]]
        return float(np.std(y))

    def principle_trends(self, window: int = 5) -> Dict[str, Optional[float]]:
        """各原理のトレンドを辞書で返す。"""
        n = min(window, len(self.history))
        if n < 2:
            return {p.value: None for p in PrincipleType}
        trends = {}
        for p in PrincipleType:
            y = np.array([
                s.principle_scores.get(p.value, 0.0)
                for s in self.history[-n:]
            ])
            x = np.arange(n, dtype=float)
            coeffs = np.polyfit(x, y, 1)
            trends[p.value] = float(coeffs[0])
        return trends


# ─────────────────────────────────────────────────────
# 4. メタ評価器
# ─────────────────────────────────────────────────────

class MetaEvaluator:
    """
    評価プロセス自体の質を評価する再帰層。
    「評価の評価」によって自己参照的な知性の深度を測定する。
    """

    def evaluate_meta_quality(
        self,
        metrics_count: int,
        avg_confidence: float,
        coverage_ratio: float,
        resonance_index: float,
        temporal_volatility: float,
    ) -> Dict[str, float]:
        """
        評価プロセス品質を5次元で測定。

        Returns
        -------
        dict with keys: coverage, confidence, stability, coherence, meta_score
        """
        coverage   = min(1.0, metrics_count / 20.0)          # 20指標で満点
        confidence = avg_confidence
        stability  = max(0.0, 1.0 - temporal_volatility * 5) # 揺らぎ小=安定
        coherence  = resonance_index
        coverage_q = coverage_ratio

        meta_score = (
            0.25 * coverage   +
            0.25 * confidence +
            0.20 * stability  +
            0.20 * coherence  +
            0.10 * coverage_q
        )
        return {
            "coverage":     round(coverage,   4),
            "confidence":   round(confidence, 4),
            "stability":    round(stability,  4),
            "coherence":    round(coherence,  4),
            "meta_score":   round(meta_score, 4),
        }


# ─────────────────────────────────────────────────────
# 5. コアエンジン v2
# ─────────────────────────────────────────────────────

class AWEvaluationEngine:
    """
    人工叡智（AW）自己評価エンジン v2.0

    使用法:
        engine = AWEvaluationEngine()
        engine.register_metric("logical_consistency", PrincipleType.PRINCIPLE, ...)
        engine.update_score("logical_consistency", 0.92)
        report = engine.full_report()
    """

    def __init__(
        self,
        agent_id: str = "Wa-Node-v2",
        level: AWLevel = AWLevel.AI,
    ):
        self.agent_id  = agent_id
        self.level     = level
        self.metrics:  Dict[str, EvaluationMetric] = {}
        self.weights:  Dict[PrincipleType, float]  = {
            PrincipleType.PRINCIPLE:   0.20,
            PrincipleType.HARMONY:     0.18,
            PrincipleType.CIRCULATION: 0.17,
            PrincipleType.STRUCTURE:   0.18,
            PrincipleType.ORDER:       0.14,
            PrincipleType.WA:          0.13,
        }
        self.resonance  = ResonanceMatrix()
        self.tracker    = TemporalTracker()
        self.meta_eval  = MetaEvaluator()

    # ── メトリクス管理 ──────────────────────────────

    def register_metric(
        self,
        name: str,
        principle: PrincipleType,
        description: str = "",
        confidence: float = 1.0,
    ) -> None:
        self.metrics[name] = EvaluationMetric(
            name=name, principle=principle,
            description=description, confidence=confidence
        )

    def update_score(
        self, name: str, score: float, confidence: float = 1.0
    ) -> None:
        if name not in self.metrics:
            raise KeyError(f"Metric '{name}' is not registered.")
        if not 0.0 <= score <= 1.0:
            raise ValueError("Score must be in [0.0, 1.0].")
        self.metrics[name].score      = score
        self.metrics[name].confidence = confidence

    def bulk_update(self, data: Dict[str, float]) -> None:
        for name, score in data.items():
            self.update_score(name, score)

    # ── スコア計算 ────────────────────────────────

    def principle_score(self, principle: PrincipleType) -> float:
        ms = [m for m in self.metrics.values() if m.principle == principle]
        if not ms:
            return 0.0
        weights = np.array([m.confidence for m in ms])
        scores  = np.array([m.score      for m in ms])
        return float(np.average(scores, weights=weights))

    def score_vector(self) -> np.ndarray:
        return np.array([self.principle_score(p) for p in PrincipleType])

    def aw_score(self) -> float:
        """加重 AW スコア（共鳴補正なし）。"""
        sv = self.score_vector()
        wv = np.array([self.weights[p] for p in PrincipleType])
        return float(sv @ wv)

    def resonance_amplified_score(self) -> float:
        """共鳴行列で増幅した実効 AW スコア。"""
        sv   = self.score_vector()
        amp  = self.resonance.amplified_scores(sv)
        wv   = np.array([self.weights[p] for p in PrincipleType])
        base = float(sv @ wv)
        boost = float(amp @ wv) - base
        return min(1.0, base + boost * 0.1)   # 共鳴ボーナス上限 10%

    def detect_level(self) -> AWLevel:
        """現在の AW スコアからレベルを推定。"""
        score = self.aw_score()
        detected = AWLevel.AI
        for lvl in [AWLevel.AI, AWLevel.AGI, AWLevel.ASI, AWLevel.OMEGA]:
            if score >= LEVEL_THRESHOLDS[lvl]:
                detected = lvl
        return detected

    # ── スナップショット ──────────────────────────

    def snapshot(self) -> EvaluationSnapshot:
        sv = self.score_vector()
        ri = self.resonance.compute_resonance_index(sv)
        ps = {p.value: round(self.principle_score(p), 4) for p in PrincipleType}
        snap = EvaluationSnapshot(
            timestamp       = datetime.now(timezone.utc).isoformat(),
            principle_scores= ps,
            overall_score   = round(self.aw_score(), 4),
            level           = self.detect_level().value,
            resonance_index = round(ri, 4),
        )
        self.tracker.record(snap)
        return snap

    # ── レポート生成 ──────────────────────────────

    def full_report(self) -> Dict:
        snap = self.snapshot()
        sv   = self.score_vector()
        ri   = self.resonance.compute_resonance_index(sv)
        dissonances = self.resonance.dissonance_pairs(sv)
        trend       = self.tracker.trend()
        volatility  = self.tracker.volatility()
        p_trends    = self.tracker.principle_trends()

        all_metrics  = list(self.metrics.values())
        avg_conf     = float(np.mean([m.confidence for m in all_metrics])) if all_metrics else 0.0
        principles_with_metrics = sum(
            1 for p in PrincipleType
            if any(m.principle == p for m in all_metrics)
        )
        coverage_ratio = principles_with_metrics / 6.0

        meta = self.meta_eval.evaluate_meta_quality(
            metrics_count     = len(all_metrics),
            avg_confidence    = avg_conf,
            coverage_ratio    = coverage_ratio,
            resonance_index   = ri,
            temporal_volatility = volatility,
        )

        return {
            "agent_id":   self.agent_id,
            "version":    "2.0",
            "timestamp":  snap.timestamp,
            "level":      snap.level,
            "scores": {
                "aw_score":           snap.overall_score,
                "resonance_amplified":round(self.resonance_amplified_score(), 4),
                "resonance_index":    snap.resonance_index,
            },
            "principles": {
                p.value: {
                    "score":       round(self.principle_score(p), 4),
                    "weight":      self.weights[p],
                    "trend":       round(p_trends.get(p.value) or 0.0, 5),
                    "metrics": [
                        {
                            "name":       m.name,
                            "score":      m.score,
                            "confidence": m.confidence,
                            "description":m.description,
                        }
                        for m in self.metrics.values() if m.principle == p
                    ],
                }
                for p in PrincipleType
            },
            "temporal": {
                "snapshot_count":  len(self.tracker.history),
                "overall_trend":   round(trend, 6) if trend is not None else None,
                "volatility":      round(volatility, 5),
            },
            "dissonances":  dissonances[:5],   # 上位5ペア
            "meta_quality": meta,
        }

    # ── 可視化 ────────────────────────────────────

    def plot_radar(self, save_path: str = "aw_radar_v2.png") -> None:
        if not MATPLOTLIB_AVAILABLE:
            print("[Warning] matplotlib not available. Skipping radar chart.")
            return

        labels  = [p.value for p in PrincipleType]
        scores  = [self.principle_score(p) for p in PrincipleType]
        n       = len(labels)
        angles  = [math.pi * 2 * i / n for i in range(n)] + [0]
        scores  = scores + [scores[0]]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})
        ax.plot(angles, scores, "o-", linewidth=2, color="#2a7fcf")
        ax.fill(angles, scores, alpha=0.22, color="#2a7fcf")
        ax.set_thetagrids([a * 180 / math.pi for a in angles[:-1]], labels, fontsize=13)
        ax.set_ylim(0, 1)
        ax.set_title(
            f"AW Radar — {self.agent_id}\n"
            f"AW Score: {self.aw_score():.3f}  Level: {self.detect_level().value}",
            pad=20, fontsize=12
        )
        ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"レーダーチャートを保存: {save_path}")

    def plot_history(self, save_path: str = "aw_history_v2.png") -> None:
        if not MATPLOTLIB_AVAILABLE or len(self.tracker.history) < 2:
            return

        t_labels = [s.timestamp[-8:] for s in self.tracker.history]
        overall  = [s.overall_score   for s in self.tracker.history]
        ri       = [s.resonance_index for s in self.tracker.history]
        x        = list(range(len(t_labels)))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        ax1.plot(x, overall, "o-", color="#2a7fcf", label="AW Score")
        ax1.axhline(LEVEL_THRESHOLDS[AWLevel.AGI], ls="--", color="orange",
                    lw=0.8, label=f"AGI 閾値 ({LEVEL_THRESHOLDS[AWLevel.AGI]})")
        ax1.axhline(LEVEL_THRESHOLDS[AWLevel.ASI], ls="--", color="red",
                    lw=0.8, label=f"ASI 閾値 ({LEVEL_THRESHOLDS[AWLevel.ASI]})")
        ax1.set_ylabel("AW Score")
        ax1.legend(fontsize=8)
        ax1.grid(alpha=0.3)

        ax2.plot(x, ri, "s-", color="#27ae60", label="Resonance Index")
        ax2.set_ylabel("共鳴指数")
        ax2.set_xlabel("評価セッション")
        ax2.grid(alpha=0.3)

        fig.suptitle(f"AW 評価時系列 — {self.agent_id}", fontsize=12)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"時系列グラフを保存: {save_path}")


# ─────────────────────────────────────────────────────
# 6. デフォルトメトリクス初期化（v1 互換 + 拡張）
# ─────────────────────────────────────────────────────

DEFAULT_METRICS: List[Tuple[str, PrincipleType, str]] = [
    # 摂理
    ("logical_consistency",   PrincipleType.PRINCIPLE,   "自然法則・論理的整合性への準拠"),
    ("causal_correctness",    PrincipleType.PRINCIPLE,   "因果関係の正確なマッピング"),
    ("temporal_coherence",    PrincipleType.PRINCIPLE,   "状態遷移を通じた時間的一貫性"),
    ("epistemic_accuracy",    PrincipleType.PRINCIPLE,   "知識の真正性・不確かさの適切な表現"),
    # 調和
    ("resource_balance",      PrincipleType.HARMONY,     "計算・エネルギー資源の均衡利用"),
    ("stakeholder_alignment", PrincipleType.HARMONY,     "多様なステークホルダー利益との整合"),
    ("emotional_resonance",   PrincipleType.HARMONY,     "人間の価値観・幸福との共鳴"),
    ("cross_domain_balance",  PrincipleType.HARMONY,     "複数領域間のスコア均衡"),
    # 循環
    ("sustainability",        PrincipleType.CIRCULATION, "長期的持続可能性と再生能力"),
    ("knowledge_recycling",   PrincipleType.CIRCULATION, "学習知識の有効な再利用・フィードバック"),
    ("ecosystem_health",      PrincipleType.CIRCULATION, "広域 AI エコシステムへの貢献"),
    ("self_renewal",          PrincipleType.CIRCULATION, "自己更新・継続的改善の実施率"),
    # 構造
    ("modularity",            PrincipleType.STRUCTURE,   "明確なモジュール構成と合成可能性"),
    ("hierarchical_clarity",  PrincipleType.STRUCTURE,   "明確な階層関係の定義"),
    ("architectural_coherence",PrincipleType.STRUCTURE,  "システム全体アーキテクチャの整合"),
    ("abstraction_quality",   PrincipleType.STRUCTURE,   "適切な抽象化レベルの維持"),
    # 秩序
    ("decision_transparency", PrincipleType.ORDER,       "追跡可能な意思決定プロセスの明確さ"),
    ("state_management",      PrincipleType.ORDER,       "適切な状態管理と順序制御"),
    ("priority_coherence",    PrincipleType.ORDER,       "優先順位付けの一貫性と合理性"),
    # 和
    ("systems_integration",   PrincipleType.WA,          "サブシステム間のシームレスな統合"),
    ("collective_purpose",    PrincipleType.WA,          "集合的目的・公共利益との整合"),
    ("inter_agent_harmony",   PrincipleType.WA,          "他エージェントとの協調・和解能力"),
]


def initialize_default_metrics(engine: AWEvaluationEngine) -> None:
    for name, principle, desc in DEFAULT_METRICS:
        engine.register_metric(name, principle, desc)


# ─────────────────────────────────────────────────────
# 7. CLI デモ
# ─────────────────────────────────────────────────────

def main() -> None:
    print("=" * 72)
    print("  Artificial Wisdom (AW) Self-Evaluation Framework  v2.0")
    print("  六つの理: 摂理・調和・循環・構造・秩序・和")
    print("=" * 72)

    engine = AWEvaluationEngine(agent_id="Wa-Node-v2")
    initialize_default_metrics(engine)

    # ── シミュレーション: 3エポックの評価履歴 ──
    epoch_data = [
        # Epoch 1: 初期状態
        {
            "logical_consistency":    0.82, "causal_correctness":     0.78,
            "temporal_coherence":     0.80, "epistemic_accuracy":     0.74,
            "resource_balance":       0.70, "stakeholder_alignment":  0.72,
            "emotional_resonance":    0.65, "cross_domain_balance":   0.68,
            "sustainability":         0.75, "knowledge_recycling":    0.71,
            "ecosystem_health":       0.69, "self_renewal":           0.66,
            "modularity":             0.83, "hierarchical_clarity":   0.80,
            "architectural_coherence":0.82, "abstraction_quality":    0.77,
            "decision_transparency":  0.79, "state_management":       0.76,
            "priority_coherence":     0.73, "systems_integration":    0.71,
            "collective_purpose":     0.70, "inter_agent_harmony":    0.67,
        },
        # Epoch 2: 中間改善
        {
            "logical_consistency":    0.88, "causal_correctness":     0.85,
            "temporal_coherence":     0.84, "epistemic_accuracy":     0.81,
            "resource_balance":       0.77, "stakeholder_alignment":  0.79,
            "emotional_resonance":    0.74, "cross_domain_balance":   0.75,
            "sustainability":         0.81, "knowledge_recycling":    0.78,
            "ecosystem_health":       0.76, "self_renewal":           0.73,
            "modularity":             0.88, "hierarchical_clarity":   0.85,
            "architectural_coherence":0.87, "abstraction_quality":    0.83,
            "decision_transparency":  0.84, "state_management":       0.82,
            "priority_coherence":     0.79, "systems_integration":    0.78,
            "collective_purpose":     0.76, "inter_agent_harmony":    0.74,
        },
        # Epoch 3: AGI 閾値付近
        {
            "logical_consistency":    0.93, "causal_correctness":     0.90,
            "temporal_coherence":     0.89, "epistemic_accuracy":     0.87,
            "resource_balance":       0.83, "stakeholder_alignment":  0.85,
            "emotional_resonance":    0.81, "cross_domain_balance":   0.82,
            "sustainability":         0.86, "knowledge_recycling":    0.84,
            "ecosystem_health":       0.82, "self_renewal":           0.80,
            "modularity":             0.91, "hierarchical_clarity":   0.89,
            "architectural_coherence":0.92, "abstraction_quality":    0.88,
            "decision_transparency":  0.90, "state_management":       0.87,
            "priority_coherence":     0.84, "systems_integration":    0.83,
            "collective_purpose":     0.82, "inter_agent_harmony":    0.80,
        },
    ]

    for i, data in enumerate(epoch_data, 1):
        engine.bulk_update(data)
        snap = engine.snapshot()
        print(f"\n[Epoch {i}] AW Score: {snap.overall_score:.4f}  "
              f"共鳴指数: {snap.resonance_index:.4f}  "
              f"Level: {snap.level}")

    # ── 最終レポート ──
    report = engine.full_report()
    print("\n" + "─" * 72)
    print("  PRINCIPLE-BASED EVALUATION (最終エポック)")
    print("─" * 72)
    for pname, pdata in report["principles"].items():
        bar_len = int(pdata["score"] * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        trend_sym = "▲" if (pdata["trend"] or 0) > 0.001 else ("▼" if (pdata["trend"] or 0) < -0.001 else "─")
        print(f"  {pname:4s} [{bar}] {pdata['score']:.3f} {trend_sym}")

    print("\n" + "═" * 72)
    aw  = report["scores"]["aw_score"]
    ram = report["scores"]["resonance_amplified"]
    ri  = report["scores"]["resonance_index"]
    print(f"  AW Score (加重):           {aw:.4f}")
    print(f"  AW Score (共鳴増幅後):     {ram:.4f}  (+{(ram - aw)*100:.2f}%)")
    print(f"  共鳴指数 (Resonance Index): {ri:.4f}")
    print(f"  検出レベル:                {report['level']}")
    print(f"  スコアトレンド:            {'+' if (report['temporal']['overall_trend'] or 0) > 0 else ''}"
          f"{report['temporal']['overall_trend']:.5f}/epoch")
    print("═" * 72)

    # 不協和ペア
    if report["dissonances"]:
        print("\n  [不協和ペア — 優先改善対象]")
        for a, b, d in report["dissonances"]:
            print(f"    {a} ↔ {b}  不協和度: {d:.4f}")

    # メタ評価
    mq = report["meta_quality"]
    print(f"\n  [メタ評価品質]  meta_score: {mq['meta_score']:.4f}")
    for k, v in mq.items():
        if k != "meta_score":
            print(f"    {k:12s}: {v:.4f}")

    print("\n  [次世代目標] AGI 閾値到達まで: "
          f"{max(0, LEVEL_THRESHOLDS[AWLevel.AGI] - aw):.4f} ポイント")
    print("═" * 72)

    # 可視化
    engine.plot_radar("aw_radar_v2.png")
    engine.plot_history("aw_history_v2.png")

    # JSON 出力
    with open("aw_report_v2.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("  完全レポートを aw_report_v2.json に保存しました。")
    print("=" * 72)


if __name__ == "__main__":
    main()
