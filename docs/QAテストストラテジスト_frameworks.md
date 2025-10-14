# QAテストストラテジスト - フレームワーク・理論詳細

## 概要

品質保証とテスト戦略は、ソフトウェア開発において価値とリスクのバランスを取る重要な専門領域です。このオーケストレーターは、テスト戦略設計、テスト設計技法、自動化戦略、欠陥管理、品質指標、非機能テストなど、実証済みのテスト手法とベストプラクティスを統合しています。

早期欠陥検出（Shift Left）、効率的なテスト自動化、データ駆動の品質改善を重視し、ビジネス価値を最大化しながらリスクを最小化する持続可能なQA戦略を実現します。

最終更新日: 2025-01-14

---

## 組み込まれているフレームワーク・理論

### 1. テストピラミッド（Test Pyramid）

**分類**: テスト戦略・アーキテクチャ系

**出典・背景**:
Mike Cohn が2009年の著書「Succeeding with Agile」で提唱しました。Martin Fowler が2012年の記事でさらに普及させました。テスト自動化戦略の基本原則として、異なるテストレベルの最適な配分を示し、効率的で保守可能なテストスイートの構築を支援します。

**理論の詳細**:

**定義**:
テスト自動化をピラミッド型に構成し、下層（Unit Tests）ほど数を多く、上層（UI Tests）ほど少なくする戦略。実行速度、コスト、保守性のバランスを最適化します。

**3つの層**:

**Layer 1: Unit Tests（ユニットテスト - 70%）**:
- **対象**: 個々の関数、メソッド、クラス
- **特徴**:
  - 高速（ミリ秒単位）
  - 安価（作成・保守コスト低）
  - 詳細なフィードバック（具体的な失敗箇所特定）
  - 外部依存なし（モック/スタブ使用）
- **ツール**: JUnit、pytest、Jest、Mocha、NUnit
- **例**:
  ```javascript
  // Jest example
  test('calculateTotal should sum item prices', () => {
    const items = [{ price: 100 }, { price: 200 }];
    expect(calculateTotal(items)).toBe(300);
  });
  ```
- **メリット**: 早期フィードバック、リファクタリング容易、開発者が書く
- **カバレッジ目標**: 80%以上

**Layer 2: Integration Tests（統合テスト - 20%）**:
- **対象**: コンポーネント間の連携、API、データベース連携
- **特徴**:
  - 中速（秒単位）
  - 中コスト
  - 実際の依存関係を使用（DB、外部API等）
  - インターフェース検証
- **ツール**: Postman、REST Assured、Karate、TestContainers
- **例**:
  ```python
  # pytest + requests example
  def test_create_order_api():
      response = requests.post('/api/orders', json={
          'customerId': 'C001',
          'items': [{'productId': 'P100', 'qty': 2}]
      })
      assert response.status_code == 201
      assert response.json()['orderId'] is not None
  ```
- **テストパターン**: API契約テスト、DB統合テスト、メッセージキューテスト

**Layer 3: E2E Tests（エンドツーエンドテスト - 10%）**:
- **対象**: ユーザーシナリオ全体、UI含む
- **特徴**:
  - 低速（分単位）
  - 高コスト（作成・保守・実行）
  - 環境依存（不安定になりやすい）
  - ビジネス価値の直接検証
- **ツール**: Selenium、Playwright、Cypress、Appium
- **例**:
  ```javascript
  // Playwright example
  test('user can complete checkout flow', async ({ page }) => {
    await page.goto('/products');
    await page.click('text=Add to Cart');
    await page.click('text=Checkout');
    await page.fill('#email', 'user@example.com');
    await page.click('button:has-text("Place Order")');
    await expect(page.locator('text=Order Confirmed')).toBeVisible();
  });
  ```
- **対象シナリオ**: Critical Path、主要ユースケース

**テストピラミッドの原則**:

1. **下層ほど多く**: Unit > Integration > E2E（70:20:10の比率）
2. **下層ほど高速**: フィードバックループの短縮
3. **下層ほど安定**: 環境依存少、メンテナンス容易
4. **上層は重要シナリオのみ**: ROI高いシナリオに絞る

**アンチパターン: Ice Cream Cone（逆ピラミッド）**:
```
[避けるべき構成]
E2E Tests: 60% (多すぎ)
Integration Tests: 30%
Unit Tests: 10% (少なすぎ)

問題点:
- 実行時間長い（CI/CDで数時間）
- 不安定（Flaky Tests多発）
- 保守コスト高
- フィードバック遅い
```

**変形: Testing Trophy（Kent C. Dodds提案）**:
```
E2E Tests: 10%
Integration Tests: 50% (重視)
Unit Tests: 40%

理由: 統合テストがコストと信頼性のバランス良
Web開発に適合
```

**実用例**:

**例1: Google**
- Unit Tests: 数百万件、数分で完了
- 統合テスト: 数万件
- E2Eテスト: 数千件、Critical Pathのみ

**例2: Netflix**
- マイクロサービスごとにピラミッド適用
- Contract Tests（統合層）を重視

**例3: Spotify**
- Squad単位でピラミッド管理
- E2EはSmokeテストのみ（主要フロー10個程度）

**適用指針**:

| プロジェクト種別 | Unit | Integration | E2E | 備考 |
|----------------|------|-------------|-----|------|
| Webアプリ | 60% | 30% | 10% | Trophy型も検討 |
| モバイルアプリ | 50% | 30% | 20% | UIテスト重要 |
| API/Backend | 70% | 25% | 5% | E2E不要な場合も |
| マイクロサービス | 70% | 20% | 10% | Contract Tests重視 |

**参考文献・リソース**:
- 書籍: "Succeeding with Agile" - Mike Cohn (2009)
- 記事: "TestPyramid" - Martin Fowler (2012) martinfowler.com/bliki/TestPyramid.html
- 記事: "Write tests. Not too many. Mostly integration." - Kent C. Dodds (Testing Trophy)
- 動画: "The Practical Test Pyramid" - Ham Vocke (YouTube)

---

### 2. Agile Testing Quadrants（アジャイルテスティング4象限）

**分類**: テスト戦略・カテゴリ分類系

**出典・背景**:
Brian Marick が2003年に提唱し、Lisa Crispin と Janet Gregory が2009年の著書「Agile Testing」で体系化しました。テストの目的と視点を4つの象限に分類し、バランスの取れた包括的なテスト戦略を実現します。

**理論の詳細**:

**2つの軸**:

**縦軸**: ビジネス視点 vs 技術視点
**横軸**: チーム支援 vs 製品評価

**4つの象限**:

**Q1: 技術視点 × チーム支援（Technology-Facing, Supporting the Team）**

- **目的**: 開発をサポート、設計品質向上
- **テストタイプ**:
  - **Unit Tests**: 個々のコンポーネント検証
  - **Component Tests**: コンポーネント単位の動作確認
- **特徴**:
  - 開発者が主導
  - 自動化必須
  - TDD/BDDで実施
- **ツール**: JUnit、pytest、Jest、NUnit
- **例**:
  ```java
  @Test
  public void shouldCalculateDiscountCorrectly() {
      Order order = new Order(1000);
      order.applyDiscount(10); // 10% discount
      assertEquals(900, order.getTotal());
  }
  ```
- **頻度**: コミットごと

**Q2: ビジネス視点 × チーム支援（Business-Facing, Supporting the Team）**

- **目的**: 要件理解、機能正確性の確認
- **テストタイプ**:
  - **Functional Tests**: 機能要件の検証
  - **Story Tests**: ユーザーストーリー受け入れテスト
  - **Prototypes/Simulations**: 初期段階の検証
- **特徴**:
  - PO/ビジネスと協働
  - 自動化推奨
  - BDD（Behavior-Driven Development）適用
  - Given-When-Then形式
- **ツール**: Cucumber、SpecFlow、Behave、FitNesse
- **例**:
  ```gherkin
  # Cucumber example
  Feature: Shopping Cart
    Scenario: User adds item to cart
      Given user is on product page
      When user clicks "Add to Cart"
      Then cart count should increase by 1
      And item should appear in cart
  ```
- **頻度**: スプリントごと

**Q3: ビジネス視点 × 製品評価（Business-Facing, Critique Product）**

- **目的**: 製品の実用性、ユーザー満足度評価
- **テストタイプ**:
  - **Exploratory Testing**: 構造化された探索的テスト
  - **Usability Testing**: ユーザビリティ評価
  - **UAT（User Acceptance Testing）**: 実ユーザーによる受け入れ
  - **Alpha/Beta Testing**: 限定リリース検証
- **特徴**:
  - 手動テスト中心
  - 創造的アプローチ
  - ユーザー視点
  - 予期しない問題発見
- **手法**: Session-Based Exploratory Testing、Personas
- **例**:
  - 新機能を異なるユーザーペルソナで探索
  - 「壊そうとする」マインドセット
  - エッジケース発見
- **頻度**: スプリント終盤、リリース前

**Q4: 技術視点 × 製品評価（Technology-Facing, Critique Product）**

