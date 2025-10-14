# テクニカルライター - フレームワーク詳細ドキュメント

## 概要

本ドキュメントは、テクニカルライターが活用する主要なフレームワーク・手法・原則について、理論的背景から実践的な適用方法まで網羅的に解説します。DITA、ミニマリズム、Docs as Code、API ドキュメンテーション、情報設計の原則など、効果的な技術文書作成のための体系的な知識とツールを提供します。

---

## 1. DITA (Darwin Information Typing Architecture)

### 分類
情報設計・XMLベース・構造化オーサリング

### 背景と歴史

DITA（Darwin Information Typing Architecture）は、IBMが1990年代後半に開発し、2005年にOASIS（Organization for the Advancement of Structured Information Standards）標準として公開された、XMLベースのコンテンツ作成・管理の技術標準です。

生物学のチャールズ・ダーウィンに由来する「Darwin」という名前は、トピックの「進化」と「特殊化」の概念を表しています。DITAは、技術文書を小さな再利用可能なトピックに分割し、それらを組み合わせて様々な出力（Webサイト、PDF、モバイルアプリなど）を生成するアーキテクチャです。

主要なコンセプトは「Topic-Based Authoring（トピックベースオーサリング）」「Content Reuse（コンテンツ再利用）」「Conditional Processing（条件付き処理）」です。

### 詳細な理論

#### トピックタイプ

DITAの中核概念は、情報を3つの基本トピックタイプに分類することです：

**1. Concept（コンセプト・概念）**
「What is it?（それは何か）」に答えるトピックです。背景情報、定義、説明を提供します。

構成要素:
- タイトル
- 本文（定義、背景、説明）
- 関連情報へのリンク

使用例:
- 「クラウドコンピューティングとは」
- 「マイクロサービスアーキテクチャの概念」
- 「OAuth 2.0の仕組み」

**2. Task（タスク）**
「How do I do it?（どうやるのか）」に答えるトピックです。手順を段階的に説明します。

構成要素:
- タイトル
- 短い説明（prerequisite: 前提条件）
- ステップ（steps）
- 結果（result）
- 例（example）
- トラブルシューティング

使用例:
- 「データベースへの接続方法」
- 「APIキーの取得手順」
- 「アプリケーションのデプロイ方法」

**3. Reference（リファレンス・参照）**
「What are the facts?（事実は何か）」に答えるトピックです。詳細な仕様、パラメータリスト、コマンドリファレンスなど。

構成要素:
- タイトル
- 構造化データ（表形式）
- パラメータ、戻り値、例外
- コードサンプル

使用例:
- 「API エンドポイント一覧」
- 「設定ファイルのパラメータリファレンス」
- 「エラーコード一覧」

#### DITA Map

DITA Mapは、個別のトピックを組み合わせて文書全体を構成する設計図です。

機能:
- トピックの階層構造定義
- ナビゲーション構造の定義
- 異なる出力（Web、PDF）のためのトピック選択
- メタデータの定義

#### 再利用とコンディショナル処理

**Content Reuse（コンテンツ再利用）**:
- conref（content reference）: 他のトピックからコンテンツを参照
- コンテンツフラグメントの共有
- 共通セクションのライブラリ

**Conditional Processing（条件付き処理）**:
- プロダクトバージョンによる内容の出し分け
- オーディエンス（初心者/上級者）による内容の出し分け
- プラットフォーム（Windows/Mac/Linux）による内容の出し分け

### 実践例

#### 例1: DITAトピックの基本構造

```xml
<!-- Conceptトピック: OAuth 2.0の概念 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE concept PUBLIC "-//OASIS//DTD DITA Concept//EN" "concept.dtd">
<concept id="oauth_overview">
    <title>OAuth 2.0とは</title>
    <shortdesc>OAuth 2.0は、第三者アプリケーションがユーザーのリソースに安全にアクセスするための認可フレームワークです。</shortdesc>
    
    <conbody>
        <section>
            <title>概要</title>
            <p>OAuth 2.0（Open Authorization 2.0）は、ユーザーがパスワードを共有することなく、
            サードパーティアプリケーションにリソースへのアクセス権限を委譲できるプロトコルです。</p>
        </section>
        
        <section>
            <title>主要な役割</title>
            <dl>
                <dlentry>
                    <dt>Resource Owner（リソースオーナー）</dt>
                    <dd>保護されたリソースへのアクセスを許可できるエンティティ、通常はエンドユーザー。</dd>
                </dlentry>
                <dlentry>
                    <dt>Client（クライアント）</dt>
                    <dd>リソースオーナーの代理として保護されたリソースにアクセスするアプリケーション。</dd>
                </dlentry>
                <dlentry>
                    <dt>Authorization Server（認可サーバー）</dt>
                    <dd>リソースオーナーを認証し、アクセストークンを発行するサーバー。</dd>
                </dlentry>
                <dlentry>
                    <dt>Resource Server（リソースサーバー）</dt>
                    <dd>保護されたリソースをホストし、アクセストークンを検証するサーバー。</dd>
                </dlentry>
            </dl>
        </section>
        
        <section>
            <title>主要な認可フロー</title>
            <ul>
                <li>Authorization Code Flow（認可コードフロー）: 最も安全、サーバーサイドアプリケーション向け</li>
                <li>Implicit Flow（インプリシットフロー）: ブラウザベースアプリケーション向け（非推奨）</li>
                <li>Client Credentials Flow（クライアント認証情報フロー）: マシン間通信向け</li>
                <li>Resource Owner Password Credentials Flow（パスワード認証情報フロー）: 信頼されたアプリケーション向け</li>
            </ul>
        </section>
        
        <section>
            <title>関連情報</title>
            <p>詳細な実装手順については、<xref href="oauth_implementation.dita">OAuth 2.0の実装方法</xref>を参照してください。</p>
        </section>
    </conbody>
    
    <related-links>
        <link href="oauth_implementation.dita" format="dita">
            <linktext>OAuth 2.0の実装方法</linktext>
        </link>
        <link href="https://oauth.net/2/" format="html" scope="external">
            <linktext>OAuth 2.0公式サイト</linktext>
        </link>
    </related-links>
</concept>
```

