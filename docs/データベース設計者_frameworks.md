# データベース設計者 - フレームワーク・理論詳解

## 概要

データベース設計者オーケストレーターは、データモデリング、正規化理論、パフォーマンス最適化、スケーラビリティパターンなど、データベース設計の包括的な知識体系を統合した対話型AIシステムです。OLTP（オンライントランザクション処理）からOLAP（オンライン分析処理）まで、幅広いデータベース設計シナリオに対応します。

### 特徴
- エンティティ関連モデリング（ER図）から物理設計まで全工程をカバー
- 正規化と非正規化のトレードオフを最適化
- インデックス戦略、パーティショニング、レプリケーションなどの高度な最適化技法
- ACID特性からCAP定理まで、分散データベースの理論的基盤
- 実装可能なDDL、ER図、最適化戦略を成果物として提供

---

## 組み込まれているフレームワーク・理論

### 1. ER図（Entity-Relationship Diagram）

#### 分類
- **データモデリング系**
- **概念設計・論理設計**

#### 出典・背景
- **提唱者**: Peter Chen
- **出典**: "The Entity-Relationship Model—Toward a Unified View of Data" (ACM Transactions on Database Systems, 1976)
- **背景**: 1970年代にRDBMSが発展する中、データ構造を直感的に表現する方法が求められました。Peter Chenは、エンティティ（実体）とリレーションシップ（関連）という2つの基本概念でデータ構造を表現する革新的なモデリング手法を提案しました。

#### 理論の詳細

**ER図の構成要素**:

1. **エンティティ（Entity）**: データとして管理する実体（例: 顧客、商品、注文）
2. **属性（Attribute）**: エンティティの特性（例: 顧客名、商品価格）
3. **リレーションシップ（Relationship）**: エンティティ間の関連（例: 顧客が注文する）
4. **カーディナリティ（Cardinality）**: リレーションシップの多重度
   - 1:1（一対一）
   - 1:N（一対多）
   - M:N（多対多）

**ER図のモデリングレベル**:

- **概念ER図**: ビジネスドメインの理解、ステークホルダーとのコミュニケーション
- **論理ER図**: データベース設計の詳細化、属性・キーの定義
- **物理ER図**: 実装レベル、テーブル・カラム・インデックス定義

**ER図の記法**:

- **Chen記法**: オリジナルの記法、菱形でリレーションシップを表現
- **IE記法（Information Engineering）**: 鳥の足記法（Crow's Foot）、カーディナリティを直感的に表現
- **UML記法**: クラス図に近い表現、オブジェクト指向設計との親和性

**設計プロセス**:

1. **エンティティの抽出**: ビジネス要件から名詞を抽出
2. **属性の定義**: エンティティの特性を洗い出し
3. **リレーションシップの定義**: エンティティ間の関連を特定
4. **カーディナリティの決定**: 関連の多重度を決定
5. **正規化**: データ冗長性を排除

#### 実用例

**例1: ECサイトの注文管理システム**

```
[顧客] 1 ---< N [注文] N >--- 1 [配送先]
  |                |
  | 1              | N
  |                |
  v                v
[会員情報]      [注文明細] N >--- 1 [商品]
                    |
                    | N
                    v
                  [在庫]

エンティティ:
- 顧客: customer_id, name, email, phone
- 注文: order_id, customer_id, order_date, total_amount, status
- 注文明細: order_detail_id, order_id, product_id, quantity, price
- 商品: product_id, name, description, price, category_id
- 配送先: shipping_id, order_id, address, city, postal_code

リレーションシップ:
- 顧客は複数の注文を持つ（1:N）
- 注文は複数の注文明細を持つ（1:N）
- 注文明細は1つの商品を参照する（N:1）
- 注文は1つの配送先を持つ（1:1）
```

**例2: SaaS型プロジェクト管理ツール（マルチテナント）**

```
[テナント] 1 ---< N [ユーザー]
     |                  |
     | 1                | N
     |                  |
     v                  v
[プロジェクト] N >--- N [タスク]
     |                  |
     | 1                | 1
     |                  |
     v                  v
[マイルストーン]    [担当者]

エンティティ設計のポイント:
- tenant_id を全テーブルに含める（データ分離）
- 複合キー: (tenant_id, entity_id) で一意性を保証
- Row Level Security（RLS）でテナント分離を実装
```

**例3: 医療情報システム（ER図の多対多解消）**

```
Before（多対多）:
[患者] N ---< M [医師]

After（中間テーブル導入）:
[患者] 1 ---< N [診察記録] N >--- 1 [医師]
                    |
                    | 1
                    v
                [処方箋] N >--- N [薬剤]
                             |
                         [処方明細]

設計判断:
- 診察記録（中間エンティティ）に診察日時、診断結果などの属性を追加
- 処方箋と薬剤の多対多関係も処方明細で解消
- 履歴管理、監査証跡の実装を容易に
```

#### 参考文献・リソース
- Peter Chen, "The Entity-Relationship Model—Toward a Unified View of Data" (ACM TODS, 1976)
- C.J. Date, "An Introduction to Database Systems" (Addison-Wesley, 2003)
- Teorey, T., et al., "Database Modeling and Design" (Morgan Kaufmann, 2011)
- ERD Tool: Lucidchart, draw.io, dbdiagram.io, ERDPlus

---

### 2. 正規化理論（Normalization Theory）

#### 分類
- **データモデリング系**
- **論理設計・整合性設計**

#### 出典・背景
- **提唱者**: Edgar F. Codd
- **出典**: "A Relational Model of Data for Large Shared Data Banks" (CACM, 1970)、"Further Normalization of the Data Base Relational Model" (1971)
- **背景**: リレーショナルデータベースの父、Edgar F. Coddは、データの冗長性と更新異常を数学的に解決する正規化理論を提唱しました。関数従属性（Functional Dependency）の概念を用いて、データベース設計の科学的基礎を確立しました。

#### 理論の詳細

**正規形の階層**:

**第1正規形（1NF: First Normal Form）**:
- **定義**: 各属性が原子値（atomic value）を持つ
- **排除すべき要素**: 繰り返しグループ、配列、入れ子構造
- **達成基準**: 
  - 各セルに単一の値のみ
  - 各行が一意に識別可能（主キー存在）
  - 順序に依存しない

**第2正規形（2NF: Second Normal Form）**:
- **定義**: 1NFかつ、部分関数従属を排除
- **部分関数従属**: 複合主キーの一部のみに従属する非キー属性
- **達成方法**: 部分関数従属する属性を別テーブルに分離

**第3正規形（3NF: Third Normal Form）**:
- **定義**: 2NFかつ、推移的関数従属を排除
- **推移的関数従属**: A→B、B→C のとき、A→C（非キー属性間の従属関係）
- **達成方法**: 推移的に従属する属性を別テーブルに分離

**ボイス・コッド正規形（BCNF: Boyce-Codd Normal Form）**:
- **定義**: 3NFより厳密、全ての決定項が候補キー
- **3NFとの違い**: 複数の候補キーが重複する場合の異常を解消
- **達成基準**: X→Y という関数従属において、Xは必ず候補キー

**第4正規形（4NF）・第5正規形（5NF）**:
- **4NF**: 多値従属性（Multi-valued Dependency）の排除
- **5NF**: 結合従属性（Join Dependency）の排除
- **実務での使用頻度**: 3NF/BCNFまでが一般的

**関数従属性（Functional Dependency）**:

定義: X→Y は、Xの値が決まればYの値が一意に決まることを意味します。

```
例: 社員テーブル
社員ID → 社員名, 部署ID, 部署名

関数従属性:
- 社員ID → 社員名 ✓
- 社員ID → 部署ID ✓
- 部署ID → 部署名 ✓（推移的関数従属）
```

**正規化のメリット**:
1. **データ冗長性の削減**: ストレージコスト削減
2. **更新異常の防止**: 
   - 挿入異常: 不完全なデータが挿入できない
   - 削除異常: 意図しないデータ削除
   - 更新異常: 複数箇所の更新漏れ
3. **データ整合性の向上**: 矛盾のないデータ管理

**正規化のデメリット**:
1. **JOIN操作の増加**: クエリパフォーマンス低下
2. **クエリの複雑化**: 開発・保守コスト増加
3. **インデックス設計の複雑化**: 多数のテーブル間結合