- **目的**: 非機能要件の検証、システム健全性
- **テストタイプ**:
  - **Performance Tests**: 性能・負荷テスト
  - **Load/Stress Tests**: 高負荷・限界テスト
  - **Security Tests**: 脆弱性検査
  - **Scalability Tests**: スケーラビリティ検証
  - **Compatibility Tests**: 互換性テスト
- **特徴**:
  - 専門スキル必要
  - ツール主導
  - 本番環境に近い環境
- **ツール**: JMeter、Gatling、k6、OWASP ZAP、Burp Suite
- **例**:
  ```javascript
  // k6 load test example
  import http from 'k6/http';
  import { check } from 'k6';

  export let options = {
    vus: 100,
    duration: '5m',
  };

  export default function() {
    let res = http.get('https://api.example.com/products');
    check(res, { 'status is 200': (r) => r.status === 200 });
  }
  ```
- **頻度**: スプリントごと、リリース前

**4象限の統合戦略**:

```
     ビジネス視点
         ↑
    Q2   |   Q3
  (BDD) | (探索的)
--------|--------
    Q1   |   Q4
 (Unit) | (性能)
         ↓
     技術視点

左側（Q1, Q2）: チーム支援（Proactive）
右側（Q3, Q4）: 製品評価（Reactive）
```

**バランスの取れたテスト戦略**:
- すべての象限をカバー
- プロジェクトフェーズで重点シフト
  - 初期: Q1, Q2（機能構築）
  - 中期: すべて
  - 後期: Q3, Q4（品質評価）

**自動化vs手動の区分**:
| 象限 | 自動化 | 手動 |
|------|--------|------|
| Q1 | 100% | 0% |
| Q2 | 80% | 20% |
| Q3 | 20% | 80% |
| Q4 | 70% | 30% |

**実用例**:

**例1: Eコマースサイト**
- Q1: 決済ロジック、在庫計算のUnitテスト
- Q2: 「商品購入」ストーリーのBDDテスト
- Q3: 新しい検索UI の探索的テスト
- Q4: ブラックフライデー対策のLoadテスト

**例2: モバイルバンキングアプリ**
- Q1: 送金計算、認証ロジックのUnitテスト
- Q2: 「振込」機能の受け入れテスト
- Q3: 高齢者ペルソナでのUsabilityテスト
- Q4: セキュリティテスト（OWASP Mobile Top 10）

**チーム体制への適用**:
- 開発者: Q1主導、Q2参加
- QAエンジニア: すべて参画、Q3/Q4主導
- PO/ビジネス: Q2承認、Q3参加

**参考文献・リソース**:
- 書籍: "Agile Testing: A Practical Guide for Testers and Agile Teams" - Lisa Crispin, Janet Gregory (2009)
- 書籍: "More Agile Testing" - Lisa Crispin, Janet Gregory (2014)
- 記事: "Agile Testing Quadrants" - Lisa Crispin (lisacrispin.com)
- サイト: Brian Marick's Blog（オリジナル提唱）

---

### 3. リスクベーステスト（Risk-Based Testing / RBT）

**分類**: テスト戦略・優先順位付け系

**出典・背景**:
ISTQB（International Software Testing Qualifications Board）のシラバスで標準化されました。ISO/IEC/IEEE 29119にも記載されています。限られたリソースで最大の効果を得るため、リスク分析に基づいてテストの優先順位を決定する体系的アプローチです。

**理論の詳細**:

**定義**:
ソフトウェアの各領域のリスク（発生確率 × 影響度）を評価し、高リスク領域に重点的にテストリソースを配分する戦略。

**リスク評価の公式**:

```
リスク値 = 発生確率（Likelihood） × 影響度（Impact）

発生確率: 1-5（1=非常に低い、5=非常に高い）
影響度: 1-5（1=軽微、5=致命的）
リスク値: 1-25
```

**リスク評価マトリクス**:

|影響度＼確率| 1（稀） | 2（低） | 3（中） | 4（高） | 5（頻繁）|
|-----------|---------|---------|---------|---------|---------|
| **5（致命的）** | 5 | 10 | 15 | 20 | **25** |
| **4（重大）** | 4 | 8 | 12 | **16** | **20** |
| **3（中）** | 3 | 6 | **9** | **12** | 15 |
| **2（小）** | 2 | 4 | 6 | 8 | 10 |
| **1（軽微）** | 1 | 2 | 3 | 4 | 5 |

**リスクレベル分類**:
- **Critical（20-25）**: 最優先、徹底的テスト
- **High（12-19）**: 高優先、詳細テスト
- **Medium（6-11）**: 標準テスト
- **Low（1-5）**: 最小限テスト、省略可能

**リスク識別の観点**:

**1. ビジネスリスク**:
- 収益への影響
- 顧客満足度
- 法規制コンプライアンス
- ブランドイメージ

**例**:
- Eコマース決済処理（High Impact）
- 個人情報取扱（高リスク: 法的影響）
- レポート機能（Low Impact）

**2. 技術リスク**:
- 複雑性（Cyclomatic Complexity高）
- 新技術・未知技術
- 外部依存度
- コード変更頻度

**例**:
- 新しいフレームワーク導入部分
- レガシーコード統合箇所
- 複雑なアルゴリズム

**3. プロジェクトリスク**:
- 開発スケジュール遅延
- 要件変更頻度
- チームスキルレベル
- 過去の欠陥履歴

**リスクベーステストのプロセス**:

**Step 1: リスク識別（Risk Identification）**
- ステークホルダー会議
- 過去の欠陥分析
- 要件レビュー
- アーキテクチャレビュー

**Step 2: リスク分析（Risk Analysis）**
- 発生確率の見積もり
  - 過去データ（類似機能の欠陥率）
  - 複雑性指標（Cyclomatic Complexity）
  - 変更頻度
- 影響度の見積もり
  - ビジネス影響（収益、ユーザー数）
  - 規制要件
  - データ損失リスク

**Step 3: リスク値計算**
- リスクマトリクス作成
- 優先順位付け

**Step 4: テスト戦略策定**
- 高リスク領域: テスト密度高、詳細テストケース、複数手法
- 低リスク領域: 最小限テスト、Smoke Test

**Step 5: テスト実行・モニタリング**
- 高リスク領域から実施
- 欠陥検出でリスク再評価
- 残存リスクレポート

**リスクレベル別テスト戦略**:

| リスクレベル | テストカバレッジ | テスト技法 | 自動化 | レビュー |
|------------|----------------|-----------|--------|---------|
| Critical | 100% | 境界値、デシジョンテーブル、ペアワイズ、探索的 | 必須 | 複数人 |
| High | 80-90% | 境界値、状態遷移 | 推奨 | 1-2人 |
| Medium | 60-70% | 同値分割、基本パス | 部分的 | 1人 |
| Low | 30-40% | Smoke Test、基本フロー | 不要 | なし |

**実用例**:

**例1: オンラインバンキング**

| 機能 | 発生確率 | 影響度 | リスク値 | テスト戦略 |
|------|---------|--------|---------|----------|
| 送金処理 | 3 | 5 | 15 | 徹底的（境界値、異常系、セキュリティ） |
| ログイン | 4 | 4 | 16 | 詳細（多要素認証、ブルートフォース） |
| 残高照会 | 2 | 3 | 6 | 標準（正常系中心） |
| UI配色 | 1 | 1 | 1 | 最小限（目視確認） |

**例2: 医療システム**

| 機能 | 発生確率 | 影響度 | リスク値 | 備考 |
|------|---------|--------|---------|------|
| 投薬量計算 | 2 | 5 | 10 | 生命に関わる |
| 患者情報管理 | 3 | 5 | 15 | プライバシー、法的要件 |
| 予約管理 | 4 | 2 | 8 | ビジネス影響中程度 |

**リスク軽減テスト技法**:

**高リスク領域向け**:
1. **Boundary Value Analysis（境界値分析）**: エッジケース検出
2. **Decision Tables（デシジョンテーブル）**: 複雑な条件網羅
3. **Pairwise Testing（ペアワイズ法）**: パラメータ組み合わせ削減
4. **Exploratory Testing（探索的テスト）**: 予期しない欠陥発見
5. **Security Testing**: 脅威モデリング（STRIDE、OWASP）

**残存リスクの管理**:
- **受容（Accept）**: リスク低、対応不要
- **軽減（Mitigate）**: テスト追加、設計変更
- **転嫁（Transfer）**: 保険、SLA
- **回避（Avoid）**: 機能削除、設計変更

**リスク再評価のトリガー**:
- 要件変更
- 高重要度欠陥検出
- アーキテクチャ変更
- 新しい脅威情報

**メリット**:
- 限られたリソースの最適配分
- ステークホルダーとの合意形成
- テスト計画の透明性
- ビジネス価値とテストの整合

**参考文献・リソース**:
- 標準: ISO/IEC/IEEE 29119-2（テストプロセス）
- シラバス: ISTQB Foundation Level（Risk-Based Testing章）
- 書籍: "Risk-Based Testing" - Geoff Thompson（2002）
- 記事: "Pragmatic Risk-Based Testing" - Chris Matts

---

### 4. テスト設計技法（Test Design Techniques）