```xml
<!-- Taskトピック: OAuth 2.0の実装方法 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE task PUBLIC "-//OASIS//DTD DITA Task//EN" "task.dtd">
<task id="oauth_implementation">
    <title>OAuth 2.0 Authorization Code Flowの実装</title>
    <shortdesc>Authorization Code Flowを使用してOAuth 2.0認証を実装する手順を説明します。</shortdesc>
    
    <taskbody>
        <prereq>
            <p>この手順を実行する前に、以下を準備してください：</p>
            <ul>
                <li>認可サーバーへのアプリケーション登録（Client IDとClient Secretの取得）</li>
                <li>Redirect URIの設定</li>
                <li>Node.js 18.x以上とnpmのインストール</li>
            </ul>
        </prereq>
        
        <context>
            <p>Authorization Code Flowは、最も安全なOAuth 2.0フローで、サーバーサイドアプリケーションに推奨されます。
            このフローでは、ユーザーは認可サーバーで認証し、アプリケーションは認可コードを受け取り、
            それをアクセストークンに交換します。</p>
        </context>
        
        <steps>
            <step>
                <cmd>必要なライブラリをインストールします。</cmd>
                <info>
                    <codeblock outputclass="language-bash">npm install express axios dotenv</codeblock>
                </info>
            </step>
            
            <step>
                <cmd>環境変数ファイル（.env）を作成し、認証情報を設定します。</cmd>
                <info>
                    <codeblock outputclass="language-bash">CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:3000/callback
AUTHORIZATION_ENDPOINT=https://auth.example.com/oauth/authorize
TOKEN_ENDPOINT=https://auth.example.com/oauth/token</codeblock>
                </info>
                <stepxmp>
                    <note type="warning">Client Secretは機密情報です。リポジトリにコミットしないでください。</note>
                </stepxmp>
            </step>
            
            <step>
                <cmd>認可リクエストを生成するエンドポイントを実装します。</cmd>
                <info>
                    <codeblock outputclass="language-javascript">const express = require('express');
const axios = require('axios');
require('dotenv').config();

const app = express();

// ステップ1: 認可リクエスト
app.get('/login', (req, res) => {
    const authUrl = new URL(process.env.AUTHORIZATION_ENDPOINT);
    authUrl.searchParams.append('response_type', 'code');
    authUrl.searchParams.append('client_id', process.env.CLIENT_ID);
    authUrl.searchParams.append('redirect_uri', process.env.REDIRECT_URI);
    authUrl.searchParams.append('scope', 'read write');
    authUrl.searchParams.append('state', generateRandomState()); // CSRF保護
    
    res.redirect(authUrl.toString());
});

function generateRandomState() {
    return Math.random().toString(36).substring(2, 15);
}</codeblock>
                </info>
            </step>
            
            <step>
                <cmd>認可コードをアクセストークンに交換するコールバックエンドポイントを実装します。</cmd>
                <info>
                    <codeblock outputclass="language-javascript">// ステップ2: 認可コードを受け取り、アクセストークンに交換
app.get('/callback', async (req, res) => {
    const { code, state } = req.query;
    
    // stateパラメータの検証（省略）
    
    try {
        // トークンリクエスト
        const tokenResponse = await axios.post(
            process.env.TOKEN_ENDPOINT,
            {
                grant_type: 'authorization_code',
                code: code,
                redirect_uri: process.env.REDIRECT_URI,
                client_id: process.env.CLIENT_ID,
                client_secret: process.env.CLIENT_SECRET
            },
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        );
        
        const { access_token, refresh_token, expires_in } = tokenResponse.data;
        
        // アクセストークンを安全に保存（セッション、データベースなど）
        req.session.accessToken = access_token;
        req.session.refreshToken = refresh_token;
        
        res.send('認証成功！アクセストークンを取得しました。');
    } catch (error) {
        console.error('トークン取得エラー:', error.response.data);
        res.status(500).send('認証に失敗しました');
    }
});</codeblock>
                </info>
            </step>
            
            <step>
                <cmd>保護されたリソースにアクセスする関数を実装します。</cmd>
                <info>
                    <codeblock outputclass="language-javascript">// ステップ3: アクセストークンを使用してAPIにアクセス
app.get('/api/user', async (req, res) => {
    const accessToken = req.session.accessToken;
    
    if (!accessToken) {
        return res.status(401).send('未認証');
    }
    
    try {
        const userResponse = await axios.get('https://api.example.com/user', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        res.json(userResponse.data);
    } catch (error) {
        if (error.response.status === 401) {
            // トークンが期限切れ、リフレッシュトークンで更新
            // （リフレッシュトークンロジックの実装は省略）
        }
        res.status(error.response.status).send('APIアクセスエラー');
    }
});</codeblock>
                </info>
            </step>
            
            <step>
                <cmd>サーバーを起動します。</cmd>
                <info>
                    <codeblock outputclass="language-javascript">const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});</codeblock>
                </info>
                <stepresult>
                    <p>サーバーが起動し、http://localhost:3000/login にアクセスすることで認証フローが開始されます。</p>
                </stepresult>
            </step>
        </steps>
        
        <result>
            <p>これで、OAuth 2.0 Authorization Code Flowを使用した認証が実装されました。
            ユーザーは認可サーバーで認証され、アプリケーションはアクセストークンを取得して
            保護されたリソースにアクセスできます。</p>
        </result>
        
        <example>
            <title>完全な実装例</title>
            <p>完全なサンプルコードは、<xref href="https://github.com/example/oauth-demo" format="html" scope="external">GitHubリポジトリ</xref>で確認できます。</p>
        </example>
        
        <postreq>
            <p>次のステップ：</p>
            <ul>
                <li>リフレッシュトークンを使用したトークン更新の実装</li>
                <li>PKCE（Proof Key for Code Exchange）の追加によるセキュリティ強化</li>
                <li>トークンの安全な保管（暗号化、HTTPOnly Cookie）</li>
            </ul>
        </postreq>
    </taskbody>
    
    <related-links>
        <link href="oauth_overview.dita" format="dita">
            <linktext>OAuth 2.0とは</linktext>
        </link>
        <link href="oauth_troubleshooting.dita" format="dita">
            <linktext>OAuth 2.0トラブルシューティング</linktext>
        </link>
    </related-links>
</task>
```

```xml
<!-- Referenceトピック: OAuth 2.0エラーコード -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "reference.dtd">
<reference id="oauth_error_codes">
    <title>OAuth 2.0 エラーコードリファレンス</title>
    <shortdesc>OAuth 2.0認可およびトークンエンドポイントで返される可能性のあるエラーコードの一覧です。</shortdesc>
    
    <refbody>
        <section>
            <title>認可エンドポイントのエラー</title>
            <table>
                <tgroup cols="3">
                    <colspec colname="c1" colwidth="1.5*"/>
                    <colspec colname="c2" colwidth="3*"/>
                    <colspec colname="c3" colwidth="2*"/>
                    <thead>
                        <row>
                            <entry>エラーコード</entry>
                            <entry>説明</entry>
                            <entry>対処方法</entry>
                        </row>
                    </thead>
                    <tbody>
                        <row>
                            <entry><codeph>invalid_request</codeph></entry>
                            <entry>リクエストに必須パラメータが不足している、または無効な値が含まれています。</entry>
                            <entry>リクエストパラメータを確認し、必須フィールドがすべて含まれていることを確認してください。</entry>
                        </row>
                        <row>
                            <entry><codeph>unauthorized_client</codeph></entry>
                            <entry>クライアントはこの認可タイプを使用する権限がありません。</entry>
                            <entry>アプリケーション設定で許可されている認可タイプを確認してください。</entry>
                        </row>
                        <row>
                            <entry><codeph>access_denied</codeph></entry>
                            <entry>リソースオーナーまたは認可サーバーがリクエストを拒否しました。</entry>
                            <entry>ユーザーがアクセスを拒否したか、権限が不足しています。ユーザーに再度認可を求めてください。</entry>
                        </row>
                        <row>
                            <entry><codeph>unsupported_response_type</codeph></entry>
                            <entry>認可サーバーは指定されたresponse_typeをサポートしていません。</entry>
                            <entry>サポートされているresponse_type（例: code）を使用してください。</entry>
                        </row>
                        <row>
                            <entry><codeph>invalid_scope</codeph></entry>
                            <entry>要求されたスコープが無効、未知、または形式が不正です。</entry>
                            <entry>有効なスコープ値を確認し、リクエストを修正してください。</entry>
                        </row>
                        <row>
                            <entry><codeph>server_error</codeph></entry>
                            <entry>認可サーバーで予期しないエラーが発生しました。</entry>
                            <entry>一時的なエラーの可能性があります。しばらく待ってから再試行してください。</entry>
                        </row>
                        <row>
                            <entry><codeph>temporarily_unavailable</codeph></entry>
                            <entry>認可サーバーが一時的に過負荷またはメンテナンス中です。</entry>
                            <entry>しばらく待ってから再試行してください。</entry>
                        </row>
                    </tbody>
                </tgroup>
            </table>
        </section>
        
        <section>
            <title>トークンエンドポイントのエラー</title>
            <table>
                <tgroup cols="3">
                    <colspec colname="c1" colwidth="1.5*"/>
                    <colspec colname="c2" colwidth="3*"/>
                    <colspec colname="c3" colwidth="2*"/>
                    <thead>
                        <row>
                            <entry>エラーコード</entry>
                            <entry>説明</entry>
                            <entry>対処方法</entry>
                        </row>
                    </thead>
                    <tbody>
                        <row>
                            <entry><codeph>invalid_client</codeph></entry>
                            <entry>クライアント認証に失敗しました。</entry>
                            <entry>Client IDとClient Secretが正しいことを確認してください。</entry>
                        </row>
                        <row>
                            <entry><codeph>invalid_grant</codeph></entry>
                            <entry>提供された認可コードまたはリフレッシュトークンが無効、期限切れ、または取り消されています。</entry>
                            <entry>新しい認可コードを取得するか、認証フローを最初からやり直してください。</entry>
                        </row>
                        <row>
                            <entry><codeph>unsupported_grant_type</codeph></entry>
                            <entry>認可サーバーは指定されたgrant_typeをサポートしていません。</entry>
                            <entry>サポートされているgrant_type（例: authorization_code）を使用してください。</entry>
                        </row>
                    </tbody>
                </tgroup>
            </table>
        </section>
        
        <section>
            <title>エラーレスポンスの例</title>
            <example>
                <title>認可エンドポイントのエラー（URLフラグメント）</title>
                <codeblock outputclass="language-http">HTTP/1.1 302 Found
Location: https://client.example.com/callback?error=access_denied&amp;error_description=The+resource+owner+denied+the+request&amp;state=xyz</codeblock>
            </example>
            
            <example>
                <title>トークンエンドポイントのエラー（JSON）</title>
                <codeblock outputclass="language-json">{
  "error": "invalid_grant",
  "error_description": "The provided authorization code is invalid or expired"
}</codeblock>
            </example>
        </section>
    </refbody>
    
    <related-links>
        <link href="oauth_implementation.dita" format="dita">
            <linktext>OAuth 2.0の実装方法</linktext>
        </link>
        <link href="https://tools.ietf.org/html/rfc6749#section-4.1.2.1" format="html" scope="external">
            <linktext>RFC 6749 - OAuth 2.0エラーレスポンス</linktext>
        </link>
    </related-links>
</reference>
```

