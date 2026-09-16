# Impact Frontiers 現行規範とのギャップ分析、および RoboEvaluater の進化方針

作成日: 2026-09-16 / 対象コミット: `836b2fc`（evidence gate 導入時点）

---

## 0. 調査条件と制約（先に読んでください）

このセッションの egress allowlist に `impactfrontiers.org` が入っておらず、
サイト本体を直接取得できなかった（プロキシが CONNECT を 403 で拒否）。
`impactmanagementplatform.org`、Google 翻訳プロキシ経由（`*.translate.goog`）、
二次解説サイト（sopact 等）もすべて同様にブロックされている。

したがって本書は **Web検索が返す要約と見出し情報にもとづく二次調査** であり、
以下の一次資料の本文は未読である。

- `The ABC of Impact: Modifications and Clarifications, 2023`（2023年12月）
- `Advancing Social Equity Through IMM`（2025年1月）と Norms 改訂付録
- `Impact Performance Reporting Norms Version 1`（2024年4月）

断定できない箇所は本文中に「未確認」と明記した。次セッションで
`impactfrontiers.org` と `impactreporting.org` を allowlist に追加すれば、
一次資料で裏取りできる（CC on web と CC デスクトップで allowlist は別スコープな点に注意）。

---

## 1. Impact Frontiers の現在地

### 1.1 沿革 — 「IMP」はもう現在形で書けない

| 時期 | できごと |
|---|---|
| 2016–2018 | Impact Management Project (IMP) が3,000以上の企業・投資家の実務家コミュニティを招集し、測定・改善・開示の合意形成 |
| 2019 | Impact Frontiers が IMP 内のイニシアチブとしてインキュベート |
| 2021 | IMP が5年の任期を終えて終了。**Impact Frontiers が Norms の steward（管理団体）を承継** |
| 2023 | ABC の公開協議 → 修正・明確化を公表 |
| 2024 | Norms の social equity audit（専門家レビュー＋公開協議） |
| 2024/04 | Impact Performance Reporting Norms V1 公表（18か月・350以上の関係者による協議の結果） |
| 2025/11 | `impactreporting.org` を独立サイトとして公開、Founding Adopters を発表（初期40以上 → 100以上） |
| 2026 | Reporting Norms の実装フェーズ（2024年半ば〜2026年半ば）、V2 は2026年後半予定、2026 cohort 実施中 |

現在の Impact Frontiers は「投資家が自らの社会・環境インパクトを管理し、
投資判断にインパクトを組み込むための学習・市場形成コラボレーション」と自称しており、
Reporting Norms については政府系・慈善系の council が集団的に steward する体制の
事務局（secretariat）を務めている。

### 1.2 サイトの構造

- **Norms（規範）** — Five Dimensions of Impact / ABC of Enterprise Impact（outcome level を含む）/
  Investor Contribution（投資家の4つの貢献戦略、`Investor Contribution 2.0`）/
  Impact-Financial Integration（統合への5ステップ）
- **New Frontiers（開発中の論点）** — Impact Performance Reporting /
  Impact Management for Social Equity / Impact Portfolio Construction
- **学習資産** — Online Curriculum（Module 10: Impact Risk、Module 11: Investor Contribution など）、
  Cohort Programs、Learn by Doing、Systems Mapping、Discussion Boards

### 1.3 重心はどこへ動いたか

**5次元は土台として安定し、動いているのはその上のレイヤー。** 具体的には3方向。

1. **ABC の裁量幅を締める方向（2023）** — 30以上の公開事例のデスクレビューと
   約10名の投資家・コンサルタントへのインタビューから出発した公開協議。
   C の基準を狭める複数の案が提示され、一部は実務家コミュニティに支持され、
   一部は支持されなかった。結果は「概念の明確さと運用の一貫性を高める穏当な変更」。
2. **社会的公平性の組み込み（2024–2025）** — Who の属性別データ分解（人種等）は
   文脈によって強く支持される場合とそうでない場合がある、という結論を含む。
   全アウトカムについて5次元すべての実績データを報告するのは負担が過大、という指摘も。