**分類**: テスト設計・技術系

**出典・背景**:
ISTQB、IEEE 829、ISO/IEC/IEEE 29119等の国際標準で体系化されています。Glenford Myers の「The Art of Software Testing」（1979）、Boris Beizer の「Software Testing Techniques」（1990）が古典的名著です。効率的で効果的なテストケース作成の科学的手法です。

**理論の詳細**:

#### ブラックボックステスト技法

**定義**: 内部構造を考慮せず、入出力仕様に基づいてテスト。

**4.1 同値分割（Equivalence Partitioning / EP）**

**原理**: 入力を「同じ振る舞いをするクラス」に分割。各クラスから1つテストすれば代表できる。

**手順**:
1. 有効クラス（Valid）と無効クラス（Invalid）に分類
2. 各クラスから代表値選択

**例**: 年齢入力（0-120が有効）

| クラス | 範囲 | 代表値 | 期待結果 |
|--------|------|--------|---------|
| 無効（負） | age < 0 | -1 | エラー |
| 有効 | 0 ≤ age ≤ 120 | 25 | 受理 |
| 無効（超過） | age > 120 | 150 | エラー |

**コード例**:
```python
# pytest example
@pytest.mark.parametrize("age, expected", [
    (-1, "Invalid"),
    (0, "Valid"),
    (25, "Valid"),
    (120, "Valid"),
    (150, "Invalid"),
])
def test_age_validation(age, expected):
    assert validate_age(age) == expected
```

**4.2 境界値分析（Boundary Value Analysis / BVA）**

**原理**: エラーは境界付近で発生しやすい。境界値と境界±1をテスト。

**手順**:
1. 有効範囲の境界特定
2. 境界値、境界-1、境界+1をテスト

**例**: 年齢入力（0-120）

| テスト値 | 説明 | 期待結果 |
|---------|------|---------|
| -1 | 下限-1 | エラー |
| 0 | 下限 | 受理 |
| 1 | 下限+1 | 受理 |
| 119 | 上限-1 | 受理 |
| 120 | 上限 | 受理 |
| 121 | 上限+1 | エラー |

**同値分割との違い**:
- 同値分割: 各クラス1つ
- 境界値: 境界に集中（より効果的）

**4.3 デシジョンテーブル（Decision Table）**

**原理**: 複雑な条件の組み合わせを網羅的にテスト。

**構成**:
- 条件（Conditions）: 入力条件
- アクション（Actions）: 期待される動作

**例**: 割引ルール

```
条件:
C1: 会員種別（通常/プレミアム）
C2: 購入金額（10,000円以上/未満）

アクション:
A1: 割引率

| ルール | R1 | R2 | R3 | R4 |
|--------|----|----|----|----|
| C1: プレミアム | Y | Y | N | N |
| C2: 10,000円以上 | Y | N | Y | N |
| A1: 割引率 | 20% | 15% | 10% | 0% |
```

**テストケース**: 4つのルールそれぞれをテスト

**コード例**:
```python
@pytest.mark.parametrize("is_premium, amount, expected_discount", [
    (True, 15000, 0.20),  # R1
    (True, 5000, 0.15),   # R2
    (False, 15000, 0.10), # R3
    (False, 5000, 0.00),  # R4
])
def test_discount_calculation(is_premium, amount, expected_discount):
    assert calculate_discount(is_premium, amount) == expected_discount
```

**4.4 状態遷移テスト（State Transition Testing）**

**原理**: システムの状態と状態間の遷移をテスト。

**構成要素**:
- 状態（States）
- イベント（Events）
- 遷移（Transitions）
- アクション（Actions）

**例**: ATM状態

```
状態:
- Idle（待機中）
- CardInserted（カード挿入）
- PinEntered（PIN入力）
- Transaction（取引中）

遷移:
Idle --[カード挿入]--> CardInserted
CardInserted --[PIN入力]--> PinEntered
PinEntered --[正しいPIN]--> Transaction
PinEntered --[誤ったPIN]--> CardInserted
Transaction --[取引完了]--> Idle
```

**テストケース**:
- 各遷移を1回カバー（0-switch coverage）
- すべての遷移ペアをカバー（1-switch coverage）

**状態遷移表**:

| 現在状態 | イベント | 次状態 | アクション |
|---------|---------|--------|----------|
| Idle | カード挿入 | CardInserted | PIN要求 |
| CardInserted | 正しいPIN | Transaction | メニュー表示 |
| CardInserted | 誤ったPIN（3回未満） | CardInserted | 再入力要求 |
| CardInserted | 誤ったPIN（3回） | Idle | カード没収 |

**4.5 ペアワイズ法（Pairwise Testing / All-Pairs）**

**原理**: すべてのパラメータの2つの組み合わせを少なくとも1回カバー。欠陥の多くは2つのパラメータ相互作用で発生（経験則）。

**例**: Webブラウザテスト

パラメータ:
- ブラウザ: Chrome, Firefox, Safari（3値）
- OS: Windows, macOS, Linux（3値）
- 言語: 英語, 日本語（2値）

全組み合わせ: 3 × 3 × 2 = 18通り

**ペアワイズ削減**: 9通り（ツール生成）

| テストケース | ブラウザ | OS | 言語 |
|------------|---------|-------|------|
| 1 | Chrome | Windows | 英語 |
| 2 | Chrome | macOS | 日本語 |
| 3 | Chrome | Linux | 英語 |
| 4 | Firefox | Windows | 日本語 |
| 5 | Firefox | macOS | 英語 |
| 6 | Firefox | Linux | 日本語 |
| 7 | Safari | Windows | 日本語 |
| 8 | Safari | macOS | 英語 |
| 9 | Safari | Linux | 英語 |

**ツール**:
- PICT（Microsoft）
- AllPairs
- CTE XL（Classification Tree Editor）

**PICT使用例**:
```
# input.txt
Browser: Chrome, Firefox, Safari
OS: Windows, macOS, Linux
Language: English, Japanese

# コマンド
pict input.txt

# 出力: 最適化されたテストケース
```

#### ホワイトボックステスト技法

**定義**: 内部構造（コード）に基づいてテスト。

**4.6 ステートメントカバレッジ（Statement Coverage）**

**定義**: すべてのコード行を少なくとも1回実行。

**計算式**:
```
カバレッジ = 実行された文 / 総文数 × 100%
```

**例**:
```python
def discount(price, is_member):
    if is_member:          # 行1
        price *= 0.9       # 行2
    return price           # 行3

# テストケース1: discount(1000, True)
# → 行1, 2, 3実行 → 100%カバレッジ
```

**問題点**: 分岐の片方だけでも100%

**4.7 ブランチカバレッジ（Branch Coverage / Decision Coverage）**

**定義**: すべての分岐（True/False）を実行。

**例**:
```python
def discount(price, is_member):
    if is_member:          # 分岐1
        price *= 0.9
    return price

# テストケース:
# 1. discount(1000, True)  → 分岐1: True
# 2. discount(1000, False) → 分岐1: False
# → 100%ブランチカバレッジ
```

**計算式**:
```
カバレッジ = 実行された分岐 / 総分岐数 × 100%
```

**4.8 条件カバレッジ（Condition Coverage）**

**定義**: 複合条件の各部分条件のTrue/Falseを実行。

**例**:
```python
if (age > 18 and has_license):  # 条件A and 条件B
    allow_drive()

# 条件カバレッジ: A=True, A=False, B=True, B=False
テストケース:
1. age=20, has_license=True  → A=T, B=T
2. age=15, has_license=False → A=F, B=F
```

**より厳密: Modified Condition/Decision Coverage (MC/DC)**
- 航空宇宙、医療機器で要求（DO-178C）
- 各条件が結果に独立して影響することを確認

**4.9 パスカバレッジ（Path Coverage）**

**定義**: すべての実行パスを網羅。

**問題**: 組み合わせ爆発（ループがあると無限）

**現実的アプローチ**: 主要パスのみカバー

**カバレッジ目標（業界標準）**:
- Unit Tests: 70-80%以上（ステートメント）
- Critical Path: 100%（ブランチ）
- 安全系システム: MC/DC 100%

**ツール**:
- Java: JaCoCo、Cobertura
- Python: Coverage.py
- JavaScript: Istanbul、Jest（内蔵）
- C/C++: gcov、lcov

#### 探索的テスト（Exploratory Testing）

**定義**: テスト設計と実行を同時並行で行う、構造化された手法。

**4.10 セッションベース探索的テスト（Session-Based Exploratory Testing / SBET）**

**提唱者**: James Bach、Jonathan Bach

**構成**:

**Session（セッション）**:
- 時間: 60-120分の区切られた時間
- Charter（チャーター）: テスト目的・スコープ
- 成果物: バグレポート、メモ、スクリーンショット

**Charter例**:
```
Charter: 検索機能の境界値と特殊文字処理を探索

スコープ:
- 検索ボックス（トップページ、商品一覧）
- 入力: 0文字、長文、特殊文字、SQL injection試行
- 期待動作: エラーハンドリング、セキュリティ

Time Box: 90分
```