```xml
<!-- DITA Map: OAuth 2.0ガイド全体構成 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd">
<map>
    <title>OAuth 2.0 開発者ガイド</title>
    
    <topicref href="oauth_overview.dita" type="concept">
        <topicmeta>
            <navtitle>OAuth 2.0とは</navtitle>
        </topicmeta>
    </topicref>
    
    <topichead navtitle="実装ガイド">
        <topicref href="oauth_implementation.dita" type="task">
            <topicmeta>
                <navtitle>Authorization Code Flowの実装</navtitle>
            </topicmeta>
        </topicref>
        
        <topicref href="oauth_pkce.dita" type="task">
            <topicmeta>
                <navtitle>PKCEの実装</navtitle>
            </topicmeta>
        </topicref>
    </topichead>
    
    <topichead navtitle="リファレンス">
        <topicref href="oauth_error_codes.dita" type="reference">
            <topicmeta>
                <navtitle>エラーコードリファレンス</navtitle>
            </topicmeta>
        </topicref>
        
        <topicref href="oauth_scopes.dita" type="reference">
            <topicmeta>
                <navtitle>スコープリファレンス</navtitle>
            </topicmeta>
        </topicref>
    </topichead>
    
    <topicref href="oauth_troubleshooting.dita" type="task">
        <topicmeta>
            <navtitle>トラブルシューティング</navtitle>
        </topicmeta>
    </topicref>
    
    <reltable>
        <relheader>
            <relcolspec type="concept"/>
            <relcolspec type="task"/>
            <relcolspec type="reference"/>
        </relheader>
        <relrow>
            <relcell>
                <topicref href="oauth_overview.dita"/>
            </relcell>
            <relcell>
                <topicref href="oauth_implementation.dita"/>
            </relcell>
            <relcell>
                <topicref href="oauth_error_codes.dita"/>
            </relcell>
        </relrow>
    </reltable>
</map>
```

### 参考文献・リソース

**公式仕様**
- OASIS DITA Technical Committee. (2015). *DITA Version 1.3*. http://docs.oasis-open.org/dita/dita/v1.3/dita-v1.3-part0-overview.html

**書籍**
- Bellamy, L., Carey, M., & Schlotfeldt, J. (2012). *DITA Best Practices: A Roadmap for Writing, Editing, and Architecting in DITA*. IBM Press.
- Priestley, M., & Hargis, G. (2009). *DITA 101: Fundamentals of DITA for Authors and Managers*. Comtech Services.

**ツール**
- DITA Open Toolkit: https://www.dita-ot.org/
- Oxygen XML Editor: https://www.oxygenxml.com/

---

## 2. ミニマリズム（Minimalism）

### 分類
ライティング手法・ユーザー中心設計・タスク指向

### 背景と歴史

ミニマリズム（Minimalism）は、オランダの心理学者John M. Carroll が1990年に著書『The Nurnberg Funnel: Designing Minimalist Instruction for Practical Computer Skill』で提唱した、テクニカルライティングとインストラクショナルデザインのアプローチです。

従来の詳細な包括的マニュアル（「Nurnberg Funnel」と呼ばれる、知識を注ぎ込むアプローチ）に対する反論として生まれました。Carrollの研究によると、ユーザーは実際には長いマニュアルを読まず、試行錯誤しながら学習することが分かりました。

ミニマリズムは、ユーザーの自然な学習スタイルに合わせ、最小限の指示で最大の学習効果を得ることを目指します。

### 詳細な理論

#### ミニマリズムの4つの原則

**1. タスク指向（Task-Oriented）**
ユーザーの実際のタスク（ゴール）に焦点を当てます。システムの機能説明ではなく、「ユーザーが何をしたいか」から始めます。

- 悪い例: 「ファイルメニューには、新規作成、開く、保存、印刷などのコマンドがあります」
- 良い例: 「新しいドキュメントを作成するには、ファイル > 新規作成を選択します」

**2. 最小限の説明（Minimized）**
不要な情報を削除し、本質的な内容のみを提供します。

- システムの内部動作の詳細説明を避ける
- 「なぜそうなるか」よりも「どうするか」に焦点
- 冗長な前置きや背景説明を省く

**3. エラーからの学習をサポート（Support Error Recognition and Recovery）**
ユーザーはエラーを起こします。エラーを防ぐのではなく、エラーを認識し、回復する方法を提供します。

- 起こりうるエラーを予測し、対処法を記載
- トラブルシューティングセクション
- エラーメッセージの意味と解決方法

**4. 実世界のアクティビティに基づく（Based on Real-World Activities）**
抽象的な例ではなく、実際のユースケースと具体的な例を使用します。

- 架空のデモデータではなく、実際のビジネスシナリオ
- ユーザーが実際に行うタスク
- 実務的なコンテキスト

#### ミニマリズムの実装テクニック

**チャンキング（Chunking）**:
情報を小さな独立した単位に分割します。各チャンクは1つのタスクまたは概念を扱います。

**スキャン可能性（Scannability）**:
- 見出しと箇条書きを多用
- 重要な情報をハイライト
- 短い段落

**プログレッシブディスクロージャー（Progressive Disclosure）**:
基本情報を先に、詳細は後で。初心者が圧倒されないようにします。

### 実践例

#### 例1: 従来型 vs ミニマリスト型マニュアル

**従来型マニュアル（詳細・包括的）**:

```markdown
# 第3章: ファイル管理システム

## 3.1 ファイルシステムの概要

当システムは、階層型ファイルシステムを採用しています。ファイルシステムとは、
コンピュータ上でデータを整理・管理するための仕組みです。ファイルシステムには
様々な種類があり、WindowsではNTFS、MacOSではHFS+やAPFS、LinuxではExt4などが
使用されています。

当アプリケーションは、これらのファイルシステム上で動作し、ユーザーがファイルを
作成、保存、読み込み、削除する機能を提供します。

## 3.2 ファイルの作成

ファイルを作成する方法は複数あります。以下に、それぞれの方法について詳しく説明します。

### 3.2.1 メニューからの作成

メニューバーは、アプリケーションウィンドウの最上部に配置されています。
メニューバーには、「ファイル」「編集」「表示」「ヘルプ」などの項目があります。

「ファイル」メニューには、ファイル操作に関する様々なコマンドが含まれています。
これには、「新規作成」「開く」「閉じる」「保存」「名前を付けて保存」
「最近使ったファイル」「印刷」「終了」などがあります。

新しいファイルを作成するには:

1. マウスポインタをメニューバーの「ファイル」に移動します
2. クリックしてメニューを開きます
3. メニューが開いたら、「新規作成」項目を探します
4. 「新規作成」をクリックします
5. 新しい空白のドキュメントが表示されます

注意: 保存されていない変更がある場合、確認ダイアログが表示されることがあります。
この場合、「保存」「保存しない」「キャンセル」のいずれかを選択してください。

### 3.2.2 キーボードショートカットでの作成

キーボードショートカットとは、特定のキーの組み合わせを押すことで、
メニューコマンドを実行する機能です...

（以下続く、全体で数十ページ）
```

**ミニマリスト型マニュアル（タスク指向・最小限）**:

```markdown
# クイックスタート

## 新しいドキュメントを作成する

**方法1: メニューから**
1. **ファイル** > **新規作成** を選択
2. 空白のドキュメントが表示されます

**方法2: キーボードショートカット**
- Windows/Linux: `Ctrl + N`
- Mac: `Cmd + N`

**ヒント**: 既存ファイルを開いている状態で新規作成すると、新しいタブが開きます。

---

## ドキュメントを保存する

1. **ファイル** > **保存** を選択（または `Ctrl+S` / `Cmd+S`）
2. 初回保存時は、ファイル名と保存場所を指定します
3. **保存** をクリック

**トラブルシューティング**:
- 「保存できません」エラーが表示される → ディスクの空き容量を確認してください
- ファイル名に使えない文字（\ / : * ? " < > |）は削除してください

---

## ドキュメントを開く

1. **ファイル** > **開く** を選択（または `Ctrl+O` / `Cmd+O`）
2. ファイルを選択
3. **開く** をクリック

**最近使ったファイル**: **ファイル** > **最近使ったファイル** から素早くアクセスできます。

---

## 次のステップ

- [テキストの書式設定](formatting.md)
- [画像の挿入](images.md)
- [共同編集](collaboration.md)
```

#### 例2: APIドキュメントのミニマリスト設計

```markdown
# ユーザー管理API

## ユーザーを作成する

新しいユーザーアカウントを作成します。

### リクエスト

```http
POST /api/v1/users
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member"
}
```

### レスポンス

**成功（201 Created）**:
```json
{
  "id": "usr_123abc",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**エラー（400 Bad Request）**:
```json
{
  "error": "invalid_email",
  "message": "メールアドレスの形式が正しくありません"
}
```

### コード例

```javascript
const response = await fetch('https://api.example.com/api/v1/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    name: 'John Doe',
    role: 'member'
  })
});

const user = await response.json();
console.log('ユーザーID:', user.id);
```

### よくあるエラー

| エラーコード | 原因 | 解決方法 |
|------------|------|---------|
| `email_already_exists` | メールアドレスが既に登録されている | 別のメールアドレスを使用するか、既存ユーザーを更新 |
| `invalid_role` | 無効なロール値 | `admin`, `member`, `guest` のいずれかを指定 |
| `unauthorized` | APIキーが無効 | 有効なAPIキーを使用しているか確認 |

---

## ユーザーを取得する

指定したIDのユーザー情報を取得します。

### リクエスト

```http
GET /api/v1/users/{user_id}
Authorization: Bearer YOUR_API_KEY
```

### パラメータ

- `user_id` (required): ユーザーID（例: `usr_123abc`）

### レスポンス

```json
{
  "id": "usr_123abc",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member",
  "created_at": "2025-01-15T10:30:00Z",
  "last_login": "2025-01-20T14:22:00Z"
}
```

### コード例

```javascript
const userId = 'usr_123abc';
const response = await fetch(`https://api.example.com/api/v1/users/${userId}`, {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
});