3. **「測る」から「報告する」へ（2024–2026）** — Reporting Norms は
   comply-or-explain（推奨内容を載せるか、載せない理由を説明するか）方式。
   私募市場のアセットマネージャーが資金提供者に NDA 下で共有する
   インパクト報告書を主対象とし、現在は他のアセットクラス・投資家類型へ拡張中。

> **RoboEvaluater にとっての含意**：追随すべき「動いている規範」は 5次元そのものではなく、
> ①ABC の適用単位と基準、②Who の分解、③主張と証拠の対応関係（報告の規律）の3つ。

---

## 2. RoboEvaluater のこれまでの進化

コミットは3つしかないが、進化の性格ははっきりしている。

| | 内容 |
|---|---|
| `014febe` | 初期コミット |
| `d1d451d` (PR #1, 2026-08-22) | MVP。Python と JS の二重実装＋パリティテスト、Claude スキルとノーバックエンド Web アプリの2フロント、GitHub Pages 配信、OSS 運営ファイル一式 |
| `836b2fc` (PR #2, 同日深夜) | **evidence gate**。実データ1件の感度分析で4シナリオ中3つ（悲観シナリオを含む）が C になったことを受け、`evidence_risk >= 4` で C を B にキャップ。両スコアラーに入力検証を追加 |

PR #2 は機能追加ではなく **モデルの妥当性の修正** である。
「対象が非常に脆弱（Who=5）で、成果が自明に重要（What=5）な団体は、
誰も何も測っていない段階で C の半分まで到達してしまう」——
つまり IMM が防ぐために存在する失敗モード（誠実な使命、未測定の成果）に
最上位の分類を与えていた、という自己批判に対する非補償的なガードだった。

**このプロジェクトの進化軸は UI でも機能数でもなく「主張の正当性（claim validity）」にある。**
そしてその軸は、Impact Frontiers 自身が2023年以降たどっている方向
（C の裁量を狭める、報告の規律を作る）と偶然にも一致している。
進化方針を考えるうえで、これが最も重要な前提である。

---

## 3. ギャップ分析

### 3.1 事実の誤り（早急に直す価値がある）

| # | 現状 | 現行規範 | 影響 |
|---|---|---|---|
| G1 | `reference/imp-five-dimensions.md`：「IMP はインパクトリスクを6種類挙げる。我々は6つすべてをスコアする」 | 標準リストは**9種類**とされる。特定できたのは evidence / external / stakeholder participation / drop-off / efficiency / **execution** / **alignment** / unexpected impact（9つ目は endurance または contribution risk。未確認） | 「すべてをスコアしている」は誤り。とくに **execution risk（活動が計画どおり実行されない確率）** は NPO 事業では最大級のリスクで、これを落としたままリスク平均を出すとリスクを過小評価する |
| G2 | 分類 B の名称が `B: Benefit Stakeholders` | 現行表記は **Benefit People and the Planet** | 用語が古い。規範準拠を謳うツールとしては信頼性に直結 |
| G3 | README / SKILL.md が IMP を現在形で参照し、リンク先だけ impactfrontiers.org | IMP は2021年終了、現在の steward は Impact Frontiers | 帰属表記の更新が必要。「IMP の5次元（現 Impact Frontiers が管理）」が正確 |

### 3.2 概念のズレ（設計判断が必要）

| # | 現状 | 現行規範 | 論点 |
|---|---|---|---|
| G4 | **プロジェクト/団体に対して分類を1つ**出す | ABC は **outcome（アウトカム）単位**で分類する | 就労支援と居場所づくりを併せ持つ団体では、強いアウトカムが弱いアウトカムを平均で覆い隠す。実務上もっとも大きなズレ |
| G5 | 目標なのか実績なのかを区別しない | **prospective（目標ベース）と retrospective（実績ベース）を区別**して分類する | evidence gate がこの区別の代理変数として機能しているが、明示したほうが強く、説明もしやすい |
| G6 | Who = `stakeholder_underserved` の 1–5 一本 | social equity 改訂は**属性別の分解**（性別・階層・人種・先住民性・その交差）を志向。ただし分解の是非は文脈依存 | 日本の NPO 文脈にそのまま持ち込めない部分がある。任意項目としての実装が現実的 |
| G7 | Contribution は counterfactual 4段階のみ | enterprise contribution と **investor contribution（4戦略）** は別概念 | 投資家向けに広げないなら「対象外」と明記すればよい。現状は区別が書かれていない |
| G8 | `outcome_valence == "negative"` → 即 `A: Act to Avoid Harm` | A は「害を回避する行動をとっている」状態であり、同一組織が別アウトカムで B や C を同時に持ちうる | G4（outcome 単位化）と同じ根。A を「排他的な最終分類」として扱う現在の実装は、規範の読み違いに近い |

### 3.3 意図的な単純化（残してよいが、根拠を明記すべき）

| # | 現状 | 論点 |
|---|---|---|
| G9 | `impact_score = mean(4次元) − max(0, risk−3)×0.5` という**単一スコア** | ABC はもともとスコアではなく**基準（criteria）による分類**。平均は補償的集計であり、弱い次元を強い次元が埋め合わせられてしまう。evidence gate はその補償性への非補償的パッチとして正しい方向を向いている。→ **進化方針：ゲートを1つから「必要条件の集合」へ増やす**（後述） |
| G10 | scale の絶対閾値（<100人 → 1、100–1000 → 3、>1000 → 5） | 日本の NPO の大多数が 1 点になる。深さ重視・小規模の事業が構造的に不利。「対象母集団に対する到達率」や「事業規模に対する相対値」への変更を検討する価値がある |
| G11 | 6つのリスクを単純平均 | リスクの種類によって「致命度」は違う（evidence risk は主張の可否に関わり、efficiency risk は改善課題にすぎない）。平均は両者を同列に扱う |

---

## 4. 進化の3シナリオ

| | S1: 規範追随型 | S2: 日本の NPO の入口ツール | S3: Reporting Norms 準拠レポート生成 |
|---|---|---|---|
| 相手 | IMM 実務家・国際的な利用者 | 休眠預金事業の実行団体、助成申請中の NPO、ソーシャルベンチャー | 私募市場の投資家、インパクトファンド |
| 勝ち筋 | 「透明で正確な OSS 実装」という公共財ポジション | 「最初の30分で自団体の弱点がわかる」実需 | Founding Adopters が100以上に増えた comply-or-explain 報告の作成支援 |
| コスト | 中（規範が動くたび追随が必要） | 中（日本語・ドメイン知識・レポート様式） | 大（V1本文の精読、V2 が2026年後半に来る） |
| リスク | 追随が止まった瞬間に「古い規範を名乗るツール」になる（nexus の旧スキルコピー問題と同型） | 差別化が UI と日本語に寄りがち | 対象顧客が RoboEvaluater の現在地から遠い。無償 OSS で戦う相手ではない |

**推奨：S2 を主軸、S1 を品質の最低ライン、S3 は当面「参考にする規範」として扱う。**

理由は日本側の実需にある。休眠預金等活用制度では、JANPIA・資金分配団体・実行団体の
**すべての事業で社会的インパクト評価の実施が求められており**、JANPIA の評価指針・
評価ハンドブックという「実務で使われている規範」がすでに存在する。
一方 Reporting Norms V1 は私募市場の投資家が NDA 下で共有する報告書を主対象としており、
日本の NPO 実務との距離は遠い。S3 に今から寄せるのは、顧客のいない場所に橋を架ける動きになる。

（推測であることを明示する：JANPIA 評価指針と IMP 5次元の対応関係は今回未検証。
S2 を選ぶ場合、最初にやるべき調査はこのマッピングである。）

---

## 5. ロードマップ

### v0.3 — 正確性（半日〜1日）

- [ ] G1: リスクを9種類に拡張（少なくとも execution / alignment を追加）。追加分の質問文と重みを決め、`parity_cases.json` にケース追加
- [ ] G2: `B: Benefit Stakeholders` → `B: Benefit People and the Planet`（レポート文言・Web アプリ表示・テスト）
- [ ] G3: README / SKILL.md / reference の帰属表記を「IMP が策定し、現在は Impact Frontiers が管理する規範」に統一
- [ ] レポートに **methodology version** を刻印する（`RoboEvaluater v0.3 / IMP 5-dimensions, 2023 ABC revision 準拠`）。規範が動くツールで、出力がいつのモデルで作られたか分からないのは致命的

### v0.4 — 構造（数日）

- [ ] G4/G8: **アウトカム単位の評価**に作り替える。1団体で複数アウトカムを登録し、それぞれに ABC を出す。団体単位のサマリーは「分類の集合」として提示し、平均しない
- [ ] G5: prospective / retrospective フラグを入力に追加し、レポート上で明示（目標ベースの C は C と呼ばない、等の規則も検討）
- [ ] G9: ゲートを複数化する。候補：
  - evidence gate（既存）
  - contribution gate — counterfactual が `most`（他でも起きた）なら C 不可
  - stakeholder gate — stakeholder_participation_risk が高いまま C は名乗れない
  - execution gate — 実行リスクが最大なら分類を保留する
- [ ] G10: scale を相対値（対象母集団に対する到達率）に変更、または絶対値と併記

### v1.0 — 文脈（週単位）

- [ ] JANPIA 評価指針・ロジックモデルとのマッピング表を作り、レポートに「助成報告にそのまま使える節」を出力
- [ ] Web アプリの英語化（CONTRIBUTING で既に言語トグルを募集済み）
- [ ] 同一事業の**再評価と時系列比較**（前回スコアとの差分、evidence_risk が下がったか）。IMM の本質は一回の採点ではなく改善のループなので、ここが本命機能になりうる
- [ ] G6: Who の属性別分解を任意項目として追加

### 横断

- [ ] `CHANGELOG.md` とモデルバージョニング。スコアリング変更のたびに「過去のレポートはどのモデルで出たか」が追えること
- [ ] CONTRIBUTING の方針どおり、スコアリング変更は Issue で先に議論する。本書の G1・G4・G9 はそれぞれ Issue 1本に相当する

---

## 6. 未確認事項（次セッションの宿題）

1. `impactfrontiers.org` / `impactreporting.org` を egress allowlist に追加し、
   ABC 修正版（2023-12）、Social Equity Revisions（2025-01）、Reporting Norms V1（2024-04）の
   一次資料を精読する
2. インパクトリスク9種類の公式リスト（8種は特定済み、9つ目が endurance risk か contribution risk か未確認）
3. JANPIA 評価指針と IMP 5次元の対応関係（S2 を選ぶ場合の最初の調査）
4. 2023年の ABC 協議で「実務家に支持されなかった C の厳格化案」が具体的に何だったか。
   RoboEvaluater の evidence gate は同種の厳格化であり、
   コミュニティが退けた理由は設計上きわめて参考になる

---

## 7. 総括

RoboEvaluater の最初の1日での進化（MVP → evidence gate）は、
Impact Frontiers が2023年以降たどっている方向と同じ問題意識に立っている。
すなわち **「良い意図を良い成果として数え上げてしまう構造を、どう塞ぐか」**。

だからこの先の進化も、機能を足す方向ではなく、この一点を深める方向に取るのが筋が良い。
具体的には、単一スコアの補償的集計を段階的に「必要条件の集合」へ置き換えること（G9）と、
分類の単位をアウトカムに合わせること（G4）。この2つが済めば、
用語や リスク種別の追随（G1–G3）は機械的な作業になる。

逆に、いま急いで Reporting Norms に寄せる必要はない。
V2 が2026年後半に来る以上、V1 に最適化した作り込みは半年で陳腐化する。