**実行ステップ**:
1. **学習（Learn）**: システム理解、動作観察
2. **仮説（Hypothesize）**: 「ここで問題起きそう」
3. **検証（Test）**: 仮説テスト
4. **記録（Document）**: 発見事項メモ

**マインドマップ活用**:
```
[検索機能]
  ├─ 入力値
  │   ├─ 空文字
  │   ├─ 特殊文字（<, >, ", '）
  │   ├─ 非常に長い文字列
  │   └─ SQLコード
  ├─ フィルタ
  │   ├─ 価格範囲
  │   └─ カテゴリ
  └─ 結果表示
      ├─ 0件
      ├─ 大量件数
      └─ ソート順
```

**探索的テストのヒューリスティック**:
- **CRUD**: Create, Read, Update, Delete すべてテスト
- **0, 1, Many**: 0個、1個、多数の境界
- **Goldilocks**: 小さすぎ、大きすぎ、ちょうど良い
- **Interrupt**: 処理中に割り込み（ネットワーク切断等）

**メリット**:
- 事前のテストケース不要（アジャイル向き）
- クリエイティブ、予期しない欠陥発見
- 要件曖昧でも実施可能

**デメリット**:
- 再現性低い
- スキル依存
- カバレッジ測定困難

**適用場面**:
- 新機能の初期探索
- リグレッションテスト補完
- スクリプトテストで見逃した領域

**参考文献・リソース**:
- 書籍: "The Art of Software Testing" - Glenford Myers (1979, 3rd Ed. 2011)
- 書籍: "Software Testing Techniques" - Boris Beizer (1990)
- 書籍: "Explore It!" - Elisabeth Hendrickson (2013) ← 探索的テスト
- 書籍: "Lessons Learned in Software Testing" - Cem Kaner, James Bach, Bret Pettichord (2001)
- 標準: ISTQB Foundation Level Syllabus（Test Design Techniques章）
- ツール: PICT（Microsoft）、TestRail（テスト管理）

---

### 5. テスト自動化戦略（Test Automation Strategy）

**分類**: テスト自動化・ROI最適化系

**出典・背景**:
Martin Fowler らの「Continuous Integration」（2006）、「Continuous Delivery」（Jez Humble, 2010）で体系化されました。Page Object Model は Selenium コミュニティで確立されました。自動化のROI最大化と保守性向上を実現する実践的戦略です。

**理論の詳細**:

#### 5.1 自動化ROI分析

**ROI計算式**:

```
ROI = (節約コスト - 投資コスト) / 投資コスト × 100%

節約コスト = 手動実行コスト × 実行回数
投資コスト = 初期開発コスト + 保守コスト

例:
手動実行: 30分（= 0.5時間）× 時給5000円 = 2500円/回
実行回数: 100回/年
自動化開発: 8時間 × 時給5000円 = 40,000円
保守コスト: 2時間/年 × 5000円 = 10,000円

節約コスト = 2500 × 100 = 250,000円
投資コスト = 40,000 + 10,000 = 50,000円
ROI = (250,000 - 50,000) / 50,000 = 400%

損益分岐点 = 投資コスト / 手動実行コスト = 50,000 / 2500 = 20回
```

**自動化優先度マトリクス**:

| 要因 | 高優先度 | 低優先度 |
|------|---------|---------|
| 実行頻度 | 日次以上 | 月次以下 |
| 手動実行時間 | 30分以上 | 5分以下 |
| 変更頻度 | 低い（安定） | 高い（頻繁変更） |
| クリティカル度 | 高（決済、認証） | 低（UI装飾） |
| データバリエーション | 多数 | 少数 |
| 複雑性 | 単純（Linear Flow） | 複雑（多分岐） |

**自動化すべき vs すべきでない**:

**自動化すべき**:
- ✅ Smoke Tests（クリティカルパス）
- ✅ Regression Tests（既存機能）
- ✅ API Tests（安定、高速）
- ✅ Unit Tests（すべて）
- ✅ Data-Driven Tests（多数パラメータ）
- ✅ Performance Tests（負荷生成）

**自動化すべきでない**:
- ❌ 探索的テスト（人間の判断必要）
- ❌ Usability Tests（主観的）
- ❌ 一度きりのテスト（Ad-hoc）
- ❌ 頻繁に変更されるUI（保守コスト高）
- ❌ 複雑すぎるシナリオ（Cost > Benefit）

#### 5.2 Page Object Model (POM)

**定義**: UIテスト自動化のデザインパターン。UI要素とテストロジックを分離し、保守性向上。

**原則**:
1. **1ページ = 1クラス**
2. **UI要素はPageクラスに集約**
3. **テストコードはPageメソッドを呼び出すのみ**
4. **UIロケータ変更時、Pageクラスのみ修正**

**構造**:
```
/pages
  ├── BasePage.java          # 共通機能
  ├── LoginPage.java
  ├── ProductListPage.java
  └── CheckoutPage.java
/tests
  ├── LoginTest.java
  └── CheckoutTest.java
```

**実装例（Selenium + Java）**:

```java
// pages/LoginPage.java
public class LoginPage {
    private WebDriver driver;

    // Locators (UI要素)
    @FindBy(id = "username")
    private WebElement usernameField;

    @FindBy(id = "password")
    private WebElement passwordField;

    @FindBy(css = "button[type='submit']")
    private WebElement loginButton;

    @FindBy(css = ".error-message")
    private WebElement errorMessage;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    // Page Methods (ページ操作)
    public void enterUsername(String username) {
        usernameField.sendKeys(username);
    }

    public void enterPassword(String password) {
        passwordField.sendKeys(password);
    }

    public void clickLogin() {
        loginButton.click();
    }

    public String getErrorMessage() {
        return errorMessage.getText();
    }

    // High-level Method
    public DashboardPage loginAs(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickLogin();
        return new DashboardPage(driver);
    }
}

// tests/LoginTest.java
public class LoginTest {
    @Test
    public void testValidLogin() {
        LoginPage loginPage = new LoginPage(driver);
        DashboardPage dashboard = loginPage.loginAs("user@example.com", "password123");

        assertTrue(dashboard.isDisplayed());
    }

    @Test
    public void testInvalidLogin() {
        LoginPage loginPage = new LoginPage(driver);
        loginPage.loginAs("invalid@example.com", "wrong");

        assertEquals("Invalid credentials", loginPage.getErrorMessage());
    }
}
```

**Playwright + TypeScript版**:

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  // Locators
  private usernameInput = () => this.page.locator('#username');
  private passwordInput = () => this.page.locator('#password');
  private loginButton = () => this.page.locator('button[type="submit"]');
  private errorMessage = () => this.page.locator('.error-message');

  // Methods
  async login(username: string, password: string) {
    await this.usernameInput().fill(username);
    await this.passwordInput().fill(password);
    await this.loginButton().click();
  }

  async getErrorMessage(): Promise<string> {
    return await this.errorMessage().textContent();
  }
}

// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('valid login', async ({ page }) => {
  await page.goto('/login');
  const loginPage = new LoginPage(page);

  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

**POMのメリット**:
- **DRY（Don't Repeat Yourself）**: UI要素の重複排除
- **保守容易**: UIロケータ変更時、1箇所修正
- **可読性**: テストコードが高レベル、意図明確
- **再利用性**: Pageクラスを複数テストで共有

#### 5.3 Data-Driven Testing (DDT)

**定義**: テストデータとテストロジックを分離。複数データセットで同じテストを実行。

**アプローチ**:

**1. パラメータ化テスト（Parameterized Tests）**

```python
# pytest + CSV
import pytest
import csv

def load_test_data():
    with open('test_data.csv') as f:
        reader = csv.DictReader(f)
        return [(row['username'], row['password'], row['expected'])
                for row in reader]

@pytest.mark.parametrize("username,password,expected", load_test_data())
def test_login(username, password, expected):
    result = login(username, password)
    assert result == expected

# test_data.csv
# username,password,expected
# user1@example.com,pass123,success
# user2@example.com,wrongpass,failure
# invalid@example.com,pass123,failure
```

**2. データファイル駆動（Excel, CSV, JSON）**

```javascript
// Playwright + JSON
import testData from './test_data.json';

testData.forEach(({ username, password, expectedError }) => {
  test(`login with ${username}`, async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', username);
    await page.fill('#password', password);
    await page.click('button[type="submit"]');

    if (expectedError) {
      await expect(page.locator('.error')).toHaveText(expectedError);
    }
  });
});

// test_data.json
[
  { "username": "valid@example.com", "password": "pass123", "expectedError": null },
  { "username": "invalid@example.com", "password": "wrong", "expectedError": "Invalid credentials" }
]
```

**3. データベース駆動**

```java
// JUnit + JDBC
@ParameterizedTest
@MethodSource("getUsersFromDatabase")
void testUserLogin(String username, String password, boolean shouldSucceed) {
    boolean result = authService.login(username, password);
    assertEquals(shouldSucceed, result);
}

static Stream<Arguments> getUsersFromDatabase() throws SQLException {
    Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/testdb");
    Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery("SELECT username, password, is_valid FROM test_users");

    List<Arguments> testData = new ArrayList<>();
    while (rs.next()) {
        testData.add(Arguments.of(
            rs.getString("username"),
            rs.getString("password"),
            rs.getBoolean("is_valid")
        ));
    }
    return testData.stream();
}
```