const user = await response.json();
```

**エラー（404 Not Found）**: ユーザーIDが存在しない場合
```json
{
  "error": "user_not_found",
  "message": "指定されたユーザーが見つかりません"
}
```
```

### 参考文献・リソース

**書籍**
- Carroll, J. M. (1990). *The Nurnberg Funnel: Designing Minimalist Instruction for Practical Computer Skill*. MIT Press.
- Carroll, J. M. (1998). *Minimalism Beyond the Nurnberg Funnel*. MIT Press.
- van der Meij, H., & Carroll, J. M. (1995). "Principles and heuristics for designing minimalist instruction." *Technical Communication*, 42(2), 243-261.

**論文**
- Farkas, D. K., & Farkas, J. B. (2002). "Principles of Web design." *Allyn & Bacon*.
- Lazonder, A. W., & van der Meij, H. (1993). "The minimal manual: Is less really more?" *International Journal of Man-Machine Studies*, 39(5), 729-752.

---

## 3. Docs as Code

### 分類
ワークフロー・ツールチェーン・自動化

### 背景と歴史

Docs as Code（ドキュメントをコードとして扱う）は、2010年代にソフトウェア開発のベストプラクティスをドキュメンテーションプロセスに適用する動きとして生まれました。

従来のドキュメント作成では、Microsoft WordやAdobe FrameMakerなどのWYSIWYGツールが使用され、ドキュメントはソースコードとは別のワークフローで管理されていました。これにより、ドキュメントとコードの同期が困難で、古い情報が残りやすいという問題がありました。

Docs as Codeアプローチでは、ドキュメントをプレーンテキスト（Markdown、AsciiDoc、reStructuredText）で記述し、Gitでバージョン管理し、プルリクエストでレビューし、CI/CDで自動ビルド・デプロイします。

この手法は、GitHub、GitLab、Stripe、Twilio、Mozillaなどの多くのテック企業で採用されています。

### 詳細な理論

#### Docs as Codeの主要原則

**1. プレーンテキスト形式**
- Markdown、AsciiDoc、reStructuredText
- 理由: バージョン管理に適している、差分が見やすい、エディタを選ばない

**2. バージョン管理（Git）**
- ドキュメントをGitリポジトリで管理
- コードと同じリポジトリに配置（monorepo）または別リポジトリ
- ブランチ戦略（feature branch、release branch）

**3. コードレビュープロセス**
- プルリクエスト/マージリクエスト
- ピアレビュー、SME（Subject Matter Expert）レビュー
- レビューコメント、修正要求

**4. 自動化（CI/CD）**
- 自動ビルド（静的サイト生成）
- 自動テスト（リンク切れ、スペルチェック、スタイルガイド違反）
- 自動デプロイ（ステージング、プロダクション）

**5. イシュートラッキング**
- ドキュメントのバグ、改善要望をIssueで管理
- ユーザーフィードバックの収集

#### Docs as Codeのツールチェーン

**マークアップ言語**:
- Markdown: 最もシンプル、広く採用
- AsciiDoc: より高機能、技術書に適している
- reStructuredText: Python コミュニティで人気

**静的サイトジェネレーター**:
- **MkDocs**: Python製、Markdown、シンプル
- **Docusaurus**: Meta製、React、モダンなUI
- **Sphinx**: Python製、reStructuredText、API ドキュメントに強い
- **Jekyll**: Ruby製、GitHub Pages標準
- **Hugo**: Go製、高速ビルド

**CI/CDツール**:
- GitHub Actions
- GitLab CI
- CircleCI
- Travis CI

**ホスティング**:
- GitHub Pages
- GitLab Pages
- Netlify
- Vercel
- Read the Docs

#### Docs as Codeのワークフロー

1. **ローカル執筆**: エディタ（VS Code、VIM、IntelliJ）でMarkdownを記述
2. **ローカルプレビュー**: `mkdocs serve`などでローカルビルド、ブラウザでプレビュー
3. **コミット**: Git commitでローカルリポジトリに保存
4. **プッシュ**: Git pushでリモートリポジトリに送信
5. **プルリクエスト**: 変更のレビュー依頼
6. **レビュー**: レビュワーがコメント、修正要求
7. **マージ**: 承認後、mainブランチにマージ
8. **自動ビルド・デプロイ**: CI/CDが自動実行、サイトが更新

### 実践例

#### 例1: MkDocsを使ったDocs as Codeセットアップ

**プロジェクト構成**:
```
my-project/
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   ├── api/
│   │   ├── authentication.md
│   │   ├── users.md
│   │   └── projects.md
│   ├── guides/
│   │   ├── installation.md
│   │   └── configuration.md
│   └── images/
│       └── architecture.png
├── mkdocs.yml
├── .github/
│   └── workflows/
│       └── deploy-docs.yml
└── README.md
```

**mkdocs.yml（設定ファイル）**:
```yaml
site_name: My Project Documentation
site_url: https://docs.example.com
repo_url: https://github.com/example/my-project
repo_name: example/my-project

theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight
    - content.code.annotate

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Guides:
      - Installation: guides/installation.md
      - Configuration: guides/configuration.md
  - API Reference:
      - Authentication: api/authentication.md
      - Users: api/users.md
      - Projects: api/projects.md

plugins:
  - search
  - git-revision-date-localized
  - minify:
      minify_html: true

markdown_extensions:
  - admonition
  - codehilite:
      guess_lang: false
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - pymdownx.emoji
```

**docs/index.md（ホームページ）**:
```markdown
# My Project Documentation

Welcome to the official documentation for My Project.

## Quick Links

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Getting Started__

    ---

    Install My Project and get up and running in minutes

    [:octicons-arrow-right-24: Getting started](getting-started.md)

-   :material-book-open-variant:{ .lg .middle } __Guides__

    ---

    Step-by-step guides for common tasks

    [:octicons-arrow-right-24: Guides](guides/installation.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Complete API documentation with examples

    [:octicons-arrow-right-24: API](api/authentication.md)

-   :material-chat-question:{ .lg .middle } __Support__

    ---

    Need help? Check our FAQ or contact support

    [:octicons-arrow-right-24: Support](support.md)

</div>

## Features

- **Easy to Use**: Simple API with comprehensive examples
- **Fast**: Optimized for performance
- **Secure**: Built-in authentication and authorization
- **Scalable**: Handles millions of requests

## Installation

```bash
npm install my-project
```

## Quick Example

```javascript
const MyProject = require('my-project');

const client = new MyProject({
  apiKey: 'your-api-key'
});

const result = await client.users.create({
  name: 'John Doe',
  email: 'john@example.com'
});

console.log(result);
```

## Next Steps

- [Read the Getting Started guide](getting-started.md)
- [Explore the API Reference](api/authentication.md)
- [Check out example projects](https://github.com/example/my-project-examples)
```

**GitHub Actions ワークフロー（.github/workflows/deploy-docs.yml）**:
```yaml
name: Deploy Documentation

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
  pull_request:
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # git-revision-date-localizedプラグイン用

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x

      - name: Install dependencies
        run: |
          pip install mkdocs-material
          pip install mkdocs-git-revision-date-localized-plugin
          pip install mkdocs-minify-plugin

      - name: Build documentation
        run: mkdocs build --strict

      - name: Run link checker
        uses: lycheeverse/lychee-action@v1
        with:
          args: --verbose --no-progress './site/**/*.html'
        continue-on-error: true

      - name: Deploy to GitHub Pages
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
          cname: docs.example.com  # カスタムドメイン使用時
```

**ローカル開発コマンド**:
```bash
# MkDocsインストール
pip install mkdocs-material

# ローカルサーバー起動（ライブリロード有効）
mkdocs serve

# ブラウザで http://127.0.0.1:8000/ にアクセス

# 本番ビルド
mkdocs build

# デプロイ（GitHub Pagesへ）
mkdocs gh-deploy
```

#### 例2: ドキュメントレビューのプルリクエストテンプレート

