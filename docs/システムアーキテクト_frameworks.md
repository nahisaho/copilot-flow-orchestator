# システムアーキテクト - フレームワーク・理論詳細

## 概要

システムアーキテクチャは、ビジネス要件を満たしながら、スケーラブルで保守性が高く、安全なシステムを設計する専門領域です。このオーケストレーターは、アーキテクチャパターン、分散システム設計、セキュリティアーキテクチャ、クラウドネイティブ設計など、現代的なシステム構築に必要な実証済みのフレームワークと設計原則を統合しています。

ビジネス価値との整合性、技術的トレードオフの明確化、長期的な進化可能性を重視し、持続可能なシステムアーキテクチャを実現します。

---

## 組み込まれているフレームワーク・理論

### 1. C4モデル（C4 Model for Software Architecture）

**分類**: アーキテクチャ可視化・コミュニケーション系

**出典・背景**:
Simon Brown が2006年頃に開発し、書籍「Software Architecture for Developers」(2012年)で体系化しました。UMLの複雑さに対するアンチテーゼとして、シンプルで理解しやすいアーキテクチャ図を提供します。Google Mapのズームイン/アウトのメタファーで、異なる抽象度でシステムを可視化します。

**理論の詳細**:

**4つの抽象レベル**:

**レベル1: System Context Diagram（システムコンテキスト図）**
- **対象読者**: 全員（非技術者含む）
- **目的**: システムの境界と外部との関係を理解
- **含む要素**:
  - 対象システム（1つの箱）
  - ユーザー・ペルソナ（人型アイコン）
  - 外部システム（箱）
  - 相互作用の線と説明
- **例**: 「Eコマースシステム」→「顧客」「配送業者API」「決済サービス」との関係

**レベル2: Container Diagram（コンテナ図）**
- **対象読者**: 開発者、運用チーム
- **目的**: 主要な技術構成要素を理解
- **含む要素**:
  - Webアプリケーション（例: React SPA）
  - モバイルアプリ（例: iOS/Android）
  - バックエンドAPI（例: Spring Boot REST API）
  - データベース（例: PostgreSQL）
  - メッセージブローカー（例: RabbitMQ）
  - ストレージ（例: S3）
- **コンテナの定義**: 個別に実行/デプロイされるアプリケーションまたはデータストア
- **例**: 「Webアプリ」→「API Server」→「Database」+ 「Redis Cache」

**レベル3: Component Diagram（コンポーネント図）**
- **対象読者**: 開発者
- **目的**: コンテナ内部の構造を理解
- **含む要素**:
  - コンポーネント（例: OrderController、PaymentService、ProductRepository）
  - コンポーネント間の依存関係
  - 技術的詳細（フレームワーク、ライブラリ）
- **例**: API Serverコンテナ内の「Controllers」「Services」「Repositories」層

**レベル4: Code Diagram（コード図）**
- **対象読者**: 開発者（詳細実装）
- **目的**: クラス・メソッドレベルの設計
- **含む要素**:
  - UMLクラス図、ERD等（必要に応じて）
- **注**: C4モデルではオプション、IDEで自動生成可能なため省略可能

**C4モデルの原則**:

1. **抽象化の一貫性**: 各レベルで適切な抽象度を保つ（混ぜない）
2. **シンプルさ**: 箱と線のみ、UMLの複雑な記法は使わない
3. **ズーム可能**: 上位レベルから詳細レベルへドリルダウン
4. **技術非依存**: レベル1-2は技術詳細を避ける
5. **凡例必須**: 各図に凡例を付ける（箱・線の意味を明示）

**記法**:
```
[Person: Label]
[Software System: Label]
[Container: Label] (technology)
[Component: Label]

→ 線に説明文（「uses」「reads from」等）
```

**実用例**:
- **Netflix**: マイクロサービスアーキテクチャの可視化
- **Spotify**: チーム間のシステム境界理解
- **金融機関**: 規制当局への説明資料

**ツール**:
- Structurizr: C4モデル公式ツール（コードでダイアグラム生成）
- PlantUML: C4 PlantUML拡張
- Miro/Lucidchart: 手動作成

**参考文献・リソース**:
- 書籍: "Software Architecture for Developers" - Simon Brown (2012)
- サイト: c4model.com（公式サイト、豊富な例）
- ツール: Structurizr (structurizr.com)

---

### 2. マイクロサービスアーキテクチャ（Microservices Architecture）

**分類**: アーキテクチャパターン・分散システム系

**出典・背景**:
2011年頃からNetflix、Amazon等が実践開始。Martin Fowler と James Lewis が2014年の記事「Microservices」で定義を確立しました。モノリシックアーキテクチャの課題（巨大化、デプロイリスク、技術スタック固定）に対する解として発展しました。

**理論の詳細**:

**定義**:
独立してデプロイ可能な小さなサービス群として構築されたアーキテクチャスタイル。各サービスはビジネス機能を中心に構成され、軽量な通信メカニズム（通常HTTP/REST または メッセージング）で協調動作する。

**主要特性**:

**1. ビジネス機能による組織化**:
- 技術層（UI、ビジネスロジック、データ）ではなく、ビジネス機能（注文、決済、在庫）で分割
- Conway's Law: 組織構造がアーキテクチャに反映される

**2. 独立デプロイ可能**:
- サービスAの変更がサービスBに影響しない
- 独立したCI/CDパイプライン
- カナリアリリース、ブルーグリーンデプロイ可能

**3. 疎結合・高凝集**:
- サービス間は疎結合（インターフェースのみ依存）
- サービス内は高凝集（関連機能を1サービスに）

**4. 自律性**:
- 各サービスが独自のデータストアを持つ（Database per Service）
- 技術スタックの自由選択
- チームの自律的意思決定

**5. 障害の分離**:
- 1サービスの障害が全体に波及しない設計
- Circuit Breaker、Bulkhead パターン
- Graceful Degradation（段階的機能低下）

**設計原則**:

**サービス境界の設計**:
- **Domain-Driven Design（DDD）**: Bounded Context がサービス境界
- **サイズの目安**: 「2 Pizza Team」（5-7人で管理可能）
- **責務**: Single Responsibility Principle（SRP）

**API設計**:
- **API契約**: OpenAPI/Swagger で明確化
- **バージョニング**: 後方互換性の維持
- **API Gateway**: クライアント向け統一エントリーポイント

**データ管理**:
- **Database per Service**: 各サービスが専用DB
- **データ整合性**: Saga Pattern、Event Sourcing
- **結果整合性**: 即座に一貫性は保証されない（Eventual Consistency）

**サービス間通信**:
- **同期通信**: REST API、gRPC
- **非同期通信**: メッセージキュー（RabbitMQ、Kafka）、イベントバス
- **サービスディスカバリー**: Consul、Eureka、Kubernetes Service

**マイクロサービスのトレードオフ**:

**メリット**:
- **独立デプロイ**: 高速なリリースサイクル
- **技術多様性**: 適材適所の技術選択
- **スケーラビリティ**: サービス単位でスケール
- **障害分離**: 部分障害で全体停止しない
- **組織スケール**: チーム独立、並行開発