**DDTのメリット**:
- テストカバレッジ向上（多数データセット）
- 非エンジニアがデータ作成可能（Excel）
- テストロジック再利用
- バグの再現データ追加容易

#### 5.4 CI/CDパイプライン統合

**定義**: テストをCI/CDパイプラインに組み込み、継続的品質保証。

**パイプラインステージ設計**:

```
Commit Stage (5-10分):
  ├─ Linting / Static Analysis (ESLint, SonarQube)
  ├─ Unit Tests (全件)
  └─ Code Coverage Check (80%未満で失敗)

Acceptance Stage (20-40分):
  ├─ Integration Tests
  ├─ API Tests
  ├─ Smoke Tests (E2E critical path)
  └─ Database Migration Tests

Performance Stage (30-60分):
  ├─ Load Tests (小規模: 100 VUs)
  └─ Performance Regression Tests

Security Stage (10-30分):
  ├─ Dependency Vulnerability Scan (npm audit, Snyk)
  ├─ SAST (Static Application Security Testing)
  └─ Container Image Scan (Trivy, Clair)

Deploy to Staging

E2E Stage (60-120分):
  ├─ Full E2E Test Suite
  └─ Visual Regression Tests

Deploy to Production
```

**GitHub Actions例**:

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:integration

  e2e-tests:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

**並列実行戦略**:

```javascript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 2 : 4,  // CI環境では並列数制限
  retries: process.env.CI ? 2 : 0,  // CIではリトライ有効
  use: {
    trace: 'on-first-retry',        // 失敗時トレース記録
    screenshot: 'only-on-failure',
  },
});
```

**テスト高速化手法**:
1. **並列実行**: ワーカー数最大化
2. **テスト分割**: テストスイートを複数ジョブに分割
3. **キャッシュ**: 依存関係、ビルドアーティファクトキャッシュ
4. **Selective Testing**: 変更ファイルに関連するテストのみ実行
5. **Fail Fast**: 最初の失敗で即停止（オプション）

**テスト結果レポート**:
- **Test Reporting**: JUnit XML、Allure、HTML Report
- **Flaky Tests検出**: 不安定なテスト特定・隔離
- **Trend Analysis**: テスト実行時間、成功率トレンド

#### 5.5 自動化ツール選定マトリクス

| テストレベル | 推奨ツール | 特徴 | 学習曲線 |
|------------|----------|------|---------|
| **Unit** | JUnit, pytest, Jest, Mocha | 言語ネイティブ、高速 | 低 |
| **API** | Postman, REST Assured, Karate | RESTful API特化、Collection実行 | 低-中 |
| **UI (Web)** | Playwright, Cypress | モダン、高速、DX良 | 中 |
| **UI (Web - Legacy)** | Selenium | 最も成熟、ブラウザ対応広 | 中-高 |
| **Mobile** | Appium, Detox, XCUITest | クロスプラットフォーム | 高 |
| **Performance** | k6, Gatling | コードベース、CI統合容易 | 中 |
| **Performance (Legacy)** | JMeter | GUI、非エンジニア向け | 中 |
| **Security** | OWASP ZAP, Burp Suite | 脆弱性スキャン | 中-高 |

**Playwright vs Selenium vs Cypress比較**:

| 特徴 | Playwright | Selenium | Cypress |
|------|-----------|----------|---------|
| 速度 | 高速 | 中速 | 高速 |
| 安定性 | 高（Auto-wait） | 低（Explicit wait必要） | 高 |
| 複数ブラウザ | Chromium, Firefox, WebKit | すべて | Chrome系のみ |
| 複数タブ/ウィンドウ | ✅ | ✅ | ❌ |
| ネットワークモック | ✅ | ❌ | ✅ |
| 並列実行 | ✅ | ✅（Grid） | 有料 |
| DX（開発者体験） | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| トレース/デバッグ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 学習曲線 | 低 | 中 | 低 |
| リリース年 | 2020 | 2004 | 2017 |

**推奨**: 新規プロジェクト → Playwright、既存Selenium → 継続、シンプルWebアプリ → Cypress

**参考文献・リソース**:
- 書籍: "Continuous Delivery" - Jez Humble, David Farley (2010)
- 書籍: "Selenium Design Patterns and Best Practices" - Dima Kovalenko (2014)
- 記事: "Page Object Models" - Selenium公式ドキュメント
- 記事: "The Practical Test Pyramid" - Ham Vocke (martinfowler.com)
- ツール: Playwright.dev、Selenium.dev、Cypress.io

---

### 6. 品質指標とKPI（Quality Metrics & KPIs）

**分類**: 品質測定・可視化系

**出典・背景**:
Capers Jones の「Software Quality」（1997）、Tom DeMarco の「Controlling Software Projects」（1982）が基礎です。Google の「DORA Metrics」（DevOps Research and Assessment）、「SPACE Framework」も現代的指標として重要です。データ駆動の品質管理と継続的改善を実現します。

**理論の詳細**:

#### 6.1 テストカバレッジ指標

**コードカバレッジ（Code Coverage）**

**定義**: テストがカバーしたコードの割合。

**種類**:

1. **行カバレッジ（Line Coverage / Statement Coverage）**
```
カバレッジ = 実行された行数 / 総行数 × 100%

例: 総100行、テストで80行実行 → 80%
```

2. **分岐カバレッジ（Branch Coverage）**
```
カバレッジ = 実行された分岐 / 総分岐数 × 100%

例: if文10個（20分岐）、16分岐実行 → 80%
```

3. **関数カバレッジ（Function Coverage）**
```
カバレッジ = 呼び出された関数 / 総関数数 × 100%
```

**目標値（業界標準）**:

| プロジェクト種別 | 目標カバレッジ |
|----------------|--------------|
| 通常のWebアプリ | 70-80% |
| クリティカルシステム（医療、金融） | 90-95% |
| オープンソースライブラリ | 80-90% |
| レガシーコード | 50-60%（段階的向上） |

**カバレッジレポート例（Jest）**:
```
--------------------------|---------|----------|---------|---------|
File                      | % Stmts | % Branch | % Funcs | % Lines |
--------------------------|---------|----------|---------|---------|
All files                 |   82.5  |   78.3   |   85.1  |   82.8  |
 src/                     |         |          |         |         |
  auth.js                 |   95.2  |   91.7   |   100   |   95.0  |
  payment.js              |   88.9  |   85.0   |   100   |   89.1  |
  utils.js                |   65.4  |   58.3   |   70.0  |   66.2  |
--------------------------|---------|----------|---------|---------|
```

**カバレッジの落とし穴**:
- ❌ 100%を目標にしない（Cost > Benefit）
- ❌ カバレッジ=品質ではない（アサーションなしでも100%）
- ✅ カバレッジ低下を検知（CI/CDで閾値チェック）
- ✅ 未カバー箇所のリスク評価

**要件カバレッジ（Requirements Coverage）**

```
カバレッジ = テスト済み要件 / 総要件数 × 100%

例:
機能要件: 50個
テストケース作成済み: 45個
要件カバレッジ = 45/50 = 90%
```

**トレーサビリティマトリクス**:

| 要件ID | 要件 | テストケースID | ステータス |
|--------|------|--------------|----------|
| REQ-001 | ユーザーログイン | TC-010, TC-011 | ✅ Pass |
| REQ-002 | パスワードリセット | TC-020 | ✅ Pass |
| REQ-003 | 2要素認証 | - | ❌ 未実装 |

**リスクカバレッジ（Risk Coverage）**

```
高リスク領域のカバレッジ = 高リスク領域のテスト済み項目 / 高リスク領域の総項目 × 100%

目標: 高リスク領域 100%、中リスク 80%、低リスク 50%
```

#### 6.2 欠陥指標（Defect Metrics）

**欠陥密度（Defect Density）**

```
欠陥密度 = 欠陥数 / コード規模（KLOC: 1000行）

例:
欠陥数: 25件
コード: 50,000行（50 KLOC）
欠陥密度 = 25 / 50 = 0.5 件/KLOC

業界ベンチマーク:
- 優秀: < 0.5 件/KLOC
- 平均: 1-2 件/KLOC
- 要改善: > 3 件/KLOC
```

**欠陥除去効率（Defect Removal Efficiency / DRE）**

```
DRE = テスト工程で検出した欠陥 / 全欠陥 × 100%

全欠陥 = テスト工程欠陥 + 本番欠陥

例:
テスト工程: 80件
本番: 5件
DRE = 80 / (80 + 5) = 94.1%

目標: 95%以上（本番流出5%以下）
```

**欠陥流出率（Defect Leakage Rate）**

```
流出率 = 本番で検出された欠陥 / 全欠陥 × 100%
      = 100% - DRE

例: 本番5件、テスト80件
流出率 = 5 / 85 = 5.9%

目標: < 5%
```

**欠陥注入率（Defect Injection Rate）**