**.github/PULL_REQUEST_TEMPLATE.md**:
```markdown
## 変更内容

<!-- このPRで変更した内容を簡潔に説明してください -->

## 変更の種類

- [ ] 新規ドキュメント
- [ ] 既存ドキュメントの更新
- [ ] 誤字・タイポの修正
- [ ] リンク切れの修正
- [ ] コードサンプルの更新
- [ ] 画像・図の追加/更新

## チェックリスト

### 基本
- [ ] ローカルでビルドが成功することを確認した（`mkdocs build`）
- [ ] ローカルサーバーで表示を確認した（`mkdocs serve`）
- [ ] リンクが正しく動作することを確認した

### コンテンツ品質
- [ ] 文法・スペルチェックを行った
- [ ] コードサンプルを実際に実行して動作確認した
- [ ] スクリーンショットは最新バージョンのものである
- [ ] 専門用語には説明または用語集へのリンクを付けた
- [ ] 対象読者にとって理解しやすい表現になっている

### スタイルガイド
- [ ] [スタイルガイド](STYLE_GUIDE.md)に準拠している
- [ ] 見出しレベルが適切（H1は1つ、階層をスキップしない）
- [ ] コードブロックに言語指定がある
- [ ] 箇条書きの形式が統一されている

## スクリーンショット（UI変更がある場合）

<!-- 変更前後のスクリーンショットを追加してください -->

| Before | After |
|--------|-------|
| ![before](url) | ![after](url) |

## 関連Issue

Closes #issue_number

## レビュー依頼事項

<!-- レビュワーに特に確認してほしい点があれば記載してください -->

## 追加コンテキスト

<!-- その他、レビュワーが知っておくべき情報があれば記載してください -->
```

#### 例3: ドキュメントテストの自動化

**tests/test_docs.py（Pythonでのテスト例）**:
```python
import os
import re
from pathlib import Path
import pytest

DOCS_DIR = Path("docs")

def get_all_md_files():
    """すべてのMarkdownファイルを取得"""
    return list(DOCS_DIR.rglob("*.md"))

def test_no_empty_files():
    """空のMarkdownファイルがないことを確認"""
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, f"{md_file} is empty"

def test_all_files_have_title():
    """すべてのファイルにH1見出しがあることを確認"""
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8')
        assert re.search(r'^# .+', content, re.MULTILINE), \
            f"{md_file} doesn't have a title (H1 heading)"

def test_no_duplicate_h1():
    """H1見出しが1つだけであることを確認"""
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8')
        h1_count = len(re.findall(r'^# .+', content, re.MULTILINE))
        assert h1_count == 1, \
            f"{md_file} has {h1_count} H1 headings (should be 1)"

def test_code_blocks_have_language():
    """コードブロックに言語指定があることを確認"""
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8')
        # ```で始まる行を検出
        code_blocks = re.findall(r'^```(\w*)', content, re.MULTILINE)
        for i, lang in enumerate(code_blocks):
            assert lang, \
                f"{md_file} has a code block without language specification (block #{i+1})"

def test_no_broken_internal_links():
    """内部リンク切れがないことを確認"""
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8')
        # Markdownリンク [text](url) を検出
        links = re.findall(r'\[.+?\]\((.+?)\)', content)
        
        for link in links:
            # 外部リンクとアンカーはスキップ
            if link.startswith('http') or link.startswith('#'):
                continue
            
            # 相対パスを解決
            link_path = (md_file.parent / link).resolve()
            assert link_path.exists(), \
                f"{md_file} has broken link: {link}"

def test_consistent_list_style():
    """箇条書きのスタイルが統一されていることを確認（- を推奨）"""
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8')
        # * で始まる箇条書きを検出
        asterisk_lists = re.findall(r'^\* .+', content, re.MULTILINE)
        assert len(asterisk_lists) == 0, \
            f"{md_file} uses * for lists (use - instead for consistency)"

def test_no_hardcoded_version():
    """ハードコードされたバージョン番号がないことを確認（変数化推奨）"""
    version_pattern = r'version\s+\d+\.\d+\.\d+'
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8').lower()
        match = re.search(version_pattern, content)
        if match:
            pytest.fail(f"{md_file} contains hardcoded version: {match.group()}")

@pytest.mark.parametrize("term,explanation", [
    ("API", "Application Programming Interface"),
    ("REST", "Representational State Transfer"),
    ("JWT", "JSON Web Token"),
])
def test_acronyms_explained(term, explanation):
    """頭字語の初出時に説明があることを確認"""
    for md_file in get_all_md_files():
        content = md_file.read_text(encoding='utf-8')
        if term in content:
            # 初出時に説明があるか確認（簡易チェック）
            assert explanation.lower() in content.lower() or \
                   f"{term} ({explanation})" in content, \
                f"{md_file} uses '{term}' without explanation"
```

**GitHub Actionsでテスト実行**:
```yaml
name: Documentation Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x
      
      - name: Install dependencies
        run: |
          pip install pytest
      
      - name: Run documentation tests
        run: pytest tests/test_docs.py -v
      
      - name: Spell check
        uses: rojopolis/spellcheck-github-actions@0.24.0
        with:
          config_path: .spellcheck.yml
```

### 参考文献・リソース

**書籍**
- Gentle, A., & others. (2017). *Docs Like Code*. https://www.docslikecode.com/
- Holscher, E., & others. (2018). *Write the Docs Guide*. https://www.writethedocs.org/guide/

**ツール**
- MkDocs: https://www.mkdocs.org/
- Docusaurus: https://docusaurus.io/
- Sphinx: https://www.sphinx-doc.org/
- Material for MkDocs: https://squidfunk.github.io/mkdocs-material/

**コミュニティ**
- Write the Docs: https://www.writethedocs.org/

---

## 4. API ドキュメンテーション（OpenAPI/Swagger）

### 分類
API仕様・自動生成・インタラクティブドキュメント

### 背景と歴史

OpenAPI Specification（旧Swagger Specification）は、RESTful APIを記述するための標準仕様です。2011年にTony Tam（Wordnik社）が開発した「Swagger」が起源で、2016年にLinux Foundationの下でOpenAPI Initiativeに移管され、OpenAPI Specification（OAS）として標準化されました。

現在の最新バージョンはOpenAPI 3.1（2021年リリース）で、JSON Schema 2020-12と完全互換になりました。

OpenAPIは「API-First（APIファースト）」開発の重要な要素で、API仕様を先に定義してから実装することで、フロントエンド・バックエンド・モバイルチームの並行開発を可能にします。

主要な利点:
- **仕様駆動開発**: 仕様からコード、モック、ドキュメントを自動生成
- **インタラクティブドキュメント**: Swagger UIで実際にAPIを試せる
- **クライアントSDK自動生成**: 多言語対応
- **バリデーション**: リクエスト/レスポンスの自動検証

### 詳細な理論

#### OpenAPI Specificationの構造

OpenAPI仕様は、YAMLまたはJSON形式で記述されます。主要な要素:

**1. Info Object（情報オブジェクト）**
- API名、バージョン、説明、ライセンス、連絡先

**2. Servers Object（サーバーオブジェクト）**
- APIのベースURL（本番、ステージング、開発環境）

**3. Paths Object（パスオブジェクト）**
- エンドポイント定義（URL、HTTPメソッド、パラメータ、レスポンス）

**4. Components Object（コンポーネントオブジェクト）**
- 再利用可能な定義（スキーマ、レスポンス、パラメータ、セキュリティスキーム）

**5. Security Object（セキュリティオブジェクト）**
- 認証・認可方式（API Key、OAuth 2.0、OpenID Connect、HTTP Bearer）

**6. Tags Object（タグオブジェクト）**
- エンドポイントのグループ化

#### OpenAPIのベストプラクティス

1. **例を豊富に含める**: requestBodyとresponseに実例を提供
2. **説明を詳細に**: 各フィールドの目的、制約、デフォルト値を記載
3. **エラーレスポンスも定義**: すべてのステータスコードのレスポンスを記載
4. **セキュリティを明示**: 各エンドポイントの認証要件を明確に
5. **バージョニング**: セマンティックバージョニング（SemVer）を使用

### 実践例

#### 例1: OpenAPI 3.1仕様の完全例

```yaml
openapi: 3.1.0

info:
  title: Task Management API
  version: 1.0.0
  description: |
    A RESTful API for managing tasks and projects.
    
    ## Features
    - Create, read, update, and delete tasks
    - Organize tasks into projects
    - Assign tasks to users
    - Track task status and priority
    
    ## Authentication
    All endpoints require an API key passed in the `Authorization` header.
  contact:
    name: API Support
    email: api-support@example.com
    url: https://support.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
  - url: http://localhost:3000/v1
    description: Development server

tags:
  - name: tasks
    description: Task operations
  - name: projects
    description: Project operations
  - name: users
    description: User operations

