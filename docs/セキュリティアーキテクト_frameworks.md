# セキュリティアーキテクト - フレームワーク・理論詳解

## 概要

セキュリティアーキテクトオーケストレーターは、ゼロトラスト、多層防御、脅威モデリング、暗号化戦略など、現代のサイバーセキュリティに必要な包括的なフレームワークを統合した対話型AIシステムです。境界防御からクラウドセキュリティ、コンプライアンス対応まで、システム全体のセキュリティ設計を支援します。

### 特徴
- ゼロトラストから多層防御まで、現代的なセキュリティモデルを網羅
- 認証・認可、暗号化、ネットワークセキュリティの実装戦略
- STRIDE、DREAD、Attack Treeによる体系的な脅威モデリング
- OWASP Top 10対策、API セキュリティなどアプリケーション防御
- GDPR、PCI DSS、ISO 27001などコンプライアンス対応
- 実装可能なセキュリティアーキテクチャ図、ポリシー、コード例を提供

---

## 組み込まれているフレームワーク・理論

### 1. ゼロトラスト (Zero Trust)

#### 分類
- **セキュリティモデル・アーキテクチャ系**
- **境界防御を超えた包括的防御**

#### 出典・背景
- **提唱者**: John Kindervag (Forrester Research)
- **出典**: "Build Security Into Your Network's DNA: The Zero Trust Network Architecture" (2010)
- **背景**: 従来の「境界防御（Castle-and-Moat）」モデルは、内部ネットワークを信頼ゾーンとして扱っていました。しかし、クラウド化、リモートワーク、サプライチェーン攻撃の増加により、「境界の内側にいる = 信頼できる」という前提が崩壊しました。2010年にForrester ResearchのJohn Kindervagが提唱したゼロトラストは、「決して信頼せず、常に検証する (Never Trust, Always Verify)」という原則に基づく新しいセキュリティモデルです。

#### 理論の詳細

**ゼロトラストの核心原則**:

1. **暗黙の信頼を前提としない**: ネットワーク境界の内外を問わず、全てのアクセスを検証
2. **最小権限アクセス (Least Privilege Access)**: 必要最小限の権限のみを付与
3. **マイクロセグメンテーション**: ネットワークを細かく分割し、侵害の拡大を防ぐ
4. **継続的な検証**: アクセス許可後も継続的に信頼性を評価
5. **全トラフィックの可視化**: ログ・監視による異常検知

**ゼロトラストの主要要素**:

**1. ID検証 (Identity Verification)**:
- 強力な認証: 多要素認証 (MFA)、生体認証
- ユーザーコンテキスト: 位置情報、時間、デバイス状態
- 継続的認証: セッション中の行動分析

**2. デバイス検証 (Device Verification)**:
- デバイス登録: 管理対象デバイスのみアクセス許可
- セキュリティ態勢評価: OS パッチレベル、アンチウイルス状態
- デバイスヘルスチェック: ジェイルブレイク検出、コンプライアンス確認

**3. ネットワーク分離 (Network Segmentation)**:
- マイクロセグメンテーション: ワークロード単位でのセグメント分離
- ソフトウェア定義境界 (SDP): アプリケーションレベルの隠蔽
- VLANとファイアウォール: 論理的・物理的分離

**4. データ保護 (Data Protection)**:
- 暗号化: 転送時・保存時の暗号化
- DLP (Data Loss Prevention): データ流出防止
- ラベル付けと分類: データの機密性レベル管理

**5. 可視化と分析 (Visibility and Analytics)**:
- SIEM統合: 全ログの集約と相関分析
- 行動分析: UEBA (User and Entity Behavior Analytics)
- リアルタイム脅威検知: 異常トラフィック検出

**ゼロトラスト実装モデル**:

**NIST SP 800-207 (Zero Trust Architecture)**:
- コアコンポーネント:
  - Policy Engine (PE): アクセス決定エンジン
  - Policy Administrator (PA): ポリシー実行
  - Policy Enforcement Point (PEP): アクセス制御ポイント
- 論理コンポーネント:
  - Continuous Diagnostics and Mitigation (CDM) System
  - Industry Compliance System
  - Threat Intelligence Feed

**Google BeyondCorp**:
- Googleの実装したゼロトラストモデル
- VPN不要のアクセス制御
- デバイス証明書ベースの認証
- コンテキスト情報による動的アクセス制御

#### 実用例

**例1: SaaS アプリケーションのゼロトラスト実装**

```yaml
# ゼロトラストポリシー定義 (例: Open Policy Agent)
package zero_trust

# デフォルト拒否
default allow = false

# アクセス許可条件
allow {
    # 1. ユーザー認証済み (MFA)
    input.user.authenticated == true
    input.user.mfa_verified == true
    
    # 2. デバイス検証
    device_trusted
    
    # 3. ネットワークコンテキスト
    network_context_valid
    
    # 4. リソースへのアクセス権限
    has_permission
}

# デバイス信頼性チェック
device_trusted {
    input.device.registered == true
    input.device.os_version >= "10.0"
    input.device.antivirus_updated == true
    input.device.jailbroken == false
}

# ネットワークコンテキスト検証
network_context_valid {
    # 許可された地域からのアクセス
    input.geo_location in ["JP", "US", "EU"]
    
    # 勤務時間内のアクセス（重要操作）
    is_business_hours
}

is_business_hours {
    hour := time.clock(time.now_ns())[0]
    hour >= 9
    hour < 18
}

# 権限チェック (RBAC)
has_permission {
    user_roles := data.users[input.user.id].roles
    required_role := data.resources[input.resource.id].required_role
    required_role in user_roles
}
```

**例2: マイクロサービスのゼロトラスト (Service Mesh with mTLS)**

```yaml
# Istio PeerAuthentication - 相互TLS強制
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # 全サービス間通信にmTLS必須

---
# AuthorizationPolicy - サービス間アクセス制御
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: order-service-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-service
  action: ALLOW
  rules:
  # payment-serviceからのアクセスのみ許可
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/payment-service"]
    to:
    - operation:
        methods: ["POST"]
        paths: ["/api/orders/*/payments"]
  
  # frontend-serviceからの読み取りアクセス
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend-service"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/orders/*"]
  
  # 他のサービスからのアクセスはデフォルト拒否

---
# RequestAuthentication - JWT検証
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-authentication
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-service
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
    audiences:
    - "api.example.com"
```

**例3: ゼロトラストネットワークアクセス (ZTNA) アーキテクチャ**