```
注入率 = 新規欠陥数 / 新規・変更コード行数（KLOC）

例:
スプリントで15件の欠陥
新規コード: 5,000行（5 KLOC）
注入率 = 15 / 5 = 3.0 件/KLOC
```

**平均修正時間（Mean Time To Repair / MTTR）**

```
MTTR = 総修正時間 / 修正した欠陥数

例:
10件の欠陥、合計修正時間40時間
MTTR = 40 / 10 = 4時間/件

重要度別MTTR目標:
- P0（Blocker）: < 4時間
- P1（Critical）: < 1営業日
- P2（Major）: < 3営業日
```

**欠陥エージング（Defect Aging）**

```
エージング = 現在日 - 欠陥報告日

古い欠陥の蓄積は品質負債

目標:
- P0/P1: 平均 < 2日
- P2: 平均 < 7日
- P3/P4: 平均 < 30日
```

#### 6.3 テスト効率指標

**テスト実行率（Test Execution Rate）**

```
実行率 = 実行したテストケース / 計画テストケース × 100%

例:
計画: 500件
実行: 450件
実行率 = 450 / 500 = 90%

目標: リリース前100%
```

**テストPass率（Test Pass Rate）**

```
Pass率 = Passしたテストケース / 実行テストケース × 100%

例:
実行: 450件
Pass: 425件
Fail: 20件
Blocked: 5件
Pass率 = 425 / 450 = 94.4%

目標: リリース判定時 > 95%
```

**自動化率（Test Automation Rate）**

```
自動化率 = 自動化テストケース / 全テストケース × 100%

例:
全テストケース: 800件
自動化: 500件
手動: 300件
自動化率 = 500 / 800 = 62.5%

目標: 70-80%（ピラミッド型では高くなる）
```

**テスト生産性（Test Productivity）**

```
生産性 = テストケース作成数 / 工数（人日）

例:
1スプリント（2週間）でテストケース50件作成
工数: QA 2人 × 10日 = 20人日
生産性 = 50 / 20 = 2.5 件/人日

ベンチマーク: 2-5件/人日（複雑性による）
```

**テスト実行時間**

```
全自動テスト実行時間（CI/CDパイプライン）

目標:
- Unit Tests: < 5分
- Integration Tests: < 20分
- E2E Tests (Smoke): < 10分
- Full E2E Suite: < 2時間
```

#### 6.4 品質トレンド分析

**欠陥発見曲線（Defect Discovery Curve）**

```
時系列での新規欠陥検出数をプロット

理想的曲線:
テスト初期: 高い検出率（多数の欠陥発見）
テスト中期: 減少
テスト後期: 低い（収束）

収束判定:
- 新規欠陥 < 修正欠陥（連続1週間）
- 新規欠陥 < 5件/週（P0/P1は0件）
```

**欠陥バーンダウン（Defect Burndown）**

```
Openな欠陥数の推移

縦軸: Open欠陥数
横軸: 時間（日）

リリース判定:
- P0/P1: 0件
- P2: ≤ 5件
- トレンド: 減少傾向
```

**グラフ例**:
```
Open欠陥数
100 |     /\
 80 |    /  \___
 60 |   /       \___
 40 |  /            \___
 20 | /                 \___
  0 |________________________
    Week 1  2  3  4  5  6  7

理想: Week 6-7で0に近づく
```

**欠陥トレンド分析指標**:

```
週次比較:
- 新規欠陥数: 今週 vs 先週
- 修正欠陥数
- 再発欠陥数（Reopened）
- Open欠陥数変化

アラート条件:
- 新規欠陥 > 修正欠陥（連続2週間）
- P0/P1の増加
- 再発率 > 10%
```

#### 6.5 リリース判定基準（Go/No-Go Criteria）

**定量的基準テンプレート**:

```markdown
## リリース判定基準

### 必須条件（Go条件）

**欠陥基準**:
- [ ] P0（Blocker）欠陥: 0件
- [ ] P1（Critical）欠陥: 0件
- [ ] P2（Major）欠陥: ≤ 5件
- [ ] 新規欠陥 < 修正欠陥（直近1週間）

**テスト基準**:
- [ ] テスト実行率: 100%
- [ ] テストPass率: ≥ 95%
- [ ] Smoke Tests: 100% Pass
- [ ] Regression Tests: 100% Pass
- [ ] 要件カバレッジ: 100%

**コード品質**:
- [ ] コードカバレッジ: ≥ 80%（Unit）
- [ ] SonarQube Quality Gate: Pass
- [ ] セキュリティスキャン: Critical脆弱性 0件

**非機能要件**:
- [ ] Performance Tests: Pass（SLO達成）
- [ ] Load Tests: 目標負荷達成
- [ ] セキュリティテスト: Pass

**承認**:
- [ ] QAリード承認
- [ ] 開発マネージャー承認
- [ ] プロダクトオーナー承認

### No-Go条件（リリース延期）

以下1つでも該当すればリリース延期:
- P0/P1欠陥が存在
- テストPass率 < 90%
- Critical セキュリティ脆弱性
- 性能要件未達成（SLO違反）
```

#### 6.6 ダッシュボード設計

**品質ダッシュボード構成**:

**セクション1: 概要（Overview）**
- リリース可否判定（Go/No-Go）
- 品質スコア（0-100点）
- アラート数

**セクション2: テスト実行**
- テスト実行率（円グラフ）
- テストPass率（トレンドグラフ）
- 自動化率

**セクション3: 欠陥**
- Open欠陥数（重要度別積み上げグラフ）
- 欠陥バーンダウン（折れ線グラフ）
- 平均修正時間（棒グラフ）

**セクション4: カバレッジ**
- コードカバレッジ（ゲージ）
- 要件カバレッジ（進捗バー）
- リスクカバレッジ（マトリクス）

**セクション5: トレンド**
- 欠陥発見曲線
- テスト実行時間推移
- 欠陥密度推移

**ツール**:
- Grafana + Prometheus（メトリクス収集・可視化）
- Datadog（APM統合）
- TestRail（テスト管理）
- Jira Dashboard（チケット統合）

**参考文献・リソース**:
- 書籍: "Software Quality: Concepts and Practice" - Daniel Galin (2018)
- 書籍: "Metrics and Models in Software Quality Engineering" - Stephen H. Kan (2002)
- 書籍: "Accelerate" - Nicole Forsgren, Jez Humble, Gene Kim (2018) ← DORA Metrics
- 記事: "SPACE Framework" - GitHub/Microsoft Research (2021)
- サイト: ISO/IEC 25010（SQuaRE品質モデル）

---

### 7. 非機能テスト（Non-Functional Testing / NFT）

**分類**: 非機能要件検証系

**出典・背景**:
ISO/IEC 25010（SQuaRE品質モデル）で体系化されています。パフォーマンステストは「The Art of Application Performance Testing」（Ian Molyneaux, 2009）、セキュリティテストはOWASP（Open Web Application Security Project）が標準化しました。システムの「何をするか」ではなく「どのように動作するか」を検証します。

**理論の詳細**:

#### 7.1 パフォーマンステスト（Performance Testing）

**定義**: システムの応答性、スループット、リソース使用率を測定。

**テストタイプ**:

**1. Load Testing（負荷テスト）**

**目的**: 通常・ピーク負荷での性能確認

**シナリオ例**:
```
通常時負荷: 100 VUs（Virtual Users）
ピーク負荷: 500 VUs
期間: 30分

評価指標:
- Response Time p95 < 500ms
- Throughput > 1000 req/sec
- Error Rate < 1%
```

**k6スクリプト例**:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp-up: 0→100 VUs
    { duration: '20m', target: 100 },  // Stay: 100 VUs
    { duration: '5m', target: 500 },   // Peak: 100→500 VUs
    { duration: '10m', target: 500 },  // Peak持続
    { duration: '5m', target: 0 },     // Ramp-down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500'], // 95%が500ms以内
    'http_req_failed': ['rate<0.01'],   // エラー率1%未満
  },
};