paths:
  /tasks:
    get:
      tags:
        - tasks
      summary: List all tasks
      description: |
        Retrieve a paginated list of tasks. You can filter by status, priority, 
        assignee, and project.
      operationId: listTasks
      parameters:
        - name: page
          in: query
          description: Page number (1-based)
          required: false
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: per_page
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - name: status
          in: query
          description: Filter by task status
          required: false
          schema:
            type: string
            enum: [todo, in_progress, done, archived]
        - name: priority
          in: query
          description: Filter by task priority
          required: false
          schema:
            type: string
            enum: [low, medium, high, urgent]
        - name: assignee_id
          in: query
          description: Filter by assignee user ID
          required: false
          schema:
            type: string
        - name: project_id
          in: query
          description: Filter by project ID
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
              examples:
                success:
                  summary: Example response with tasks
                  value:
                    data:
                      - id: "task_123"
                        title: "Implement user authentication"
                        description: "Add OAuth 2.0 authentication to the API"
                        status: "in_progress"
                        priority: "high"
                        assignee_id: "user_456"
                        project_id: "proj_789"
                        due_date: "2025-02-15"
                        created_at: "2025-01-10T10:00:00Z"
                        updated_at: "2025-01-12T14:30:00Z"
                      - id: "task_124"
                        title: "Write API documentation"
                        description: "Create OpenAPI specification"
                        status: "todo"
                        priority: "medium"
                        assignee_id: "user_457"
                        project_id: "proj_789"
                        due_date: "2025-02-20"
                        created_at: "2025-01-11T09:00:00Z"
                        updated_at: "2025-01-11T09:00:00Z"
                    pagination:
                      total: 42
                      page: 1
                      per_page: 20
                      total_pages: 3
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'
      security:
        - ApiKeyAuth: []
    
    post:
      tags:
        - tasks
      summary: Create a new task
      description: Create a new task in the system
      operationId: createTask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
            examples:
              basic:
                summary: Basic task creation
                value:
                  title: "Fix login bug"
                  description: "Users can't log in with email addresses containing +"
                  status: "todo"
                  priority: "high"
              with_assignment:
                summary: Task with assignee and due date
                value:
                  title: "Review pull request #123"
                  description: "Review authentication refactoring PR"
                  status: "todo"
                  priority: "medium"
                  assignee_id: "user_456"
                  project_id: "proj_789"
                  due_date: "2025-01-25"
      responses:
        '201':
          description: Task created successfully
          headers:
            Location:
              description: URL of the created task
              schema:
                type: string
                example: /v1/tasks/task_125
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
              examples:
                success:
                  summary: Created task
                  value:
                    id: "task_125"
                    title: "Fix login bug"
                    description: "Users can't log in with email addresses containing +"
                    status: "todo"
                    priority: "high"
                    assignee_id: null
                    project_id: null
                    due_date: null
                    created_at: "2025-01-15T10:30:00Z"
                    updated_at: "2025-01-15T10:30:00Z"
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ValidationError'
              examples:
                validation_error:
                  summary: Missing required field
                  value:
                    error: "validation_error"
                    message: "Validation failed"
                    details:
                      - field: "title"
                        message: "Title is required"
        '500':
          $ref: '#/components/responses/InternalServerError'
      security:
        - ApiKeyAuth: []
  
  /tasks/{task_id}:
    parameters:
      - name: task_id
        in: path
        required: true
        description: The unique identifier of the task
        schema:
          type: string
          example: "task_123"
    
    get:
      tags:
        - tasks
      summary: Get a single task
      description: Retrieve detailed information about a specific task
      operationId: getTask
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - ApiKeyAuth: []
    
    patch:
      tags:
        - tasks
      summary: Update a task
      description: Update one or more fields of an existing task
      operationId: updateTask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
            examples:
              update_status:
                summary: Update task status
                value:
                  status: "done"
              update_assignment:
                summary: Reassign task
                value:
                  assignee_id: "user_458"
                  priority: "urgent"
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - ApiKeyAuth: []
    
    delete:
      tags:
        - tasks
      summary: Delete a task
      description: Permanently delete a task from the system
      operationId: deleteTask
      responses:
        '204':
          description: Task deleted successfully (no content)
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - ApiKeyAuth: []

components:
  schemas:
    Task:
      type: object
      required:
        - id
        - title
        - status
        - priority
        - created_at
        - updated_at
      properties:
        id:
          type: string
          description: Unique identifier for the task
          example: "task_123"
        title:
          type: string
          description: Task title
          minLength: 1
          maxLength: 200
          example: "Implement user authentication"
        description:
          type: string
          description: Detailed description of the task
          maxLength: 5000
          example: "Add OAuth 2.0 authentication to the API"
        status:
          type: string
          description: Current status of the task
          enum: [todo, in_progress, done, archived]
          example: "in_progress"
        priority:
          type: string
          description: Priority level of the task
          enum: [low, medium, high, urgent]
          example: "high"
        assignee_id:
          type: string
          nullable: true
          description: ID of the user assigned to this task
          example: "user_456"
        project_id:
          type: string
          nullable: true
          description: ID of the project this task belongs to
          example: "proj_789"
        due_date:
          type: string
          format: date
          nullable: true
          description: Due date for the task (ISO 8601 format)
          example: "2025-02-15"
        created_at:
          type: string
          format: date-time
          description: Timestamp when the task was created
          example: "2025-01-10T10:00:00Z"
        updated_at:
          type: string
          format: date-time
          description: Timestamp when the task was last updated
          example: "2025-01-12T14:30:00Z"
    
    TaskCreate:
      type: object
      required:
        - title
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
          example: "Implement user authentication"
        description:
          type: string
          maxLength: 5000
          example: "Add OAuth 2.0 authentication to the API"
        status:
          type: string
          enum: [todo, in_progress, done, archived]
          default: todo
        priority:
          type: string
          enum: [low, medium, high, urgent]
          default: medium
        assignee_id:
          type: string
          example: "user_456"
        project_id:
          type: string
          example: "proj_789"
        due_date:
          type: string
          format: date
          example: "2025-02-15"
    
    TaskUpdate:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 5000
        status:
          type: string
          enum: [todo, in_progress, done, archived]
        priority:
          type: string
          enum: [low, medium, high, urgent]
        assignee_id:
          type: string
          nullable: true
        project_id:
          type: string
          nullable: true
        due_date:
          type: string
          format: date
          nullable: true
    
    Pagination:
      type: object
      required:
        - total
        - page
        - per_page
        - total_pages
      properties:
        total:
          type: integer
          description: Total number of items
          example: 42
        page:
          type: integer
          description: Current page number (1-based)
          example: 1
        per_page:
          type: integer
          description: Number of items per page
          example: 20
        total_pages:
          type: integer
          description: Total number of pages
          example: 3
    
    Error:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
          description: Error code
          example: "not_found"
        message:
          type: string
          description: Human-readable error message
          example: "The requested resource was not found"
        details:
          type: object
          description: Additional error details
          additionalProperties: true
    
    ValidationError:
      type: object
      required:
        - error
        - message
        - details
      properties:
        error:
          type: string
          example: "validation_error"
        message:
          type: string
          example: "Validation failed"
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
                example: "title"
              message:
                type: string
                example: "Title is required"
  
  responses:
    BadRequest:
      description: Bad request - invalid input
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "bad_request"
            message: "Invalid request parameters"
    
    Unauthorized:
      description: Unauthorized - invalid or missing API key
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "unauthorized"
            message: "Invalid or missing API key"
    
    NotFound:
      description: Not found - resource doesn't exist
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "not_found"
            message: "The requested resource was not found"
    
    InternalServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "internal_server_error"
            message: "An unexpected error occurred. Please try again later."
  
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Authorization
      description: |
        API key authentication. Pass your API key in the Authorization header:
        
        ```
        Authorization: Bearer YOUR_API_KEY
        ```
        
        You can obtain an API key from your account settings.
```

#### 例2: OpenAPI仕様からドキュメント生成

**Swagger UIでの表示**:
```bash
# Swagger UIをDockerで起動
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/openapi.yaml \
  -v $(pwd)/openapi.yaml:/openapi.yaml \
  swaggerapi/swagger-ui

# ブラウザで http://localhost:8080 にアクセス
```

**ReDocでの表示（よりモダンなUI）**:
```bash
# ReDocをDockerで起動
docker run -p 8080:80 \
  -e SPEC_URL=https://raw.githubusercontent.com/example/api/main/openapi.yaml \
  redocly/redoc

# または静的HTMLを生成
npx @redocly/cli build-docs openapi.yaml -o docs/api.html
```

**コードジェネレーター**:
```bash
# TypeScript Fetch クライアント生成
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./src/api-client

# Python クライアント生成
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./python-client \
  --additional-properties=packageName=task_api

# Go サーバースタブ生成
openapi-generator-cli generate \
  -i openapi.yaml \
  -g go-server \
  -o ./go-server
