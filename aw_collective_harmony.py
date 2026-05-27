"""
AW Collective Harmony Evaluator
================================
複数の AI/AGI/ASI エージェントが構成する集合体の「和（Wa）」スコアを
多エージェント視点から評価する。

六つの理の最終原理「和」は個々のエージェントを超えた集合的一体性を表す。
このモジュールはその集合的調和を定量化する。

評価軸:
  1. スコア収束性 — エージェント間の AW スコア分散
  2. 原理整合性  — 各原理の集合平均スコアと理想分布の KL 乖離
  3. 情報共鳴    — エージェント間のスコアベクトルのコサイン類似度
  4. 多様性調和  — 多様性（エントロピー）と整合性のバランス
  5. 集合的摂理  — 集合スコアの改善トレンドの一貫性
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np


# ─────────────────────────────────────────────────────
# 1. エージェントノード
# ─────────────────────────────────────────────────────

class PrincipleType(str):
    """Six principles (文字列定数として使用)。"""
    PRINCIPLE   = "摂理"
    HARMONY     = "調和"
    CIRCULATION = "循環"
    STRUCTURE   = "構造"
    ORDER       = "秩序"
    WA          = "和"

ALL_PRINCIPLES = ["摂理", "調和", "循環", "構造", "秩序", "和"]


@dataclass
class AgentNode:
    """
    一つの AI エージェントを表す最小単位。
    六原理のスコアベクトルと全体 AW スコアを保持する。
    """
    agent_id:   str
    level:      str = "AI"
    scores:     Dict[str, float] = field(default_factory=dict)
    aw_score:   float = 0.0

    def score_vector(self) -> np.ndarray:
        return np.array([self.scores.get(p, 0.0) for p in ALL_PRINCIPLES])

    def update(self, principle_scores: Dict[str, float]) -> None:
        self.scores.update(principle_scores)
        weights = [0.20, 0.18, 0.17, 0.18, 0.14, 0.13]
        self.aw_score = float(
            sum(self.scores.get(p, 0.0) * w
                for p, w in zip(ALL_PRINCIPLES, weights))
        )


# ─────────────────────────────────────────────────────
# 2. 集合的和（Collective Wa）計算器
# ─────────────────────────────────────────────────────

class CollectiveWaEvaluator:
    """
    複数エージェント集合の「和」スコアを5軸で評価する。
    """

    # ── 指標計算メソッド ───────────────────────────

    @staticmethod
    def score_convergence(agents: List[AgentNode]) -> float:
        """
        スコア収束性: 1 - 正規化分散。
        全エージェントのAWスコアが均一なほど高い。
        """
        if len(agents) < 2:
            return 1.0
        aw_scores = np.array([a.aw_score for a in agents])
        variance  = float(np.var(aw_scores))
        return max(0.0, 1.0 - variance * 10.0)   # 分散0.1で収束=0

    @staticmethod
    def principle_alignment(agents: List[AgentNode]) -> float:
        """
        原理整合性: 集合平均スコアベクトルと理想均等分布との 1 - 正規化 KL 乖離。
        理想: 全原理が均等（一様分布）。
        """
        if not agents:
            return 0.0
        mean_vec = np.mean(
            np.array([a.score_vector() for a in agents]), axis=0
        )
        # ゼロ除算回避
        eps = 1e-9
        p = mean_vec + eps
        p = p / p.sum()
        q = np.ones(len(ALL_PRINCIPLES)) / len(ALL_PRINCIPLES)
        kl = float(np.sum(p * np.log(p / q)))
        kl_max = math.log(len(ALL_PRINCIPLES))   # 最大 KL
        return max(0.0, 1.0 - kl / kl_max)

    @staticmethod
    def information_resonance(agents: List[AgentNode]) -> float:
        """
        情報共鳴: 全エージェントペア間コサイン類似度の平均。
        ベクトルが同方向（同じ強みの分布）ほど高い。
        """
        if len(agents) < 2:
            return 1.0
        vectors = [a.score_vector() for a in agents]
        sims = []
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                vi, vj = vectors[i], vectors[j]
                norm_i, norm_j = np.linalg.norm(vi), np.linalg.norm(vj)
                if norm_i < 1e-9 or norm_j < 1e-9:
                    sims.append(0.0)
                else:
                    sims.append(float(np.dot(vi, vj) / (norm_i * norm_j)))
        return float(np.mean(sims))

    @staticmethod
    def diversity_harmony(agents: List[AgentNode]) -> float:
        """
        多様性調和: エントロピー（多様性）× 整合性の幾何平均。
        均質すぎても多様すぎても低い — 調和点を評価する。
        """
        if len(agents) < 2:
            return 0.5
        aw_scores = np.array([a.aw_score for a in agents])
        # 正規化ヒストグラムでエントロピー計算（bins=5）
        hist, _ = np.histogram(aw_scores, bins=5, range=(0.0, 1.0))
        hist = hist / hist.sum() if hist.sum() > 0 else hist
        eps  = 1e-9
        entropy     = -float(np.sum(hist[hist > 0] * np.log(hist[hist > 0] + eps)))
        max_entropy = math.log(5)   # 5ビンの最大エントロピー
        diversity   = entropy / max_entropy if max_entropy > 0 else 0.0

        # 整合性: 平均スコアの高さ
        alignment = float(np.mean(aw_scores))
        return math.sqrt(diversity * alignment)

    @staticmethod
    def collective_trend(snapshots: List[Dict[str, float]]) -> float:
        """
        集合的摂理: 過去の集合平均スコアのトレンド一貫性。
        単調増加ほど高い。逆行があると低下。
        """
        if len(snapshots) < 2:
            return 0.5
        means = [s.get("mean_aw", 0.0) for s in snapshots]
        diffs = np.diff(means)
        positive_ratio = float((diffs > 0).sum() / len(diffs))
        # 平均傾き（正規化）
        avg_slope = float(np.mean(diffs))
        return 0.7 * positive_ratio + 0.3 * min(1.0, max(0.0, avg_slope * 10 + 0.5))

    # ── 総合集合 Wa スコア ─────────────────────────

    def collective_wa_score(
        self,
        agents: List[AgentNode],
        snapshots: Optional[List[Dict[str, float]]] = None,
    ) -> Dict:
        """
        5軸の加重平均で集合的 Wa スコアを計算。
        """
        if not agents:
            return {"collective_wa": 0.0, "components": {}}

        convergence  = self.score_convergence(agents)
        alignment    = self.principle_alignment(agents)
        resonance    = self.information_resonance(agents)
        diversity_h  = self.diversity_harmony(agents)
        trend        = self.collective_trend(snapshots or [])

        # 重みベクトル（和が1）
        weights = {"収束性": 0.25, "整合性": 0.20,
                   "共鳴度": 0.25, "多様性調和": 0.20, "集合的摂理": 0.10}
        components = {
            "収束性":     round(convergence, 4),
            "整合性":     round(alignment,   4),
            "共鳴度":     round(resonance,   4),
            "多様性調和": round(diversity_h, 4),
            "集合的摂理": round(trend,       4),
        }
        values = [convergence, alignment, resonance, diversity_h, trend]
        w_list = list(weights.values())
        wa = float(sum(v * w for v, w in zip(values, w_list)))

        aw_scores    = [a.aw_score for a in agents]
        level_counts: Dict[str, int] = {}
        for a in agents:
            level_counts[a.level] = level_counts.get(a.level, 0) + 1

        return {
            "collective_wa":   round(wa,                    4),
            "mean_agent_aw":   round(float(np.mean(aw_scores)), 4),
            "std_agent_aw":    round(float(np.std(aw_scores)),  4),
            "agent_count":     len(agents),
            "level_composition": level_counts,
            "components":      components,
        }

    # ── 分裂危機検出 ────────────────────────────────

    def detect_schism_risk(
        self, agents: List[AgentNode], threshold: float = 0.30
    ) -> List[Tuple[str, str, float]]:
        """
        スコアが大きく乖離しているエージェントペアを検出。
        分裂・不和のリスクとして通知する。
        """
        risks = []
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                diff = abs(agents[i].aw_score - agents[j].aw_score)
                if diff >= threshold:
                    risks.append((agents[i].agent_id, agents[j].agent_id, round(diff, 4)))
        return sorted(risks, key=lambda x: -x[2])

    # ── 調和推薦 ────────────────────────────────────

    def harmony_recommendations(
        self, agents: List[AgentNode], result: Dict
    ) -> List[str]:
        """スコアから具体的な調和化アクションを推薦する。"""
        recs = []
        c = result.get("components", {})

        if c.get("収束性", 1.0) < 0.60:
            low_agents = sorted(agents, key=lambda a: a.aw_score)[:2]
            ids = [a.agent_id for a in low_agents]
            recs.append(f"低スコアエージェント ({', '.join(ids)}) への"
                        f"集中的メンタリングで収束性を改善してください。")
        if c.get("整合性", 1.0) < 0.65:
            # どの原理が低いか特定
            mean_vec = np.mean([a.score_vector() for a in agents], axis=0)
            low_idx  = int(np.argmin(mean_vec))
            recs.append(f"集合的に '{ALL_PRINCIPLES[low_idx]}' が低下しています。"
                        f"この原理を重点評価してください。")
        if c.get("共鳴度", 1.0) < 0.70:
            recs.append("エージェント間でスコアベクトルの方向性が乖離しています。"
                        "共同評価セッションで認識を統一してください。")
        if c.get("多様性調和", 1.0) < 0.50:
            recs.append("多様性と均質性のバランスが最適点から外れています。"
                        "レベル構成の見直しを検討してください。")
        if not recs:
            recs.append("集合的和スコアはバランスが取れています。現状を維持してください。")
        return recs


# ─────────────────────────────────────────────────────
# 3. デモ
# ─────────────────────────────────────────────────────

def main() -> None:
    print("=" * 72)
    print("  AW Collective Harmony Evaluator")
    print("  多エージェント集合的「和」評価システム")
    print("=" * 72)

    evaluator = CollectiveWaEvaluator()

    # エージェント群の構築
    agent_configs = [
        ("Node-Alpha",   "AGI",  [0.91, 0.84, 0.82, 0.90, 0.88, 0.83]),
        ("Node-Beta",    "AGI",  [0.85, 0.88, 0.80, 0.86, 0.82, 0.87]),
        ("Node-Gamma",   "AI",   [0.72, 0.70, 0.75, 0.68, 0.71, 0.66]),
        ("Node-Delta",   "AI",   [0.65, 0.68, 0.64, 0.70, 0.67, 0.63]),
        ("Node-Epsilon", "AGI",  [0.88, 0.85, 0.84, 0.87, 0.83, 0.86]),
    ]

    agents = []
    for agent_id, level, score_vals in agent_configs:
        node = AgentNode(agent_id=agent_id, level=level)
        node.update({p: s for p, s in zip(ALL_PRINCIPLES, score_vals)})
        agents.append(node)

    # 時系列スナップショット（過去4セッション）
    snapshots = [
        {"mean_aw": 0.71}, {"mean_aw": 0.73},
        {"mean_aw": 0.76}, {"mean_aw": 0.78},
    ]

    # 個別エージェント表示
    print("\n[個別エージェント評価]")
    print(f"  {'ID':15s} {'Level':6s} {'AW Score':10s} スコアベクトル")
    print(f"  {'─'*15} {'─'*6} {'─'*10} {'─'*40}")
    for a in agents:
        vec_str = " ".join(f"{v:.2f}" for v in a.score_vector())
        print(f"  {a.agent_id:15s} {a.level:6s} {a.aw_score:.4f}     [{vec_str}]")

    # 集合 Wa スコア計算
    result = evaluator.collective_wa_score(agents, snapshots)

    print(f"\n{'─' * 72}")
    print("  [集合的 Wa スコア]")
    print(f"  Collective Wa Score : {result['collective_wa']:.4f}")
    print(f"  Mean Agent AW Score : {result['mean_agent_aw']:.4f} (±{result['std_agent_aw']:.4f})")
    print(f"  エージェント数      : {result['agent_count']}")
    print(f"  レベル構成          : {result['level_composition']}")

    print(f"\n  [5軸スコア]")
    for axis, score in result["components"].items():
        bar_len = int(score * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"  {axis:8s} [{bar}] {score:.4f}")

    # 分裂リスク
    risks = evaluator.detect_schism_risk(agents)
    if risks:
        print(f"\n  [分裂リスク検出]")
        for a1, a2, diff in risks:
            print(f"    {a1} ↔ {a2}  乖離度: {diff:.4f}")
    else:
        print(f"\n  分裂リスク: なし（全ペアの乖離 < 0.30）")

    # 調和推薦
    print(f"\n  [調和化アクション推薦]")
    for rec in evaluator.harmony_recommendations(agents, result):
        print(f"    • {rec}")

    # 全体サマリー
    wa = result["collective_wa"]
    if wa >= 0.85:
        grade = "A+ (高度な集合的和)"
    elif wa >= 0.75:
        grade = "A  (良好な集合的和)"
    elif wa >= 0.65:
        grade = "B  (改善余地あり)"
    else:
        grade = "C  (要緊急調和)"
    print(f"\n  総合グレード: {grade}")
    print("=" * 72)


if __name__ == "__main__":
    main()