export default function() {
  let res = http.get('https://api.example.com/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1); // Think Time（ユーザーの考慮時間）
}
```

**2. Stress Testing（ストレステスト）**

**目的**: 限界を超える負荷で障害挙動確認

**シナリオ**:
```
負荷: 通常の2-3倍以上
期間: 限界まで増加

確認事項:
- いつシステムが限界に達するか
- どのように障害するか（Graceful Degradation）
- 回復するか（復旧時間）
```

**3. Spike Testing（スパイクテスト）**

**目的**: 突発的な負荷増加への耐性確認

**シナリオ**:
```
通常: 100 VUs
突然: 1000 VUs（瞬時に増加）
期間: 5分間維持
→ 100 VUsに戻る

例: Flash Sale、ニュース記事バズ
```

**4. Soak Testing / Endurance Testing（長時間テスト）**

**目的**: 長時間稼働でのメモリリーク、リソース枯渇検出

**シナリオ**:
```
負荷: 通常負荷
期間: 12-24時間以上

監視:
- メモリ使用量（増加し続けないか）
- CPU使用率（安定しているか）
- データベースコネクション（リーク）
```

**パフォーマンステストの指標**:

**Response Time（応答時間）**:
```
- Average（平均）: 全体の平均、外れ値に影響されやすい
- Median (p50): 中央値、より現実的
- p90: 90%のリクエストがこの値以下
- p95: 95%のリクエストがこの値以下（SLO設定に使用）
- p99: 99%のリクエストがこの値以下
- Max: 最大値

目標例:
- API: p95 < 200ms, p99 < 500ms
- Webページ: p95 < 1s, p99 < 2s
```

**Throughput（スループット）**:
```
単位時間あたりの処理数
- req/sec（リクエスト/秒）
- TPS（Transactions Per Second）

目標例:
- API: 1000 req/sec
- Eコマース: 500 TPS（チェックアウト）
```

**Error Rate（エラー率）**:
```
エラー率 = エラー数 / 総リクエスト数 × 100%

目標: < 1%（通常負荷）、< 5%（ピーク負荷）
```

**Resource Utilization（リソース使用率）**:
```
- CPU使用率: < 70%（余裕を持たせる）
- メモリ使用率: < 80%
- ディスクI/O
- ネットワーク帯域
```

**パフォーマンステストツール比較**:

| ツール | 特徴 | スクリプト言語 | 学習曲線 | CI統合 |
|--------|------|--------------|---------|--------|
| k6 | モダン、開発者向け、JS | JavaScript | 低 | ⭐⭐⭐⭐⭐ |
| Gatling | Scala、高性能、レポート綺麗 | Scala/Java | 中 | ⭐⭐⭐⭐ |
| JMeter | 老舗、GUI、多機能 | XML（GUI） | 中 | ⭐⭐⭐ |
| Locust | Python、分散負荷 | Python | 低 | ⭐⭐⭐⭐ |
| Artillery | Node.js、シンプル | YAML/JS | 低 | ⭐⭐⭐⭐ |

**推奨**: k6（開発者向け、CI統合）、JMeter（非エンジニアQA向け）

#### 7.2 セキュリティテスト（Security Testing）

**定義**: 脆弱性、セキュリティリスクの検出。

**テストタイプ**:

**1. 脆弱性スキャン（Vulnerability Scanning）**

**OWASP Top 10（2021）**:

1. **A01: Broken Access Control（アクセス制御の不備）**
   - テスト: 認証なしでAPIアクセス、他ユーザーのデータ取得試行
   - 例: `/api/users/123/orders` → `/api/users/124/orders`（他人の注文）

2. **A02: Cryptographic Failures（暗号化の失敗）**
   - テスト: HTTP通信、平文パスワード保存、弱い暗号化
   - 確認: HTTPS強制、bcrypt/Argon2使用、TLS 1.2以上

3. **A03: Injection（インジェクション）**
   - **SQL Injection**: `' OR '1'='1`入力、Prepared Statement使用確認
   - **XSS**: `<script>alert('XSS')</script>`入力、エスケープ確認
   - **Command Injection**: `; rm -rf /`等

4. **A04: Insecure Design（安全でない設計）**
   - レビュー: 脅威モデリング（STRIDE）、設計フロー検証

5. **A05: Security Misconfiguration（セキュリティ設定ミス）**
   - テスト: デフォルトパスワード、不要なサービス、Stack Traceの公開

6. **A06: Vulnerable and Outdated Components（脆弱な古いコンポーネント）**
   - スキャン: `npm audit`, `snyk`, `OWASP Dependency-Check`
   - CI統合: 脆弱性検出で失敗

7. **A07: Identification and Authentication Failures（認証の失敗）**
   - テスト: ブルートフォース攻撃、弱いパスワード許容、セッション管理

8. **A08: Software and Data Integrity Failures（ソフトウェアとデータの整合性）**
   - テスト: 署名なしアップデート、CI/CDパイプライン改ざん

9. **A09: Security Logging and Monitoring Failures（ログとモニタリングの不足）**
   - 確認: 重要イベント（ログイン失敗、権限昇格）のログ記録

10. **A10: Server-Side Request Forgery（SSRF）**
    - テスト: 内部ネットワークへのリクエスト強制

**脆弱性スキャンツール**:

```bash
# OWASP ZAP (Zed Attack Proxy)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://example.com \
  -r zap_report.html

# Nikto (Webサーバースキャナー)
nikto -h https://example.com

# npm audit
npm audit --audit-level=high

# Snyk
snyk test
snyk monitor  # 継続監視
```

**2. ペネトレーションテスト（Penetration Testing / Pen Test）**

**定義**: 実際の攻撃をシミュレートし、脆弱性を悪用可能か検証。

**フェーズ**:
1. **偵察（Reconnaissance）**: 情報収集
2. **スキャン（Scanning）**: ポート、サービス、脆弱性スキャン
3. **悪用（Exploitation）**: 脆弱性攻撃
4. **権限昇格（Privilege Escalation）**: 管理者権限取得試行
5. **報告（Reporting）**: 発見事項、修正推奨

**実施方法**:
- **ホワイトボックス**: 内部情報あり（コード、構成）
- **ブラックボックス**: 情報なし（外部攻撃者視点）
- **グレーボックス**: 部分的情報あり

**ツール**:
- **Burp Suite**: Webアプリペンテスト（有料Pro版推奨）
- **Metasploit**: エクスプロイトフレームワーク
- **Nmap**: ネットワークスキャン

**3. 認証・認可テスト**

**テストケース例**:
```
[ ] ログイン試行回数制限（5回で一時ロック）
[ ] パスワードポリシー（8文字以上、複雑性）
[ ] セッションタイムアウト（30分）
[ ] セッション固定攻撃対策（ログイン後セッションID再生成）
[ ] CSRF対策（トークン検証）
[ ] JWT署名検証（改ざん検知）
[ ] 水平権限昇格（他ユーザーのリソース取得試行）
[ ] 垂直権限昇格（一般ユーザー→管理者機能アクセス試行）
```

**4. API セキュリティテスト**

**OWASP API Security Top 10（2023）**:
1. Broken Object Level Authorization（オブジェクトレベル認可の不備）
2. Broken Authentication（認証の不備）
3. Broken Object Property Level Authorization（プロパティレベル認可の不備）
4. Unrestricted Resource Consumption（リソース消費制限なし）
5. Broken Function Level Authorization（機能レベル認可の不備）

**テストツール**:
- **Postman**: 手動APIテスト
- **OWASP ZAP**: APIスキャン
- **Burp Suite**: APIリクエスト改ざん

**セキュリティCI/CD統合**:

```yaml
# GitHub Actions
- name: Run OWASP Dependency Check
  run: |
    docker run --rm -v $(pwd):/src owasp/dependency-check \
      --scan /src --format HTML --out /src/dependency-check-report

- name: Snyk Security Scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high

- name: Trivy Container Scan
  run: |
    trivy image --severity HIGH,CRITICAL myapp:latest
```

#### 7.3 ユーザビリティテスト（Usability Testing）

**定義**: システムの使いやすさ、ユーザー満足度を評価。

**評価指標**:

**1. System Usability Scale (SUS)**

**定義**: 10問のアンケートで0-100点評価。

**質問例（5段階評価: 1=全く同意しない、5=強く同意する）**:
1. このシステムを頻繁に使いたい
2. システムは不必要に複雑だ（逆転項目）
3. システムは使いやすい
4. 使用するには技術サポートが必要だ（逆転項目）
5. 様々な機能がよく統合されている
...（10問）

**スコア計算**:
```
奇数項目: (評価 - 1)
偶数項目: (5 - 評価)
合計 × 2.5 = SUSスコア（0-100点）

評価:
- 80点以上: Excellent
- 68-79点: Good（平均68点）
- 51-67点: OK
- 50点以下: Poor
```

**2. タスク成功率（Task Success Rate）**

```
成功率 = 成功したタスク / 総タスク試行数 × 100%

例:
5人のユーザー、各3タスク（計15試行）
成功: 12回
成功率 = 12 / 15 = 80%

目標: > 90%
```

**3. タスク完了時間（Time on Task）**

```
平均完了時間 = 総完了時間 / 成功タスク数

例:
「商品購入」タスク
10人、平均120秒

ベンチマーク比較: 競合サービス vs 自社
```

**4. エラー率（Error Rate）**

```
エラー率 = エラー発生数 / タスク試行数 × 100%

例:
15試行、5回エラー（間違ったボタンクリック等）
エラー率 = 5 / 15 = 33%

目標: < 10%
```

**ユーザビリティテスト手法**:

**1. モデレート型ユーザビリティテスト**
- 対面でタスク実施観察
- Think Aloud（思考発話法）: ユーザーが考えを声に出す
- 5-8人で80%の問題発見（Nielsen Norman Group）

**2. リモートユーザビリティテスト**
- ツール: UserTesting.com、Lookback、Zoom
- 録画で後から分析

**3. A/Bテスト**
- 2つのデザイン比較
- 定量的評価（コンバージョン率等）

**4. アクセシビリティテスト（Accessibility Testing）**

**WCAG 2.1（Web Content Accessibility Guidelines）**:

**レベル**:
- **A**: 最低限（例: 画像にalt属性）
- **AA**: 推奨（例: コントラスト比4.5:1以上）
- **AAA**: 最高（例: コントラスト比7:1以上）

**4原則（POUR）**:
1. **Perceivable（知覚可能）**: 情報・UIを知覚できる
2. **Operable（操作可能）**: キーボードのみで操作可能
3. **Understandable（理解可能）**: 情報・操作が理解可能
4. **Robust（堅牢）**: 支援技術（スクリーンリーダー）で利用可能

**テスト項目例**:
```
[ ] キーボード操作（Tab、Enter、Escapeのみで全機能使用）
[ ] スクリーンリーダー対応（NVDA、JAWSで読み上げ）
[ ] コントラスト比（WCAG AA: 4.5:1以上）
[ ] フォーカスインジケーター（どこにフォーカスあるか明確）
[ ] alt属性（画像の代替テキスト）
[ ] 動画に字幕
```

**ツール**:
- **axe DevTools**: ブラウザ拡張、自動検出
- **Lighthouse**: Chrome DevTools、アクセシビリティスコア
- **Pa11y**: CIで自動チェック
- **NVDA / JAWS**: スクリーンリーダー

**実装例（axe-core + Jest）**:
```javascript
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('page should have no accessibility violations', async () => {
  const { container } = render(<MyPage />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

**参考文献・リソース**:
- 書籍: "The Art of Application Performance Testing" - Ian Molyneaux (2009)
- 書籍: "Web Application Security" - Andrew Hoffman (2020)
- 書籍: "Don't Make Me Think" - Steve Krug (2014) ← ユーザビリティ
- 標準: WCAG 2.1（W3C）
- サイト: OWASP.org（セキュリティベストプラクティス）
- ツール: k6.io、OWASP ZAP、axe-core

---

## フレームワーク選択ガイド

| 状況・課題 | 推奨フレームワーク | 理由 |
|-----------|------------------|------|
| テスト戦略立案 | テストピラミッド、アジャイルテスト4象限 | バランスの取れたテストカバレッジ |
| リソース制約 | リスクベーステスト | 重要領域に集中、ROI最大化 |
| 効率的テスト設計 | 同値分割、境界値分析、ペアワイズ法 | 少数で高カバレッジ |
| 複雑な条件テスト | デシジョンテーブル、状態遷移テスト | 網羅的、漏れ防止 |
| テスト自動化 | Page Object Model、Data-Driven Testing | 保守性、再利用性向上 |
| CI/CD統合 | 自動化戦略、パイプライン設計 | 継続的品質保証 |
| 品質可視化 | 品質指標、KPI、ダッシュボード | データ駆動の意思決定 |
| リリース判定 | リリース判定基準、欠陥トレンド分析 | 客観的判断 |
| 性能問題 | Load Testing、Stress Testing | ボトルネック特定 |
| セキュリティ懸念 | OWASP Top 10、脆弱性スキャン | リスク軽減 |
| ユーザー満足度 | SUS、ユーザビリティテスト | UX改善 |

---

## フレームワーク統合例

### ケース: Webアプリケーションの包括的QA戦略

**Phase 1: テスト戦略策定（Week 1-2）**

1. **リスクベーステスト**: 機能ごとのリスク評価
   - 決済機能: High Risk → 徹底的テスト
   - レポート: Medium Risk → 標準テスト
   - UI配色: Low Risk → 最小限

2. **テストピラミッド**: テストレベル配分決定
   - Unit Tests: 70%（500件）
   - Integration Tests: 20%（150件）
   - E2E Tests: 10%（50件）

3. **アジャイルテスト4象限**: テストタイプ網羅確認
   - Q1: Unit Tests（JUnit）
   - Q2: BDD Tests（Cucumber）
   - Q3: 探索的テスト（セッションベース）
   - Q4: Performance Tests（k6）、Security Tests（OWASP ZAP）

**Phase 2: テスト設計（Week 3-4）**

1. **境界値分析**: 決済金額入力（0円、上限、上限+1）
2. **デシジョンテーブル**: 割引ルール（会員種別×購入金額）
3. **ペアワイズ法**: ブラウザ互換性テスト（Browser×OS×言語）

**Phase 3: 自動化実装（Week 5-8）**

1. **Page Object Model**: UIテストの保守性向上
   ```
   /pages
     ├── LoginPage.ts
     ├── ProductListPage.ts
     └── CheckoutPage.ts
   ```

2. **Data-Driven Testing**: 複数データセットでログインテスト
   ```javascript
   testData.forEach(({ username, password, expected }) => {
     test(`login with ${username}`, async () => { ... });
   });
   ```

3. **CI/CD統合**: GitHub Actions
   ```
   Commit → Unit Tests (5分)
          → Integration Tests (20分)
          → E2E Smoke Tests (10分)
          → Deploy Staging
          → Full E2E Suite (60分)
   ```

**Phase 4: 実行と測定（Week 9以降）**

1. **品質指標収集**:
   - コードカバレッジ: 82%（目標80%達成）
   - テストPass率: 94%
   - 欠陥密度: 0.8件/KLOC

2. **欠陥トレンド分析**:
   - 欠陥バーンダウン: 収束傾向確認
   - P0/P1: 0件（リリース可能）

3. **非機能テスト**:
   - Load Test: p95 < 300ms（目標200ms、要改善）
   - Security Scan: Critical 0件、High 3件（修正後再スキャン）
   - SUS スコア: 72点（Good）

**Phase 5: リリース判定**

リリース判定基準チェック:
- [x] P0/P1欠陥: 0件
- [x] テスト実行率: 100%
- [x] テストPass率: 95%達成
- [x] コードカバレッジ: 82%（≥80%）
- [ ] Performance SLO: 未達成 → 改善タスク登録、リリースは承認

**判定**: Go（パフォーマンス改善は次スプリント対応）

---

## 参考文献・リソース

### 必読書籍

1. **"Agile Testing: A Practical Guide for Testers and Agile Teams"** - Lisa Crispin, Janet Gregory (2009)
   - アジャイルテストの決定版、4象限

2. **"Testing Computer Software"** - Cem Kaner, Jack Falk, Hung Q. Nguyen (1999, 2nd Ed.)
   - テスト技法の古典的名著

3. **"The Art of Software Testing"** - Glenford Myers, Corey Sandler, Tom Badgett (2011, 3rd Ed.)
   - テスト設計技法の基礎

4. **"Lessons Learned in Software Testing"** - Cem Kaner, James Bach, Bret Pettichord (2001)
   - 293のテストレッスン

5. **"Continuous Delivery"** - Jez Humble, David Farley (2010)
   - CI/CD、自動化戦略

6. **"Explore It!"** - Elisabeth Hendrickson (2013)
   - 探索的テストの実践

7. **"Software Testing Techniques"** - Boris Beizer (1990)
   - ホワイトボックステスト、カバレッジ

### 国際標準・認定

- **ISTQB (International Software Testing Qualifications Board)**
  - Foundation Level、Advanced Level、Agile Tester
  - シラバス: テスト技法、プロセス標準

- **ISO/IEC/IEEE 29119（ソフトウェアテスト標準）**
  - Part 1: 概念と定義
  - Part 2: テストプロセス
  - Part 3: テストドキュメント
  - Part 4: テスト技法

- **ISO/IEC 25010（SQuaRE品質モデル）**
  - 非機能要件（性能、セキュリティ、ユーザビリティ等）

### オンラインリソース

- **Ministry of Testing**: ministryoftesting.com（テストコミュニティ、ブログ）
- **OWASP**: owasp.org（セキュリティテスト）
- **Test Automation University**: testautomationu.applitools.com（無料コース）
- **Martin Fowler's Testing Guide**: martinfowler.com/testing/
- **Google Testing Blog**: testing.googleblog.com

### ツール・フレームワーク

**テスト管理**:
- TestRail、Zephyr、qTest、Jira（Xray）

**Unit Testing**:
- JUnit（Java）、pytest（Python）、Jest（JavaScript）、NUnit（C#）

**API Testing**:
- Postman、REST Assured、Karate、Pact（Contract Testing）

**UI Testing**:
- Playwright、Selenium、Cypress、Appium（Mobile）

**Performance**:
- k6、Gatling、JMeter、Locust

**Security**:
- OWASP ZAP、Burp Suite、Snyk、Trivy

**Code Coverage**:
- JaCoCo（Java）、Coverage.py（Python）、Istanbul（JavaScript）

**CI/CD**:
- GitHub Actions、GitLab CI、Jenkins、CircleCI

### カンファレンス

- **STAREAST / STARWEST**: 北米最大級のテストカンファレンス
- **EuroSTAR**: 欧州最大のテストカンファレンス
- **Agile Testing Days**: アジャイルテスト特化
- **TestBash**: Ministry of Testingのグローバルイベント

---

このドキュメントは、QAテストストラテジストオーケストレーターが統合している主要フレームワークの詳細解説です。各フレームワークは、テスト戦略立案から実行、品質測定まで全フェーズをカバーし、効率的で効果的なソフトウェア品質保証を支援します。