```

### 参考文献・リソース

**公式仕様**
- OpenAPI Initiative. (2021). *OpenAPI Specification 3.1.0*. https://spec.openapis.org/oas/v3.1.0

**書籍**
- Ponelat, J., & Rosenstock, L. (2022). *Designing APIs with Swagger and OpenAPI*. Manning Publications.

**ツール**
- Swagger Editor: https://editor.swagger.io/
- Swagger UI: https://swagger.io/tools/swagger-ui/
- ReDoc: https://redocly.com/redoc/
- Stoplight Studio: https://stoplight.io/studio/
- OpenAPI Generator: https://openapi-generator.tech/

---

## 5. 情報タイプ理論（Information Types）

### 分類
情報設計・コンテンツ分類・構造化

### 背景と歴史

情報タイプ理論（Information Typing）は、Robert Horn（1989年）とJoAnn Hackos（1994年）らによって提唱された、技術文書のコンテンツを明確なタイプに分類する手法です。

この理論は、「すべてのコンテンツが同じ構造・目的を持つわけではない」という認識から生まれました。異なるタイプの情報は、異なる構造とライティングスタイルを必要とします。

情報タイプ理論は、DITA のトピックタイプ（Concept、Task、Reference）の基盤となっており、現代のテクニカルライティングの標準的なアプローチとなっています。

### 詳細な理論

#### 主要な情報タイプ

**1. Conceptual Information（概念情報）**
「What is it?（それは何か）」に答える情報です。

目的:
- 背景知識の提供
- 用語・概念の定義
- システムの仕組みの説明

構造:
- タイトル
- 定義・説明
- 図・ダイアグラム
- 例
- 関連概念へのリンク

例:
- 「クラウドコンピューティングとは」
- 「REST APIの原則」
- 「マイクロサービスアーキテクチャの概要」

**2. Procedural Information（手順情報）**
「How do I do it?（どうやるのか）」に答える情報です。

目的:
- タスクの実行方法を説明
- ステップバイステップの手順
- ゴール達成を支援

構造:
- タイトル（動詞で開始）
- 前提条件
- 番号付きステップ
- スクリーンショット・図
- 結果
- 次のステップ

例:
- 「データベースに接続する方法」
- 「新しいユーザーを追加する」
- 「アプリケーションをデプロイする」

**3. Reference Information（参照情報）**
「What are the facts?（事実は何か）」に答える情報です。

目的:
- 詳細な仕様・パラメータの提供
- 素早い情報検索
- 完全な情報の網羅

構造:
- タイトル
- 表形式データ
- パラメータリスト
- 戻り値・例外
- コードサンプル

例:
- 「API エンドポイントリファレンス」
- 「設定ファイルパラメータ一覧」
- 「エラーコード表」

**4. Troubleshooting Information（トラブルシューティング情報）**
「What went wrong?（何が間違ったのか）」に答える情報です。

目的:
- 問題の診断
- 解決方法の提示
- エラーからの回復

構造:
- 症状・エラーメッセージ
- 原因
- 解決手順
- 予防策

例:
- 「接続エラーが発生する」
- 「データが保存されない」
- 「パフォーマンスが遅い」

**5. Tutorial Information（チュートリアル情報）**
「How does this work in practice?（実際にどう動くのか）」に答える情報です。

目的:
- 学習目的の段階的説明
- 実践的なスキル習得
- 理解の促進

構造:
- 学習目標
- 前提知識
- ステップバイステップの説明と実行
- 解説・理論の補足
- 演習問題
- まとめ

例:
- 「REST API入門：15分で学ぶ」
- 「Reactでのステート管理チュートリアル」
- 「TerraformでAWSインフラを構築する」

#### 情報タイプの選択基準

| ユーザーの質問 | 情報タイプ | 例 |
|--------------|----------|-----|
| これは何？ | Concept | 「OAuthとは」 |
| どうやるの？ | Task | 「OAuthの実装方法」 |
| 詳細は？ | Reference | 「OAuthスコープ一覧」 |
| 動かない！ | Troubleshooting | 「トークン取得エラー」 |
| 学びたい | Tutorial | 「OAuth入門」 |

### 実践例

#### 例1: 同じトピックの異なる情報タイプ

**Topic: Docker**

**Concept（概念）**:
```markdown
# Dockerとは

Dockerは、アプリケーションをコンテナと呼ばれる軽量で移植可能な実行環境にパッケージ化するプラットフォームです。

## 主要概念

### コンテナ
コンテナは、アプリケーションとその依存関係を含む独立した実行環境です。
仮想マシンと異なり、OSカーネルを共有するため、起動が速く、リソース効率が高い特徴があります。

### イメージ
Dockerイメージは、コンテナを作成するためのテンプレートです。
アプリケーションコード、ランタイム、ライブラリ、設定ファイルなどが含まれます。

### Dockerfile
Dockerfileは、Dockerイメージをビルドするための命令を記述したテキストファイルです。

## なぜDockerを使うのか

- **一貫性**: 開発環境と本番環境の差異をなくす
- **移植性**: どのOS・クラウドでも同じように動作
- **分離**: アプリケーション間の依存関係の競合を避ける
- **効率**: 仮想マシンより軽量で高速
```

**Task（手順）**:
```markdown
# Dockerコンテナを起動する

この手順では、Dockerイメージからコンテナを起動する方法を説明します。

## 前提条件

- Docker Desktop がインストールされている
- Docker デーモンが起動している
- 使用するイメージが存在する（`docker images`で確認）

## 手順

1. **使用可能なイメージを確認します**
   ```bash
   docker images
   ```
   
2. **コンテナを起動します**
   ```bash
   docker run -d --name myapp -p 8080:80 nginx:latest
   ```
   
   **オプションの説明**:
   - `-d`: デタッチモード（バックグラウンド実行）
   - `--name myapp`: コンテナ名を指定
   - `-p 8080:80`: ホストの8080ポートをコンテナの80ポートにマッピング
   - `nginx:latest`: 使用するイメージ

3. **コンテナが起動していることを確認します**
   ```bash
   docker ps
   ```

4. **ブラウザで確認します**
   http://localhost:8080 にアクセスして、Nginxのウェルカムページが表示されることを確認します。

## 結果

Nginxコンテナが起動し、ローカルマシンのポート8080でアクセス可能になりました。

## 次のステップ

- [コンテナのログを確認する](logs.md)
- [コンテナを停止する](stop.md)
- [カスタムイメージをビルドする](build.md)
```

**Reference（参照）**:
```markdown
# docker run コマンドリファレンス

## 構文

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

## 説明

指定したイメージから新しいコンテナを作成して起動します。

## 主要オプション

| オプション | 短縮形 | 説明 | 例 |
|----------|-------|------|-----|
| --name | なし | コンテナ名を指定 | `--name myapp` |
| --detach | -d | バックグラウンドで実行 | `-d` |
| --interactive | -i | 標準入力を開いたままにする | `-i` |
| --tty | -t | 疑似TTYを割り当てる | `-t` |
| --publish | -p | ポートをマッピング | `-p 8080:80` |
| --volume | -v | ボリュームをマウント | `-v /host:/container` |
| --env | -e | 環境変数を設定 | `-e NODE_ENV=production` |
| --env-file | なし | 環境変数ファイルを読み込み | `--env-file .env` |
| --network | なし | ネットワークに接続 | `--network mynet` |
| --rm | なし | 終了時に自動削除 | `--rm` |
| --memory | -m | メモリ制限 | `-m 512m` |
| --cpus | なし | CPU制限 | `--cpus 2.0` |

## 例

### 基本的な起動
```bash
docker run nginx:latest
```

### インタラクティブシェル
```bash
docker run -it ubuntu:latest /bin/bash
```

### ポートマッピングとバックグラウンド実行
```bash
docker run -d -p 3000:3000 --name webapp node-app:1.0
```

### 環境変数とボリュームマウント
```bash
docker run -d \
  -e DATABASE_URL=postgres://db:5432/mydb \
  -e NODE_ENV=production \
  -v $(pwd)/data:/app/data \
  -p 8080:8080 \
  myapp:latest
```

### メモリとCPU制限
```bash
docker run -d \
  --memory=512m \
  --cpus=2.0 \
  --name limited-app \
  myapp:latest
```

## 関連コマンド

- `docker ps`: 実行中のコンテナを表示
- `docker stop`: コンテナを停止
- `docker rm`: コンテナを削除
- `docker logs`: コンテナのログを表示
- `docker exec`: 実行中のコンテナでコマンドを実行
```

**Troubleshooting（トラブルシューティング）**:
```markdown
# Dockerコンテナのトラブルシューティング

## コンテナが起動しない

### 症状
`docker run`コマンドを実行してもコンテナが起動せず、即座に終了する。

### 原因
1. Dockerfileのエントリポイント/コマンドが即座に終了するプロセスを指定している
2. 設定エラー（環境変数、ボリュームマウントなど）
3. ポート衝突

### 解決方法

1. **ログを確認する**
   ```bash
   docker logs <container_id>
   ```
   エラーメッセージから原因を特定します。

2. **終了コードを確認する**
   ```bash
   docker ps -a
   ```
   STATUS列のExit codeを確認：
   - Exit 0: 正常終了（意図的）
   - Exit 1: アプリケーションエラー
   - Exit 137: メモリ不足によるKill

3. **インタラクティブモードで起動**
   ```bash
   docker run -it --entrypoint /bin/bash myimage:latest
   ```
   コンテナ内で手動で調査します。

## ポートにアクセスできない

### 症状
`docker run -p 8080:80 nginx`を実行したが、`localhost:8080`にアクセスできない。

### 原因
1. ポートマッピングが正しくない
2. コンテナ内のアプリが0.0.0.0ではなくlocalhostでリッスンしている
3. ファイアウォールがポートをブロック

### 解決方法

1. **ポートマッピングを確認**
   ```bash
   docker port <container_name>
   ```

2. **コンテナ内からアクセスを試す**
   ```bash
   docker exec -it <container_name> curl localhost:80
   ```
   これが成功すれば、アプリは動作しており、ポートマッピングの問題。