```
┌─────────────────────────────────────────────────────────────┐
│                      ユーザー/デバイス                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ 社内PC   │  │リモートPC │  │モバイル  │                 │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                 │
└───────┼─────────────┼─────────────┼────────────────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │  Identity Provider (IdP) │  ← MFA, デバイス検証
        │  (Okta, Azure AD)        │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Policy Decision Point   │  ← ゼロトラストポリシーエンジン
        │  (PDP)                   │     - ユーザーコンテキスト評価
        └────────────┬─────────────┘     - デバイス態勢チェック
                     │                   - リスクスコア計算
                     ▼
        ┌─────────────────────────┐
        │  Policy Enforcement      │  ← アクセス制御ポイント
        │  Point (PEP)             │     - トラフィック検査
        │  (Reverse Proxy/Gateway) │     - セッション管理
        └────────────┬─────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌────────────────┐      ┌────────────────┐
│ Internal App 1 │      │ Internal App 2 │  ← マイクロセグメント
│ (Web Server)   │      │ (Database)     │     分離されたアプリ
└────────────────┘      └────────────────┘

実装例: Cloudflare Access + Identity Provider

# Cloudflare Access Policy
{
  "name": "Internal Dashboard Access",
  "decision": "allow",
  "include": [
    {"email_domain": {"domain": "example.com"}},
    {"geo": {"country_code": ["JP", "US"]}}
  ],
  "require": [
    {"mfa": true},
    {"certificate": true}  # デバイス証明書
  ],
  "exclude": [
    {"ip": {"ip": "203.0.113.0/24"}}  # ブロックリスト
  ]
}
```

**例4: ゼロトラスト段階的導入ロードマップ**

```
フェーズ1: 可視化と基盤構築 (3-6ヶ月)
┌────────────────────────────────────────┐
│ ✓ 資産の洗い出し (全ユーザー・デバイス・アプリ)│
│ ✓ ネットワークトラフィック可視化 (SIEM導入) │
│ ✓ IDプロバイダー統合 (SSO構築)            │
│ ✓ MFA展開 (全管理者アカウント)            │
└────────────────────────────────────────┘

フェーズ2: マイクロセグメンテーション (6-12ヶ月)
┌────────────────────────────────────────┐
│ ✓ ネットワークセグメント分離             │
│ ✓ ファイアウォールルール最適化           │
│ ✓ 内部トラフィック暗号化 (mTLS)         │
│ ✓ デバイス管理 (MDM/UEM導入)            │
└────────────────────────────────────────┘

フェーズ3: ポリシーエンジン構築 (12-18ヶ月)
┌────────────────────────────────────────┐
│ ✓ 動的アクセス制御ポリシー策定           │
│ ✓ コンテキストベース認証                │
│ ✓ リスクベースアクセス制御               │
│ ✓ UEBA (行動分析) 導入                 │
└────────────────────────────────────────┘

フェーズ4: 自動化と最適化 (18-24ヶ月)
┌────────────────────────────────────────┐
│ ✓ 自動応答 (SOAR統合)                  │
│ ✓ AI/ML脅威検知                        │
│ ✓ 継続的コンプライアンス監視            │
│ ✓ ゼロトラスト成熟度評価                │
└────────────────────────────────────────┘
```

#### 参考文献・リソース
- John Kindervag, "Build Security Into Your Network's DNA: The Zero Trust Network Architecture" (Forrester Research, 2010)
- NIST SP 800-207, "Zero Trust Architecture" (2020)
- Google, "BeyondCorp: A New Approach to Enterprise Security" (2014)
- Rose, S., et al., "Zero Trust Architecture" (NIST, 2020) - https://csrc.nist.gov/publications/detail/sp/800-207/final
- Microsoft, "Zero Trust Deployment Guide" - https://docs.microsoft.com/en-us/security/zero-trust/

---

### 2. STRIDE脅威モデリング

#### 分類
- **脅威モデリング・リスク分析系**
- **設計段階のセキュリティ評価**

#### 出典・背景
- **提唱者**: Praerit Garg, Loren Kohnfelder (Microsoft)
- **出典**: "The Threats to Our Products" (Microsoft, 1999)
- **背景**: 1990年代後半、Microsoftは製品の脆弱性による深刻なセキュリティインシデントに直面していました。ビル・ゲイツが2002年に発表した「Trustworthy Computing」イニシアチブの一環として、開発プロセスにセキュリティを組み込む手法が求められました。STRIDEは、脅威を体系的に分類し、設計段階で潜在的なセキュリティ問題を識別するためのフレームワークとして開発されました。

#### 理論の詳細

**STRIDEの6つの脅威カテゴリ**:

**S - Spoofing (なりすまし)**:
- **定義**: 正当なユーザーやシステムになりすます攻撃
- **侵害されるCIA要素**: 認証 (Authentication)
- **例**: 
  - 盗まれたパスワードでログイン
  - IPアドレス偽装
  - セッションハイジャック
- **対策**: 
  - 多要素認証 (MFA)
  - デジタル証明書
  - 強力な認証プロトコル (Kerberos, OAuth)

**T - Tampering (改ざん)**:
- **定義**: データやコードの不正な変更
- **侵害されるCIA要素**: 完全性 (Integrity)
- **例**:
  - データベースの不正変更
  - 通信中のデータ改ざん (Man-in-the-Middle)
  - ファイルシステムの改ざん
- **対策**:
  - デジタル署名
  - ハッシュ値検証
  - アクセス制御リスト (ACL)
  - 改ざん検知 (IDS/IPS)

**R - Repudiation (否認)**:
- **定義**: 実行した行為を否定する
- **侵害されるCIA要素**: 否認防止 (Non-Repudiation)
- **例**:
  - 取引の否認
  - 不正操作の痕跡隠蔽
  - ログの削除
- **対策**:
  - 監査ログ
  - デジタル署名
  - タイムスタンプ
  - 改ざん防止ログ (WORM)

**I - Information Disclosure (情報漏洩)**:
- **定義**: 機密情報の不正な開示
- **侵害されるCIA要素**: 機密性 (Confidentiality)
- **例**:
  - SQLインジェクションによるデータ漏洩
  - エラーメッセージでの内部情報露出
  - パーミッション設定ミスによる情報公開
- **対策**:
  - 暗号化 (at Rest, in Transit)
  - アクセス制御
  - エラーメッセージの適切なハンドリング
  - データマスキング

**D - Denial of Service (サービス拒否)**:
- **定義**: 正当なユーザーのサービス利用を妨害
- **侵害されるCIA要素**: 可用性 (Availability)
- **例**:
  - DDoS攻撃
  - リソース枯渇攻撃
  - アプリケーションクラッシュ
- **対策**:
  - レート制限
  - 負荷分散
  - リソース監視
  - DDoS対策サービス (CloudFlare, AWS Shield)

**E - Elevation of Privilege (権限昇格)**:
- **定義**: 低権限ユーザーが高権限を不正に取得
- **侵害されるCIA要素**: 認可 (Authorization)
- **例**:
  - バッファオーバーフロー
  - SQLインジェクション
  - 不適切なアクセス制御
- **対策**:
  - 最小権限の原則
  - 入力検証
  - セキュアコーディング
  - 権限分離

**STRIDE分析プロセス**:

1. **システムモデリング**: データフロー図 (DFD) の作成
   - プロセス、データストア、データフロー、外部エンティティを識別
2. **脅威の識別**: 各要素に対してSTRIDEカテゴリを適用
3. **脅威の評価**: リスクスコアリング (DREAD など)
4. **対策の立案**: 緩和策の設計
5. **検証**: 残存リスクの評価

#### 実用例

**例1: Webアプリケーションの STRIDE 分析**