**デメリット**:
- **分散システムの複雑性**: ネットワーク遅延、部分障害
- **データ整合性**: 分散トランザクション困難
- **運用オーバーヘッド**: 多数のサービス管理、デプロイ
- **テスト複雑化**: 統合テスト、E2Eテスト困難
- **デバッグ困難**: 分散トレーシング必須

**いつマイクロサービスを選ぶか**:
- ✅ 大規模チーム（50人以上）
- ✅ 高頻度デプロイ（週複数回）
- ✅ ドメインが複雑で明確に分割可能
- ✅ 部分的な高スケーラビリティが必要
- ❌ 小規模チーム（< 10人）
- ❌ ドメインがシンプル
- ❌ トランザクション整合性が重要

**移行戦略**:
- **Strangler Fig Pattern**: モノリスから段階的に移行
- **Anti-Corruption Layer**: レガシーシステムとの境界

**実用例**:
- **Netflix**: 数百のマイクロサービス、1日数千デプロイ
- **Amazon**: 「Two Pizza Team」ルール、サービス指向アーキテクチャ
- **Uber**: 地理的分散、高スケーラビリティ
- **Spotify**: Squad単位で自律的開発

**参考文献・リソース**:
- 記事: "Microservices" - Martin Fowler, James Lewis (2014)
- 書籍: "Building Microservices" - Sam Newman (2021, 2nd Ed.)
- 書籍: "Microservices Patterns" - Chris Richardson (2018)
- サイト: microservices.io（パターンカタログ）

---

### 3. CAP定理（CAP Theorem）

**分類**: 分散システム理論・データ整合性系

**出典・背景**:
Eric Brewer（カリフォルニア大学バークレー校教授）が2000年のPODC会議で提唱。Seth Gilbert と Nancy Lynch が2002年に厳密な証明を発表しました。分散システム設計における根本的なトレードオフを示す定理で、NoSQLデータベース設計の理論的基盤となっています。

**理論の詳細**:

**3つの特性**:

**C - Consistency（一貫性）**:
- 定義: すべてのノードが同じタイミングで同じデータを見る
- 読み取りは必ず最新の書き込み結果を返す
- 例: 銀行口座残高（古いデータは許容不可）

**A - Availability（可用性）**:
- 定義: すべての要求が（成功または失敗の）応答を受け取る
- ノード障害があっても、他のノードがサービス提供
- 例: ソーシャルメディア（一部表示されないより、少し古くても表示）

**P - Partition Tolerance（分断耐性）**:
- 定義: ネットワーク分断が発生しても、システムは動作し続ける
- ノード間の通信障害があっても、各ノードは動作継続
- **注**: 分散システムではネットワーク分断は避けられない（必須）

**CAP定理の本質**:
```
分散システムでは、C、A、Pの3つのうち、
同時に2つまでしか保証できない。

ただし、Pは分散システムでは必須
→ 実質的には C か A の選択
```

**CP（一貫性＋分断耐性）**:
- ネットワーク分断時、一貫性を保つため一部ノードは応答を返さない
- 可用性を犠牲にする
- **例**: 
  - RDBMS（PostgreSQL、MySQL with synchronous replication）
  - HBase、MongoDB（デフォルト設定）
  - ZooKeeper、etcd
- **用途**: 金融取引、在庫管理、予約システム

**AP（可用性＋分断耐性）**:
- ネットワーク分断時、古いデータでも応答を返す（Eventual Consistency）
- 一貫性を犠牲にする（一時的に不整合）
- **例**:
  - Cassandra、DynamoDB
  - CouchDB、Riak
  - DNS
- **用途**: ソーシャルメディア、コンテンツ配信、ログ収集

**CA（一貫性＋可用性）**:
- ネットワーク分断がない前提（単一ノード、LAN内）
- 現実の分散システムでは実現不可
- **例**: 単一RDBMS（厳密には分散システムではない）

**PACELC定理（CAP定理の拡張）**:
Daniel Abadi が2010年に提唱。通常時（ネットワーク分断なし）のトレードオフも考慮。

```
if Partition (分断発生時):
    A (可用性) か C (一貫性) を選択
else (通常時):
    L (Latency/遅延) か C (一貫性) を選択
```

**例**:
- **PA/EL**: Cassandra（分断時は可用性、通常時は低遅延優先）
- **PC/EC**: HBase（分断時も通常時も一貫性優先、遅延増加）

**実用的な設計指針**:

**1. 要件に応じた選択**:
```
一貫性が重要（金融、予約） → CP
可用性が重要（SNS、分析） → AP
```

**2. 結果整合性（Eventual Consistency）**:
- AP選択時の現実解
- 一定時間後には整合性が取れる
- タイムウィンドウの許容範囲を定義

**3. 整合性レベルの調整**:
- Cassandraの例: Quorum（半数以上）、One（1ノード）、All（全ノード）
- 読み取り・書き込みごとに整合性レベル指定可能

**4. ハイブリッドアプローチ**:
- 重要データはCP、その他はAP
- 例: 在庫（CP）+ 商品レビュー（AP）

**実用例**:

**例1: Amazon DynamoDB（AP）**
- 高可用性優先（24/7稼働）
- 結果整合性デフォルト、強整合性もオプション
- ショッピングカート、セッション管理等

**例2: Google Spanner（CP寄り）**
- グローバル分散しながら強一貫性
- TrueTimeでクロック同期
- 金融トランザクション等

**例3: Netflix（AP）**
- 可用性最優先（視聴体験の継続）
- 一時的な不整合許容（視聴履歴の遅延同期等）

**誤解の解消**:
- CAP定理は「3つから2つ選ぶ」ではなく、「Pは必須、CとAはトレードオフ」
- 0か1かではなく、グラデーション（どの程度一貫性/可用性を重視するか）
- 分断は稀だが、発生時の挙動を設計時に決める必要がある

**参考文献・リソース**:
- 論文: "Towards Robust Distributed Systems" - Eric Brewer (2000)
- 論文: "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services" - Gilbert & Lynch (2002)
- 記事: "CAP Twelve Years Later: How the 'Rules' Have Changed" - Eric Brewer (2012)
- 記事: "Problems with CAP, and Yahoo's little known NoSQL system" - Daniel Abadi (PACELC) (2010)

---

### 4. ドメイン駆動設計（Domain-Driven Design / DDD）

**分類**: ソフトウェア設計・モデリング系

**出典・背景**:
Eric Evans が2003年の著書「Domain-Driven Design: Tackling Complexity in the Heart of Software」で体系化しました。複雑なビジネスドメインを持つソフトウェアの設計手法として、ビジネスとエンジニアリングの橋渡しをする実践的アプローチです。

**理論の詳細**:

**核心概念**:
ソフトウェアの価値はドメイン（ビジネス領域）にある。技術ではなくドメインモデルを中心に設計し、ドメインエキスパートと開発者が共通言語（Ubiquitous Language）でコミュニケーションする。

**戦略的設計（Strategic Design）**:

**1. Ubiquitous Language（ユビキタス言語）**:
- ドメインエキスパートと開発者が共有する言葉
- コード、ドキュメント、会話で一貫して使用
- 曖昧さを排除、誤解を防ぐ
- **例**: 「User」ではなく「Customer」「Merchant」と区別