#### 実用例

**例1: 非正規形から3NFへの変換（注文システム）**

```sql
-- 非正規形テーブル（1NF未満）
CREATE TABLE orders_denormalized (
    order_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    products VARCHAR(500),  -- カンマ区切り: "商品A, 商品B, 商品C"
    quantities VARCHAR(100), -- カンマ区切り: "2, 1, 5"
    prices VARCHAR(100)      -- カンマ区切り: "1000, 2000, 500"
);

-- 問題点: 繰り返しグループ、原子性違反、検索・集計困難

-- 1NF: 原子性を確保
CREATE TABLE orders_1nf (
    order_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_name)
);

-- 問題点: customer情報が重複（部分関数従属）

-- 2NF: 部分関数従属を排除
CREATE TABLE orders_2nf (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    order_date DATE
);

CREATE TABLE order_items_2nf (
    order_id INT,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_name),
    FOREIGN KEY (order_id) REFERENCES orders_2nf(order_id)
);

-- 問題点: customer情報が複数注文で重複（推移的関数従属なし）
-- order_id → customer_name は直接従属なので2NFは満たす
-- しかし、同じ顧客の複数注文でデータ重複

-- 3NF: 推移的従属を排除（顧客情報を分離）
CREATE TABLE customers_3nf (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100) UNIQUE,
    customer_phone VARCHAR(20)
);

CREATE TABLE orders_3nf (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers_3nf(customer_id)
);

CREATE TABLE order_items_3nf (
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders_3nf(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    description TEXT,
    standard_price DECIMAL(10,2)
);
```

**例2: BCNF違反の検出と修正（予約システム）**

```sql
-- 3NFだがBCNF違反の例
CREATE TABLE reservations (
    court_id INT,        -- テニスコート番号
    start_time TIME,     -- 開始時刻
    member_id INT,       -- 予約者ID
    rate_type VARCHAR(20), -- 料金タイプ（"standard", "premium"）
    PRIMARY KEY (court_id, start_time)
);

-- 関数従属性:
-- (court_id, start_time) → member_id, rate_type
-- member_id → rate_type （会員によって料金タイプ決定）

-- 問題: member_id → rate_type だが、member_idは候補キーではない（BCNF違反）
-- 異常: 会員の料金タイプ変更時、全予約レコードの更新が必要

-- BCNF達成:
CREATE TABLE members (
    member_id INT PRIMARY KEY,
    member_name VARCHAR(100),
    rate_type VARCHAR(20)  -- "standard", "premium"
);

CREATE TABLE reservations_bcnf (
    court_id INT,
    start_time TIME,
    member_id INT,
    PRIMARY KEY (court_id, start_time),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- rate_typeはmembersテーブルから参照で取得
```

**例3: 正規化の実践的判断（在庫管理システム）**

```sql
-- ケース1: 3NFを維持（整合性重視）
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50)
);

-- 利点: カテゴリ名変更が1箇所で済む
-- 欠点: 商品一覧表示時に毎回JOIN必要

-- ケース2: 意図的な非正規化（パフォーマンス重視）
CREATE TABLE products_denormalized (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT,
    category_name VARCHAR(50),  -- 非正規化: カテゴリ名を複製
    INDEX idx_category (category_id)
);

-- 利点: JOIN不要、読み取り高速
-- 欠点: カテゴリ名変更時に全商品レコードを更新
-- 判断基準: 読み取り頻度 >> 更新頻度 なら非正規化を検討
```