```
システム: ECサイトの注文処理

データフロー図 (DFD):
[ユーザー] --①ログイン--> [Webサーバー] --②注文データ--> [DBサーバー]
                |                          |
                ③カード情報                 ④在庫確認
                |                          |
                v                          v
        [決済ゲートウェイ]            [在庫DB]

STRIDE分析:

┌────────────────────────────────────────────────────────────────┐
│ データフロー: ①ログイン (ユーザー → Webサーバー)                    │
├────────────────────────────────────────────────────────────────┤
│ S (Spoofing)     │ 攻撃: パスワード推測、フィッシング            │
│                  │ 対策: MFA、アカウントロックアウト            │
├──────────────────┼───────────────────────────────────────────┤
│ T (Tampering)    │ 攻撃: セッションクッキー改ざん                │
│                  │ 対策: 署名付きクッキー、HTTPS                │
├──────────────────┼───────────────────────────────────────────┤
│ R (Repudiation)  │ 攻撃: ログイン履歴の否認                     │
│                  │ 対策: 監査ログ、IPアドレス記録               │
├──────────────────┼───────────────────────────────────────────┤
│ I (Info Discl.)  │ 攻撃: 認証エラーでユーザー存在確認            │
│                  │ 対策: 汎用エラーメッセージ                   │
├──────────────────┼───────────────────────────────────────────┤
│ D (DoS)          │ 攻撃: ログイン試行によるリソース枯渇          │
│                  │ 対策: レート制限、CAPTCHA                   │
├──────────────────┼───────────────────────────────────────────┤
│ E (EoP)          │ 攻撃: SQLインジェクションで管理者権限取得    │
│                  │ 対策: パラメータ化クエリ、入力検証           │
└──────────────────┴───────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ データストア: DBサーバー                                          │
├────────────────────────────────────────────────────────────────┤
│ S (Spoofing)     │ 攻撃: DB接続情報の盗用                       │
│                  │ 対策: 接続文字列暗号化、最小権限DBユーザー   │
├──────────────────┼───────────────────────────────────────────┤
│ T (Tampering)    │ 攻撃: 注文データの直接改ざん                 │
│                  │ 対策: アクセス制御、トリガーによる整合性チェック│
├──────────────────┼───────────────────────────────────────────┤
│ R (Repudiation)  │ 攻撃: データ変更履歴の削除                   │
│                  │ 対策: 監査テーブル、変更履歴の自動記録       │
├──────────────────┼───────────────────────────────────────────┤
│ I (Info Discl.)  │ 攻撃: SQLインジェクションでデータ漏洩        │
│                  │ 対策: パラメータ化クエリ、最小権限           │
├──────────────────┼───────────────────────────────────────────┤
│ D (DoS)          │ 攻撃: 大量クエリでDB過負荷                   │
│                  │ 対策: クエリタイムアウト、接続プール制限     │
├──────────────────┼───────────────────────────────────────────┤
│ E (EoP)          │ 攻撃: ストアドプロシージャの脆弱性悪用       │
│                  │ 対策: コードレビュー、動的権限制御           │
└──────────────────┴───────────────────────────────────────────┘
```

**例2: API エンドポイントの STRIDE 分析 (実装例)**

```python
# API: POST /api/orders (注文作成)

from flask import Flask, request, jsonify
from functools import wraps
import jwt
import hashlib
import time

app = Flask(__name__)

# S (Spoofing) 対策: JWT トークン検証
def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        
        try:
            # JWT検証 (なりすまし防止)
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
            request.user_role = payload['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

# T (Tampering) 対策: リクエストボディの署名検証
def verify_signature(data, signature):
    expected_sig = hashlib.sha256(
        f"{data}{SECRET_KEY}".encode()
    ).hexdigest()
    return signature == expected_sig

# R (Repudiation) 対策: 監査ログ
def audit_log(user_id, action, details):
    log_entry = {
        'timestamp': time.time(),
        'user_id': user_id,
        'action': action,
        'details': details,
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    }
    # 改ざん防止ログストレージに保存
    audit_storage.append(log_entry)

# I (Information Disclosure) 対策: データマスキング
def mask_sensitive_data(order):
    return {
        'order_id': order['id'],
        'total': order['total'],
        'card_number': f"****-****-****-{order['card_number'][-4:]}"
    }

# D (DoS) 対策: レート制限
from flask_limiter import Limiter
limiter = Limiter(
    app,
    key_func=lambda: request.headers.get('X-User-ID'),
    default_limits=["100 per hour", "10 per minute"]
)

# E (Elevation of Privilege) 対策: 権限チェック
def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if request.user_role != required_role:
                audit_log(request.user_id, 'UNAUTHORIZED_ACCESS_ATTEMPT', 
                         {'endpoint': request.path, 'required_role': required_role})
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

# 統合実装
@app.route('/api/orders', methods=['POST'])
@limiter.limit("10 per minute")  # D対策
@verify_token                     # S対策
def create_order():
    data = request.get_json()
    
    # T対策: 署名検証
    signature = request.headers.get('X-Signature')
    if not verify_signature(data, signature):
        return jsonify({'error': 'Invalid signature'}), 400
    
    # 入力検証 (E対策: SQLインジェクション防止)
    if not validate_order_data(data):
        return jsonify({'error': 'Invalid input'}), 400
    
    # ビジネスロジック実行
    order = create_order_in_db(request.user_id, data)
    
    # R対策: 監査ログ
    audit_log(request.user_id, 'ORDER_CREATED', {'order_id': order['id']})
    
    # I対策: 機密情報マスキング
    response_data = mask_sensitive_data(order)
    
    return jsonify(response_data), 201
```

**例3: STRIDE + DREAD によるリスク優先順位付け**

```
脅威リスクスコアリング (DREADモデル)

DREAD評価基準 (各1-10点):
- D (Damage): 被害の大きさ
- R (Reproducibility): 再現性
- E (Exploitability): 悪用の容易さ
- A (Affected Users): 影響を受けるユーザー数
- D (Discoverability): 発見の容易さ

┌─────────────────────────────────────────────────────────────────┐
│ 脅威ID: T001                                                     │
│ STRIDE分類: Information Disclosure (情報漏洩)                    │
│ 脅威: SQLインジェクションによる顧客データ漏洩                      │
├─────────────────────────────────────────────────────────────────┤
│ DREADスコア:                                                     │
│   Damage (D):           9/10  (全顧客データ漏洩)                 │
│   Reproducibility (R):  8/10  (再現容易)                        │
│   Exploitability (E):   7/10  (公開ツールで可能)                 │
│   Affected Users (A):  10/10  (全ユーザー)                      │
│   Discoverability (D):  6/10  (自動スキャンで検出可能)           │
│   合計スコア: 40/50 (高リスク)                                   │
├─────────────────────────────────────────────────────────────────┤
│ 対策の優先度: ★★★★★ (最優先)                                    │
│ 推奨対策:                                                        │
│  1. パラメータ化クエリ実装 (即時)                                 │
│  2. WAF導入 (1週間以内)                                         │
│  3. 定期的脆弱性スキャン (継続)                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 脅威ID: T002                                                     │
│ STRIDE分類: Denial of Service (サービス拒否)                     │
│ 脅威: ログイン試行によるリソース枯渇                              │
├─────────────────────────────────────────────────────────────────┤
│ DREADスコア:                                                     │
│   Damage (D):           5/10  (一時的なサービス停止)             │
│   Reproducibility (R):  9/10  (簡単に再現可能)                   │
│   Exploitability (E):   9/10  (スクリプト実行のみ)               │
│   Affected Users (A):   7/10  (全ユーザーに影響)                 │
│   Discoverability (D):  8/10  (容易に発見可能)                   │
│   合計スコア: 38/50 (高リスク)                                   │
├─────────────────────────────────────────────────────────────────┤
│ 対策の優先度: ★★★★☆ (高)                                       │
│ 推奨対策:                                                        │
│  1. レート制限実装 (1週間以内)                                   │
│  2. CAPTCHA導入 (2週間以内)                                     │
│  3. CDN/DDoS対策サービス検討 (1ヶ月以内)                         │
└─────────────────────────────────────────────────────────────────┘
```