**2. Bounded Context（境界づけられたコンテキスト）**:
- 特定のドメインモデルが適用される明確な境界
- コンテキスト内では用語の意味が一意
- 異なるコンテキストでは同じ用語が異なる意味を持つ可能性
- **例**: 
  - 販売コンテキスト: 「Product」= 販売商品
  - 配送コンテキスト: 「Product」= 配送物
  - 在庫コンテキスト: 「Product」= 在庫品

**3. Context Map（コンテキストマップ）**:
- Bounded Context間の関係を可視化
- 統合パターン:
  - **Shared Kernel**: 共通のモデル共有
  - **Customer-Supplier**: 上流・下流関係
  - **Conformist**: 下流が上流に従う
  - **Anti-Corruption Layer（ACL）**: 変換層で境界保護
  - **Open Host Service**: 公開APIで統合
  - **Published Language**: 共通フォーマット（JSON Schema等）

**4. マイクロサービスとの関係**:
- Bounded Context = マイクロサービスの境界
- 各サービスが独自のドメインモデルを持つ

**戦術的設計（Tactical Design）**:

**Building Blocks（構成要素）**:

**1. Entity（エンティティ）**:
- 一意の識別子を持つオブジェクト
- ライフサイクル全体で同一性を保つ
- **例**: User (ID: 12345)、Order (注文番号: ORD-001)

**2. Value Object（値オブジェクト）**:
- 識別子を持たない、属性値のみで識別
- 不変（Immutable）
- **例**: Money (100, "USD")、Address ("東京都渋谷区...")、DateRange

**3. Aggregate（集約）**:
- 一貫性境界を持つEntity/Value Objectのクラスター
- Aggregate Root: 集約への唯一のエントリーポイント
- トランザクション境界 = 集約境界
- **例**: Order（Aggregate Root）+ OrderLineItems

**4. Repository（リポジトリ）**:
- 集約の永続化・取得を抽象化
- ドメインモデルをインフラから分離
- **例**: OrderRepository.findById(orderId)

**5. Domain Service（ドメインサービス）**:
- 複数の集約にまたがるビジネスロジック
- ステートレス
- **例**: PriceCalculationService（商品、クーポン、配送から価格計算）

**6. Domain Event（ドメインイベント）**:
- ドメイン内で発生した重要な出来事
- 疎結合な連携を実現
- **例**: OrderPlaced、PaymentCompleted

**レイヤードアーキテクチャ（DDDでの推奨構造）**:
```
Presentation Layer (UI)
    ↓
Application Layer (ユースケース、トランザクション境界)
    ↓
Domain Layer (ビジネスロジック、集約、ドメインサービス)
    ↓
Infrastructure Layer (DB、外部API、メッセージング)
```

**依存性の規則**: 外側→内側への依存のみ（ドメイン層は他に依存しない）

**DDDの適用場面**:

**適している**:
- ✅ 複雑なビジネスルール
- ✅ 長期的なプロジェクト（5年以上）
- ✅ ドメインエキスパートとの緊密な協働が可能
- ✅ 継続的なモデルの洗練が必要

**適していない**:
- ❌ シンプルなCRUD
- ❌ 短期プロジェクト
- ❌ ドメインエキスパート不在
- ❌ 技術主導のシステム（データパイプライン等）

**実用例**:

**例1: Eコマースドメイン**
```
Bounded Context:
- Sales Context: Order, Product, Customer
- Inventory Context: Stock, Warehouse
- Shipping Context: Shipment, DeliveryAddress

Aggregate例:
Order (Aggregate Root)
  - OrderId (Entity ID)
  - OrderLineItems (Entity collection)
  - ShippingAddress (Value Object)
  - TotalAmount (Value Object: Money)
```

**例2: 保険ドメイン**
```
Bounded Context:
- Underwriting Context: RiskAssessment, Premium
- Claims Context: Claim, ClaimItem
- Policy Context: Policy, Coverage

Domain Event:
PolicyIssued → ClaimSubmitted → ClaimApproved
```

**DDDとマイクロサービス統合**:
- Bounded Context境界 = サービス境界
- Domain Event = サービス間通信
- Anti-Corruption Layer = API Gateway、変換層

**参考文献・リソース**:
- 書籍: "Domain-Driven Design: Tackling Complexity in the Heart of Software" - Eric Evans (2003)
- 書籍: "Implementing Domain-Driven Design" - Vaughn Vernon (2013)
- 書籍: "Domain-Driven Design Distilled" - Vaughn Vernon (2016) ← コンパクト版
- 書籍: "Learning Domain-Driven Design" - Vlad Khononov (2021)

---

### 5. イベント駆動アーキテクチャ（Event-Driven Architecture / EDA）

**分類**: アーキテクチャパターン・非同期通信系

**出典・背景**:
1990年代のメッセージ指向ミドルウェア（MOM）から発展。Martin Fowler が2005年の記事「Event Sourcing」で概念整理。マイクロサービスの普及とともに2010年代に再注目されました。イベントを中心にシステムを構成し、疎結合で柔軟なアーキテクチャを実現します。

**理論の詳細**:

**核心概念**:
システム内で発生するイベント（状態変化、重要な出来事）を駆動力として、コンポーネントが非同期に反応・協調動作する。

**主要パターン**:

**1. Event Notification（イベント通知）**:
- **定義**: イベント発生を通知するだけ（最小限の情報）
- **内容**: イベントID、タイムスタンプ、何が起きたか
- **特徴**: 受信者が必要に応じて詳細情報を取得（Pull）
- **例**: 
  ```
  { "eventType": "OrderPlaced", "orderId": "12345", "timestamp": "2024-01-15T10:30:00Z" }
  ```
- **メリット**: 疎結合、送信者は受信者を知らない
- **デメリット**: 受信者が追加APIコールで詳細取得（依存関係残る）

**2. Event-Carried State Transfer（イベント担持状態転送）**:
- **定義**: イベントに状態変化の全データを含める
- **内容**: 変更された全属性値
- **特徴**: 受信者は追加クエリ不要、ローカルキャッシュ保持
- **例**:
  ```json
  {
    "eventType": "OrderPlaced",
    "orderId": "12345",
    "customer": { "id": "C001", "name": "田中太郎" },
    "items": [{"productId": "P100", "quantity": 2, "price": 1000}],
    "totalAmount": 2000,
    "timestamp": "2024-01-15T10:30:00Z"
  }
  ```
- **メリット**: 完全な疎結合、読み取りパフォーマンス向上
- **デメリット**: イベントサイズ大、データ重複、結果整合性

**3. Event Sourcing（イベントソーシング）**:
- **定義**: すべての状態変化をイベントとして永続化、現在状態はイベント再生で復元
- **特徴**:
  - イベントストア: 不変のイベントログ
  - 現在状態 = イベント列の累積適用
  - タイムトラベル: 任意時点の状態を復元可能
- **例**:
  ```
  Event Stream:
  1. OrderCreated (orderId: 123, customer: C001)
  2. ItemAdded (orderId: 123, productId: P100, qty: 2)
  3. OrderShipped (orderId: 123, trackingNo: TRK-456)
  
  現在のOrder状態 = イベント1→2→3を適用した結果
  ```