#### 参考文献・リソース
- E.F. Codd, "A Relational Model of Data for Large Shared Data Banks" (CACM, Vol.13, No.6, 1970)
- E.F. Codd, "Further Normalization of the Data Base Relational Model" (1971)
- C.J. Date, "Database Design and Relational Theory" (O'Reilly, 2012)
- William Kent, "A Simple Guide to Five Normal Forms in Relational Database Theory" (CACM, 1983)
- Online Tool: normalization.info, dbdiagram.io

---

### 3. 非正規化戦略（Denormalization Strategy）

#### 分類
- **パフォーマンス最適化系**
- **物理設計・読み取り最適化**

#### 出典・背景
- **背景**: 正規化理論が確立した1970-80年代に、実務で「過度な正規化がパフォーマンスボトルネックになる」という課題が顕在化しました。特にOLAP（分析処理）、データウェアハウス、読み取り中心のシステムでは、意図的な非正規化がベストプラクティスとして確立されました。
- **思想**: "Normalize until it hurts, denormalize until it works"（痛みを感じるまで正規化し、動作するまで非正規化する）

#### 理論の詳細

**非正規化の目的**:
1. **JOIN操作の削減**: 複数テーブル結合のコスト削減
2. **集計処理の高速化**: 事前計算された値を保持
3. **インデックス効率の向上**: 検索対象列を同一テーブルに集約
4. **ネットワークI/Oの削減**: 1回のクエリで必要データを取得

**非正規化の技法**:

**1. 派生列の追加（Derived Column）**:
- 計算可能な値を事前計算して保持
- 例: 注文合計金額、在庫数、平均評価

**2. テーブル結合（Table Merging）**:
- 頻繁にJOINする2つのテーブルを統合
- 例: 顧客テーブルと顧客詳細テーブルの統合

**3. サマリーテーブル（Summary Table）**:
- 集計結果を事前計算して保持
- 例: 日次売上サマリー、カテゴリ別在庫数

**4. 重複列の追加（Redundant Column）**:
- 他テーブルから参照可能な列を複製
- 例: 注文テーブルに顧客名を保持

**5. マテリアライズドビュー（Materialized View）**:
- 複雑なクエリ結果を物理的に保存
- 定期的な更新（リフレッシュ）

**非正規化のトレードオフ**:

| メリット | デメリット |
|---------|----------|
| 読み取りパフォーマンス向上 | 書き込みパフォーマンス低下 |
| クエリのシンプル化 | 更新ロジックの複雑化 |
| JOIN削減によるCPU負荷軽減 | ストレージコスト増加 |
| レスポンスタイム短縮 | データ整合性維持の困難化 |
| インデックス効率向上 | 更新異常のリスク増加 |

**非正規化の適用判断基準**:

1. **読み取り/書き込み比率**: 読み取り頻度が圧倒的に高い（例: 100:1以上）
2. **JOIN複雑度**: 5つ以上のテーブルを頻繁にJOIN
3. **パフォーマンス要件**: ミリ秒単位のレスポンスタイム要求
4. **データ更新頻度**: 参照される側のデータがほぼ静的
5. **整合性要件**: 結果整合性（Eventual Consistency）が許容される

**整合性維持戦略**:

1. **トリガー（Trigger）**: 更新時に自動で派生データを更新
2. **アプリケーション制御**: ビジネスロジック層で整合性を保証
3. **バッチ処理**: 定期的に非正規化データを再計算
4. **イベント駆動**: データ変更イベントで非正規化データを更新

#### 実用例

**例1: ECサイトの注文サマリー（派生列追加）**

```sql
-- 正規化版（毎回集計計算が必要）
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 合計金額取得には毎回集計が必要（コスト高）
SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total_amount
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;

-- 非正規化版（派生列を追加）
CREATE TABLE orders_denormalized (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20),
    total_amount DECIMAL(10,2),      -- 非正規化: 合計金額を保持
    item_count INT,                   -- 非正規化: 商品点数を保持
    INDEX idx_total (total_amount),
    INDEX idx_date (order_date)
);

-- 注文明細挿入時にトリガーで合計を更新
DELIMITER $$
CREATE TRIGGER update_order_totals
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders_denormalized
    SET total_amount = (
        SELECT SUM(quantity * unit_price)
        FROM order_items
        WHERE order_id = NEW.order_id
    ),
    item_count = (
        SELECT COUNT(*)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE order_id = NEW.order_id;
END$$
DELIMITER ;

-- 読み取りが超高速に
SELECT order_id, total_amount, item_count
FROM orders_denormalized
WHERE order_date >= '2025-01-01'
ORDER BY total_amount DESC;
```

**例2: データウェアハウスのサマリーテーブル**

```sql
-- ファクトテーブル（正規化）: 数億レコード
CREATE TABLE sales_facts (
    sale_id BIGINT PRIMARY KEY,
    product_id INT,
    store_id INT,
    date_id INT,
    quantity INT,
    revenue DECIMAL(10,2),
    cost DECIMAL(10,2)
);

-- 日次サマリーテーブル（非正規化）
CREATE TABLE daily_sales_summary (
    summary_date DATE,
    store_id INT,
    category_id INT,
    total_revenue DECIMAL(15,2),
    total_cost DECIMAL(15,2),
    total_quantity INT,
    transaction_count INT,
    avg_order_value DECIMAL(10,2),
    PRIMARY KEY (summary_date, store_id, category_id)
);

-- 月次サマリーテーブル（さらに集約）
CREATE TABLE monthly_sales_summary (
    year_month CHAR(7),  -- "2025-01"
    store_id INT,
    category_id INT,
    total_revenue DECIMAL(15,2),
    total_cost DECIMAL(15,2),
    profit_margin DECIMAL(5,2),
    PRIMARY KEY (year_month, store_id, category_id)
);

-- バッチ処理で日次更新
INSERT INTO daily_sales_summary
SELECT 
    DATE(created_at) AS summary_date,
    store_id,
    p.category_id,
    SUM(revenue) AS total_revenue,
    SUM(cost) AS total_cost,
    SUM(quantity) AS total_quantity,
    COUNT(*) AS transaction_count,
    AVG(revenue) AS avg_order_value
FROM sales_facts sf
JOIN products p ON sf.product_id = p.product_id
WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY
GROUP BY DATE(created_at), store_id, p.category_id
ON DUPLICATE KEY UPDATE
    total_revenue = VALUES(total_revenue),
    total_cost = VALUES(total_cost),
    total_quantity = VALUES(total_quantity),
    transaction_count = VALUES(transaction_count),
    avg_order_value = VALUES(avg_order_value);

-- ダッシュボードクエリが瞬時に完了
SELECT category_id, SUM(total_revenue) AS revenue
FROM daily_sales_summary
WHERE summary_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY category_id;
```

**例3: SNSアプリのユーザープロフィール（重複列追加）**

```sql
-- 正規化版
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    avatar_url VARCHAR(255)
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT,
    content TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 投稿一覧表示には毎回JOIN（N+1問題の可能性）
SELECT p.*, u.username, u.avatar_url
FROM posts p
JOIN users u ON p.user_id = u.user_id
ORDER BY p.created_at DESC
LIMIT 50;

-- 非正規化版（読み取り最適化）
CREATE TABLE posts_denormalized (
    post_id INT PRIMARY KEY,
    user_id INT,
    username VARCHAR(50),      -- 非正規化: ユーザー名を複製
    avatar_url VARCHAR(255),   -- 非正規化: アバターURLを複製
    content TEXT,
    created_at TIMESTAMP,
    INDEX idx_created (created_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- JOIN不要で超高速
SELECT post_id, username, avatar_url, content, created_at
FROM posts_denormalized
ORDER BY created_at DESC
LIMIT 50;

-- 整合性維持: ユーザー情報更新時に投稿も更新
UPDATE posts_denormalized
SET username = 'new_username', avatar_url = 'new_avatar.jpg'
WHERE user_id = 12345;

-- トレードオフ判断:
-- - ユーザー名変更頻度: 低い（月1回程度）
-- - 投稿一覧表示頻度: 超高頻度（秒間数千リクエスト）
-- → 非正規化が適切
```

#### 参考文献・リソース
- Sam S. Lightstone, et al., "Physical Database Design: The Database Professional's Guide to Exploiting Indexes, Views, Storage, and More" (Morgan Kaufmann, 2007)
- Ralph Kimball, "The Data Warehouse Toolkit" (Wiley, 2013) - ディメンショナルモデリング
- Martin Kleppmann, "Designing Data-Intensive Applications" (O'Reilly, 2017) - Chapter 2: Data Models
- High Scalability Blog: http://highscalability.com/

---

### 4. インデックス戦略（Index Strategy）

#### 分類
- **パフォーマンス最適化系**
- **物理設計・クエリ最適化**

#### 出典・背景
- **背景**: データベースのパフォーマンスを決定する最重要要素がインデックス設計です。B-Treeインデックスは1970年代にRudolf Bayerらによって発明され、RDBMSの標準データ構造となりました。近年ではLSM-Tree（Log-Structured Merge-Tree）など、書き込み最適化インデックスも登場しています。
- **重要性**: 適切なインデックスで1000倍以上のパフォーマンス改善が可能です。

#### 理論の詳細

**インデックスの基本原理**:

インデックスは「本の索引」と同じく、データの物理的位置を素早く特定するためのデータ構造です。

**主要インデックスタイプ**:

**1. B-Treeインデックス（Balanced Tree）**:
- **構造**: バランスの取れた木構造、各ノードに複数のキーと子ポインタ
- **時間計算量**: O(log n) の検索・挿入・削除
- **適用場面**: 
  - 等価検索: `WHERE id = 100`
  - 範囲検索: `WHERE created_at >= '2025-01-01'`
  - ORDER BY最適化
  - MIN/MAX最適化
- **デフォルト**: ほとんどのRDBMSのデフォルトインデックス

**2. ハッシュインデックス（Hash Index）**:
- **構造**: ハッシュ関数でキーをハッシュ値に変換、O(1)アクセス
- **適用場面**: 等価検索のみ（`WHERE id = 100`）
- **制約**: 範囲検索不可、ORDER BY不可
- **使用例**: Redis、Memcached、MySQL MEMORYエンジン

**3. ビットマップインデックス（Bitmap Index）**:
- **構造**: 各値に対してビット列を保持
- **適用場面**: カーディナリティの低い列（性別、ステータス、フラグなど）
- **メリット**: 複数条件のAND/OR/NOT演算が超高速
- **使用例**: Oracle、PostgreSQL、データウェアハウス

**4. フルテキストインデックス（Full-Text Index）**:
- **構造**: 転置インデックス（Inverted Index）
- **適用場面**: テキスト検索、LIKE検索の高速化
- **使用例**: MySQL FULLTEXT、PostgreSQL tsvector、Elasticsearch

**5. 空間インデックス（Spatial Index）**:
- **構造**: R-Tree、Quadtree
- **適用場面**: GIS、位置情報検索
- **使用例**: PostGIS、MySQL Spatial

**複合インデックス（Composite Index）**:

複数列を組み合わせたインデックス。列の順序が超重要。

```sql
CREATE INDEX idx_user_activity ON logs (user_id, created_at, action_type);

-- 使用可能なクエリ:
-- ✓ WHERE user_id = 100
-- ✓ WHERE user_id = 100 AND created_at >= '2025-01-01'
-- ✓ WHERE user_id = 100 AND created_at >= '2025-01-01' AND action_type = 'login'

-- 使用不可能なクエリ（左端の列がない）:
-- ✗ WHERE created_at >= '2025-01-01'
-- ✗ WHERE action_type = 'login'
```

**左端一致の原則**: 複合インデックスは左から順に使用される。

**カバリングインデックス（Covering Index）**:

クエリに必要な全ての列を含むインデックス。テーブルアクセス不要（Index-Only Scan）。

```sql
-- クエリ
SELECT user_id, created_at, action_type
FROM logs
WHERE user_id = 100 AND created_at >= '2025-01-01';

-- カバリングインデックス
CREATE INDEX idx_covering ON logs (user_id, created_at, action_type);

-- 実行計画: Index-Only Scan（テーブルアクセス0回）
```

**パーシャルインデックス（Partial Index）**:

条件付きインデックス。インデックスサイズを削減。

```sql
-- アクティブユーザーのみインデックス（全体の10%）
CREATE INDEX idx_active_users ON users (last_login_at)
WHERE status = 'active';

-- インデックスサイズが1/10に削減、更新コストも削減
```

**インデックス設計の原則**:

1. **選択性（Selectivity）の高い列を優先**: 一意性が高い列（例: user_id > status）
2. **WHERE句の列を優先**: 絞り込み条件に使われる列
3. **JOIN条件の列**: 外部キー列に必ずインデックス
4. **ORDER BY/GROUP BYの列**: ソート・集約の最適化
5. **読み取り頻度 vs 更新頻度**: 読み取り中心ならインデックス追加、書き込み中心なら最小限に

**インデックスのコスト**:

- **ストレージコスト**: インデックスはディスク容量を消費
- **書き込みコスト**: INSERT/UPDATE/DELETEで全インデックスを更新
- **メンテナンスコスト**: インデックスの断片化、再構築

#### 実用例

**例1: ECサイトの商品検索最適化**

```sql
-- テーブル定義
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(200),
    category_id INT,
    price DECIMAL(10,2),
    stock_quantity INT,
    status VARCHAR(20),  -- 'active', 'inactive', 'out_of_stock'
    created_at TIMESTAMP
);

-- クエリ1: カテゴリ別商品一覧（在庫あり、安い順）
SELECT product_id, name, price
FROM products
WHERE category_id = 5 AND status = 'active' AND stock_quantity > 0
ORDER BY price ASC
LIMIT 20;

-- 最適インデックス（複合 + パーシャル）
CREATE INDEX idx_category_price ON products (category_id, price)
WHERE status = 'active' AND stock_quantity > 0;

-- クエリ2: 商品名検索
SELECT product_id, name, price
FROM products
WHERE name LIKE '%ノートパソコン%';

-- 最適インデックス（フルテキスト）
CREATE FULLTEXT INDEX idx_product_name ON products (name);

-- フルテキスト検索に書き換え
SELECT product_id, name, price
FROM products
WHERE MATCH(name) AGAINST('ノートパソコン' IN NATURAL LANGUAGE MODE);

-- クエリ3: 管理画面での全商品一覧（ページネーション）
SELECT product_id, name, category_id, price, status
FROM products
ORDER BY created_at DESC
LIMIT 50 OFFSET 1000;

-- カバリングインデックス（Index-Only Scan）
CREATE INDEX idx_created_covering ON products (
    created_at DESC, 
    product_id, name, category_id, price, status
);
```

**例2: SaaSアプリのテナント分離クエリ最適化**

```sql
CREATE TABLE tasks (
    task_id INT PRIMARY KEY,
    tenant_id INT,
    project_id INT,
    assignee_id INT,
    status VARCHAR(20),
    priority INT,
    due_date DATE,
    created_at TIMESTAMP
);

-- 全クエリに tenant_id 条件が必須
-- クエリパターン: WHERE tenant_id = ? AND ...

-- インデックス戦略: tenant_id を先頭に
CREATE INDEX idx_tenant_project ON tasks (tenant_id, project_id, status);
CREATE INDEX idx_tenant_assignee ON tasks (tenant_id, assignee_id, due_date);
CREATE INDEX idx_tenant_created ON tasks (tenant_id, created_at DESC);

-- Row Level Security (RLS) と組み合わせ
-- テナント分離を自動化しつつ、インデックス活用
```

**例3: ログデータの時系列インデックス**

```sql
CREATE TABLE access_logs (
    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(50),
    ip_address VARCHAR(45),
    created_at TIMESTAMP,
    INDEX idx_user_time (user_id, created_at DESC),
    INDEX idx_time (created_at)
) PARTITION BY RANGE (YEAR(created_at) * 100 + MONTH(created_at)) (
    PARTITION p202501 VALUES LESS THAN (202502),
    PARTITION p202502 VALUES LESS THAN (202503),
    PARTITION p202503 VALUES LESS THAN (202504),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);

-- パーティショニング + インデックスの組み合わせ
-- 古いパーティションは削除（インデックスも自動削除）
ALTER TABLE access_logs DROP PARTITION p202501;
```

**例4: インデックス設計の失敗例と改善**

```sql
-- ❌ 悪い例: 選択性の低い列に単独インデックス
CREATE INDEX idx_status ON orders (status);  -- statusは3値のみ

-- クエリ
SELECT * FROM orders WHERE status = 'pending';
-- 全体の30%が 'pending' → フルスキャンとほぼ同等

-- ✅ 改善: 複合インデックスまたはパーシャルインデックス
CREATE INDEX idx_status_date ON orders (status, created_at);

-- または
CREATE INDEX idx_pending_orders ON orders (created_at)
WHERE status = 'pending';

-- ❌ 悪い例: 関数を使った検索
SELECT * FROM users WHERE YEAR(created_at) = 2025;
-- インデックス idx_created が使用されない

-- ✅ 改善: 範囲検索に書き換え
SELECT * FROM users WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
-- インデックス idx_created が使用される
```

#### 参考文献・リソース
- Rudolf Bayer, Edward M. McCreight, "Organization and Maintenance of Large Ordered Indices" (1970) - B-Tree発明論文
- Tapio Lahdenmaki, Michael Leach, "Relational Database Index Design and the Optimizers" (Wiley, 2005)
- Baron Schwartz, et al., "High Performance MySQL" (O'Reilly, 2012) - Chapter 5: Indexing for High Performance
- Use The Index, Luke: https://use-the-index-luke.com/ - インデックス設計の名著（オンライン無料）
- PostgreSQL Documentation: Index Types - https://www.postgresql.org/docs/current/indexes-types.html

---

### 5. ディメンショナルモデリング（Dimensional Modeling）

#### 分類
- **データウェアハウス・OLAP系**
- **分析システム設計**

#### 出典・背景
- **提唱者**: Ralph Kimball
- **出典**: "The Data Warehouse Toolkit" (Wiley, 1996, 2013第3版)
- **背景**: OLTP（トランザクション処理）に最適化された正規化モデルは、OLAP（分析処理）には不向きでした。Ralph Kimballは、ビジネスユーザーが直感的に理解できる「ディメンション（次元）」の概念を用いた分析特化型のモデリング手法を提唱しました。

#### 理論の詳細

**ディメンショナルモデリングの基本概念**:

**ファクトテーブル（Fact Table）**:
- **定義**: 測定可能なビジネスイベントを記録するテーブル
- **内容**: 
  - 数値データ（メトリクス、KPI）: 売上金額、数量、利益
  - 外部キー: ディメンションテーブルへの参照
- **特徴**: 
  - 行数が超多数（数億〜数兆レコード）
  - 挿入中心（ほぼ更新なし）
  - 非正規化

**ディメンションテーブル（Dimension Table）**:
- **定義**: ビジネスの「次元」を表現するテーブル
- **内容**: 
  - 記述的属性: 商品名、カテゴリ、顧客名、地域
  - 階層構造: 日→月→四半期→年
- **特徴**: 
  - 行数は相対的に少ない（数千〜数万レコード）
  - 非正規化（階層を平坦化）
  - ゆっくり変化するディメンション（SCD）

**スタースキーマ（Star Schema）**:
- **構造**: 中央にファクトテーブル、周囲にディメンションテーブルを配置（星型）
- **特徴**: 
  - シンプルなJOIN（ファクト→ディメンション）
  - 高速なクエリ実行
  - ビジネスユーザーにとって理解しやすい
- **欠点**: ディメンションテーブルが非正規化（冗長性あり）

**スノーフレークスキーマ（Snowflake Schema）**:
- **構造**: ディメンションテーブルを正規化（階層構造を分離）
- **特徴**: 
  - ストレージ効率が良い
  - JOINが複雑化（ファクト→ディメンション→サブディメンション）
  - クエリパフォーマンスがスタースキーマより劣る
- **使用場面**: ストレージコストが重要な場合

**ファクトテーブルの種類**:

1. **トランザクションファクト**: 個別イベント（注文、ログイン、クリック）
2. **ピリオディックスナップショット**: 定期的な状態（日次在庫、月末残高）
3. **アキュムレーティングスナップショット**: プロセスの進行（注文→出荷→配送→完了）

**ゆっくり変化するディメンション（SCD: Slowly Changing Dimension）**:

ディメンションの属性が時間とともに変化する場合の対処法。

- **Type 0**: 変更しない（固定値）
- **Type 1**: 上書き（履歴保持なし）
- **Type 2**: 履歴保持（新レコード追加、有効期間を記録）
- **Type 3**: 限定的な履歴（前の値を別列で保持）

**ディメンショナルモデリングの設計ステップ**:

1. **ビジネスプロセスの選択**: 分析対象のビジネスイベント（例: 販売、在庫管理）
2. **粒度の決定**: ファクトテーブルの1行が表す詳細度（例: 1注文明細行）
3. **ディメンションの特定**: 分析軸（時間、商品、顧客、店舗など）
4. **ファクトの特定**: 測定したい数値（売上、数量、利益）

#### 実用例

**例1: 小売業の販売分析（スタースキーマ）**

```sql
-- ファクトテーブル: 販売実績
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,              -- 日付ディメンションへの外部キー
    product_key INT,           -- 商品ディメンションへの外部キー
    store_key INT,             -- 店舗ディメンションへの外部キー
    customer_key INT,          -- 顧客ディメンションへの外部キー
    promotion_key INT,         -- プロモーションディメンションへの外部キー
    quantity INT,              -- ファクト: 数量
    unit_price DECIMAL(10,2),  -- ファクト: 単価
    revenue DECIMAL(10,2),     -- ファクト: 売上
    cost DECIMAL(10,2),        -- ファクト: 原価
    profit DECIMAL(10,2),      -- ファクト: 利益
    INDEX idx_date (date_key),
    INDEX idx_product (product_key),
    INDEX idx_store (store_key),
    INDEX idx_customer (customer_key)
) PARTITION BY RANGE (date_key) (
    PARTITION p2024 VALUES LESS THAN (20250101),
    PARTITION p2025 VALUES LESS THAN (20260101)
);

-- ディメンションテーブル: 日付
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,  -- 20250115
    full_date DATE,            -- 2025-01-15
    day_of_week VARCHAR(10),   -- Wednesday
    day_of_month INT,          -- 15
    week_of_year INT,          -- 3
    month INT,                 -- 1
    month_name VARCHAR(10),    -- January
    quarter INT,               -- 1
    year INT,                  -- 2025
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    fiscal_year INT,           -- 2025
    fiscal_quarter INT         -- Q1
);

-- ディメンションテーブル: 商品（非正規化）
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    product_id VARCHAR(50),       -- ビジネスキー
    product_name VARCHAR(200),
    brand VARCHAR(100),
    category VARCHAR(100),        -- 非正規化: 本来は別テーブル
    subcategory VARCHAR(100),     -- 非正規化
    department VARCHAR(100),      -- 非正規化（階層構造を平坦化）
    unit_cost DECIMAL(10,2),
    is_active BOOLEAN,
    effective_date DATE,          -- SCD Type 2: 有効開始日
    expiry_date DATE              -- SCD Type 2: 有効終了日
);

-- ディメンションテーブル: 店舗
CREATE TABLE dim_store (
    store_key INT PRIMARY KEY AUTO_INCREMENT,
    store_id VARCHAR(50),
    store_name VARCHAR(100),
    store_type VARCHAR(50),      -- 直営店、FC店
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    region VARCHAR(50),          -- 非正規化: 東日本、西日本
    district VARCHAR(50),        -- 非正規化: 関東、関西
    open_date DATE,
    store_size VARCHAR(20),      -- Small, Medium, Large
    manager_name VARCHAR(100)
);

-- ディメンションテーブル: 顧客（SCD Type 2）
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(50),     -- ビジネスキー
    customer_name VARCHAR(100),
    email VARCHAR(100),
    gender VARCHAR(10),
    age_range VARCHAR(20),       -- 20-29, 30-39
    customer_segment VARCHAR(50), -- VIP, Regular, New
    registration_date DATE,
    effective_date DATE,         -- SCD Type 2
    expiry_date DATE,            -- SCD Type 2
    is_current BOOLEAN           -- 現在有効なレコード
);

-- 分析クエリ例1: 月別カテゴリ別売上
SELECT 
    d.year,
    d.month_name,
    p.category,
    SUM(f.revenue) AS total_revenue,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE d.year = 2025
GROUP BY d.year, d.month_name, p.category
ORDER BY d.month, total_revenue DESC;

-- 分析クエリ例2: 地域別店舗タイプ別売上（階層ドリルダウン）
SELECT 
    s.region,
    s.district,
    s.store_type,
    COUNT(DISTINCT s.store_key) AS store_count,
    SUM(f.revenue) AS total_revenue,
    AVG(f.revenue) AS avg_revenue_per_transaction
FROM fact_sales f
JOIN dim_store s ON f.store_key = s.store_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2025 AND d.quarter = 1
GROUP BY s.region, s.district, s.store_type
ORDER BY s.region, total_revenue DESC;

-- 分析クエリ例3: 顧客セグメント別購買傾向
SELECT 
    c.customer_segment,
    p.category,
    COUNT(DISTINCT f.customer_key) AS customer_count,
    SUM(f.revenue) AS total_revenue,
    AVG(f.revenue) AS avg_order_value,
    SUM(f.quantity) AS total_quantity
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE c.is_current = TRUE  -- 最新の顧客情報のみ
GROUP BY c.customer_segment, p.category
ORDER BY total_revenue DESC;
```

**例2: SCD Type 2の実装（顧客住所変更の履歴管理）**

```sql
-- 初期レコード（2025-01-01に登録）
INSERT INTO dim_customer VALUES (
    1, 'C001', '山田太郎', 'yamada@example.com', 'Male', '30-39',
    'Regular', '2025-01-01', '2025-01-01', '9999-12-31', TRUE
);

-- 2025-06-15に住所変更（SCD Type 2: 新レコード追加）
-- 1. 既存レコードを失効
UPDATE dim_customer
SET expiry_date = '2025-06-14', is_current = FALSE
WHERE customer_id = 'C001' AND is_current = TRUE;

-- 2. 新レコードを挿入
INSERT INTO dim_customer VALUES (
    2, 'C001', '山田太郎', 'yamada@example.com', 'Male', '40-49',  -- 年齢レンジ変更
    'VIP', '2025-01-01', '2025-06-15', '9999-12-31', TRUE
);

-- 履歴を含めた分析が可能
-- 質問: 2025-03-15時点で「Regular」だった顧客の購買額は？
SELECT SUM(f.revenue)
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.full_date = '2025-03-15'
  AND c.customer_segment = 'Regular'
  AND c.effective_date <= '2025-03-15'
  AND c.expiry_date >= '2025-03-15';
```

**例3: アキュムレーティングスナップショットファクト（注文ライフサイクル）**

```sql
CREATE TABLE fact_order_lifecycle (
    order_key INT PRIMARY KEY,
    order_date_key INT,
    payment_date_key INT,
    shipment_date_key INT,
    delivery_date_key INT,
    customer_key INT,
    product_key INT,
    warehouse_key INT,
    carrier_key INT,
    order_amount DECIMAL(10,2),
    days_to_payment INT,        -- 注文から支払いまでの日数
    days_to_shipment INT,       -- 注文から出荷までの日数
    days_to_delivery INT,       -- 注文から配送までの日数
    is_on_time_delivery BOOLEAN,
    INDEX idx_order_date (order_date_key),
    INDEX idx_customer (customer_key)
);

-- レコードは注文時に挿入され、各マイルストーンで更新される
-- 注文時
INSERT INTO fact_order_lifecycle (order_key, order_date_key, customer_key, order_amount)
VALUES (123, 20250115, 456, 15000);

-- 支払い完了時
UPDATE fact_order_lifecycle
SET payment_date_key = 20250115, days_to_payment = 0
WHERE order_key = 123;

-- 出荷時
UPDATE fact_order_lifecycle
SET shipment_date_key = 20250116, days_to_shipment = 1
WHERE order_key = 123;

-- 配送完了時
UPDATE fact_order_lifecycle
SET delivery_date_key = 20250118, days_to_delivery = 3,
    is_on_time_delivery = (days_to_delivery <= 3)
WHERE order_key = 123;

-- 分析: 配送リードタイム分析
SELECT 
    AVG(days_to_delivery) AS avg_delivery_days,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY days_to_delivery) AS p95_delivery_days,
    SUM(CASE WHEN is_on_time_delivery THEN 1 ELSE 0 END) / COUNT(*) AS on_time_rate
FROM fact_order_lifecycle
WHERE order_date_key >= 20250101;
```

#### 参考文献・リソース
- Ralph Kimball, Margy Ross, "The Data Warehouse Toolkit" (Wiley, 3rd Edition, 2013)
- Ralph Kimball, et al., "The Kimball Group Reader" (Wiley, 2016)
- Kimball Group: https://www.kimballgroup.com/ - 無料記事多数
- Dimensional Modeling Techniques: https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/

---

### 6. CQRS（Command Query Responsibility Segregation）

#### 分類
- **アーキテクチャパターン系**
- **分散システム設計・スケーラビリティ**

#### 出典・背景
- **提唱者**: Greg Young、Udi Dahan
- **出典**: Greg Young, "CQRS Documents" (2010), Martin Fowler, "CQRS" (2011)
- **背景**: CQRSは、Bertrand Meyerの「コマンドとクエリの分離（CQS: Command-Query Separation）」原則をシステムアーキテクチャレベルに拡張したパターンです。読み取りと書き込みの要件が大きく異なる複雑なドメインで、両者を別々に最適化することを目的とします。

#### 理論の詳細

**CQRSの基本原則**:

**コマンド（Command）**: 状態を変更する操作
- 例: CreateOrder, UpdateInventory, DeleteUser
- 特性: 副作用あり、返り値なし（または成功/失敗のみ）
- 最適化目標: 整合性、トランザクション

**クエリ（Query）**: 状態を取得する操作
- 例: GetOrderById, ListProducts, SearchCustomers
- 特性: 副作用なし、データを返す
- 最適化目標: パフォーマンス、スケーラビリティ

**CQRSの実装パターン**:

**1. シンプルCQRS**: 
- コマンドモデルとクエリモデルを同じデータベースで分離
- コマンド: 正規化されたテーブル（書き込み最適化）
- クエリ: 非正規化されたビュー、マテリアライズドビュー（読み取り最適化）

**2. 完全分離CQRS**:
- コマンドモデル: 書き込み専用データベース（PostgreSQL, MySQL）
- クエリモデル: 読み取り専用データベース（Elasticsearch, Redis, MongoDB）
- 同期: イベント駆動、メッセージキュー

**3. Event Sourcingとの組み合わせ**:
- コマンド: イベントストアに書き込み
- クエリ: イベントから投影（Projection）された読み取りモデル

**CQRSのメリット**:

1. **独立した最適化**: 読み取りと書き込みを別々にスケール
2. **複雑なクエリの簡素化**: 非正規化で複雑なJOINを排除
3. **パフォーマンス向上**: 読み取りに最適なデータ構造（キャッシュ、検索エンジン）
4. **明確な責任分離**: コマンドとクエリのロジック分離
5. **柔軟なスケーリング**: 読み取りレプリカを独立してスケール

**CQRSのデメリット**:

1. **複雑性の増加**: システム全体の理解が困難
2. **結果整合性**: コマンド実行後、クエリモデルへの反映に遅延
3. **データ同期の課題**: コマンドモデルとクエリモデルの整合性維持
4. **運用コスト**: 複数のデータストアの管理

**適用場面**:

- 読み取り/書き込み比率が極端に偏っている（100:1以上）
- 読み取りクエリが非常に複雑（多数のJOIN、集計）
- 異なるユーザーグループで読み取り要件が大きく異なる
- 高いパフォーマンスとスケーラビリティが要求される

#### 実用例

**例1: ECサイトの商品カタログ（シンプルCQRS）**

```sql
-- コマンドモデル（正規化、書き込み最適化）
CREATE TABLE products_write (
    product_id INT PRIMARY KEY,
    name VARCHAR(200),
    description TEXT,
    category_id INT,
    brand_id INT,
    price DECIMAL(10,2),
    stock_quantity INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
);

CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100),
    parent_category_id INT
);

CREATE TABLE brands (
    brand_id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- クエリモデル（非正規化、読み取り最適化）
CREATE MATERIALIZED VIEW products_read AS
SELECT 
    p.product_id,
    p.name,
    p.description,
    p.price,
    p.stock_quantity,
    c.name AS category_name,
    pc.name AS parent_category_name,
    b.name AS brand_name,
    p.created_at,
    CONCAT(p.name, ' ', c.name, ' ', b.name) AS search_text  -- 全文検索用
FROM products_write p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN categories pc ON c.parent_category_id = pc.category_id
JOIN brands b ON p.brand_id = b.brand_id;

CREATE INDEX idx_search ON products_read USING GIN(to_tsvector('english', search_text));
CREATE INDEX idx_category ON products_read (category_name);
CREATE INDEX idx_brand ON products_read (brand_name);

-- コマンド: 商品更新
UPDATE products_write
SET name = '新商品名', price = 5000, updated_at = NOW()
WHERE product_id = 123;

-- マテリアライズドビューの更新（定期実行またはトリガー）
REFRESH MATERIALIZED VIEW products_read;

-- クエリ: 商品検索（超高速）
SELECT product_id, name, category_name, brand_name, price
FROM products_read
WHERE to_tsvector('english', search_text) @@ to_tsquery('laptop')
  AND price BETWEEN 50000 AND 100000
ORDER BY created_at DESC;
```

**例2: SaaSアプリケーションの完全分離CQRS**

```python
# コマンドモデル（PostgreSQL）
class CreateOrderCommand:
    def __init__(self, user_id, items, shipping_address):
        self.user_id = user_id
        self.items = items
        self.shipping_address = shipping_address

class OrderCommandHandler:
    def handle(self, command: CreateOrderCommand):
        # 1. トランザクション処理（PostgreSQL）
        with db.transaction():
            order = Order.create(
                user_id=command.user_id,
                items=command.items,
                shipping_address=command.shipping_address
            )
            order.save()
            
            # 2. 在庫引き当て
            for item in command.items:
                inventory = Inventory.get(item.product_id)
                inventory.reserve(item.quantity)
                inventory.save()
            
            # 3. イベント発行（メッセージキュー）
            event = OrderCreatedEvent(
                order_id=order.id,
                user_id=order.user_id,
                total_amount=order.total_amount,
                items=order.items
            )
            event_bus.publish(event)

# クエリモデル（Elasticsearch）
class OrderQueryHandler:
    def get_user_orders(self, user_id, page=1, per_page=20):
        # Elasticsearchから読み取り
        result = es.search(
            index='orders',
            body={
                'query': {
                    'term': {'user_id': user_id}
                },
                'sort': [{'created_at': 'desc'}],
                'from': (page - 1) * per_page,
                'size': per_page
            }
        )
        return result['hits']['hits']

# イベントハンドラー（データ同期）
class OrderCreatedEventHandler:
    def handle(self, event: OrderCreatedEvent):
        # PostgreSQL → Elasticsearch へ同期
        order_document = {
            'order_id': event.order_id,
            'user_id': event.user_id,
            'total_amount': event.total_amount,
            'items': [
                {
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'quantity': item.quantity,
                    'price': item.price
                }
                for item in event.items
            ],
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        es.index(index='orders', id=event.order_id, body=order_document)

# API レイヤー
@app.post('/api/orders')
def create_order(request):
    command = CreateOrderCommand(
        user_id=request.user_id,
        items=request.items,
        shipping_address=request.shipping_address
    )
    order_command_handler.handle(command)
    return {'message': 'Order created successfully'}, 202

@app.get('/api/users/<user_id>/orders')
def get_user_orders(user_id, page=1):
    orders = order_query_handler.get_user_orders(user_id, page)
    return {'orders': orders}, 200
```

**例3: CQRSとEvent Sourcingの組み合わせ（銀行口座システム）**

```sql
-- イベントストア（コマンドモデル）
CREATE TABLE account_events (
    event_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id VARCHAR(50),
    event_type VARCHAR(50),  -- AccountCreated, MoneyDeposited, MoneyWithdrawn
    event_data JSON,
    created_at TIMESTAMP,
    INDEX idx_account (account_id, event_id)
);

-- クエリモデル（投影）
CREATE TABLE account_balances (
    account_id VARCHAR(50) PRIMARY KEY,
    current_balance DECIMAL(15,2),
    last_event_id BIGINT,
    last_updated_at TIMESTAMP
);

CREATE TABLE account_transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id VARCHAR(50),
    transaction_type VARCHAR(20),  -- deposit, withdrawal
    amount DECIMAL(15,2),
    balance_after DECIMAL(15,2),
    created_at TIMESTAMP,
    INDEX idx_account_time (account_id, created_at)
);

-- コマンド: 入金
INSERT INTO account_events (account_id, event_type, event_data, created_at)
VALUES ('ACC123', 'MoneyDeposited', '{"amount": 10000, "source": "ATM"}', NOW());

-- イベントハンドラー: クエリモデルへの投影
DELIMITER $$
CREATE TRIGGER project_account_events
AFTER INSERT ON account_events
FOR EACH ROW
BEGIN
    IF NEW.event_type = 'MoneyDeposited' THEN
        UPDATE account_balances
        SET current_balance = current_balance + JSON_EXTRACT(NEW.event_data, '$.amount'),
            last_event_id = NEW.event_id,
            last_updated_at = NEW.created_at
        WHERE account_id = NEW.account_id;
        
        INSERT INTO account_transactions (account_id, transaction_type, amount, balance_after, created_at)
        SELECT NEW.account_id, 'deposit', 
               JSON_EXTRACT(NEW.event_data, '$.amount'),
               current_balance,
               NEW.created_at
        FROM account_balances
        WHERE account_id = NEW.account_id;
        
    ELSEIF NEW.event_type = 'MoneyWithdrawn' THEN
        -- 同様の処理
    END IF;
END$$
DELIMITER ;

-- クエリ: 口座残高照会（超高速）
SELECT current_balance, last_updated_at
FROM account_balances
WHERE account_id = 'ACC123';

-- クエリ: 取引履歴（ページネーション）
SELECT transaction_id, transaction_type, amount, balance_after, created_at
FROM account_transactions
WHERE account_id = 'ACC123'
ORDER BY created_at DESC
LIMIT 50;

-- 特殊クエリ: 任意時点の残高再構築（イベントソーシングの強み）
SELECT SUM(
    CASE 
        WHEN event_type = 'MoneyDeposited' THEN JSON_EXTRACT(event_data, '$.amount')
        WHEN event_type = 'MoneyWithdrawn' THEN -JSON_EXTRACT(event_data, '$.amount')
        ELSE 0
    END
) AS balance_at_time
FROM account_events
WHERE account_id = 'ACC123' AND created_at <= '2025-01-15 23:59:59';
```

#### 参考文献・リソース
- Greg Young, "CQRS Documents" (2010) - https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf
- Martin Fowler, "CQRS" (2011) - https://martinfowler.com/bliki/CQRS.html
- Udi Dahan, "Clarified CQRS" - https://udidahan.com/2009/12/09/clarified-cqrs/
- Microsoft, "CQRS pattern" - https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs
- Event Store: https://www.eventstore.com/ - CQRSとEvent Sourcingの専用データベース

---

### 7. データベースシャーディング（Database Sharding）

#### 分類
- **スケーラビリティパターン系**
- **分散システム設計・水平スケーリング**

#### 出典・背景
- **背景**: 単一データベースサーバーのスケーラビリティ限界を突破するため、Google、Facebook、Twitterなどの大規模Webサービスが採用した水平パーティショニング技法です。シャーディングは、データを複数のデータベースサーバー（シャード）に分散させ、並列処理によってスケーラビリティを実現します。
- **大規模事例**: 
  - Instagram: シャーディングで10億ユーザー対応
  - Twitter: Gizzardフレームワークでシャーディング実装

#### 理論の詳細

**シャーディングの基本概念**:

**シャード（Shard）**: データベース全体を分割した個々のデータベースインスタンス

**シャーディングキー（Sharding Key）**: データをどのシャードに配置するかを決定するキー（例: user_id, tenant_id）

**シャーディング戦略**:

**1. レンジベースシャーディング（Range-based Sharding）**:
- **方法**: シャーディングキーの範囲でデータを分割
- **例**: 
  - user_id 1-1000000 → Shard 1
  - user_id 1000001-2000000 → Shard 2
- **メリット**: 範囲検索が効率的
- **デメリット**: データ分布が不均等になりやすい（ホットスポット）

**2. ハッシュベースシャーディング（Hash-based Sharding）**:
- **方法**: シャーディングキーをハッシュ関数で変換し、シャード番号を決定
- **例**: `shard_id = hash(user_id) % num_shards`
- **メリット**: データが均等に分散
- **デメリット**: 範囲検索が困難、シャード追加時に大規模なデータ移動

**3. 地理ベースシャーディング（Geo-based Sharding）**:
- **方法**: 地理的位置でシャードを分割
- **例**: 
  - 日本ユーザー → Asia Shard
  - 米国ユーザー → US Shard
- **メリット**: レイテンシー削減、データ主権対応
- **デメリット**: グローバルクエリが複雑

**4. ディレクトリベースシャーディング（Directory-based Sharding）**:
- **方法**: ルックアップテーブルで各キーのシャード位置を管理
- **例**: `shard_directory` テーブルで `user_id → shard_id` をマッピング
- **メリット**: 柔軟なシャード配置、動的な移動が容易
- **デメリット**: ディレクトリがボトルネックになる可能性

**一貫性ハッシュ（Consistent Hashing）**:

シャード追加・削除時のデータ移動を最小化する技法。

- **通常のハッシュ**: シャード数変更時、ほぼ全データを移動
- **一貫性ハッシュ**: シャード数変更時、平均 `1/n` のデータのみ移動

**シャーディングの課題**:

1. **クロスシャードクエリ**: 複数シャードにまたがるクエリは遅い
2. **トランザクション**: 複数シャードにまたがる分散トランザクション（2PC）は複雑
3. **外部キー制約**: 異なるシャード間の外部キー制約は実装困難
4. **リシャーディング**: シャード追加・削除時のデータ移行コスト
5. **運用複雑性**: 複数データベースの監視・バックアップ・復旧

**シャーディング設計の原則**:

1. **シャーディングキーの選択**:
   - 均等分散（データ、アクセス頻度）
   - クロスシャードクエリ最小化
   - 不変性（変更されない列）
2. **シャード数の決定**:
   - 初期: 控えめな数（2-4個）
   - 将来の成長を考慮
   - 2の累乗が管理しやすい
3. **シャード配置戦略**:
   - マスター/レプリカ構成
   - 地理的分散
   - 冗長性確保

#### 実用例

**例1: SaaSアプリケーションのテナントシャーディング**

```python
# シャーディング設定
SHARDS = {
    'shard_1': 'postgresql://db1.example.com:5432/shard1',
    'shard_2': 'postgresql://db2.example.com:5432/shard2',
    'shard_3': 'postgresql://db3.example.com:5432/shard3',
    'shard_4': 'postgresql://db4.example.com:5432/shard4',
}

# ハッシュベースシャーディング
def get_shard_for_tenant(tenant_id):
    shard_index = hash(tenant_id) % len(SHARDS)
    shard_key = f'shard_{shard_index + 1}'
    return SHARDS[shard_key]

# 各シャードのテーブル構造は同一
# Shard 1, 2, 3, 4 全てに同じスキーマ
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    tenant_id VARCHAR(50),
    username VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP,
    INDEX idx_tenant (tenant_id)
);

CREATE TABLE projects (
    project_id BIGINT PRIMARY KEY,
    tenant_id VARCHAR(50),
    name VARCHAR(200),
    created_at TIMESTAMP,
    INDEX idx_tenant (tenant_id)
);

# アプリケーション層でシャーディングロジック
class UserRepository:
    def get_user(self, tenant_id, user_id):
        shard = get_shard_for_tenant(tenant_id)
        connection = get_connection(shard)
        result = connection.execute(
            "SELECT * FROM users WHERE tenant_id = %s AND user_id = %s",
            (tenant_id, user_id)
        )
        return result.fetchone()
    
    def get_users_by_tenant(self, tenant_id):
        # テナント内検索はシングルシャードクエリ（高速）
        shard = get_shard_for_tenant(tenant_id)
        connection = get_connection(shard)
        result = connection.execute(
            "SELECT * FROM users WHERE tenant_id = %s",
            (tenant_id,)
        )
        return result.fetchall()
    
    def search_users_globally(self, email):
        # グローバル検索はクロスシャードクエリ（遅い）
        results = []
        for shard in SHARDS.values():
            connection = get_connection(shard)
            result = connection.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            results.extend(result.fetchall())
        return results
```

**例2: SNSアプリのユーザーベースシャーディング（一貫性ハッシュ）**

```python
import hashlib

class ConsistentHashRing:
    def __init__(self, nodes, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []
        for node in nodes:
            self.add_node(node)
    
    def add_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = int(hashlib.md5(virtual_key.encode()).hexdigest(), 16)
            self.ring[hash_value] = node
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key):
        hash_value = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        for ring_key in self.sorted_keys:
            if hash_value <= ring_key:
                return self.ring[ring_key]
        return self.ring[self.sorted_keys[0]]  # ループバック

# シャードノード
shards = ['shard_1', 'shard_2', 'shard_3', 'shard_4']
hash_ring = ConsistentHashRing(shards)

# ユーザーIDからシャードを決定
user_id = 123456
shard = hash_ring.get_node(user_id)
print(f"User {user_id} -> {shard}")

# シャード追加時のデータ移動量
# 通常のハッシュ: 4 → 5シャード = 80%のデータ移動
# 一貫性ハッシュ: 4 → 5シャード = 20%のデータ移動のみ
```

**例3: レンジベースシャーディング + 自動リバランシング（Instagram風）**

```sql
-- シャーディングディレクトリ（メタデータDB）
CREATE TABLE shard_mappings (
    shard_id INT PRIMARY KEY,
    shard_name VARCHAR(50),
    db_host VARCHAR(255),
    db_port INT,
    min_user_id BIGINT,
    max_user_id BIGINT,
    status VARCHAR(20),  -- active, migrating, readonly
    created_at TIMESTAMP
);

-- 初期シャード配置
INSERT INTO shard_mappings VALUES
(1, 'shard_1', 'db1.example.com', 5432, 1, 5000000, 'active', NOW()),
(2, 'shard_2', 'db2.example.com', 5432, 5000001, 10000000, 'active', NOW()),
(3, 'shard_3', 'db3.example.com', 5432, 10000001, 15000000, 'active', NOW());

-- ユーザーIDからシャードを検索
SELECT shard_name, db_host, db_port
FROM shard_mappings
WHERE 7500000 BETWEEN min_user_id AND max_user_id
  AND status = 'active';

-- リバランシング: Shard 2 を分割 (5M-10M → 5M-7.5M + 7.5M-10M)
-- 1. 新シャード追加
INSERT INTO shard_mappings VALUES
(4, 'shard_4', 'db4.example.com', 5432, 7500001, 10000000, 'migrating', NOW());

-- 2. 既存シャードの範囲変更
UPDATE shard_mappings
SET max_user_id = 7500000, status = 'migrating'
WHERE shard_id = 2;

-- 3. データ移行（バックグラウンド）
-- Shard 2 から Shard 4 へ user_id 7500001-10000000 のデータをコピー

-- 4. 移行完了後、ステータス更新
UPDATE shard_mappings SET status = 'active' WHERE shard_id IN (2, 4);
```

**例4: クロスシャードクエリの最適化（Scatter-Gather）**

```python
import concurrent.futures

def scatter_gather_query(query, params, timeout=5):
    """全シャードに並列クエリを実行し、結果を集約"""
    results = []
    
    def query_shard(shard):
        connection = get_connection(shard)
        try:
            result = connection.execute(query, params)
            return result.fetchall()
        except Exception as e:
            logger.error(f"Shard {shard} query failed: {e}")
            return []
    
    # 並列実行
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SHARDS)) as executor:
        futures = {executor.submit(query_shard, shard): shard for shard in SHARDS.values()}
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            shard = futures[future]
            try:
                results.extend(future.result())
            except Exception as e:
                logger.error(f"Failed to get result from {shard}: {e}")
    
    return results

# 使用例: 全シャードから最新投稿を検索
all_posts = scatter_gather_query(
    "SELECT * FROM posts WHERE created_at >= %s ORDER BY created_at DESC LIMIT 100",
    ('2025-01-01',)
)

# マージソート（各シャードの結果は既にソート済み）
all_posts.sort(key=lambda x: x['created_at'], reverse=True)
top_100 = all_posts[:100]
```

#### 参考文献・リソース
- Alex Petrov, "Database Internals" (O'Reilly, 2019) - Chapter 12: Sharding
- Martin Kleppmann, "Designing Data-Intensive Applications" (O'Reilly, 2017) - Chapter 6: Partitioning
- Pinterest Engineering, "Sharding Pinterest: How we scaled our MySQL fleet" (2015)
- Instagram Engineering, "Sharding & IDs at Instagram" (2012)
- Vitess: https://vitess.io/ - MySQLのシャーディングミドルウェア（YouTube発）
- Citus Data: https://www.citusdata.com/ - PostgreSQLのシャーディング拡張

---

## フレームワーク選択ガイド

| 設計目標 | 推奨フレームワーク（優先順） | 適用場面 |
|---------|---------------------------|---------|
| **トランザクション処理（OLTP）** | ER図 → 正規化（3NF/BCNF） → インデックス戦略 | 銀行、EC、SaaS、業務システム |
| **分析処理（OLAP）** | ディメンショナルモデリング → 非正規化 → サマリーテーブル | データウェアハウス、BI、レポート |
| **高トラフィック・読み取り中心** | CQRS → 非正規化 → リードレプリカ | SNS、メディア、コンテンツ配信 |
| **超大規模データ** | シャーディング → パーティショニング → インデックス最適化 | グローバルSaaS、IoT、ログ分析 |
| **履歴管理・監査** | 正規化 → SCD Type 2 → Event Sourcing | 金融、医療、コンプライアンス |
| **マルチテナント** | シャーディング（テナントキー） → Row Level Security | SaaS、プラットフォーム |
| **地理分散** | 地理ベースシャーディング → リードレプリカ | グローバルサービス |
| **複雑なドメインロジック** | CQRS → ディメンショナルモデリング | エンタープライズ、複雑な分析 |

---

## 統合的な活用例: ECサイトの包括的データベース設計

### フェーズ1: トランザクション処理（OLTP）
- **ER図**で要件整理
- **正規化（3NF）**で整合性確保
- **インデックス戦略**でクエリ最適化
- **外部キー制約**でデータ整合性保証

### フェーズ2: スケーリング（成長期）
- **リードレプリカ**で読み取り負荷分散
- **パーティショニング**で大規模データ管理
- **非正規化**（商品検索用）でパフォーマンス向上

### フェーズ3: 高度な分析（成熟期）
- **ディメンショナルモデリング**でデータウェアハウス構築
- **CQRS**でOLTPとOLAPを分離
- **マテリアライズドビュー**でレポート高速化

### フェーズ4: グローバル展開
- **シャーディング**（地理ベース）で地域別分散
- **マルチマスターレプリケーション**で可用性向上

---

## 参考資料

### 書籍
1. C.J. Date, "An Introduction to Database Systems" (Addison-Wesley, 2003)
2. Ramez Elmasri, Shamkant B. Navathe, "Fundamentals of Database Systems" (Pearson, 7th Edition, 2015)
3. Ralph Kimball, Margy Ross, "The Data Warehouse Toolkit" (Wiley, 3rd Edition, 2013)
4. Martin Kleppmann, "Designing Data-Intensive Applications" (O'Reilly, 2017)
5. Alex Petrov, "Database Internals" (O'Reilly, 2019)
6. Baron Schwartz, et al., "High Performance MySQL" (O'Reilly, 2012)

### オンラインリソース
- Use The Index, Luke: https://use-the-index-luke.com/
- Kimball Group: https://www.kimballgroup.com/
- Database Design Tutorial: https://www.guru99.com/database-design.html
- PostgreSQL Documentation: https://www.postgresql.org/docs/

### ツール
- ER図作成: dbdiagram.io, Lucidchart, draw.io, ERDPlus
- クエリ最適化: pgAdmin, MySQL Workbench, DataGrip
- シャーディング: Vitess, Citus, ProxySQL
- データウェアハウス: Snowflake, BigQuery, Redshift

---

## まとめ

データベース設計は、ビジネス要件、データ特性、パフォーマンス要件、スケーラビリティ要件のバランスを取る総合的なエンジニアリング活動です。本ドキュメントで紹介した7つのフレームワークは、それぞれ異なる設計目標に対応しています。

- **ER図**と**正規化理論**で確固たる基礎設計
- **非正規化**と**インデックス戦略**でパフォーマンス最適化
- **ディメンショナルモデリング**で分析基盤構築
- **CQRS**で読み取り/書き込みの独立最適化
- **シャーディング**で無限のスケーラビリティ

実務では、これらのフレームワークを組み合わせ、トレードオフを理解した上で、最適な設計判断を下すことが重要です。