#### 参考文献・リソース
- Adam Shostack, "Threat Modeling: Designing for Security" (Wiley, 2014)
- Microsoft, "The STRIDE Threat Model" - https://docs.microsoft.com/en-us/previous-versions/commerce-server/ee823878(v=cs.20)
- OWASP, "Application Threat Modeling" - https://owasp.org/www-community/Threat_Modeling
- Microsoft SDL, "SDL Threat Modeling Tool" - https://aka.ms/threatmodelingtool

---

### 3. OAuth 2.0 / OpenID Connect

#### 分類
- **認証・認可プロトコル系**
- **委譲アクセス・SSO**

#### 出典・背景
- **OAuth 2.0提唱**: Dick Hardt (編集者)
- **出典**: RFC 6749 "The OAuth 2.0 Authorization Framework" (2012)
- **OpenID Connect**: OpenID Foundation
- **出典**: "OpenID Connect Core 1.0" (2014)
- **背景**: 2000年代後半、ユーザーがサードパーティアプリケーションにパスワードを直接提供する「パスワードアンチパターン」が一般的でした。OAuth 1.0 (2007年) は複雑すぎるという課題があり、よりシンプルで安全な委譲認可フレームワークとしてOAuth 2.0が2012年に標準化されました。OpenID Connectは、OAuth 2.0上に認証レイヤーを追加したプロトコルです。

#### 理論の詳細

**OAuth 2.0 の役割と用語**:

**4つの役割**:
1. **Resource Owner (リソースオーナー)**: 保護されたリソースへのアクセスを許可できるエンティティ（通常はエンドユーザー）
2. **Resource Server (リソースサーバー)**: 保護されたリソースをホストするサーバー（APIサーバー）
3. **Client (クライアント)**: リソースオーナーの代わりに保護されたリソースにアクセスするアプリケーション
4. **Authorization Server (認可サーバー)**: アクセストークンを発行するサーバー

**トークンの種類**:
- **Access Token (アクセストークン)**: リソースサーバーへのアクセス権限を表す
- **Refresh Token (リフレッシュトークン)**: 新しいアクセストークンを取得するためのトークン
- **Authorization Code (認可コード)**: アクセストークンと交換する一時的なコード

**OAuth 2.0 の4つの主要フロー**:

**1. Authorization Code Flow (認可コードフロー)**:
- **用途**: Webアプリケーション、最も安全
- **特徴**: クライアントシークレット使用、バックチャネル通信
- **フロー**:
  1. クライアントがユーザーを認可サーバーにリダイレクト
  2. ユーザーが認証・同意
  3. 認可サーバーが認可コードを返す
  4. クライアントが認可コードをアクセストークンと交換

**2. Implicit Flow (インプリシットフロー)**:
- **用途**: SPA (Single Page Application)
- **特徴**: ブラウザのみで完結、クライアントシークレット不要
- **非推奨**: PKCE付きAuthorization Code Flowが推奨される

**3. Resource Owner Password Credentials Flow**:
- **用途**: 高度に信頼されたアプリケーション
- **特徴**: ユーザー名・パスワードを直接送信
- **非推奨**: セキュリティリスクが高い

**4. Client Credentials Flow**:
- **用途**: マシン間通信、バックエンドサービス
- **特徴**: ユーザーコンテキストなし、クライアント認証のみ

**PKCE (Proof Key for Code Exchange)**:
- **目的**: 認可コード横取り攻撃の防止
- **推奨**: 全てのパブリッククライアントで使用
- **仕組み**:
  1. Code Verifier (ランダム文字列) 生成
  2. Code Challenge (Code Verifierのハッシュ) を認可リクエストに含める
  3. トークンリクエスト時にCode Verifierを送信し検証

**OpenID Connect (OIDC)**:

OAuth 2.0上に構築された認証レイヤー。

**追加要素**:
- **ID Token**: JWT形式のユーザー情報トークン
- **UserInfo Endpoint**: ユーザー情報取得エンドポイント
- **標準スコープ**: `openid`, `profile`, `email`, `address`, `phone`

**ID Tokenの構造 (JWT)**:
```json
{
  "iss": "https://auth.example.com",    // 発行者
  "sub": "user123",                      // ユーザーID
  "aud": "client-app-id",                // 対象クライアント
  "exp": 1735689600,                     // 有効期限
  "iat": 1735686000,                     // 発行時刻
  "nonce": "random-nonce",               // リプレイ攻撃防止
  "email": "user@example.com",
  "email_verified": true
}
```

#### 実用例

**例1: Authorization Code Flow with PKCE 実装 (Python/Flask)**

```python
import secrets
import hashlib
import base64
import requests
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 認可サーバー設定
AUTH_SERVER = 'https://auth.example.com'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'  # Confidential Clientの場合
REDIRECT_URI = 'http://localhost:5000/callback'

# ステップ1: 認可リクエスト開始
@app.route('/login')
def login():
    # PKCE: Code Verifier生成 (43-128文字のランダム文字列)
    code_verifier = base64.urlsafe_b64encode(
        secrets.token_bytes(32)
    ).decode('utf-8').rstrip('=')
    session['code_verifier'] = code_verifier
    
    # PKCE: Code Challenge生成 (SHA256ハッシュ)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    
    # State生成 (CSRF対策)
    state = secrets.token_urlsafe(32)
    session['state'] = state
    
    # 認可リクエスト構築
    auth_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email',  # OpenID Connect
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',   # SHA256
    }
    
    auth_url = f"{AUTH_SERVER}/authorize?" + '&'.join(
        f"{k}={v}" for k, v in auth_params.items()
    )
    
    return redirect(auth_url)

# ステップ2: コールバック処理
@app.route('/callback')
def callback():
    # State検証 (CSRF対策)
    returned_state = request.args.get('state')
    if returned_state != session.get('state'):
        return 'Invalid state', 400
    
    # エラーチェック
    error = request.args.get('error')
    if error:
        return f'Authorization failed: {error}', 400
    
    # 認可コード取得
    code = request.args.get('code')
    if not code:
        return 'No authorization code', 400
    
    # ステップ3: トークンリクエスト
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,  # Confidential Clientのみ
        'code_verifier': session.get('code_verifier'),  # PKCE
    }
    
    token_response = requests.post(
        f"{AUTH_SERVER}/token",
        data=token_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    if token_response.status_code != 200:
        return 'Token request failed', 400
    
    tokens = token_response.json()
    access_token = tokens['access_token']
    id_token = tokens.get('id_token')  # OpenID Connectの場合
    refresh_token = tokens.get('refresh_token')
    
    # ID Token検証 (OpenID Connect)
    if id_token:
        user_info = verify_and_decode_id_token(id_token)
        session['user_id'] = user_info['sub']
        session['email'] = user_info.get('email')
    
    # アクセストークン保存
    session['access_token'] = access_token
    if refresh_token:
        session['refresh_token'] = refresh_token
    
    return redirect(url_for('profile'))

# ステップ4: 保護されたリソースへのアクセス
@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))
    
    # UserInfo Endpoint呼び出し (OpenID Connect)
    headers = {'Authorization': f'Bearer {access_token}'}
    user_response = requests.get(
        f"{AUTH_SERVER}/userinfo",
        headers=headers
    )
    
    if user_response.status_code != 200:
        return 'Failed to get user info', 400
    
    user_data = user_response.json()
    return f"Hello, {user_data.get('name')}! Email: {user_data.get('email')}"

# リフレッシュトークンによるトークン更新
@app.route('/refresh')
def refresh():
    refresh_token = session.get('refresh_token')
    if not refresh_token:
        return 'No refresh token', 400
    
    token_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    token_response = requests.post(
        f"{AUTH_SERVER}/token",
        data=token_data
    )
    
    tokens = token_response.json()
    session['access_token'] = tokens['access_token']
    
    return 'Token refreshed'

# JWT検証 (簡易版)
import jwt

def verify_and_decode_id_token(id_token):
    # 実運用では公開鍵を取得して検証 (JWKS Endpoint)
    jwks_response = requests.get(f"{AUTH_SERVER}/.well-known/jwks.json")
    jwks = jwks_response.json()
    
    # JWT検証
    decoded = jwt.decode(
        id_token,
        jwks,
        algorithms=['RS256'],
        audience=CLIENT_ID,
        issuer=AUTH_SERVER
    )
    
    return decoded
```