- **メリット**: 完全な監査証跡、デバッグ容易、時間旅行
- **デメリット**: 複雑性増加、イベントスキーマ進化の管理、パフォーマンス

**4. CQRS（Command Query Responsibility Segregation）**:
- **定義**: 読み取り（Query）と書き込み（Command）でモデル分離
- **構成**:
  - Write Model: コマンド処理、ビジネスルール検証
  - Read Model: クエリ最適化、非正規化ビュー
  - イベントで同期: Write→イベント発行→Read Modelを更新
- **メリット**: 読み書きの独立最適化、スケール戦略の分離
- **デメリット**: 結果整合性、複雑性
- **よく組み合わせ**: Event Sourcing + CQRS

**イベント駆動システムの構成要素**:

**1. Event Producer（イベント生成者）**:
- ドメインイベントを発行
- ビジネスロジック実行後に発行

**2. Event Channel（イベントチャネル）**:
- **Point-to-Point**: キュー（RabbitMQ、AWS SQS）
- **Pub/Sub**: トピック（Kafka、AWS SNS/SQS、Google Pub/Sub）
- **イベントストリーム**: Kafka、AWS Kinesis、Azure Event Hubs

**3. Event Consumer（イベント消費者）**:
- イベント受信、処理
- 複数の独立したコンシューマーが並行処理可能

**4. Event Store（イベントストア）**:
- イベントの永続化（Event Sourcingの場合）
- EventStoreDB、Kafka（ログ保持）

**メリット**:
- **疎結合**: プロデューサーとコンシューマー独立
- **スケーラビリティ**: コンシューマーを並列スケール
- **柔軟性**: 新機能は新コンシューマー追加のみ
- **非同期処理**: 高スループット、応答性向上
- **イベント駆動型リアクション**: リアルタイム処理

**デメリット**:
- **結果整合性**: 即座には一貫性取れない
- **デバッグ困難**: 非同期、分散トレーシング必須
- **イベント順序**: 順序保証の複雑性
- **障害処理**: リトライ、デッドレターキュー
- **イベントスキーマ進化**: バージョニング戦略必要

**実用パターン**:

**Saga Pattern（分散トランザクション）**:
- 複数サービスにまたがる長期トランザクション
- イベント連鎖で実現
- **Choreography**: イベント駆動で各サービスが自律的に反応
- **Orchestration**: 中央オーケストレーターが制御
- 補償トランザクション（Compensating Transaction）で ロールバック

**実用例**:

**例1: Eコマース注文処理（Saga）**
```
OrderPlaced (注文サービス)
  → PaymentProcessed (決済サービス) or PaymentFailed
      → InventoryReserved (在庫サービス) or ReservationFailed
          → OrderShipped (配送サービス)

失敗時:
PaymentFailed → OrderCancelled
ReservationFailed → PaymentRefunded → OrderCancelled
```

**例2: Netflix（イベントストリーミング）**
- ユーザー視聴イベント→リアルタイム分析→レコメンデーション更新
- 数百億イベント/日

**例3: Uber（Event Sourcing）**
- 配車リクエスト、位置更新、運賃計算すべてイベント
- 紛争解決、監査証跡に活用

**イベント設計のベストプラクティス**:

1. **イベント命名**: 過去形（OrderPlaced、PaymentCompleted）
2. **イベント粒度**: 粗すぎず細かすぎず、ドメインイベント単位
3. **イベント不変性**: 発行後は変更しない
4. **スキーマバージョニング**: Avro、Protobufでスキーマ管理
5. **べき等性**: 重複イベント処理しても問題ない設計
6. **順序保証**: 必要ならパーティションキー使用（Kafkaのパーティション）