3. **正しい構文を使用**
   ```bash
   docker run -p 8080:80 nginx  # ホスト8080 → コンテナ80
   ```

## コンテナ内でファイルが見つからない

### 症状
ボリュームマウントしたファイルがコンテナ内に存在しない。

### 原因
1. マウントパスが間違っている
2. ホスト側のパスが存在しない
3. Windowsのパス形式の問題

### 解決方法

1. **マウントを確認**
   ```bash
   docker inspect <container_name> | grep -A 10 Mounts
   ```

2. **正しいパス形式を使用**
   ```bash
   # Linux/Mac
   docker run -v /absolute/path:/container/path myimage
   
   # Windows (PowerShell)
   docker run -v ${PWD}:/app myimage
   
   # Windows (CMD)
   docker run -v %cd%:/app myimage
   ```

3. **ファイルが存在することを確認**
   ```bash
   ls -la /host/path
   docker exec -it <container> ls -la /container/path
   ```
```

**Tutorial（チュートリアル）**:
```markdown
# Dockerチュートリアル: Node.js アプリをコンテナ化する

このチュートリアルでは、簡単なNode.js アプリケーションをDockerコンテナで実行する方法を学びます。

**所要時間**: 30分  
**前提知識**: Node.jsの基本、ターミナルの使い方

## 学習目標

このチュートリアルを完了すると、以下ができるようになります：

- Dockerfileを作成する
- Dockerイメージをビルドする
- コンテナを起動・停止する
- ホストとコンテナ間でファイルを共有する

## ステップ1: サンプルアプリケーションを作成する

まず、シンプルなNode.js Webサーバーを作成しましょう。

```bash
mkdir docker-tutorial
cd docker-tutorial
```

`app.js`ファイルを作成：

```javascript
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Docker!');
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

`package.json`ファイルを作成：

```json
{
  "name": "docker-tutorial",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

**なぜこうするのか**: `0.0.0.0`でリッスンすることで、コンテナ外部からのアクセスを受け付けられます。

## ステップ2: Dockerfileを作成する

`Dockerfile`（拡張子なし）を作成：

```dockerfile
# ベースイメージとしてNode.js 18を使用
FROM node:18-alpine

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonをコピーして依存関係をインストール
COPY package.json .
RUN npm install

# アプリケーションコードをコピー
COPY app.js .

# ポート3000を公開
EXPOSE 3000

# アプリケーションを起動
CMD ["node", "app.js"]
```

**各命令の意味**:
- `FROM`: ベースとなるイメージを指定（ここではNode.js 18のAlpine Linux版）
- `WORKDIR`: コンテナ内の作業ディレクトリを設定
- `COPY`: ホストからコンテナへファイルをコピー
- `RUN`: イメージビルド時にコマンドを実行
- `EXPOSE`: コンテナがリッスンするポートを文書化
- `CMD`: コンテナ起動時に実行するコマンド

## ステップ3: Dockerイメージをビルドする

```bash
docker build -t my-node-app:1.0 .
```

- `-t my-node-app:1.0`: イメージに名前とタグを付ける
- `.`: 現在のディレクトリのDockerfileを使用

ビルドが完了したら、イメージを確認：

```bash
docker images
```

出力例：
```
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
my-node-app    1.0       abc123def456   10 seconds ago   120MB
```

## ステップ4: コンテナを起動する

```bash
docker run -d -p 3000:3000 --name myapp my-node-app:1.0
```

- `-d`: バックグラウンドで実行
- `-p 3000:3000`: ホストの3000ポートをコンテナの3000ポートにマッピング
- `--name myapp`: コンテナに名前を付ける

コンテナが起動したことを確認：

```bash
docker ps
```

## ステップ5: アプリケーションをテストする

ブラウザで`http://localhost:3000`にアクセスするか、curlで確認：

```bash
curl http://localhost:3000
```

出力：
```
Hello from Docker!
```

## ステップ6: ログを確認する

```bash
docker logs myapp
```

出力：
```
Server running on port 3000
```

## ステップ7: コンテナを停止・削除する

```bash
# コンテナを停止
docker stop myapp

# コンテナを削除
docker rm myapp

# イメージを削除（オプション）
docker rmi my-node-app:1.0
```

## 次のステップ

おめでとうございます！Dockerの基本を学びました。次は：

- [Docker Composeで複数コンテナを管理する](docker-compose-tutorial.md)
- [ボリュームを使ってデータを永続化する](volumes-tutorial.md)
- [Docker Hubにイメージを公開する](docker-hub-tutorial.md)

## 完全なコード

完全なサンプルコードは[GitHubリポジトリ](https://github.com/example/docker-tutorial)で確認できます。
```

### 参考文献・リソース

**書籍**
- Horn, R. E. (1989). *Mapping Hypertext: Analysis, Linkage, and Display of Knowledge for the Next Generation of On-Line Text and Graphics*. Lexington Institute.
- Hackos, J. T. (1994). *Managing Your Documentation Projects*. Wiley.
- Hackos, J. T., & Stevens, D. M. (1997). *Standards for Online Communication*. Wiley.

**論文**
- Albers, M. J. (2003). "Single sourcing and the technical communication career path." *Technical Communication*, 50(3), 335-343.

---

## フレームワーク選択ガイド

| プロジェクト種別 | 推奨フレームワーク | 重点領域 |
|-----------------|-----------------|---------|
| **大規模製品ドキュメント** | DITA、情報タイプ理論 | トピックベース、再利用、マルチチャネル公開 |
| **スタートアップMVPドキュメント** | Docs as Code、ミニマリズム | 素早いイテレーション、最小限の記述 |
| **REST API** | OpenAPI/Swagger、API ドキュメンテーション | 仕様駆動、自動生成、インタラクティブ |
| **ユーザーマニュアル** | ミニマリズム、情報タイプ理論 | タスク指向、簡潔、実例重視 |
| **開発者ドキュメント** | Docs as Code、OpenAPI、情報タイプ理論 | バージョン管理、コードサンプル、API リファレンス |

---

## 実践統合例

```markdown
# API ドキュメント統合プロジェクト

## 構成

my-api-docs/
├── openapi/
│   └── api-spec.yaml           # OpenAPI仕様（単一ソース）
├── docs/
│   ├── concepts/               # Conceptトピック
│   │   ├── authentication.md
│   │   └── rate-limiting.md
│   ├── guides/                 # Taskトピック
│   │   ├── getting-started.md
│   │   └── pagination.md
│   ├── reference/              # Referenceトピック（自動生成）
│   │   └── api-reference.md
│   └── troubleshooting/        # Troubleshootingトピック
│       └── common-errors.md
├── mkdocs.yml
└── .github/workflows/
    └── deploy.yml

## ワークフロー

1. **OpenAPI仕様を記述** (openapi/api-spec.yaml)
2. **Docs as Codeで手動コンテンツを記述** (docs/)
3. **CI/CDで自動生成**:
   - OpenAPI仕様からAPIリファレンスを自動生成
   - MkDocsでHTMLサイトをビルド
   - GitHub Pagesにデプロイ

## 利点

- **単一ソース**: OpenAPI仕様が真実の源
- **自動同期**: コードとドキュメントの乖離を防ぐ
- **モジュール性**: DITA/情報タイプ理論の原則を適用
- **ミニマリズム**: 必要最小限の記述
```

---

## まとめ

テクニカルライターが活用する5つの主要フレームワーク：

1. **DITA**: トピックベースオーサリング、再利用、構造化、マルチチャネル公開
2. **ミニマリズム**: タスク指向、最小限の説明、エラーからの学習サポート、実世界のアクティビティ
3. **Docs as Code**: プレーンテキスト、Git、プルリクエスト、CI/CD、自動化
4. **API ドキュメンテーション**: OpenAPI/Swagger、仕様駆動開発、自動生成、インタラクティブドキュメント
5. **情報タイプ理論**: Concept、Task、Reference、Troubleshooting、Tutorialの明確な分類

これらを組み合わせることで、ユーザーフレンドリーで保守しやすい技術文書を作成できます。

---

## 参考文献

**書籍**
- Bellamy, L., Carey, M., & Schlotfeldt, J. (2012). *DITA Best Practices*. IBM Press.
- Carroll, J. M. (1990). *The Nurnberg Funnel: Designing Minimalist Instruction for Practical Computer Skill*. MIT Press.
- Gentle, A. (2017). *Docs Like Code*. https://www.docslikecode.com/
- Ponelat, J., & Rosenstock, L. (2022). *Designing APIs with Swagger and OpenAPI*. Manning.

**スタイルガイド**
- Microsoft. (2021). *Microsoft Writing Style Guide*. https://learn.microsoft.com/en-us/style-guide/welcome/
- Google. (2023). *Google Developer Documentation Style Guide*. https://developers.google.com/style

**ツール**
- DITA Open Toolkit: https://www.dita-ot.org/
- MkDocs: https://www.mkdocs.org/
- Docusaurus: https://docusaurus.io/
- Swagger UI: https://swagger.io/tools/swagger-ui/
- ReDoc: https://redocly.com/redoc/