**例2: APIゲートウェイでのOAuth 2.0トークン検証**

```yaml
# Kong API Gateway設定例
services:
- name: user-api
  url: http://backend.example.com
  routes:
  - name: user-route
    paths:
    - /api/users
  plugins:
  - name: oauth2
    config:
      # OAuth 2.0プラグイン設定
      scopes:
      - read:users
      - write:users
      mandatory_scope: true
      token_expiration: 3600
      enable_authorization_code: true
      enable_client_credentials: true
      enable_implicit_grant: false  # 非推奨のため無効化
      enable_password_grant: false   # 非推奨のため無効化
      
  - name: rate-limiting
    config:
      minute: 100
      policy: local
```

**例3: マイクロサービス間のClient Credentials Flow**

```python
# サービスAからサービスBへのAPI呼び出し
import requests

def call_service_b_api():
    # Client Credentials Flowでトークン取得
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': 'service-a-client-id',
        'client_secret': 'service-a-client-secret',
        'scope': 'api:read api:write'
    }
    
    token_response = requests.post(
        'https://auth.example.com/token',
        data=token_data
    )
    
    access_token = token_response.json()['access_token']
    
    # サービスBのAPI呼び出し
    headers = {'Authorization': f'Bearer {access_token}'}
    api_response = requests.get(
        'https://service-b.example.com/api/resource',
        headers=headers
    )
    
    return api_response.json()
```

#### 参考文献・リソース
- RFC 6749, "The OAuth 2.0 Authorization Framework" (2012) - https://tools.ietf.org/html/rfc6749
- RFC 7636, "Proof Key for Code Exchange (PKCE)" (2015) - https://tools.ietf.org/html/rfc7636
- OpenID Connect Core 1.0 - https://openid.net/specs/openid-connect-core-1_0.html
- OAuth 2.0 Security Best Current Practice - https://tools.ietf.org/html/draft-ietf-oauth-security-topics
- Auth0, "OAuth 2.0 Playground" - https://auth0.com/docs/authorization/flows

---

### 4. 暗号化戦略 (Encryption Strategy)

#### 分類
- **データ保護・暗号技術系**
- **機密性保証**

#### 出典・背景
- **現代暗号の基礎**: Claude Shannon, "Communication Theory of Secrecy Systems" (1949)
- **AES標準化**: NIST, "Advanced Encryption Standard (AES)" (2001)
- **TLS 1.3**: RFC 8446 (2018)
- **背景**: データ侵害が組織に壊滅的な影響を与える現代において、暗号化は「最後の防衛線」です。仮にネットワークやアプリケーションが侵害されても、適切に暗号化されたデータは攻撃者にとって無価値となります。

#### 理論の詳細

**暗号化の3つの状態**:

**1. Encryption at Rest (保存時暗号化)**:
- **定義**: ストレージに保存されているデータの暗号化
- **対象**: データベース、ファイルシステム、バックアップ、ログ
- **脅威**: 物理的盗難、不正アクセス、内部脅威
- **実装手法**:
  - フルディスク暗号化 (FDE): BitLocker, FileVault, LUKS
  - データベース暗号化: Transparent Data Encryption (TDE)
  - ファイルレベル暗号化: ファイルシステム暗号化 (eCryptfs, EFS)
  - アプリケーションレベル暗号化: フィールド単位の暗号化

**2. Encryption in Transit (転送時暗号化)**:
- **定義**: ネットワーク経由で送信されるデータの暗号化
- **対象**: HTTP通信、API通信、データベース接続、サービス間通信
- **脅威**: 盗聴 (Eavesdropping)、中間者攻撃 (MITM)
- **実装手法**:
  - TLS 1.3: HTTPS, API通信
  - VPN: IPsec, WireGuard
  - SSH: リモートアクセス、ファイル転送
  - mTLS: マイクロサービス間通信

**3. Encryption in Use (処理時暗号化)**:
- **定義**: メモリ上で処理中のデータの暗号化
- **対象**: 処理中の機密データ
- **脅威**: メモリダンプ攻撃、特権エスカレーション
- **実装手法**:
  - 準同型暗号 (Homomorphic Encryption): 暗号化したまま演算
  - 機密コンピューティング (Confidential Computing): Intel SGX, AMD SEV
  - セキュアエンクレーブ: Trusted Execution Environment (TEE)

**対称鍵暗号 vs 公開鍵暗号**:

**対称鍵暗号 (Symmetric Encryption)**:
- **特徴**: 同じ鍵で暗号化・復号化
- **アルゴリズム**: AES-256, ChaCha20
- **用途**: 大量データの暗号化 (高速)
- **課題**: 鍵の配送問題

**公開鍵暗号 (Asymmetric Encryption)**:
- **特徴**: 公開鍵で暗号化、秘密鍵で復号化
- **アルゴリズム**: RSA-2048/4096, ECDSA (楕円曲線)
- **用途**: 鍵交換、デジタル署名
- **課題**: 処理速度が遅い

**ハイブリッド暗号化**:
- 公開鍵暗号でデータ暗号化鍵 (DEK) を暗号化
- 対称鍵暗号で実データを暗号化
- TLS、PGP、S/MIMEで採用

**鍵管理 (Key Management)**:

**鍵のライフサイクル**:
1. **生成 (Generation)**: 強力なランダム性
2. **保管 (Storage)**: HSM, KMS, Key Vault
3. **配布 (Distribution)**: セキュアチャネル経由
4. **使用 (Usage)**: アクセス制御、監査ログ
5. **ローテーション (Rotation)**: 定期的な鍵更新
6. **破棄 (Destruction)**: 安全な鍵削除