**参考文献・リソース**:
- 記事: "What do you mean by 'Event-Driven'?" - Martin Fowler (2017)
- 書籍: "Designing Event-Driven Systems" - Ben Stopford (2018, O'Reilly, Kafka)
- 書籍: "Implementing Domain-Driven Design" - Vaughn Vernon (CQRS/Event Sourcing章)
- 書籍: "Microservices Patterns" - Chris Richardson (Saga Pattern)

---

### 6. サービスメッシュ（Service Mesh）

**分類**: マイクロサービス基盤・インフラ系

**出典・背景**:
Buoyant社がLinkerdを2016年にリリース、サービスメッシュという用語を普及させました。Google内部のTrafficDirector、Lyftの内製プロキシが起源。Istio（Google、IBM、Lyftの共同開発）が2017年にリリースされ、事実上の標準となりました。マイクロサービス間通信の複雑性をアプリケーションコードから分離します。

**理論の詳細**:

**定義**:
マイクロサービス間の通信を管理する専用インフラ層。アプリケーションコードに手を加えず、トラフィック管理、セキュリティ、可観測性を提供。

**アーキテクチャ**:

**1. Data Plane（データプレーン）**:
- **Sidecarプロキシ**: 各サービスポッドに併設されるプロキシ
- **役割**: 実際のトラフィック転送、ロードバランシング、暗号化、メトリクス収集
- **実装**: Envoy Proxy（最も一般的）、NGINX、Linkerd2-proxy

**2. Control Plane（コントロールプレーン）**:
- **役割**: Sidecarプロキシの設定管理、ポリシー配布
- **機能**: サービスディスカバリー、証明書管理、設定配信
- **実装**: Istio Pilot、Linkerd Controller

**主要機能**:

**1. トラフィック管理（Traffic Management）**:

**ロードバランシング**:
- ラウンドロビン、最小リクエスト、ランダム
- ゾーン/リージョン対応

**トラフィック分割**:
- カナリアリリース: 10%→30%→100%と段階的
- A/Bテスト: ヘッダーやユーザー属性で振り分け
- ブルーグリーンデプロイ

**リトライ・タイムアウト**:
- 自動リトライ（指数バックオフ）
- タイムアウト設定（サービス間SLA）

**Circuit Breaker**:
- 連続失敗で一時遮断、過負荷サービス保護
- Half-Open状態で回復確認

**2. セキュリティ（Security）**:

**mTLS（相互TLS認証）**:
- サービス間通信を自動暗号化
- 証明書の自動発行・ローテーション
- サービスIDベース認証

**認可ポリシー**:
- サービスAはサービスBを呼べる/呼べない
- Role-Based Access Control（RBAC）

**3. 可観測性（Observability）**:

**分散トレーシング**:
- リクエストの全経路追跡（Jaeger、Zipkin統合）
- レイテンシーのボトルネック特定

**メトリクス**:
- リクエスト数、レイテンシー、エラー率（Golden Signals）
- Prometheus統合

**アクセスログ**:
- すべてのサービス間通信記録

**4. レジリエンス（Resilience）**:
- Fault Injection: 意図的な障害注入でテスト
- Rate Limiting: リクエスト数制限
- Bulkhead: リソース分離で障害波及防止

**主要実装**:

**Istio**:
- 最も機能豊富、エンタープライズ向け
- Envoy Proxy（Data Plane）
- 豊富なトラフィック管理機能
- 学習曲線steep、リソース消費大

**Linkerd**:
- シンプル、軽量、高速
- Rust製プロキシ
- 初心者向け、生産準備済み（Production-ready）
- Istioより機能は少ないがシンプル

**Consul Connect**:
- HashiCorp製、Consulのサービスメッシュ機能
- 既存Consul利用者に最適

**AWS App Mesh**:
- AWSマネージドサービスメッシュ
- Envoyベース、ECS/EKS統合

**サービスメッシュのトレードオフ**:

**メリット**:
- **アプリコード不要**: 通信ロジックを分離、ポリグロット対応
- **統一された可観測性**: 全サービス一貫したメトリクス
- **セキュリティ標準化**: mTLSを全サービスに自動適用
- **トラフィック制御**: カナリア、A/Bテストが宣言的に実現

**デメリット**:
- **複雑性**: 新たなインフラ層、学習コスト
- **パフォーマンスオーバーヘッド**: プロキシの追加レイテンシー（1-3ms程度）
- **リソース消費**: 各ポッドにSidecar（メモリ50-100MB/プロキシ）
- **デバッグ複雑化**: ネットワークスタック増加

**いつサービスメッシュを導入すべきか**:

**導入すべき**:
- ✅ 多数のマイクロサービス（20以上）
- ✅ 複雑なサービス間通信
- ✅ mTLS必須（コンプライアンス）
- ✅ 高度なトラフィック管理（カナリア、A/B）
- ✅ Kubernetes環境

**不要な場合**:
- ❌ モノリス、少数サービス（< 10）
- ❌ シンプルな通信パターン
- ❌ リソース制約（エッジデバイス等）

**実用例**:

**例1: eBay（Istio）**
- 数千のマイクロサービス
- カナリアデプロイ、A/Bテスト
- mTLSで全通信暗号化

**例2: Nordstrom（Istio）**
- 小売ECサイト
- トラフィック管理、段階的ロールアウト

**例3: Airbnb**
- 独自サービスメッシュ→Istio移行検討

**サービスメッシュ vs API Gateway**:
- **API Gateway**: 外部→内部（North-South）
- **Service Mesh**: 内部↔内部（East-West）
- 併用が一般的

**参考文献・リソース**:
- 書籍: "Istio: Up and Running" - Lee Calcote, Zack Butcher (2019)
- 書籍: "The Enterprise Path to Service Mesh Architectures" - Lee Calcote (2018)
- サイト: servicemesh.io（パターン集）
- サイト: istio.io、linkerd.io（公式ドキュメント）

---

### 7. Infrastructure as Code（IaC）

**分類**: インフラ管理・自動化系

**出典・背景**:
2006年頃からの「Programmable Infrastructure」概念が起源。2011年のChef、Puppet普及、2014年のTerraform登場で確立。DevOpsムーブメントの中核技術として、インフラをコードで宣言的に管理する手法です。

**理論の詳細**:

**定義**:
インフラストラクチャの構成・プロビジョニング・管理をコード（設定ファイル）で定義し、自動化・バージョン管理・再現性を実現する。

**主要アプローチ**:

**1. 宣言的（Declarative）**:
- **特徴**: 「あるべき状態」を記述
- **ツール**: Terraform、CloudFormation、Pulumi
- **例**:
  ```hcl
  resource "aws_instance" "web" {
    ami           = "ami-12345678"
    instance_type = "t3.micro"
    count         = 3
  }
  ```
- **メリット**: 冪等性（何度実行しても同じ状態）、差分検出、状態管理

**2. 手続き的（Imperative）**:
- **特徴**: 「手順」を記述
- **ツール**: Ansible、Bash scripts
- **例**:
  ```yaml
  - name: Install nginx
    apt: name=nginx state=present
  - name: Start nginx
    service: name=nginx state=started
  ```
- **メリット**: 柔軟、複雑なロジック対応

**主要ツール**:

**Terraform（HashiCorp）**:
- **特徴**: マルチクラウド対応（AWS、Azure、GCP、Kubernetes等）
- **言語**: HCL（HashiCorp Configuration Language）
- **状態管理**: terraform.tfstateファイル（リモートバックエンド推奨）
- **ワークフロー**: init → plan → apply → destroy
- **例**:
  ```hcl
  provider "aws" {
    region = "ap-northeast-1"
  }
  
  resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"
    tags = { Name = "main-vpc" }
  }
  
  resource "aws_subnet" "public" {
    vpc_id     = aws_vpc.main.id
    cidr_block = "10.0.1.0/24"
  }
  ```

**AWS CloudFormation**:
- **特徴**: AWSネイティブ、AWSリソース専用
- **言語**: JSON / YAML
- **スタック管理**: テンプレート→スタック作成→更新→削除
- **メリット**: AWS統合（IAM、料金アラート等）、無料

**Pulumi**:
- **特徴**: 実プログラミング言語使用（TypeScript、Python、Go、C#）
- **メリット**: プログラミング言語の強力さ（ループ、条件、関数）
- **例**:
  ```typescript
  import * as aws from "@pulumi/aws";
  const vpc = new aws.ec2.Vpc("main", {
      cidrBlock: "10.0.0.0/16",
  });
  ```

**Ansible**:
- **特徴**: 構成管理（Configuration Management）ツール、エージェントレス
- **言語**: YAML（Playbook）
- **用途**: OSレベル設定、アプリデプロイ、サーバー構成
- **例**:
  ```yaml
  - hosts: webservers
    tasks:
      - name: Install nginx
        apt: name=nginx state=present
  ```

**IaCのベストプラクティス**:

**1. バージョン管理**:
- すべてのIaCコードをGit管理
- ブランチ戦略（feature、dev、prod）

**2. モジュール化**:
- 再利用可能なモジュール作成
- **Terraform Module例**: vpc、security-group、rds

**3. 環境分離**:
- dev、staging、prodで設定分離
- 変数ファイル（variables.tf、terraform.tfvars）
- Workspaceまたは別ディレクトリ

**4. 状態管理（Terraform）**:
- リモートバックエンド使用（S3 + DynamoDB for locking、Terraform Cloud）
- 状態ファイルは機密情報含む→暗号化、アクセス制限

**5. CI/CD統合**:
- Pull Request時に `terraform plan` 実行
- main mergeで `terraform apply`自動実行
- GitHub Actions、GitLab CI、CircleCI

**6. ポリシーチェック**:
- セキュリティ、コストのポリシー適用
- **ツール**: Terraform Sentinel、OPA（Open Policy Agent）、Checkov

**7. ドキュメント化**:
- READMEに構成説明
- 図（C4モデル、インフラ図）

**8. イミュータブルインフラ**:
- サーバー設定変更ではなく、新サーバー作成・旧サーバー破棄
- AMI、Dockerイメージ

**メリット**:
- **再現性**: 同じコードで同じインフラを何度でも構築
- **バージョン管理**: 変更履歴、ロールバック可能
- **ドキュメント**: コード自体がドキュメント
- **自動化**: 手作業エラー削減、高速デプロイ
- **レビュー**: インフラ変更をコードレビュー
- **スケール**: 大量のリソース管理

**デメリット**:
- **学習曲線**: ツールの習熟必要
- **状態管理**: Terraform等の状態ファイル管理
- **ドリフト**: 手動変更による実環境との乖離

**実用例**:

**例1: Netflix（Terraform）**
- 数千のAWSリソースをTerraformで管理
- モジュール化、再利用

**例2: Airbnb（Terraform）**
- マルチクラウド（AWS、GCP）対応

**例3: GitLab（Terraform + Ansible）**
- Terraformでインフラプロビジョニング
- Ansibleでアプリデプロイ・設定

**IaC vs ClickOps（手動操作）**:
| 項目 | IaC | ClickOps（GUIポチポチ） |
|------|-----|----------------------|
| 再現性 | ✅ 高 | ❌ 低 |
| 変更履歴 | ✅ Git履歴 | ❌ なし |
| レビュー | ✅ PR | ❌ 困難 |
| 自動化 | ✅ CI/CD | ❌ 手作業 |
| スピード | ✅ 高速（初期は遅い） | ❌ 遅い |
| 学習曲線 | ❌ Steep | ✅ 低 |

**参考文献・リソース**:
- 書籍: "Terraform: Up & Running" - Yevgeniy Brikman (2022, 3rd Ed.)
- 書籍: "Infrastructure as Code" - Kief Morris (2020, 2nd Ed.)
- サイト: registry.terraform.io（Terraformモジュールレジストリ）
- コース: HashiCorp Learn（無料Terraformコース）

---

### 8. SLI/SLO/SLA

**分類**: 可観測性・サービスレベル管理系

**出典・背景**:
GoogleのSite Reliability Engineering（SRE）実践から体系化。2016年の書籍「Site Reliability Engineering」（通称SRE本）で詳述されました。サービスの信頼性を定量的に測定・管理するフレームワークです。

**理論の詳細**:

**3つの概念**:

**1. SLI（Service Level Indicator / サービスレベル指標）**:
- **定義**: サービス品質を測定する定量的指標
- **特徴**: 測定可能、顧客体験に関連、時系列データ

**主要なSLI**:

**可用性（Availability）**:
```
可用性 = 成功したリクエスト数 / 総リクエスト数

例: 99.99% (4-nine) = 10,000リクエスト中9,999成功
```

**レイテンシ（Latency）**:
```
レイテンシSLI = パーセンタイル値

例: p50 < 100ms, p95 < 500ms, p99 < 1000ms
```
- **なぜパーセンタイル**: 平均は外れ値に影響されやすい
- **p95**: 95%のリクエストがこの値以下

**エラー率（Error Rate）**:
```
エラー率 = エラーレスポンス数 / 総リクエスト数

例: 5xx エラー < 0.1%
```

**スループット（Throughput）**:
```
スループット = 単位時間あたりの処理数

例: 10,000 requests/sec
```

**2. SLO（Service Level Objective / サービスレベル目標）**:
- **定義**: SLIの目標値、達成すべきレベル
- **特徴**: ビジネス要件と技術実現可能性のバランス

**SLO設定例**:
```
可用性 SLO: 99.9% (3-nine)
レイテンシ SLO: p95 < 200ms
エラー率 SLO: < 0.1%
```

**SLOの設定方法**:
1. 顧客の期待値を理解（ユーザーリサーチ）
2. 現状のパフォーマンス測定
3. ビジネス影響を分析（99.9% vs 99.99%のコスト差）
4. 現実的な目標設定（100%は不可能）

**3. SLA（Service Level Agreement / サービスレベル契約）**:
- **定義**: 顧客との法的契約、SLO未達成時の補償
- **特徴**: 外部公開、法的拘束力、ペナルティ条項

**SLA例（AWS EC2）**:
```
月次稼働率 < 99.99%の場合:
- 99.0% ~ 99.99%: 10% クレジット
- 95.0% ~ 99.0%: 25% クレジット
- < 95.0%: 100% クレジット
```

**3つの関係**:
```
SLI (測定) → SLO (目標) → SLA (契約)

例:
SLI: 今月の可用性 99.95%
SLO: 99.9%以上（内部目標）
SLA: 99.5%以上（顧客契約）

通常: SLO > SLA （余裕を持たせる）
```

**エラーバジェット（Error Budget）**:

**定義**:
```
エラーバジェット = 100% - SLO

例: SLO 99.9%の場合、エラーバジェット 0.1% (= 43分/月)
```

**活用方法**:
- バジェット消費中: 新機能開発に注力
- バジェット枯渇: 信頼性改善にシフト（新機能凍結）
- リリース判断: 「このリリースはエラーバジェットの何%消費するか」

**1ヶ月（30日）のダウンタイム許容量**:
| SLO | 月次ダウンタイム | 年次ダウンタイム |
|-----|----------------|----------------|
| 90% | 72時間 | 36.5日 |
| 99% | 7.2時間 | 3.65日 |
| 99.9% (3-nine) | 43分 | 8.76時間 |
| 99.95% | 21分 | 4.38時間 |
| 99.99% (4-nine) | 4.3分 | 52.6分 |
| 99.999% (5-nine) | 26秒 | 5.26分 |

**SLI/SLO設計のベストプラクティス**:

**1. ユーザー中心のSLI**:
- システム内部指標（CPU使用率）ではなく、ユーザー体験指標（レスポンス時間）

**2. 少数の重要SLI**:
- 多すぎると管理困難（3-5個に絞る）
- Golden Signals推奨: Latency、Traffic、Errors、Saturation

**3. 現実的なSLO**:
- 100%は不可能（メンテナンス、依存サービス障害）
- 過剰なSLOはコスト増（99.99% → 99.999%はコスト10倍）

**4. SLOレビュー**:
- 四半期ごとに見直し
- ビジネス要件変化、技術進化に対応

**5. アラート設計**:
- SLOベースアラート: バジェット消費率に基づく
- Symptom-based（症状ベース）vs Cause-based（原因ベース）

**実用例**:

**例1: Google Search（SRE本より）**
- 可用性 SLO: 99.99%
- レイテンシ SLO: p99 < 100ms
- エラーバジェット管理でリリース判断

**例2: Spotify**
- ストリーミング開始レイテンシ SLO: p95 < 300ms
- 再生エラー率 SLO: < 0.5%

**例3: Netflix**
- ストリーミング開始成功率 SLO: 99.9%
- 再生品質 SLO: 高画質率 > 90%

**SLI/SLO実装ツール**:
- **Prometheus + Grafana**: SLI計測、ダッシュボード
- **Datadog**: SLO Tracking機能
- **New Relic**: SLI/SLO管理
- **Google Cloud Monitoring**: SLO機能ネイティブサポート

**参考文献・リソース**:
- 書籍: "Site Reliability Engineering" - Google (2016) ← SRE本
- 書籍: "The Site Reliability Workbook" - Google (2018) ← 実践編
- 書籍: "Implementing Service Level Objectives" - Alex Hidalgo (2020)
- サイト: sre.google（SREリソース）

---

### 9. Twelve-Factor App

**分類**: クラウドネイティブ・アプリケーション設計系

**出典・背景**:
Heroku共同創業者のAdam Wiggins が2011年に提唱。PaaS（Platform as a Service）環境でのベストプラクティスを12の原則にまとめました。現代のクラウドネイティブアプリケーション、マイクロサービス設計の基礎となっています。

**理論の詳細**:

**12の原則**:

**I. コードベース（Codebase）**:
- 1つのアプリ = 1つのコードベース（Git repository）
- 複数環境（dev、staging、prod）は同じコードベースから
- **避ける**: 複数アプリが1リポジトリを共有

**II. 依存関係（Dependencies）**:
- 依存関係を明示的に宣言（package.json、requirements.txt、Gemfile）
- システム全体のパッケージに依存しない
- **例**: Node.js: `npm install` で再現可能

**III. 設定（Config）**:
- 環境ごとの設定（DB接続文字列、APIキー）はコードから分離
- 環境変数に格納
- **避ける**: 設定をコードにハードコード、設定ファイルをコミット
- **例**: `DATABASE_URL=postgres://user:pass@host:5432/db`

**IV. バックエンドサービス（Backing Services）**:
- DB、キャッシュ、メッセージキューを「接続されたリソース」として扱う
- 設定変更のみでサービス切り替え可能（ローカルMySQL → AWS RDS）
- **例**: URLの変更だけでRedisをローカル→Elasticache切替

**V. ビルド、リリース、実行（Build, Release, Run）**:
- **ビルド**: コード→実行可能バイナリ（依存解決、コンパイル）
- **リリース**: ビルド + 設定 → 実行可能リリース
- **実行**: リリースを環境で実行
- **厳格な分離**: 実行中に変更不可、ロールバックはリリース切り替え

**VI. プロセス（Processes）**:
- アプリはステートレスプロセス
- 永続データは外部サービス（DB）に保存
- **避ける**: セッションをメモリに保存、ローカルファイルシステムへの永続化
- **代替**: セッションはRedis、ファイルはS3

**VII. ポートバインディング（Port Binding）**:
- アプリはHTTPサーバーを内包、ポート経由で公開
- Webサーバー（Apache、Nginx）への依存なし
- **例**: Node.jsのExpressがポート3000でリッスン、コンテナ化容易

**VIII. 並行性（Concurrency）**:
- プロセスモデルで水平スケール
- プロセスタイプ（webプロセス、workerプロセス）ごとにスケール
- **避ける**: 単一巨大プロセス、スレッドベースの並行性のみ
- **例**: Webリクエスト処理（webプロセス × 5）、バックグラウンドジョブ（workerプロセス × 10）

**IX. 廃棄容易性（Disposability）**:
- 高速起動、グレースフルシャットダウン
- プロセスは突然終了に耐える
- **起動**: 数秒以内
- **シャットダウン**: SIGTERMで進行中のリクエスト完了後終了
- **用途**: 迅速なスケール、素早いデプロイ

**X. 開発/本番一致（Dev/Prod Parity）**:
- dev、staging、prodの差異を最小化
- **時間差**: デプロイサイクル短縮（数時間～数日）
- **人材差**: 開発者が自分でデプロイ
- **ツール差**: 同じDB、同じOS（Dockerで統一）
- **避ける**: 開発はSQLite、本番はPostgreSQL

**XI. ログ（Logs）**:
- アプリはログファイルに書かない
- 標準出力（stdout）にストリーム出力
- 実行環境がログ収集・集約
- **例**: Docker logs、Kubernetes → Fluentd → Elasticsearch

**XII. 管理プロセス（Admin Processes）**:
- 管理タスク（DB migration、REPL）は1回限りのプロセス
- 本番環境と同じリリース、同じ依存関係で実行
- **例**: `rails db:migrate`、`node scripts/seed.js`

**Twelve-Factor Appのメリット**:
- **クラウドネイティブ**: PaaS、Kubernetes等で最適動作
- **スケーラビリティ**: 水平スケール容易
- **可搬性**: クラウド間移行、ローカル開発が同じ
- **継続的デプロイ**: 高頻度デプロイに適合
- **保守性**: 環境差異による問題減少

**実用例**:
- **Heroku**: Twelve-Factor Appが設計基準
- **AWS Elastic Beanstalk**: 同じ原則
- **Kubernetes**: StatelessなPodが原則に適合
- **Netflix、Spotify**: マイクロサービスで原則適用

**Beyond Twelve-Factor（15-Factor）**:
Kevin Hoffman が2016年に3つ追加提案:
- **XIII. API First**: APIを最初に設計
- **XIV. Telemetry**: 可観測性組み込み
- **XV. Authentication & Authorization**: セキュリティ組み込み

**参考文献・リソース**:
- サイト: 12factor.net（公式、多言語翻訳あり）
- 書籍: "Beyond the Twelve-Factor App" - Kevin Hoffman (2016)
- 記事: "The Twelve-Factor App" - Adam Wiggins (2011)

---

### 10. アーキテクチャ決定記録（ADR / Architecture Decision Records）

**分類**: ドキュメンテーション・意思決定系

**出典・背景**:
Michael Nygard が2011年のブログ記事「Documenting Architecture Decisions」で提唱しました。アーキテクチャの重要な決定を軽量に文書化し、後から「なぜこの決定をしたのか」を理解できるようにします。

**理論の詳細**:

**定義**:
アーキテクチャ上の重要な決定を、その理由・背景・トレードオフとともに記録する短い文書。

**ADRの構成**:

**基本フォーマット（Michael Nygardテンプレート）**:
```markdown
# ADR [番号]: [タイトル]

## ステータス
[Proposed | Accepted | Deprecated | Superseded]

## コンテキスト
[どのような状況で、なぜこの決定が必要か]

## 決定
[何を決定したか]

## 結果
[この決定による影響、トレードオフ、メリット/デメリット]
```

**詳細例**:
```markdown
# ADR 003: マイクロサービス間通信にRESTful APIを使用

## ステータス
Accepted (2024-01-15)

## コンテキスト
当社のEコマースプラットフォームはモノリスからマイクロサービスへ移行中。
サービス間通信の標準プロトコルを決定する必要がある。

チームの大半はREST APIに慣れている。一部メンバーがgRPCを提案。
リアルタイム性は必須ではなく、外部パートナーとのAPI統合も想定。

## 決定
サービス間通信の標準プロトコルとしてRESTful API（JSON over HTTP）を採用する。

理由:
- チームの既存スキル（REST経験豊富）
- ツールの成熟度（Swagger/OpenAPI、Postman等）
- デバッグ容易性（curlで確認可能）
- 外部連携（パートナーAPIもREST）

## 結果

**ポジティブ:**
- 学習コスト低い
- デバッグ・テストが容易
- 外部APIとの一貫性

**ネガティブ:**
- gRPCより低速（ただし要件上問題なし）
- 型安全性が低い（OpenAPIで緩和）

**トレードオフ:**
パフォーマンスを犠牲にして、開発速度と保守性を優先。
将来的に高スループットが必要なサービス（推薦エンジン等）では
gRPCを部分的に導入する可能性を残す。

**関連ADR:**
- ADR 002: マイクロサービスアーキテクチャ採用
- ADR 010: API Gateway導入（未来の決定）
```

**ADRのライフサイクル**:

**ステータス遷移**:
```
Proposed (提案)
    ↓
Accepted (承認) ← 決定実施中
    ↓
[以下のいずれか]
- Deprecated (非推奨) → Superseded by ADR [番号]
- Rejected (却下)
- Superseded (置き換え) → ADR [番号]が置き換え
```

**ADRを書くべき決定**:

**書くべき**:
- ✅ アーキテクチャパターン選択（モノリス vs マイクロサービス）
- ✅ 技術スタック選択（React vs Angular、PostgreSQL vs MongoDB）
- ✅ 通信プロトコル（REST vs gRPC vs メッセージキュー）
- ✅ デプロイ戦略（Kubernetes vs ECS）
- ✅ 認証方式（JWT vs Session）
- ✅ データベース設計（正規化 vs 非正規化）

**書かなくてよい**:
- ❌ 些細な実装詳細（変数名、コメント書き方）
- ❌ 自明な決定（「ログを出力する」）
- ❌ すぐに変わる決定（UI配色）

**ADRのベストプラクティス**:

**1. 軽量に保つ**:
- 1ページ以内（長すぎると読まれない）
- 重要な情報のみ

**2. トレードオフを明示**:
- メリット・デメリット両方記載
- なぜ他の選択肢を採用しなかったか

**3. バージョン管理**:
- コードと同じリポジトリ（`docs/adr/` ディレクトリ）
- Gitで履歴管理

**4. 番号付け**:
- 連番（ADR-001、ADR-002）
- 削除せず Deprecated ステータスに

**5. 早期作成**:
- 決定後すぐ書く（記憶が新鮮なうちに）
- レトロスペクティブで書かない（理由が思い出せない）

**6. レビュー**:
- Pull Requestで関係者レビュー
- チーム合意が重要

**ADRツール**:
- **adr-tools**: CLIツール（ADR作成、ステータス管理）
- **log4brains**: WebベースADRブラウザ
- **Markdown**: 最もシンプル（特別なツール不要）

**実用例**:

**例1: GitHub（公開ADR）**
- github/gov（governance）リポジトリで一部公開
- オープンソースプロジェクトで透明性

**例2: ThoughtWorks**
- ADRを標準実践
- プロジェクト引き継ぎで有用

**例3: Spotify**
- "Decision Log"として実践
- Squad単位で管理

**ADRの価値**:

**1. オンボーディング**:
- 新メンバーが過去の決定理由を理解
- 「なぜこうなってるの？」に答える

**2. 意思決定の透明性**:
- トレードオフが明示され、責任の所在明確

**3. 歴史的記録**:
- 当時の前提条件を記録（後から「今ならこうしない」も理解）

**4. リファクタリング判断**:
- 前提条件変化で、再検討のトリガー

**参考文献・リソース**:
- 記事: "Documenting Architecture Decisions" - Michael Nygard (2011)
- 書籍: "Design It!" - Michael Keeling (2017、ADR章あり)
- GitHub: joelparkerhenderson/architecture-decision-record（テンプレート集）
- ツール: adr-tools (GitHub: npryce/adr-tools)

---

## フレームワーク選択ガイド

| 状況・課題 | 推奨フレームワーク | 理由 |
|-----------|------------------|------|
| アーキテクチャ可視化・コミュニケーション | C4モデル、4+1ビュー | ステークホルダーごとの抽象度調整 |
| マイクロサービス設計 | DDD（Bounded Context）、CAP定理、イベント駆動 | サービス境界、データ整合性、疎結合 |
| 分散システム設計 | CAP定理、PACELC、Saga Pattern | 一貫性・可用性のトレードオフ |
| クラウド移行・クラウドネイティブ | Twelve-Factor App、Kubernetes、IaC | 可搬性、スケーラビリティ、自動化 |
| セキュリティ設計 | Zero Trust、Defense in Depth、STRIDE | 多層防御、脅威モデリング |
| サービス間通信管理 | Service Mesh、API Gateway | トラフィック管理、可観測性、セキュリティ |
| 信頼性・SRE | SLI/SLO/SLA、エラーバジェット、Golden Signals | 定量的品質管理、バランスの取れたリリース |
| インフラ管理・自動化 | IaC (Terraform/CloudFormation)、GitOps | 再現性、バージョン管理、自動化 |
| アーキテクチャ決定の文書化 | ADR、C4モデル | 透明性、オンボーディング、意思決定記録 |

---

## フレームワーク統合例

### ケース: レガシーモノリスからマイクロサービスへの移行

**Phase 1: 現状分析とビジョン策定（0-2ヶ月）**
1. **C4モデル**: 現状アーキテクチャ可視化（Context→Container）
2. **DDD**: ドメイン分析、Bounded Context特定
3. **ADR-001**: マイクロサービス採用の決定記録

**Phase 2: 移行戦略設計（2-4ヶ月）**
1. **Strangler Fig Pattern**: 段階的移行計画
2. **CAP定理**: サービスごとの一貫性要件分析
3. **ADR-002**: データベース戦略（Database per Service）
4. **SLI/SLO**: 各サービスの信頼性目標設定

**Phase 3: 実装・基盤構築（4-12ヶ月）**
1. **Kubernetes**: コンテナオーケストレーション基盤
2. **IaC (Terraform)**: インフラコード化
3. **Service Mesh (Istio)**: サービス間通信管理
4. **Event-Driven Architecture**: 非同期連携（Kafka）
5. **Twelve-Factor App**: 各サービスの実装原則
6. **ADR-003〜010**: 技術選定の記録

**Phase 4: 運用・改善（12ヶ月以降）**
1. **SLI/SLO監視**: Prometheus + Grafana
2. **分散トレーシング**: Jaeger
3. **エラーバジェット**: リリース判断
4. **継続的ADR更新**: アーキテクチャ進化の記録

---

## 参考文献・リソース

### 必読書籍
1. **"Software Architecture: The Hard Parts"** - Neal Ford et al. (2021)
   - 現代的アーキテクチャ設計の難題と解決策
   
2. **"Building Microservices"** - Sam Newman (2021, 2nd Ed.)
   - マイクロサービスの決定版

3. **"Designing Data-Intensive Applications"** - Martin Kleppmann (2017)
   - 分散システム、データベースの深い理解

4. **"Site Reliability Engineering"** - Google (2016)
   - SRE実践、SLI/SLO、可観測性

5. **"Domain-Driven Design"** - Eric Evans (2003)
   - DDDの原典

6. **"Clean Architecture"** - Robert C. Martin (2017)
   - アーキテクチャ原則、SOLID

### オンラインリソース
- **Martin Fowler's Blog**: martinfowler.com（アーキテクチャパターン解説）
- **AWS Architecture Center**: aws.amazon.com/architecture（リファレンスアーキテクチャ）
- **Google Cloud Architecture Framework**: cloud.google.com/architecture
- **Microsoft Azure Architecture Center**: docs.microsoft.com/azure/architecture
- **The Architect Elevator**: architectelevator.com（Gregor Hohpeのブログ）

### ツール
- **アーキテクチャ図**: Structurizr（C4）、Lucidchart、Draw.io
- **IaC**: Terraform、Pulumi、AWS CloudFormation
- **コンテナ**: Docker、Kubernetes
- **サービスメッシュ**: Istio、Linkerd
- **可観測性**: Prometheus、Grafana、Jaeger、Datadog

---

このドキュメントは、システムアーキテクトオーケストレーターが統合している主要フレームワークの詳細解説です。各フレームワークは、アーキテクチャ設計の全フェーズをカバーし、スケーラブルで保守性が高く、ビジネス価値と整合したシステム構築を支援します。