**KMS (Key Management Service)**:
- **クラウドKMS**: AWS KMS, Azure Key Vault, Google Cloud KMS
- **機能**: 
  - 鍵生成・保管
  - アクセス制御 (IAM統合)
  - 監査ログ
  - 自動ローテーション
  - エンベロープ暗号化

**エンベロープ暗号化 (Envelope Encryption)**:
```
データ暗号化鍵 (DEK) でデータを暗号化
    ↓
マスター鍵 (KEK) でDEKを暗号化
    ↓
暗号化されたDEKをデータと共に保存
    ↓
復号時: KEKでDEKを復号 → DEKでデータを復号
```

メリット:
- DEKの頻繁なローテーションが容易
- マスター鍵はKMSで厳重管理
- データ暗号化/復号化の性能向上

#### 実用例

**例1: データベースのフィールドレベル暗号化 (Python)**

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

class FieldEncryption:
    """フィールドレベル暗号化 (AES-128 via Fernet)"""
    
    def __init__(self, master_key: bytes):
        """
        master_key: KMSから取得したマスター鍵
        """
        self.cipher = Fernet(master_key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        プレーンテキストを暗号化
        返り値: Base64エンコードされた暗号文
        """
        ciphertext = self.cipher.encrypt(plaintext.encode('utf-8'))
        return base64.urlsafe_b64encode(ciphertext).decode('utf-8')
    
    def decrypt(self, ciphertext: str) -> str:
        """
        暗号文を復号化
        """
        decoded = base64.urlsafe_b64decode(ciphertext.encode('utf-8'))
        plaintext = self.cipher.decrypt(decoded)
        return plaintext.decode('utf-8')

# 使用例: ユーザーのクレジットカード番号を暗号化
import boto3

# AWS KMSからデータ暗号化鍵を取得
kms_client = boto3.client('kms')
response = kms_client.generate_data_key(
    KeyId='alias/my-master-key',
    KeySpec='AES_256'
)

# プレーンテキストのDEK (メモリ上でのみ使用)
plaintext_dek = response['Plaintext']

# 暗号化されたDEK (データベースに保存)
encrypted_dek = response['CiphertextBlob']

# Fernetキー生成 (DEKから派生)
kdf = PBKDF2(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'static_salt_for_fernet',  # 実運用では安全に管理
    iterations=100000,
)
fernet_key = base64.urlsafe_b64encode(kdf.derive(plaintext_dek))

# フィールド暗号化
encryptor = FieldEncryption(fernet_key)

# データベースへの保存
card_number = "1234-5678-9012-3456"
encrypted_card = encryptor.encrypt(card_number)

# データベース挿入 (疑似コード)
db.execute("""
    INSERT INTO users (id, name, encrypted_card_number, dek_ciphertext)
    VALUES (?, ?, ?, ?)
""", (user_id, name, encrypted_card, encrypted_dek))

# 復号化時
row = db.fetchone("SELECT encrypted_card_number, dek_ciphertext FROM users WHERE id = ?", user_id)
encrypted_card = row['encrypted_card_number']
encrypted_dek = row['dek_ciphertext']

# KMSでDEKを復号化
dek_response = kms_client.decrypt(CiphertextBlob=encrypted_dek)
plaintext_dek = dek_response['Plaintext']

# Fernetキー再生成
fernet_key = base64.urlsafe_b64encode(kdf.derive(plaintext_dek))
decryptor = FieldEncryption(fernet_key)

# カード番号復号化
card_number = decryptor.decrypt(encrypted_card)
print(f"Card: {card_number}")
```

**例2: TLS 1.3 設定 (Nginx)**

```nginx
# /etc/nginx/sites-available/secure-api

server {
    listen 443 ssl http2;
    server_name api.example.com;

    # TLS 1.3のみ許可 (TLS 1.2以下は脆弱性リスク)
    ssl_protocols TLSv1.3;
    
    # 証明書 (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    
    # 暗号スイート (TLS 1.3は自動選択)
    # TLS 1.2互換性が必要な場合のみ以下を追加
    # ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    # ssl_prefer_server_ciphers off;
    
    # OCSP Stapling (証明書検証の高速化)
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/api.example.com/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # セッションキャッシュ
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;  # PFS (Perfect Forward Secrecy) のため無効化
    
    # HSTSヘッダー (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # セキュリティヘッダー
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    location / {
        proxy_pass http://backend:8080;
        
        # バックエンドへの接続もTLS化
        # proxy_pass https://backend:8443;
        # proxy_ssl_protocols TLSv1.3;
        # proxy_ssl_certificate /etc/nginx/client.crt;
        # proxy_ssl_certificate_key /etc/nginx/client.key;
    }
}

# HTTP → HTTPS リダイレクト
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$host$request_uri;
}
```

**例3: AWS S3バケットの暗号化設定**

```yaml
# Terraform設定: S3バケットのデフォルト暗号化

resource "aws_s3_bucket" "sensitive_data" {
  bucket = "my-company-sensitive-data"
  
  tags = {
    Environment = "Production"
    Compliance  = "PCI-DSS"
  }
}

# デフォルト暗号化 (SSE-KMS)
resource "aws_s3_bucket_server_side_encryption_configuration" "sensitive_data" {
  bucket = aws_s3_bucket.sensitive_data.id

  rule {
    apply_server_side_encryption_by_default {
      # AWS KMSマスターキーで暗号化
      kms_master_key_id = aws_kms_key.s3_key.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true  # S3 Bucket Keyで性能向上
  }
}

# KMSキー定義
resource "aws_kms_key" "s3_key" {
  description             = "KMS key for S3 bucket encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true  # 自動ローテーション有効化

  tags = {
    Name = "s3-encryption-key"
  }
}

# KMSキーポリシー
resource "aws_kms_key_policy" "s3_key" {
  key_id = aws_kms_key.s3_key.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow S3 to use the key"
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "*"
      }
    ]
  })
}

# バケットポリシー: 暗号化されていないアップロードを拒否
resource "aws_s3_bucket_policy" "enforce_encryption" {
  bucket = aws_s3_bucket.sensitive_data.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "DenyUnencryptedObjectUploads"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:PutObject"
        Resource  = "${aws_s3_bucket.sensitive_data.arn}/*"
        Condition = {
          StringNotEquals = {
            "s3:x-amz-server-side-encryption" = "aws:kms"
          }
        }
      }
    ]
  })
}
```

#### 参考文献・リソース
- NIST SP 800-57, "Recommendation for Key Management" (2020)
- NIST SP 800-175B, "Guideline for Using Cryptographic Standards" (2020)
- RFC 8446, "The Transport Layer Security (TLS) Protocol Version 1.3" (2018)
- Bruce Schneier, "Applied Cryptography" (Wiley, 2015)
- AWS, "Encryption at Rest" - https://docs.aws.amazon.com/whitepapers/latest/kms-best-practices/encryption-at-rest.html

---

### 5. OWASP Top 10 対策

#### 分類
- **アプリケーションセキュリティ系**
- **Webアプリケーション脆弱性対策**

#### 出典・背景
- **提唱組織**: OWASP (Open Web Application Security Project)
- **出典**: "OWASP Top 10" (最新版: 2021)
- **背景**: OWASPは2001年に設立されたオープンソースのセキュリティコミュニティです。OWASP Top 10は、Webアプリケーションにおける最も重大な10のセキュリティリスクをまとめたドキュメントで、3-4年ごとに更新されています。開発者、セキュリティ専門家、組織がアプリケーションセキュリティを向上させるための事実上の標準となっています。

#### 理論の詳細

**OWASP Top 10 - 2021**:

**A01:2021 - Broken Access Control (アクセス制御の不備)**:
- **リスク**: 権限のないユーザーが機密データやリソースにアクセス
- **例**: 
  - URL直接入力で他ユーザーのデータ閲覧
  - APIエンドポイントの権限チェック不足
  - IDOR (Insecure Direct Object Reference)
- **対策**:
  - デフォルト拒否の原則
  - 全リクエストでアクセス制御チェック
  - セッション検証
  - CORS設定の適切化

**A02:2021 - Cryptographic Failures (暗号化の失敗)**:
- **リスク**: 機密データの保護不足
- **例**:
  - 平文でのパスワード保存
  - HTTP通信（TLS未使用）
  - 弱い暗号アルゴリズム (MD5, SHA1)
- **対策**:
  - TLS 1.3使用
  - 保存時データ暗号化
  - 強力な暗号アルゴリズム (AES-256, bcrypt)
  - 機密データの最小化

**A03:2021 - Injection (インジェクション)**:
- **リスク**: 悪意あるコードがインタープリタに実行される
- **例**:
  - SQLインジェクション
  - NoSQLインジェクション
  - OSコマンドインジェクション
  - LDAPインジェクション
- **対策**:
  - パラメータ化クエリ（プリペアドステートメント）
  - ORM使用
  - 入力検証（ホワイトリスト）
  - 最小権限の原則

**A04:2021 - Insecure Design (安全でない設計)**:
- **リスク**: 設計段階でのセキュリティ考慮不足
- **例**:
  - 脅威モデリング欠如
  - レート制限なし
  - ビジネスロジックの脆弱性
- **対策**:
  - セキュアバイデザイン
  - 脅威モデリング (STRIDE)
  - セキュリティ要件定義
  - ペネトレーションテスト

**A05:2021 - Security Misconfiguration (セキュリティ設定ミス)**:
- **リスク**: 不適切な設定による脆弱性
- **例**:
  - デフォルト認証情報
  - 不要なサービス有効化
  - 詳細なエラーメッセージ
  - 古いソフトウェアバージョン
- **対策**:
  - セキュアデフォルト
  - 最小限の機能有効化
  - 定期的なパッチ適用
  - 自動化された設定管理

**A06:2021 - Vulnerable and Outdated Components (脆弱で古いコンポーネント)**:
- **リスク**: 既知の脆弱性を持つライブラリ使用
- **例**:
  - 古いバージョンのフレームワーク
  - 脆弱性が公開されたライブラリ
  - サポート終了のソフトウェア
- **対策**:
  - 依存関係の定期監査
  - SCA (Software Composition Analysis)
  - 自動更新
  - サプライチェーンセキュリティ

**A07:2021 - Identification and Authentication Failures (識別と認証の失敗)**:
- **リスク**: 認証メカニズムの不備
- **例**:
  - ブルートフォース攻撃対策なし
  - 弱いパスワードポリシー
  - クレデンシャルスタッフィング
  - セッション管理の脆弱性
- **対策**:
  - 多要素認証 (MFA)
  - レート制限
  - セッションタイムアウト
  - 強力なパスワードポリシー

**A08:2021 - Software and Data Integrity Failures (ソフトウェアとデータの整合性の失敗)**:
- **リスク**: 検証なしのコード/データ使用
- **例**:
  - 署名されていないアップデート
  - CI/CD パイプラインの侵害
  - 安全でないデシリアライゼーション
- **対策**:
  - デジタル署名検証
  - CI/CDパイプラインの保護
  - 依存関係の整合性チェック

**A09:2021 - Security Logging and Monitoring Failures (セキュリティログとモニタリングの失敗)**:
- **リスク**: インシデント検知の遅延
- **例**:
  - ログ記録不足
  - アラート未設定
  - ログの改ざん可能性
- **対策**:
  - 包括的ログ記録
  - SIEM統合
  - リアルタイムアラート
  - ログの改ざん防止

**A10:2021 - Server-Side Request Forgery (SSRF)**:
- **リスク**: サーバーが意図しないリソースにアクセス
- **例**:
  - 内部APIへの不正アクセス
  - クラウドメタデータサービス攻撃
  - ポートスキャン
- **対策**:
  - URLホワイトリスト
  - ネットワークセグメンテーション
  - メタデータサービス保護

#### 実用例

**例1: SQLインジェクション対策 (Python/Flask)**

```python
# ❌ 脆弱なコード: SQLインジェクションの脆弱性
from flask import Flask, request
import sqlite3

@app.route('/user')
def get_user_vulnerable():
    user_id = request.args.get('id')
    
    # 危険: ユーザー入力を直接SQL文に埋め込み
    query = f"SELECT * FROM users WHERE id = {user_id}"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)  # SQLインジェクション可能
    
    # 攻撃例: /user?id=1 OR 1=1 -- 
    # 実行されるSQL: SELECT * FROM users WHERE id = 1 OR 1=1 --
    # 結果: 全ユーザーのデータが返される
    
    return cursor.fetchall()

# ✅ 安全なコード: パラメータ化クエリ
@app.route('/user')
def get_user_secure():
    user_id = request.args.get('id')
    
    # 入力検証
    if not user_id.isdigit():
        return {'error': 'Invalid user ID'}, 400
    
    # プリペアドステートメント使用
    query = "SELECT id, name, email FROM users WHERE id = ?"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))  # パラメータバインディング
    
    result = cursor.fetchone()
    if result:
        return {
            'id': result[0],
            'name': result[1],
            'email': result[2]
        }
    else:
        return {'error': 'User not found'}, 404

# ✅ ORM使用 (SQLAlchemy)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

@app.route('/user')
def get_user_orm():
    user_id = request.args.get('id')
    
    if not user_id.isdigit():
        return {'error': 'Invalid user ID'}, 400
    
    # ORMは自動的にパラメータ化クエリを生成
    user = User.query.get(int(user_id))
    
    if user:
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    else:
        return {'error': 'User not found'}, 404
```

**例2: XSS (Cross-Site Scripting) 対策**

```python
from flask import Flask, request, render_template_string, escape
import bleach

app = Flask(__name__)

# ❌ 脆弱なコード: XSS脆弱性
@app.route('/comment', methods=['POST'])
def post_comment_vulnerable():
    comment = request.form.get('comment')
    
    # 危険: ユーザー入力をHTMLに直接埋め込み
    html = f"<div>{comment}</div>"
    
    # 攻撃例: comment = "<script>alert('XSS')</script>"
    # 結果: スクリプトが実行される
    
    return html

# ✅ 安全なコード: エスケープ処理
@app.route('/comment', methods=['POST'])
def post_comment_escaped():
    comment = request.form.get('comment')
    
    # HTMLエスケープ
    safe_comment = escape(comment)
    
    # <script>alert('XSS')</script> → &lt;script&gt;alert('XSS')&lt;/script&gt;
    # ブラウザで "<script>alert('XSS')</script>" とテキスト表示される
    
    return f"<div>{safe_comment}</div>"

# ✅ Jinja2テンプレート (自動エスケープ)
@app.route('/comment', methods=['POST'])
def post_comment_template():
    comment = request.form.get('comment')
    
    # Jinja2は自動的にエスケープ (autoescapeがデフォルトでTrue)
    template = "<div>{{ comment }}</div>"
    return render_template_string(template, comment=comment)

# ✅ サニタイゼーション (HTMLを許可する場合)
@app.route('/rich_comment', methods=['POST'])
def post_rich_comment():
    comment = request.form.get('comment')
    
    # 許可するHTMLタグのホワイトリスト
    allowed_tags = ['b', 'i', 'u', 'a', 'p', 'br']
    allowed_attributes = {'a': ['href', 'title']}
    
    # bleachライブラリでサニタイゼーション
    safe_comment = bleach.clean(
        comment,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    
    return f"<div>{safe_comment}</div>"

# Content Security Policy (CSP) ヘッダー設定
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://trusted-cdn.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "frame-ancestors 'none'; "
        "base-uri 'self';"
    )
    return response
```

**例3: アクセス制御の実装 (RBAC)**

```python
from flask import Flask, request, jsonify
from functools import wraps
import jwt

app = Flask(__name__)
SECRET_KEY = 'your-secret-key'

# ロール定義
ROLES = {
    'admin': ['read', 'write', 'delete'],
    'editor': ['read', 'write'],
    'viewer': ['read']
}

# JWT検証デコレータ
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Token required'}), 401
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

# 権限チェックデコレータ
def require_permission(required_permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = request.user.get('role')
            
            if user_role not in ROLES:
                return jsonify({'error': 'Invalid role'}), 403
            
            permissions = ROLES[user_role]
            
            if required_permission not in permissions:
                # 監査ログ
                log_unauthorized_access(
                    user_id=request.user.get('user_id'),
                    required_permission=required_permission,
                    user_role=user_role,
                    endpoint=request.path
                )
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator

# API エンドポイント
@app.route('/api/articles/<int:article_id>', methods=['GET'])
@require_auth
@require_permission('read')
def get_article(article_id):
    # リソース所有者チェック (IDOR対策)
    article = Article.query.get(article_id)
    
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # テナント分離 (マルチテナント環境)
    if article.tenant_id != request.user.get('tenant_id'):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(article.to_dict())

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
@require_auth
@require_permission('delete')
def delete_article(article_id):
    article = Article.query.get(article_id)
    
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # リソース所有者またはadminのみ削除可能
    if article.author_id != request.user.get('user_id') and request.user.get('role') != 'admin':
        return jsonify({'error': 'You can only delete your own articles'}), 403
    
    db.session.delete(article)
    db.session.commit()
    
    # 監査ログ
    log_audit_event('ARTICLE_DELETED', {
        'article_id': article_id,
        'user_id': request.user.get('user_id')
    })
    
    return jsonify({'message': 'Article deleted successfully'})
```

#### 参考文献・リソース
- OWASP, "OWASP Top 10 - 2021" - https://owasp.org/Top10/
- OWASP, "Web Security Testing Guide" - https://owasp.org/www-project-web-security-testing-guide/
- OWASP, "Cheat Sheet Series" - https://cheatsheetseries.owasp.org/
- PortSwigger, "Web Security Academy" - https://portswigger.net/web-security

---

## セキュリティ戦略選択ガイド

| セキュリティ要件 | 推奨フレームワーク（優先順） | 適用場面 |
|-----------------|---------------------------|---------|
| **境界防御の強化** | ゼロトラスト → 多層防御 → ネットワークセグメンテーション | クラウド環境、リモートワーク |
| **認証・認可** | OAuth 2.0 / OIDC → MFA → RBAC/ABAC | API保護、SSO、マイクロサービス |
| **データ保護** | 暗号化戦略 (at Rest/in Transit) → KMS → DLP | 個人情報、クレジットカード情報 |
| **Webアプリ保護** | OWASP Top 10対策 → WAF → CSP | ECサイト、SaaS、ポータル |
| **設計段階のセキュリティ** | STRIDE脅威モデリング → セキュアバイデザイン | 新規システム開発 |
| **コンプライアンス** | ISO 27001 → GDPR → PCI DSS | 金融、医療、EC |

---

## 統合的な活用例: SaaS アプリケーションの包括的セキュリティ設計

### レイヤー1: ネットワーク・インフラ層
- **ゼロトラスト**: デフォルト拒否、全アクセス検証
- **暗号化 (in Transit)**: TLS 1.3、mTLS

### レイヤー2: 認証・認可層
- **OAuth 2.0 / OIDC**: SSO、API認証
- **MFA**: 全管理者アカウント
- **RBAC**: ロールベースアクセス制御

### レイヤー3: アプリケーション層
- **OWASP Top 10対策**: 入力検証、XSS対策、SQLインジェクション対策
- **CSP**: コンテンツセキュリティポリシー
- **レート制限**: DDoS対策

### レイヤー4: データ層
- **暗号化 (at Rest)**: データベース暗号化、KMS
- **フィールドレベル暗号化**: 機密フィールド

### レイヤー5: 監視・対応層
- **セキュリティログ**: 全アクセスログ記録
- **SIEM**: リアルタイム脅威検知
- **インシデント対応**: 自動アラート、SOAR

---

## 参考資料

### 書籍
1. Ross Anderson, "Security Engineering" (Wiley, 3rd Edition, 2020)
2. Bruce Schneier, "Applied Cryptography" (Wiley, 2015)
3. Kim Zetter, "Countdown to Zero Day" (Crown, 2014) - Stuxnet事例
4. Chris Sanders, Jason Smith, "Applied Network Security Monitoring" (Syngress, 2013)

### 標準・ガイドライン
- NIST Cybersecurity Framework (CSF)
- ISO/IEC 27001:2013
- CIS Controls v8
- OWASP Application Security Verification Standard (ASVS)

### オンラインリソース
- NIST Computer Security Resource Center: https://csrc.nist.gov/
- OWASP: https://owasp.org/
- SANS Institute: https://www.sans.org/
- US-CERT: https://www.cisa.gov/uscert

---

## まとめ

サイバーセキュリティは、技術、プロセス、人の3要素を統合した継続的な取り組みです。本ドキュメントで紹介した5つのフレームワーク——ゼロトラスト、STRIDE脅威モデリング、OAuth 2.0、暗号化戦略、OWASP Top 10対策——は、現代のシステムセキュリティ設計において不可欠な要素です。

- **ゼロトラスト**で境界の概念を超えた防御
- **STRIDE**で設計段階から脅威を識別
- **OAuth 2.0**で安全な認証・認可
- **暗号化**でデータの最後の防衛線を構築
- **OWASP Top 10**でアプリケーションの脆弱性を排除

これらを組み合わせ、リスクベースアプローチで優先順位を付け、多層防御を実現することが重要です。
