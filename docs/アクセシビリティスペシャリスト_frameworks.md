# アクセシビリティスペシャリスト - フレームワーク詳細ドキュメント

## 概要

本ドキュメントは、アクセシビリティスペシャリストが活用する主要なフレームワーク・基準・設計原則について、理論的背景から実践的な適用方法まで網羅的に解説します。WCAG（Web Content Accessibility Guidelines）を中心に、ARIA、ユニバーサルデザイン原則、インクルーシブデザインの考え方、支援技術への対応、テスト・評価手法まで、アクセシビリティ実現のための体系的な知識とツールを提供します。

---

## 1. WCAG (Web Content Accessibility Guidelines)

### 分類
国際標準・法規制準拠・ガイドライン

### 背景と歴史

WCAG（Web Content Accessibility Guidelines）は、W3C（World Wide Web Consortium）のWeb Accessibility Initiative（WAI）が策定した、Webコンテンツのアクセシビリティに関する国際標準ガイドラインです。1999年にWCAG 1.0が発表され、2008年にWCAG 2.0、2018年にWCAG 2.1、2023年にWCAG 2.2へと進化してきました。

WCAG 2.0以降は、技術中立的な設計がなされ、HTML、CSS、JavaScript、PDF、モバイルアプリなど幅広い技術に適用可能です。米国のADA（Americans with Disabilities Act）、Section 508、EU Accessibility Act、日本のJIS X 8341など、世界中の法規制の基準として採用されています。

WCAG 2.xは「POUR原則」と呼ばれる4つの大原則（Perceivable, Operable, Understandable, Robust）に基づき、3つの適合レベル（A、AA、AAA）で構成されます。

### 詳細な理論

#### POUR原則の詳細

**1. Perceivable（知覚可能）**
情報とユーザーインターフェースコンポーネントは、ユーザーが知覚できる方法で提示されなければなりません。視覚、聴覚などの感覚に依存せず、代替手段が提供される必要があります。

- ガイドライン1.1 代替テキスト: 画像、音声、動画などの非テキストコンテンツに代替テキストを提供
- ガイドライン1.2 時間依存メディア: 音声・動画に字幕、音声解説、トランスクリプトを提供
- ガイドライン1.3 適応可能: 情報や構造を失わずに異なる方法で提示可能
- ガイドライン1.4 識別可能: 前景と背景を区別しやすく、色コントラスト確保

**2. Operable（操作可能）**
ユーザーインターフェースコンポーネントとナビゲーションは操作可能でなければなりません。特にキーボードのみで全機能を利用できることが重要です。

- ガイドライン2.1 キーボードアクセス可能: すべての機能をキーボードで操作可能
- ガイドライン2.2 十分な時間: ユーザーがコンテンツを読み、使用するのに十分な時間を提供
- ガイドライン2.3 発作と身体的反応: 発作を引き起こす恐れのあるコンテンツを避ける
- ガイドライン2.4 ナビゲート可能: ユーザーがナビゲート、コンテンツ発見、現在位置確認できる
- ガイドライン2.5 入力モダリティ: キーボード以外のさまざまな入力方法に対応

**3. Understandable（理解可能）**
情報とユーザーインターフェースの操作は理解可能でなければなりません。

- ガイドライン3.1 読みやすさ: テキストコンテンツを読みやすく理解可能に
- ガイドライン3.2 予測可能: Webページの表示や動作を予測可能に
- ガイドライン3.3 入力支援: ユーザーのミスを防ぎ、修正を支援

**4. Robust（堅牢）**
コンテンツは、支援技術を含む幅広いユーザーエージェントで確実に解釈できるよう堅牢でなければなりません。

- ガイドライン4.1 互換性: 現在および将来のユーザーエージェントとの互換性を最大化

#### 適合レベル

- **レベルA**: 最低限の適合レベル。これを満たさないとアクセスできないユーザーがいる
- **レベルAA**: 推奨される適合レベル。多くの法規制が要求する標準（コントラスト比4.5:1など）
- **レベルAAA**: 最高レベルの適合。すべてのコンテンツに適用するのは現実的でない場合もある（コントラスト比7:1など）

### 実践例

#### 例1: WCAG AA準拠のフォーム実装

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>会員登録フォーム - WCAG AA準拠</title>
    <style>
        /* 1.4.3 コントラスト (AA): 最低でも4.5:1 */
        body {
            font-size: 16px;
            color: #333333; /* コントラスト比 12.6:1 with white */
            background: #ffffff;
            font-family: 'Noto Sans JP', sans-serif;
            line-height: 1.5;
        }
        
        /* 2.4.7 フォーカスの可視化 (AA) */
        *:focus {
            outline: 3px solid #0066cc;
            outline-offset: 2px;
        }
        
        /* 1.4.11 非テキストコントラスト (AA) */
        input, select, textarea {
            border: 2px solid #767676; /* コントラスト比 4.54:1 */
            padding: 8px;
            font-size: 16px;
        }
        
        /* エラー表示: 3.3.1 エラー識別 (A) */
        .error {
            color: #d32f2f;
            background: #ffebee;
            border-left: 4px solid #d32f2f;
            padding: 8px;
            margin-top: 4px;
        }
        
        .error-icon::before {
            content: "⚠ ";
        }
        
        /* 必須フィールド: 色だけに依存しない */
        .required-label::after {
            content: " *";
            color: #d32f2f;
            font-weight: bold;
        }
        
        .required-note {
            font-size: 14px;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <!-- 2.4.1 ブロックスキップ (A) -->
    <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>
    
    <!-- 1.3.1 情報及び関係性 (A): セマンティックHTML -->
    <main id="main-content">
        <h1>会員登録フォーム</h1>
        
        <!-- 3.3.2 ラベル又は説明 (A) -->
        <p class="required-note">
            <span aria-hidden="true">*</span> の項目は必須です。
        </p>
        
        <form action="/register" method="post" novalidate>
            <!-- 1.3.1 labelとinputの関連付け -->
            <div class="form-group">
                <label for="username" class="required-label">
                    ユーザー名
                </label>
                <!-- 3.3.2 説明の提供 -->
                <p id="username-desc" class="field-description">
                    4文字以上20文字以下の半角英数字で入力してください。
                </p>
                <input 
                    type="text" 
                    id="username" 
                    name="username"
                    required
                    minlength="4"
                    maxlength="20"
                    aria-required="true"
                    aria-describedby="username-desc username-error"
                    aria-invalid="false"
                >
                <!-- 3.3.1 エラー識別 + 3.3.3 エラー修正の提案 (AA) -->
                <div id="username-error" class="error" role="alert" style="display:none;">
                    <span class="error-icon"></span>
                    ユーザー名は4文字以上20文字以下で入力してください。
                </div>
            </div>
            
            <div class="form-group">
                <label for="email" class="required-label">
                    メールアドレス
                </label>
                <input 
                    type="email" 
                    id="email" 
                    name="email"
                    required
                    aria-required="true"
                    aria-describedby="email-error"
                    autocomplete="email"
                >
                <div id="email-error" class="error" role="alert" style="display:none;">
                    <span class="error-icon"></span>
                    正しいメールアドレス形式で入力してください（例: user@example.com）。
                </div>
            </div>
            
            <div class="form-group">
                <label for="password" class="required-label">
                    パスワード
                </label>
                <p id="password-desc" class="field-description">
                    8文字以上で、英大文字、英小文字、数字、記号をそれぞれ1文字以上含めてください。
                </p>
                <input 
                    type="password" 
                    id="password" 
                    name="password"
                    required
                    minlength="8"
                    aria-required="true"
                    aria-describedby="password-desc password-error"
                    autocomplete="new-password"
                >
                <div id="password-error" class="error" role="alert" style="display:none;">
                    <span class="error-icon"></span>
                    パスワードは8文字以上で、英大文字、英小文字、数字、記号を含める必要があります。
                </div>
            </div>
            
            <!-- 1.3.1 セマンティックなグループ化 -->
            <fieldset>
                <legend class="required-label">性別</legend>
                <div class="radio-group">
                    <input type="radio" id="gender-male" name="gender" value="male" required>
                    <label for="gender-male">男性</label>
                </div>
                <div class="radio-group">
                    <input type="radio" id="gender-female" name="gender" value="female">
                    <label for="gender-female">女性</label>
                </div>
                <div class="radio-group">
                    <input type="radio" id="gender-other" name="gender" value="other">
                    <label for="gender-other">その他</label>
                </div>
                <div class="radio-group">
                    <input type="radio" id="gender-na" name="gender" value="na">
                    <label for="gender-na">回答しない</label>
                </div>
            </fieldset>
            
            <!-- 3.3.4 エラー回避（法的、金融、データ） (AA) -->
            <div class="form-group">
                <input type="checkbox" id="terms" name="terms" required aria-required="true">
                <label for="terms" class="required-label">
                    <a href="/terms" target="_blank">利用規約</a>に同意します
                </label>
            </div>
            
            <!-- 2.1.1 キーボード操作可能 -->
            <div class="form-actions">
                <button type="submit">登録する</button>
                <button type="reset">リセット</button>
            </div>
        </form>
    </main>
    
    <script>
        // クライアントサイドバリデーション
        const form = document.querySelector('form');
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            let isValid = true;
            const errors = [];
            
            // ユーザー名検証
            const username = document.getElementById('username');
            const usernameError = document.getElementById('username-error');
            if (username.value.length < 4 || username.value.length > 20) {
                username.setAttribute('aria-invalid', 'true');
                usernameError.style.display = 'block';
                isValid = false;
                errors.push('ユーザー名');
            } else {
                username.setAttribute('aria-invalid', 'false');
                usernameError.style.display = 'none';
            }
            
            // メールアドレス検証
            const email = document.getElementById('email');
            const emailError = document.getElementById('email-error');
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email.value)) {
                email.setAttribute('aria-invalid', 'true');
                emailError.style.display = 'block';
                isValid = false;
                errors.push('メールアドレス');
            } else {
                email.setAttribute('aria-invalid', 'false');
                emailError.style.display = 'none';
            }
            
            // パスワード検証
            const password = document.getElementById('password');
            const passwordError = document.getElementById('password-error');
            const hasUpper = /[A-Z]/.test(password.value);
            const hasLower = /[a-z]/.test(password.value);
            const hasNumber = /[0-9]/.test(password.value);
            const hasSymbol = /[^A-Za-z0-9]/.test(password.value);
            
            if (password.value.length < 8 || !hasUpper || !hasLower || !hasNumber || !hasSymbol) {
                password.setAttribute('aria-invalid', 'true');
                passwordError.style.display = 'block';
                isValid = false;
                errors.push('パスワード');
            } else {
                password.setAttribute('aria-invalid', 'false');
                passwordError.style.display = 'none';
            }
            
            // 3.3.1 エラー識別: サマリーを表示
            if (!isValid) {
                // エラーサマリーをページ上部に追加
                let errorSummary = document.getElementById('error-summary');
                if (!errorSummary) {
                    errorSummary = document.createElement('div');
                    errorSummary.id = 'error-summary';
                    errorSummary.setAttribute('role', 'alert');
                    errorSummary.setAttribute('aria-live', 'assertive');
                    form.insertBefore(errorSummary, form.firstChild);
                }
                errorSummary.innerHTML = `
                    <h2>入力エラーがあります</h2>
                    <p>以下の項目を修正してください:</p>
                    <ul>
                        ${errors.map(field => `<li>${field}</li>`).join('')}
                    </ul>
                `;
                errorSummary.focus();
            } else {
                // フォーム送信（実際にはサーバー送信）
                alert('登録が完了しました');
            }
        });
    </script>
</body>
</html>
```

#### 例2: WCAG 2.2の新しい達成基準への対応

```html
<!-- 2.4.11 フォーカスの外観（最小限） (AA) - WCAG 2.2 -->
<style>
    /* フォーカスインジケーターの最小サイズ要件 */
    button:focus-visible,
    a:focus-visible,
    input:focus-visible {
        /* コントラスト比3:1以上 */
        outline: 2px solid #0066cc;
        outline-offset: 2px;
        /* フォーカスインジケーターの面積が十分 */
    }
    
    /* 2.4.12 フォーカスの外観（高度） (AAA) - WCAG 2.2 */
    .enhanced-focus button:focus-visible {
        outline: 3px solid #0066cc;
        outline-offset: 3px;
        box-shadow: 0 0 8px rgba(0, 102, 204, 0.5);
    }
    
    /* 2.5.7 ドラッグ動作 (AA) - WCAG 2.2 */
    .sortable-list {
        /* ドラッグ&ドロップだけでなく、ボタンでも操作可能に */
    }
    
    /* 2.5.8 ターゲットのサイズ（最小限） (AA) - WCAG 2.2 */
    button,
    a,
    input[type="checkbox"],
    input[type="radio"] {
        /* タッチターゲットサイズ: 24x24 CSSピクセル以上 */
        min-width: 24px;
        min-height: 24px;
        /* または、ターゲット間のスペーシングが適切 */
    }
    
    /* より推奨される 44x44 ピクセル */
    .touch-friendly button {
        min-width: 44px;
        min-height: 44px;
    }
    
    /* 3.2.6 一貫したヘルプ (A) - WCAG 2.2 */
    .help-link {
        /* 全ページで同じ相対位置にヘルプリンクを配置 */
        position: fixed;
        bottom: 20px;
        right: 20px;
    }
    
    /* 3.3.7 冗長な入力 (A) - WCAG 2.2 */
    /* autocomplete属性を適切に使用 */
    
    /* 3.3.8 アクセシブル認証（最小限） (AA) - WCAG 2.2 */
    /* CAPTCHAの代わりにアクセシブルな認証方法 */
</style>

<!-- ドラッグ&ドロップの代替操作 -->
<div class="sortable-list" role="list">
    <div class="sortable-item" role="listitem">
        <span class="item-content">アイテム1</span>
        <!-- 2.5.7 ドラッグ以外の操作方法を提供 -->
        <button aria-label="アイテム1を上に移動">↑</button>
        <button aria-label="アイテム1を下に移動">↓</button>
    </div>
    <div class="sortable-item" role="listitem">
        <span class="item-content">アイテム2</span>
        <button aria-label="アイテム2を上に移動">↑</button>
        <button aria-label="アイテム2を下に移動">↓</button>
    </div>
</div>

<!-- 一貫したヘルプ -->
<a href="/help" class="help-link" aria-label="ヘルプ">
    <svg aria-hidden="true" width="24" height="24"><!-- ヘルプアイコン --></svg>
</a>

<!-- 冗長な入力の回避 -->
<form>
    <!-- 住所入力を一度だけに -->
    <label for="billing-address">請求先住所</label>
    <input type="text" id="billing-address" name="billing-address" autocomplete="street-address">
    
    <input type="checkbox" id="same-address" name="same-address">
    <label for="same-address">配送先住所も同じ</label>
    
    <!-- チェックされたら自動入力 -->
    <label for="shipping-address">配送先住所</label>
    <input type="text" id="shipping-address" name="shipping-address" autocomplete="street-address">
</form>

<!-- アクセシブル認証 -->
<form action="/login" method="post">
    <label for="email">メールアドレス</label>
    <input type="email" id="email" name="email" autocomplete="email" required>
    
    <label for="password">パスワード</label>
    <input type="password" id="password" name="password" autocomplete="current-password" required>
    
    <!-- 3.3.8: 認知機能テストを要求しない -->
    <!-- CAPTCHAの代わりにトークンベース認証やソーシャルログインを推奨 -->
    
    <button type="submit">ログイン</button>
</form>

<!-- パスワードレス認証の例 -->
<div class="passwordless-auth">
    <p>メールアドレスにマジックリンクを送信します</p>
    <label for="magic-email">メールアドレス</label>
    <input type="email" id="magic-email" name="email" autocomplete="email">
    <button type="button">マジックリンクを送信</button>
</div>
```

### 参考文献・リソース

**公式仕様**
- W3C. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/
- W3C. (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*. https://www.w3.org/TR/WCAG21/

**解説書**
- Kirkpatrick, A., et al. (2023). *Understanding WCAG 2.2*. W3C. https://www.w3.org/WAI/WCAG22/Understanding/
- W3C. (2023). *How to Meet WCAG (Quick Reference)*. https://www.w3.org/WAI/WCAG22/quickref/

**書籍**
- Pickering, H. (2016). *Inclusive Design Patterns*. Smashing Magazine.
- Horton, S., & Quesenbery, W. (2013). *A Web for Everyone: Designing Accessible User Experiences*. Rosenfeld Media.

**ツール**
- axe DevTools: https://www.deque.com/axe/devtools/
- WAVE: https://wave.webaim.org/
- Lighthouse: https://developers.google.com/web/tools/lighthouse

---

## 2. ARIA (Accessible Rich Internet Applications)

### 分類
技術仕様・動的コンテンツ対応・支援技術連携

### 背景と歴史

ARIA（Accessible Rich Internet Applications）は、W3Cが2014年に勧告したWeb標準仕様（WAI-ARIA 1.0）で、2017年にWAI-ARIA 1.1、2023年にWAI-ARIA 1.2へと進化しました。

従来のHTMLだけでは表現できない複雑なWebアプリケーションのUIコンポーネント（タブパネル、ツリービュー、ダイアログなど）やダイナミックコンテンツを、スクリーンリーダーなどの支援技術に正しく伝えるための属性群です。

ARIAは「HTMLで表現できないものを補完する」ための技術であり、**「セマンティックHTMLファースト、ARIAはセカンド」**という原則（First Rule of ARIA Use）が重要です。

### 詳細な理論

#### ARIAの5つのカテゴリ

**1. ロール（Roles）**
要素の役割を定義します。

- **ランドマークロール**: ページの構造的な領域（banner, navigation, main, complementary, contentinfo, search, form, region）
- **ウィジェットロール**: インタラクティブなコンポーネント（button, checkbox, tab, tabpanel, dialog, alertdialog, menu, menuitem, slider, progressbar）
- **ドキュメント構造ロール**: コンテンツの構造（heading, list, listitem, table, row, cell）
- **ライブリージョンロール**: 動的に変化するコンテンツ（alert, status, log, timer）

**2. ステート（States）**
要素の現在の状態を示します（動的に変化）。

- `aria-checked`: チェックボックス・ラジオボタンの選択状態
- `aria-expanded`: 展開/折りたたみ状態
- `aria-hidden`: 支援技術から隠す
- `aria-selected`: 選択状態（タブなど）
- `aria-pressed`: トグルボタンの押下状態
- `aria-disabled`: 無効状態
- `aria-invalid`: 入力エラー状態

**3. プロパティ（Properties）**
要素の性質を示します（通常は静的）。

- `aria-label`: 要素のラベル
- `aria-labelledby`: ラベル要素のID参照
- `aria-describedby`: 説明要素のID参照
- `aria-required`: 必須フィールド
- `aria-readonly`: 読み取り専用
- `aria-haspopup`: ポップアップメニュー/ダイアログの有無

**4. ライブリージョン（Live Regions）**
動的に変化するコンテンツを支援技術に通知します。

- `aria-live="polite"`: 現在の読み上げが終わった後に通知
- `aria-live="assertive"`: 即座に割り込んで通知
- `aria-live="off"`: 通知しない
- `aria-atomic`: 変更部分だけか全体を読むか
- `aria-relevant`: どの変更を通知するか

**5. リレーションシップ（Relationships）**
要素間の関係性を示します。

- `aria-controls`: 制御する要素のID
- `aria-owns`: 所有する子要素のID
- `aria-activedescendant`: フォーカスを持つ子孫要素のID
- `aria-flowto`: 読み上げ順序の指定

#### ARIAの原則

1. **No ARIA is better than Bad ARIA**: 誤ったARIAは何もないよりも悪い
2. **Don't Override Semantic HTML**: セマンティックHTMLを優先
3. **All Interactive Elements Must Be Keyboard Accessible**: ARIAを使ったインタラクティブ要素は必ずキーボード操作可能に
4. **Don't Use role="presentation" or aria-hidden on Focusable Elements**: フォーカス可能な要素を隠さない
5. **All Interactive Elements Must Have an Accessible Name**: すべてのインタラクティブ要素にアクセシブルな名前を

### 実践例

#### 例1: カスタムタブパネル（ARIA Authoring Practices準拠）

```html
<div class="tabs">
    <!-- タブリスト -->
    <div role="tablist" aria-label="製品情報タブ">
        <button 
            role="tab" 
            id="tab-description"
            aria-selected="true"
            aria-controls="panel-description"
            tabindex="0"
        >
            製品説明
        </button>
        <button 
            role="tab" 
            id="tab-specs"
            aria-selected="false"
            aria-controls="panel-specs"
            tabindex="-1"
        >
            仕様
        </button>
        <button 
            role="tab" 
            id="tab-reviews"
            aria-selected="false"
            aria-controls="panel-reviews"
            tabindex="-1"
        >
            レビュー
        </button>
    </div>
    
    <!-- タブパネル -->
    <div 
        role="tabpanel" 
        id="panel-description"
        aria-labelledby="tab-description"
        tabindex="0"
    >
        <h3>製品説明</h3>
        <p>この製品は...</p>
    </div>
    
    <div 
        role="tabpanel" 
        id="panel-specs"
        aria-labelledby="tab-specs"
        hidden
    >
        <h3>仕様</h3>
        <ul>
            <li>サイズ: 10cm x 15cm</li>
            <li>重量: 200g</li>
        </ul>
    </div>
    
    <div 
        role="tabpanel" 
        id="panel-reviews"
        aria-labelledby="tab-reviews"
        hidden
    >
        <h3>レビュー</h3>
        <p>評価: 4.5/5</p>
    </div>
</div>

<style>
    .tabs [role="tab"] {
        padding: 8px 16px;
        border: 1px solid #ccc;
        background: #f0f0f0;
        cursor: pointer;
    }
    
    .tabs [role="tab"][aria-selected="true"] {
        background: white;
        border-bottom: 2px solid white;
        font-weight: bold;
    }
    
    .tabs [role="tabpanel"] {
        padding: 16px;
        border: 1px solid #ccc;
    }
    
    .tabs [role="tabpanel"][hidden] {
        display: none;
    }
</style>

<script>
    // ARIA Authoring Practices準拠のキーボード操作
    const tablist = document.querySelector('[role="tablist"]');
    const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
    const panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));
    
    // タブクリック処理
    tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => {
            activateTab(index);
        });
        
        // キーボードナビゲーション
        tab.addEventListener('keydown', (e) => {
            let newIndex = index;
            
            // 左矢印キー: 前のタブ
            if (e.key === 'ArrowLeft') {
                newIndex = index === 0 ? tabs.length - 1 : index - 1;
                e.preventDefault();
            }
            // 右矢印キー: 次のタブ
            else if (e.key === 'ArrowRight') {
                newIndex = index === tabs.length - 1 ? 0 : index + 1;
                e.preventDefault();
            }
            // Homeキー: 最初のタブ
            else if (e.key === 'Home') {
                newIndex = 0;
                e.preventDefault();
            }
            // Endキー: 最後のタブ
            else if (e.key === 'End') {
                newIndex = tabs.length - 1;
                e.preventDefault();
            }
            
            if (newIndex !== index) {
                activateTab(newIndex);
                tabs[newIndex].focus();
            }
        });
    });
    
    function activateTab(index) {
        // すべてのタブを非選択に
        tabs.forEach((tab, i) => {
            const isSelected = i === index;
            tab.setAttribute('aria-selected', isSelected);
            tab.setAttribute('tabindex', isSelected ? '0' : '-1');
        });
        
        // すべてのパネルを非表示に
        panels.forEach((panel, i) => {
            panel.hidden = i !== index;
        });
    }
</script>
```

#### 例2: ライブリージョンを使った動的通知

```html
<!-- 検索結果のライブ更新 -->
<div class="search-container">
    <label for="product-search">製品検索</label>
    <input 
        type="search" 
        id="product-search"
        aria-controls="search-results"
        aria-describedby="search-instructions"
    >
    <p id="search-instructions">入力すると自動的に検索結果が更新されます</p>
    
    <!-- ライブリージョン: 検索結果数を通知 -->
    <div 
        role="status" 
        aria-live="polite" 
        aria-atomic="true"
        class="sr-only"
    >
        <span id="result-count"></span>
    </div>
    
    <div id="search-results" role="region" aria-label="検索結果">
        <!-- 検索結果がここに表示される -->
    </div>
</div>

<script>
    const searchInput = document.getElementById('product-search');
    const resultCount = document.getElementById('result-count');
    const resultsContainer = document.getElementById('search-results');
    
    let debounceTimer;
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        
        debounceTimer = setTimeout(() => {
            const query = e.target.value.trim();
            
            if (query.length > 0) {
                performSearch(query);
            } else {
                resultsContainer.innerHTML = '';
                resultCount.textContent = '';
            }
        }, 300);
    });
    
    async function performSearch(query) {
        // 検索実行（ダミー）
        const results = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
            .then(res => res.json());
        
        // 結果を表示
        resultsContainer.innerHTML = results.map(item => `
            <div class="result-item">
                <h3><a href="${item.url}">${item.name}</a></h3>
                <p>${item.description}</p>
            </div>
        `).join('');
        
        // スクリーンリーダーに結果数を通知（aria-live）
        resultCount.textContent = `${results.length}件の検索結果が見つかりました`;
    }
</script>

<!-- ショッピングカートの更新通知 -->
<button 
    id="add-to-cart"
    aria-label="カートに追加"
    aria-describedby="cart-status"
>
    カートに追加
</button>

<!-- アラート: 即座に通知 -->
<div 
    id="cart-status"
    role="alert" 
    aria-live="assertive" 
    aria-atomic="true"
    class="sr-only"
></div>

<script>
    document.getElementById('add-to-cart').addEventListener('click', () => {
        // カートに追加処理
        addToCart();
        
        // 即座に通知（aria-live="assertive"）
        const cartStatus = document.getElementById('cart-status');
        cartStatus.textContent = '商品がカートに追加されました';
        
        // 視覚的なフィードバックも提供
        showToast('カートに追加しました');
    });
</script>

<!-- リアルタイムチャットのログ -->
<div class="chat-container">
    <div 
        id="chat-log"
        role="log" 
        aria-live="polite" 
        aria-atomic="false"
        aria-label="チャットログ"
        class="chat-messages"
    >
        <!-- 新しいメッセージが追加される -->
    </div>
    
    <form class="chat-input-form">
        <label for="chat-message" class="sr-only">メッセージ</label>
        <input 
            type="text" 
            id="chat-message"
            placeholder="メッセージを入力..."
            aria-describedby="chat-help"
        >
        <p id="chat-help" class="sr-only">
            Enterキーで送信、Shift+Enterで改行
        </p>
        <button type="submit">送信</button>
    </form>
</div>

<script>
    // チャットメッセージ受信（WebSocketなど）
    function receiveMessage(message) {
        const chatLog = document.getElementById('chat-log');
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message';
        messageElement.innerHTML = `
            <strong>${message.sender}:</strong>
            <span>${message.text}</span>
        `;
        
        // ログに追加（aria-live="polite"により自動通知）
        chatLog.appendChild(messageElement);
        
        // 最新メッセージにスクロール
        chatLog.scrollTop = chatLog.scrollHeight;
    }
</script>

<!-- スクリーンリーダー専用テキスト用のCSSクラス -->
<style>
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border-width: 0;
    }
</style>
```

#### 例3: アクセシブルなモーダルダイアログ

```html
<button id="open-dialog" aria-haspopup="dialog">
    設定を開く
</button>

<div 
    id="settings-dialog"
    role="dialog" 
    aria-labelledby="dialog-title"
    aria-describedby="dialog-desc"
    aria-modal="true"
    class="dialog"
    hidden
>
    <div class="dialog-content">
        <h2 id="dialog-title">設定</h2>
        <p id="dialog-desc">アプリケーションの設定を変更できます</p>
        
        <form>
            <div class="form-group">
                <label for="setting-language">言語</label>
                <select id="setting-language">
                    <option value="ja">日本語</option>
                    <option value="en">English</option>
                </select>
            </div>
            
            <div class="form-group">
                <input type="checkbox" id="setting-notifications">
                <label for="setting-notifications">通知を有効にする</label>
            </div>
            
            <div class="dialog-actions">
                <button type="submit" id="save-settings">保存</button>
                <button type="button" id="close-dialog">キャンセル</button>
            </div>
        </form>
    </div>
</div>

<div id="dialog-overlay" class="dialog-overlay" hidden></div>

<style>
    .dialog {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
        background: white;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        max-width: 500px;
        width: 90%;
    }
    
    .dialog[hidden] {
        display: none;
    }
    
    .dialog-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
    }
    
    .dialog-overlay[hidden] {
        display: none;
    }
</style>

<script>
    const openButton = document.getElementById('open-dialog');
    const closeButton = document.getElementById('close-dialog');
    const dialog = document.getElementById('settings-dialog');
    const overlay = document.getElementById('dialog-overlay');
    
    let previousFocus = null;
    
    // ダイアログを開く
    openButton.addEventListener('click', () => {
        // 現在のフォーカスを保存
        previousFocus = document.activeElement;
        
        // ダイアログを表示
        dialog.hidden = false;
        overlay.hidden = false;
        
        // body のスクロールを無効化
        document.body.style.overflow = 'hidden';
        
        // ダイアログ内の最初のフォーカス可能要素にフォーカス
        const firstFocusable = dialog.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (firstFocusable) {
            firstFocusable.focus();
        }
        
        // フォーカストラップを設定
        setupFocusTrap();
    });
    
    // ダイアログを閉じる
    function closeDialog() {
        dialog.hidden = true;
        overlay.hidden = true;
        document.body.style.overflow = '';
        
        // フォーカスを元の場所に戻す
        if (previousFocus) {
            previousFocus.focus();
        }
    }
    
    closeButton.addEventListener('click', closeDialog);
    
    // オーバーレイクリックで閉じる
    overlay.addEventListener('click', closeDialog);
    
    // Escapeキーで閉じる
    dialog.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeDialog();
        }
    });
    
    // フォーカストラップ（ダイアログ内にフォーカスを閉じ込める）
    function setupFocusTrap() {
        const focusableElements = dialog.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        dialog.addEventListener('keydown', function trapFocus(e) {
            if (e.key !== 'Tab') return;
            
            // Shift+Tab: 最初の要素から前に戻ろうとしたら最後へ
            if (e.shiftKey && document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            }
            // Tab: 最後の要素から次に進もうとしたら最初へ
            else if (!e.shiftKey && document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        });
    }
</script>
```

### 参考文献・リソース

**公式仕様**
- W3C. (2023). *Accessible Rich Internet Applications (WAI-ARIA) 1.2*. https://www.w3.org/TR/wai-aria-1.2/
- W3C. (2023). *ARIA Authoring Practices Guide (APG)*. https://www.w3.org/WAI/ARIA/apg/

**実装パターン集**
- W3C. (2023). *ARIA Design Patterns*. https://www.w3.org/WAI/ARIA/apg/patterns/

**ツール**
- ARIA DevTools: https://github.com/ziolko/aria-devtools
- Accessibility Insights: https://accessibilityinsights.io/

---

## 3. ユニバーサルデザイン7原則

### 分類
設計思想・包括的デザイン・製品設計

### 背景と歴史

ユニバーサルデザイン（Universal Design）は、1997年にノースカロライナ州立大学のRonald L. Mace教授を中心とする研究チームが提唱した設計思想です。「すべての人のためのデザイン」を目指し、年齢、能力、状況に関わらず、最大限多くの人が利用できる製品・環境・サービスの設計を追求します。

「バリアフリー」が障害者のための特別な配慮であるのに対し、ユニバーサルデザインは最初からすべての人を対象とする点が異なります。

7つの原則は、物理的な製品だけでなく、Webサイト、アプリ、サービスデザインにも広く応用されています。

### 詳細な理論

#### 7つの原則の詳細

**原則1: 公平な利用（Equitable Use）**
デザインは、多様な能力を持つ人々にとって有用で、販売可能であること。

ガイドライン:
- すべてのユーザーに同じ利用手段を提供（可能な限り同一、不可能な場合は同等）
- いかなるユーザーも差別したり、遠ざけたりしない
- プライバシー、セキュリティ、安全性をすべてのユーザーに平等に提供
- デザインをすべてのユーザーにとって魅力的にする

**原則2: 利用の柔軟性（Flexibility in Use）**
デザインは、幅広い個人の好みや能力に対応すること。

ガイドライン:
- 利用方法の選択肢を提供
- 右利き・左利きどちらでもアクセス・利用可能
- ユーザーの正確さと精度に対応
- ユーザーのペースに適応

**原則3: 単純で直感的（Simple and Intuitive Use）**
デザインの使用方法は、ユーザーの経験、知識、言語能力、集中力に関わらず理解しやすいこと。

ガイドライン:
- 不必要な複雑さを排除
- ユーザーの期待や直感と一致
- 幅広い読み書き能力と言語スキルに対応
- 情報を重要度順に整理
- 作業中および作業後に効果的なプロンプトとフィードバックを提供

**原則4: 認知できる情報（Perceptible Information）**
デザインは、周囲の条件やユーザーの感覚能力に関わらず、必要な情報を効果的にユーザーに伝えること。

ガイドライン:
- 本質的な情報を伝えるために異なるモード（絵、言葉、触覚）を使用
- 本質的な情報のコントラストを最大化
- 重要な情報の「読みやすさ」を最大化
- 要素を区別しやすくする（説明しやすく、指示しやすく）
- 感覚的な制限を持つ人々が使用する様々な技術やデバイスとの互換性を提供

**原則5: エラーの許容（Tolerance for Error）**
デザインは、危険や意図しない行動による悪影響を最小限に抑えること。

ガイドライン:
- 危険や誤りを最小限に抑える要素を配置（最も使用される要素を最もアクセスしやすく、危険な要素を排除、隔離、または保護）
- 危険や誤りについて警告を提供
- フェイルセーフ機能を提供
- 注意を要する作業での無意識な行動を防ぐ

**原則6: 少ない身体的負担（Low Physical Effort）**
デザインは、効率的かつ快適に、疲労を最小限に抑えて使用できること。

ガイドライン:
- ユーザーが自然な姿勢を維持できるようにする
- 合理的な操作力を使用
- 繰り返し動作を最小限に
- 持続的な身体的努力を最小限に

**原則7: 接近や利用のためのサイズと空間（Size and Space for Approach and Use）**
デザインは、ユーザーの体格、姿勢、移動能力に関わらず、接近、到達、操作、使用のための適切なサイズと空間を提供すること。

ガイドライン:
- 座位・立位のユーザーにとって重要な要素への視線を明確に
- すべてのユーザー（座位・立位）が、すべてのコンポーネントに快適に手が届く
- さまざまな手のサイズや握力に対応
- 支援機器や個人的な支援のための適切なスペースを提供

### 実践例

#### 例1: ユニバーサルデザイン原則を適用したWebフォーム

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>予約フォーム - ユニバーサルデザイン</title>
    <style>
        body {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 18px; /* 原則6: 読みやすい大きなフォント */
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background: #fff;
        }
        
        /* 原則4: 認知できる情報 - 高いコントラスト */
        h1 {
            color: #000;
            font-size: 2rem;
        }
        
        /* 原則3: 単純で直感的 - 明確なグループ化 */
        fieldset {
            border: 2px solid #0066cc;
            padding: 20px;
            margin-bottom: 24px;
            border-radius: 8px;
        }
        
        legend {
            font-size: 1.3rem;
            font-weight: bold;
            color: #0066cc;
            padding: 0 10px;
        }
        
        /* 原則6: 少ない身体的負担 - 大きなタッチターゲット */
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        input, select, textarea {
            font-size: 18px;
            padding: 12px;
            border: 2px solid #767676;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
            /* 原則7: 適切なサイズ */
            min-height: 48px;
        }
        
        /* 原則2: 利用の柔軟性 - 複数の入力方法 */
        .date-input-group {
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }
        
        .date-input-group input {
            flex: 1;
        }
        
        /* 原則1: 公平な利用 - フォーカスの明確な視覚化 */
        *:focus {
            outline: 4px solid #ff9800;
            outline-offset: 2px;
        }
        
        /* 原則5: エラーの許容 - 明確なエラー表示 */
        .error-message {
            background: #ffebee;
            border-left: 5px solid #d32f2f;
            color: #b71c1c;
            padding: 12px;
            margin-top: 8px;
            border-radius: 4px;
            font-weight: 600;
        }
        
        .error-message::before {
            content: "⚠ ";
            font-size: 1.2em;
        }
        
        /* 原則3: 単純で直感的 - プログレスインジケーター */
        .progress-bar {
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            margin-bottom: 24px;
            overflow: hidden;
        }
        
        .progress-bar-fill {
            height: 100%;
            background: #4caf50;
            transition: width 0.3s ease;
        }
        
        .progress-label {
            text-align: center;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        /* 原則4: 認知できる情報 - 複数のモードで情報提供 */
        .help-text {
            font-size: 0.9rem;
            color: #555;
            margin-top: 4px;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        
        .help-text::before {
            content: "ℹ";
            display: inline-block;
            width: 20px;
            height: 20px;
            background: #2196f3;
            color: white;
            border-radius: 50%;
            text-align: center;
            flex-shrink: 0;
        }
        
        /* 原則5: エラーの許容 - 確認画面 */
        .confirmation {
            background: #e8f5e9;
            border: 2px solid #4caf50;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        /* 原則6: 少ない身体的負担 - 大きなボタン */
        button {
            font-size: 1.1rem;
            padding: 16px 32px;
            min-height: 56px;
            min-width: 120px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: #0066cc;
            color: white;
        }
        
        .btn-primary:hover {
            background: #0052a3;
            transform: scale(1.02);
        }
        
        .btn-secondary {
            background: #757575;
            color: white;
            margin-left: 10px;
        }
        
        /* 原則2: 利用の柔軟性 - レスポンシブ */
        @media (max-width: 600px) {
            body {
                font-size: 16px;
            }
            
            .date-input-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <h1>レストラン予約フォーム</h1>
    
    <!-- 原則3: 進捗状況を明確に -->
    <div class="progress-label">ステップ 1/3: 基本情報</div>
    <div class="progress-bar">
        <div class="progress-bar-fill" style="width: 33%;" role="progressbar" aria-valuenow="33" aria-valuemin="0" aria-valuemax="100"></div>
    </div>
    
    <form id="reservation-form">
        <!-- 原則3: 明確なグループ化 -->
        <fieldset>
            <legend>お客様情報</legend>
            
            <div class="form-group">
                <label for="name">お名前 *</label>
                <input 
                    type="text" 
                    id="name" 
                    name="name"
                    required
                    aria-required="true"
                    aria-describedby="name-help"
                    autocomplete="name"
                >
                <!-- 原則4: 認知できる情報 - ヘルプテキスト -->
                <div id="name-help" class="help-text">
                    フルネームでご記入ください
                </div>
            </div>
            
            <div class="form-group">
                <label for="phone">電話番号 *</label>
                <!-- 原則2: 柔軟性 - 複数の入力形式を許容 -->
                <input 
                    type="tel" 
                    id="phone" 
                    name="phone"
                    required
                    aria-required="true"
                    aria-describedby="phone-help"
                    autocomplete="tel"
                    pattern="[0-9\-\(\)\s]+"
                >
                <div id="phone-help" class="help-text">
                    ハイフンあり・なし、どちらでも入力できます（例: 03-1234-5678 または 0312345678）
                </div>
            </div>
            
            <div class="form-group">
                <label for="email">メールアドレス *</label>
                <input 
                    type="email" 
                    id="email" 
                    name="email"
                    required
                    aria-required="true"
                    autocomplete="email"
                >
            </div>
        </fieldset>
        
        <fieldset>
            <legend>予約内容</legend>
            
            <div class="form-group">
                <label for="date">予約日 *</label>
                <!-- 原則2: 柔軟性 - date pickerとテキスト入力の両方に対応 -->
                <div class="date-input-group">
                    <input 
                        type="date" 
                        id="date" 
                        name="date"
                        required
                        aria-required="true"
                        aria-describedby="date-help"
                    >
                    <button type="button" onclick="setToday()">今日</button>
                    <button type="button" onclick="setTomorrow()">明日</button>
                </div>
                <div id="date-help" class="help-text">
                    カレンダーから選択、または「今日」「明日」ボタンをご利用ください
                </div>
            </div>
            
            <div class="form-group">
                <label for="time">予約時間 *</label>
                <!-- 原則3: 単純で直感的 - 選択肢を提示 -->
                <select 
                    id="time" 
                    name="time"
                    required
                    aria-required="true"
                >
                    <option value="">時間を選択してください</option>
                    <option value="11:00">11:00</option>
                    <option value="11:30">11:30</option>
                    <option value="12:00">12:00（ランチピーク）</option>
                    <option value="12:30">12:30（ランチピーク）</option>
                    <option value="13:00">13:00</option>
                    <option value="17:00">17:00</option>
                    <option value="18:00">18:00（ディナー開始）</option>
                    <option value="19:00">19:00（ディナーピーク）</option>
                    <option value="20:00">20:00</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="guests">人数 *</label>
                <!-- 原則6: 少ない身体的負担 - スピナーの代わりに選択肢 -->
                <select 
                    id="guests" 
                    name="guests"
                    required
                    aria-required="true"
                >
                    <option value="">人数を選択してください</option>
                    <option value="1">1名</option>
                    <option value="2">2名</option>
                    <option value="3">3名</option>
                    <option value="4">4名</option>
                    <option value="5">5名</option>
                    <option value="6">6名以上（備考欄にご記入ください）</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="requests">ご要望・備考</label>
                <textarea 
                    id="requests" 
                    name="requests"
                    rows="4"
                    aria-describedby="requests-help"
                ></textarea>
                <div id="requests-help" class="help-text">
                    アレルギー、お子様連れ、車椅子での来店など、ご要望をお聞かせください
                </div>
            </div>
        </fieldset>
        
        <!-- 原則5: エラーの許容 - 送信前の確認 -->
        <div class="form-actions">
            <button type="button" class="btn-primary" onclick="showConfirmation()">
                予約内容を確認
            </button>
            <button type="reset" class="btn-secondary">
                入力をクリア
            </button>
        </div>
    </form>
    
    <!-- 確認画面（原則5: エラーの許容） -->
    <div id="confirmation-section" style="display:none;">
        <div class="confirmation">
            <h2>予約内容の確認</h2>
            <dl>
                <dt>お名前:</dt>
                <dd id="confirm-name"></dd>
                <dt>電話番号:</dt>
                <dd id="confirm-phone"></dd>
                <dt>メールアドレス:</dt>
                <dd id="confirm-email"></dd>
                <dt>予約日:</dt>
                <dd id="confirm-date"></dd>
                <dt>予約時間:</dt>
                <dd id="confirm-time"></dd>
                <dt>人数:</dt>
                <dd id="confirm-guests"></dd>
                <dt>ご要望:</dt>
                <dd id="confirm-requests"></dd>
            </dl>
        </div>
        
        <div class="form-actions">
            <button type="button" class="btn-primary" onclick="submitReservation()">
                この内容で予約する
            </button>
            <button type="button" class="btn-secondary" onclick="editReservation()">
                内容を修正する
            </button>
        </div>
    </div>
    
    <script>
        // 原則2: 柔軟性 - 日付入力の補助
        function setToday() {
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('date').value = today;
        }
        
        function setTomorrow() {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            document.getElementById('date').value = tomorrow.toISOString().split('T')[0];
        }
        
        // 原則5: エラーの許容 - 確認画面
        function showConfirmation() {
            const form = document.getElementById('reservation-form');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            
            document.getElementById('confirm-name').textContent = document.getElementById('name').value;
            document.getElementById('confirm-phone').textContent = document.getElementById('phone').value;
            document.getElementById('confirm-email').textContent = document.getElementById('email').value;
            document.getElementById('confirm-date').textContent = document.getElementById('date').value;
            document.getElementById('confirm-time').textContent = document.getElementById('time').value;
            document.getElementById('confirm-guests').textContent = document.getElementById('guests').value;
            document.getElementById('confirm-requests').textContent = document.getElementById('requests').value || 'なし';
            
            form.style.display = 'none';
            document.getElementById('confirmation-section').style.display = 'block';
        }
        
        function editReservation() {
            document.getElementById('reservation-form').style.display = 'block';
            document.getElementById('confirmation-section').style.display = 'none';
        }
        
        function submitReservation() {
            alert('予約が完了しました。確認メールをお送りします。');
        }
    </script>
</body>
</html>
```

### 参考文献・リソース

**書籍**
- Mace, R. L., et al. (1997). *The Principles of Universal Design*. North Carolina State University.
- Story, M. F., Mueller, J. L., & Mace, R. L. (1998). *The Universal Design File: Designing for People of All Ages and Abilities*. Center for Universal Design.

**Webリソース**
- Center for Universal Design: https://design.ncsu.edu/research/center-for-universal-design/
- Universal Design Principles: https://universaldesign.ie/what-is-universal-design/the-7-principles/

---

## 4. インクルーシブデザイン

### 分類
設計プロセス・ユーザー参加型・多様性対応

### 背景と歴史

インクルーシブデザイン（Inclusive Design）は、1990年代にイギリスのRoger Coleman教授らによって提唱された設計アプローチです。ユニバーサルデザインと似ていますが、デザインプロセスに「当事者の参加」を重視する点が特徴です。

Microsoft、Google、Appleなどの大手テック企業がインクルーシブデザインを企業方針として採用し、製品開発に組み込んでいます。特にMicrosoftの「Inclusive Design Toolkit」(2016)は、実践的なガイドとして広く活用されています。

インクルーシブデザインは「エクスクルージョン（排除）」を特定し、それを解決することで、すべての人にとってより良いデザインを実現します。

### 詳細な理論

#### Microsoftのインクルーシブデザイン原則

**1. Recognize Exclusion（排除を認識する）**
誰が排除されているかを認識することから始めます。障害は個人の属性ではなく、人とその環境のミスマッチです。

- **永続的障害（Permanent）**: 片腕を失った人
- **一時的障害（Temporary）**: 腕を骨折している人
- **状況的制限（Situational）**: 赤ちゃんを抱いている人

これら3つは同じニーズ（片手での操作）を持ちます。

**2. Learn from Diversity（多様性から学ぶ）**
人間の多様性はイノベーションの源です。エッジケース（極端なユースケース）をデザインすることで、すべての人にとってより良い体験が生まれます。

例: OXO Good Gripsの皮むき器は、関節炎の妻のためにデザインされましたが、結果としてすべての人にとって使いやすくなりました。

**3. Solve for One, Extend to Many（一人のために解決し、多くの人に拡張する）**
特定の個人やコミュニティの課題を深く理解し解決することで、より広い範囲の人々に恩恵をもたらします。

例: 字幕は聴覚障害者のために開発されましたが、騒がしい環境、外国語学習者、情報を素早く把握したい人など、多くの人に利用されています。

#### パーソナスペクトラム（Persona Spectrum）

従来のペルソナデザインを拡張し、永続的・一時的・状況的な制約を持つユーザーを包括的に考慮します。

| 能力 | 永続的 | 一時的 | 状況的 |
|------|--------|--------|--------|
| **触覚** | 片腕 | 腕の怪我 | 赤ちゃんを抱く |
| **視覚** | 失明 | 白内障 | 運転中 |
| **聴覚** | 聴覚障害 | 耳の感染症 | バーテンダー |
| **発話** | 非言語的 | 喉頭炎 | 非ネイティブ |

### 実践例

#### 例1: インクルーシブなビデオプレーヤー

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>インクルーシブビデオプレーヤー</title>
    <style>
        .video-container {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            background: #000;
        }
        
        video {
            width: 100%;
            display: block;
        }
        
        /* カスタムコントロール */
        .video-controls {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
        }
        
        /* 大きなタッチターゲット（UD原則6, 7） */
        .video-controls button {
            min-width: 48px;
            min-height: 48px;
            padding: 8px;
            background: transparent;
            border: 2px solid white;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 20px;
        }
        
        .video-controls button:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .video-controls button:focus {
            outline: 3px solid #ff9800;
            outline-offset: 2px;
        }
        
        /* プログレスバー */
        .progress-container {
            flex: 1;
            height: 48px;
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
            position: relative;
        }
        
        .progress-filled {
            height: 100%;
            background: #ff0000;
            border-radius: 4px;
            width: 0%;
        }
        
        /* 音量コントロール */
        .volume-control {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        input[type="range"] {
            width: 100px;
            height: 8px;
        }
        
        /* 字幕表示エリア */
        .captions-container {
            position: absolute;
            bottom: 80px;
            left: 0;
            right: 0;
            text-align: center;
            padding: 0 20px;
            pointer-events: none;
        }
        
        .caption-text {
            display: inline-block;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 16px;
            font-size: 1.2rem;
            line-height: 1.4;
            border-radius: 4px;
        }
        
        /* 再生速度メニュー */
        .speed-menu {
            position: absolute;
            bottom: 100%;
            background: rgba(0, 0, 0, 0.9);
            border-radius: 4px;
            padding: 8px;
            margin-bottom: 8px;
            display: none;
        }
        
        .speed-menu.open {
            display: block;
        }
        
        .speed-option {
            display: block;
            width: 100%;
            padding: 8px 16px;
            text-align: left;
            background: transparent;
            border: none;
            color: white;
            cursor: pointer;
            min-height: 40px;
        }
        
        .speed-option:hover,
        .speed-option.active {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="video-container">
        <video 
            id="video" 
            poster="thumbnail.jpg"
            aria-label="製品紹介ビデオ"
        >
            <source src="video.mp4" type="video/mp4">
            <track 
                kind="captions" 
                src="captions-ja.vtt" 
                srclang="ja" 
                label="日本語"
                default
            >
            <track 
                kind="captions" 
                src="captions-en.vtt" 
                srclang="en" 
                label="English"
            >
            <track 
                kind="descriptions" 
                src="audio-description.vtt" 
                srclang="ja" 
                label="音声解説"
            >
        </video>
        
        <!-- カスタム字幕表示（スタイル変更可能） -->
        <div class="captions-container" aria-live="polite" aria-atomic="true">
            <div id="custom-caption" class="caption-text" style="display:none;"></div>
        </div>
        
        <div class="video-controls" role="group" aria-label="ビデオコントロール">
            <!-- 再生/一時停止 -->
            <button 
                id="play-pause" 
                aria-label="再生"
                aria-pressed="false"
            >
                ▶
            </button>
            
            <!-- 10秒巻き戻し -->
            <button 
                id="rewind" 
                aria-label="10秒巻き戻し"
            >
                ⏪
            </button>
            
            <!-- 10秒早送り -->
            <button 
                id="forward" 
                aria-label="10秒早送り"
            >
                ⏩
            </button>
            
            <!-- プログレスバー -->
            <div class="progress-container" role="slider" aria-label="再生位置" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" tabindex="0">
                <div class="progress-bar">
                    <div class="progress-filled" id="progress"></div>
                </div>
            </div>
            
            <!-- 時間表示 -->
            <span id="time-display" aria-live="off">0:00 / 0:00</span>
            
            <!-- 音量コントロール -->
            <div class="volume-control">
                <button 
                    id="mute" 
                    aria-label="ミュート"
                    aria-pressed="false"
                >
                    🔊
                </button>
                <input 
                    type="range" 
                    id="volume" 
                    min="0" 
                    max="100" 
                    value="100"
                    aria-label="音量"
                >
            </div>
            
            <!-- 字幕オン/オフ -->
            <button 
                id="captions-toggle" 
                aria-label="字幕"
                aria-pressed="true"
            >
                CC
            </button>
            
            <!-- 再生速度 -->
            <div style="position: relative;">
                <button 
                    id="speed-button" 
                    aria-label="再生速度"
                    aria-haspopup="true"
                    aria-expanded="false"
                >
                    1x
                </button>
                <div id="speed-menu" class="speed-menu" role="menu">
                    <button class="speed-option" role="menuitem" data-speed="0.5">0.5x</button>
                    <button class="speed-option" role="menuitem" data-speed="0.75">0.75x</button>
                    <button class="speed-option active" role="menuitem" data-speed="1">1x（標準）</button>
                    <button class="speed-option" role="menuitem" data-speed="1.25">1.25x</button>
                    <button class="speed-option" role="menuitem" data-speed="1.5">1.5x</button>
                    <button class="speed-option" role="menuitem" data-speed="2">2x</button>
                </div>
            </div>
            
            <!-- フルスクリーン -->
            <button 
                id="fullscreen" 
                aria-label="フルスクリーン"
            >
                ⛶
            </button>
        </div>
    </div>
    
    <script>
        const video = document.getElementById('video');
        const playPauseBtn = document.getElementById('play-pause');
        const rewindBtn = document.getElementById('rewind');
        const forwardBtn = document.getElementById('forward');
        const progressBar = document.getElementById('progress');
        const timeDisplay = document.getElementById('time-display');
        const muteBtn = document.getElementById('mute');
        const volumeSlider = document.getElementById('volume');
        const captionsToggle = document.getElementById('captions-toggle');
        const speedButton = document.getElementById('speed-button');
        const speedMenu = document.getElementById('speed-menu');
        const fullscreenBtn = document.getElementById('fullscreen');
        const customCaption = document.getElementById('custom-caption');
        
        // 再生/一時停止
        playPauseBtn.addEventListener('click', () => {
            if (video.paused) {
                video.play();
                playPauseBtn.textContent = '⏸';
                playPauseBtn.setAttribute('aria-label', '一時停止');
                playPauseBtn.setAttribute('aria-pressed', 'true');
            } else {
                video.pause();
                playPauseBtn.textContent = '▶';
                playPauseBtn.setAttribute('aria-label', '再生');
                playPauseBtn.setAttribute('aria-pressed', 'false');
            }
        });
        
        // スペースキーで再生/一時停止
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target.tagName !== 'BUTTON' && e.target.tagName !== 'INPUT') {
                e.preventDefault();
                playPauseBtn.click();
            }
        });
        
        // 10秒巻き戻し/早送り
        rewindBtn.addEventListener('click', () => {
            video.currentTime = Math.max(0, video.currentTime - 10);
        });
        
        forwardBtn.addEventListener('click', () => {
            video.currentTime = Math.min(video.duration, video.currentTime + 10);
        });
        
        // プログレスバー更新
        video.addEventListener('timeupdate', () => {
            const percent = (video.currentTime / video.duration) * 100;
            progressBar.style.width = percent + '%';
            
            const current = formatTime(video.currentTime);
            const duration = formatTime(video.duration);
            timeDisplay.textContent = `${current} / ${duration}`;
        });
        
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        }
        
        // 音量コントロール
        volumeSlider.addEventListener('input', (e) => {
            video.volume = e.target.value / 100;
            updateMuteIcon();
        });
        
        muteBtn.addEventListener('click', () => {
            video.muted = !video.muted;
            muteBtn.setAttribute('aria-pressed', video.muted);
            updateMuteIcon();
        });
        
        function updateMuteIcon() {
            if (video.muted || video.volume === 0) {
                muteBtn.textContent = '🔇';
                muteBtn.setAttribute('aria-label', 'ミュート解除');
            } else if (video.volume < 0.5) {
                muteBtn.textContent = '🔉';
                muteBtn.setAttribute('aria-label', 'ミュート');
            } else {
                muteBtn.textContent = '🔊';
                muteBtn.setAttribute('aria-label', 'ミュート');
            }
        }
        
        // 字幕トグル
        let captionsEnabled = true;
        captionsToggle.addEventListener('click', () => {
            captionsEnabled = !captionsEnabled;
            captionsToggle.setAttribute('aria-pressed', captionsEnabled);
            
            const tracks = video.textTracks;
            for (let i = 0; i < tracks.length; i++) {
                if (tracks[i].kind === 'captions') {
                    tracks[i].mode = captionsEnabled ? 'showing' : 'hidden';
                }
            }
            
            customCaption.style.display = captionsEnabled ? 'block' : 'none';
        });
        
        // カスタム字幕表示（サイズ・色変更可能）
        video.textTracks[0].addEventListener('cuechange', function() {
            const cue = this.activeCues[0];
            if (cue && captionsEnabled) {
                customCaption.textContent = cue.text;
                customCaption.style.display = 'block';
            } else {
                customCaption.style.display = 'none';
            }
        });
        
        // 再生速度
        speedButton.addEventListener('click', () => {
            const isOpen = speedMenu.classList.toggle('open');
            speedButton.setAttribute('aria-expanded', isOpen);
        });
        
        speedMenu.querySelectorAll('.speed-option').forEach(option => {
            option.addEventListener('click', () => {
                const speed = parseFloat(option.dataset.speed);
                video.playbackRate = speed;
                speedButton.textContent = speed + 'x';
                
                speedMenu.querySelectorAll('.speed-option').forEach(o => o.classList.remove('active'));
                option.classList.add('active');
                
                speedMenu.classList.remove('open');
                speedButton.setAttribute('aria-expanded', 'false');
            });
        });
        
        // フルスクリーン
        fullscreenBtn.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                video.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        });
    </script>
</body>
</html>
```

### 参考文献・リソース

**書籍・ガイド**
- Microsoft. (2016). *Inclusive Design Toolkit*. https://inclusive.microsoft.design/
- Holmes, K. (2018). *Mismatch: How Inclusion Shapes Design*. MIT Press.
- Waller, S., et al. (2015). *Inclusive Design Toolkit*. University of Cambridge.

**オンラインリソース**
- Microsoft Inclusive Design: https://inclusive.microsoft.design/
- W3C Inclusive Design Research Centre: https://idrc.ocadu.ca/

---

## 5. 支援技術テスト

### 分類
品質保証・実機検証・ユーザビリティテスト

### 背景と歴史

支援技術（Assistive Technology）は、障害のある人が情報技術にアクセスするために使用するハードウェアやソフトウェアです。スクリーンリーダー、拡大鏡、音声入力、スイッチコントロールなどが含まれます。

Webアクセシビリティの実現には、自動テストツール（axe、WAVE、Lighthouseなど）だけでは不十分で、実際の支援技術を使った手動テストが不可欠です。自動テストは約30%の問題しか検出できないと言われています。

主要な支援技術には、スクリーンリーダー（NVDA、JAWS、VoiceOver、TalkBack、Narrator）、拡大ツール（ZoomText、Windows Magnifier、macOS Zoom）、音声入力（Dragon NaturallySpeaking、音声コントロール）などがあります。

### 詳細な理論

#### 支援技術の種類と対応

**1. スクリーンリーダー（視覚障害者向け）**

主要ツール:
- **NVDA（NonVisual Desktop Access）**: Windows、無料、最も広く使用
- **JAWS（Job Access With Speech）**: Windows、有料、企業環境で多用
- **VoiceOver**: macOS/iOS、標準搭載
- **TalkBack**: Android、標準搭載
- **Narrator**: Windows、標準搭載

テスト項目:
- セマンティックHTML（見出し、リスト、ランドマーク）の正しい使用
- 画像のalt属性
- フォームのlabel関連付け
- ARIAロール・ステート・プロパティ
- フォーカス管理（モーダル、動的コンテンツ）
- ライブリージョン
- キーボード操作

**2. 拡大ツール（ロービジョン向け）**

主要ツール:
- **ZoomText**: Windows、拡大+スクリーンリーダー
- **Windows Magnifier**: Windows標準
- **macOS Zoom**: macOS標準
- ブラウザズーム: 200-400%

テスト項目:
- 200-400%ズームでのレイアウト崩れ
- テキストのリフロー
- ズーム時の水平スクロール回避
- フォーカスインジケーターの可視性

**3. 音声入力（運動障害者向け）**

主要ツール:
- **Dragon NaturallySpeaking**: Windows、音声入力
- **音声コントロール**: macOS/iOS
- **Voice Access**: Android

テスト項目:
- すべてのインタラクティブ要素に明確なラベル
- クリック可能要素の適切なサイズ
- 音声コマンドでのナビゲーション

**4. スイッチコントロール（重度運動障害者向け）**

主要ツール:
- **Switch Control**: iOS/macOS
- **Switch Access**: Android

テスト項目:
- キーボードナビゲーション
- フォーカスの論理的順序
- スキップリンク

#### テスト戦略

**レベル1: 自動テスト（30%の問題を検出）**
- axe DevTools
- WAVE
- Lighthouse
- Pa11y

**レベル2: 手動テスト（キーボードナビゲーション）**
- Tabキーのみでの全機能操作
- フォーカスインジケーターの可視性
- フォーカストラップ（モーダル）

**レベル3: スクリーンリーダーテスト**
- NVDA/JAWSでの読み上げ確認
- VoiceOverでの操作確認

**レベル4: ユーザーテスト**
- 実際の障害のあるユーザーによるテスト

### 実践例

#### 例1: NVDAスクリーンリーダーテストチェックリスト

```markdown
# NVDAスクリーンリーダーテスト - チェックリスト

## 準備
- [ ] NVDAをダウンロード・インストール (https://www.nvaccess.org/)
- [ ] NVDA + Nキーでブラウズモードを確認
- [ ] NVDA + スペースでフォーカスモード/ブラウズモード切り替えを確認

## 基本操作
- [ ] **ページタイトル読み上げ**: ページ読み込み時にタイトルが読み上げられるか
- [ ] **見出しナビゲーション**: Hキーで見出しを移動、1-6キーでレベル別見出し移動
- [ ] **ランドマークナビゲーション**: Dキーでランドマーク（main, nav, aside等）を移動
- [ ] **リンクナビゲーション**: Kキーでリンクを移動
- [ ] **リストナビゲーション**: Lキーでリストを移動、Iキーでリストアイテムを移動
- [ ] **ボタンナビゲーション**: Bキーでボタンを移動

## ページ構造
- [ ] **見出し階層**: 見出しレベルが論理的（h1 → h2 → h3、飛ばさない）
- [ ] **ランドマーク**: header/banner, nav, main, aside, footer/contentinfo が適切に配置
- [ ] **スキップリンク**: 「メインコンテンツへスキップ」が最初に読み上げられる
- [ ] **言語指定**: lang属性でページ言語が正しく指定されている

## 画像
- [ ] **代替テキスト**: 意味のある画像に説明的なalt属性
- [ ] **装飾画像**: 装飾的画像はalt=""で読み上げをスキップ
- [ ] **複雑な画像**: チャート・グラフに詳細な説明（longdescまたはaria-describedby）
- [ ] **アイコンボタン**: アイコンのみのボタンにaria-label

## フォーム
- [ ] **labelとinputの関連付け**: フォーカス時にラベルが読み上げられる
- [ ] **必須フィールド**: aria-required="true"またはrequired属性
- [ ] **エラーメッセージ**: エラー時にaria-invalid="true"とエラーメッセージが読み上げ
- [ ] **フィールド説明**: aria-describedbyで説明が関連付けられている
- [ ] **グループ化**: fieldset/legendで関連フィールドがグループ化

## インタラクティブ要素
- [ ] **ボタン**: ボタンの目的が明確に読み上げられる
- [ ] **リンク**: リンクテキストが文脈から独立して理解可能
- [ ] **リンクとボタンの区別**: roleが正しく設定されている

## 動的コンテンツ
- [ ] **ライブリージョン**: 動的更新がaria-liveで通知される
- [ ] **モーダルダイアログ**: 開いたときにフォーカスが移動し、タイトルが読み上げ
- [ ] **タブパネル**: タブ切り替え時に新しいパネルの内容が読み上げ
- [ ] **アコーディオン**: 展開/折りたたみ状態がaria-expandedで伝わる

## テーブル
- [ ] **テーブルヘッダー**: <th>要素またはrole="columnheader"
- [ ] **テーブルキャプション**: <caption>でテーブルの説明
- [ ] **複雑なテーブル**: scope属性またはheaders属性で関連付け

## キーボード操作
- [ ] **全機能アクセス**: Tabキーとキーボードだけで全機能にアクセス可能
- [ ] **フォーカスインジケーター**: フォーカス位置が視覚的に明確
- [ ] **フォーカストラップ**: モーダル内でフォーカスが閉じ込められる
- [ ] **論理的Tab順序**: DOM順序が論理的

## モバイル（VoiceOver on iOS）
- [ ] **1本指右スワイプ**: 次の要素へ移動
- [ ] **2本指スワイプ**: スクロール
- [ ] **ローター**: 2本指回転で見出し・リンク・フォームコントロール間を移動
- [ ] **ダブルタップ**: 要素をアクティベート

## テスト後チェック
- [ ] 発見した問題をすべて記録
- [ ] 重大度を評価（クリティカル、高、中、低）
- [ ] 修正方法を提案
- [ ] 修正後に再テスト
```

#### 例2: アクセシビリティテスト自動化スクリプト

```javascript
// axe-coreを使った自動テスト（Jest + Puppeteer）

const { AxePuppeteer } = require('@axe-core/puppeteer');
const puppeteer = require('puppeteer');

describe('Accessibility Tests', () => {
    let browser;
    let page;
    
    beforeAll(async () => {
        browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
    });
    
    afterAll(async () => {
        await browser.close();
    });
    
    beforeEach(async () => {
        page = await browser.newPage();
        await page.setBypassCSP(true);
    });
    
    afterEach(async () => {
        await page.close();
    });
    
    test('Homepage should have no accessibility violations', async () => {
        await page.goto('http://localhost:3000');
        
        const results = await new AxePuppeteer(page)
            .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
            .analyze();
        
        expect(results.violations).toHaveLength(0);
        
        if (results.violations.length > 0) {
            console.log('Accessibility Violations:');
            results.violations.forEach(violation => {
                console.log(`\n[${violation.impact}] ${violation.id}: ${violation.description}`);
                console.log(`Help: ${violation.helpUrl}`);
                violation.nodes.forEach(node => {
                    console.log(`  - ${node.html}`);
                    console.log(`    ${node.failureSummary}`);
                });
            });
        }
    }, 30000);
    
    test('Form page should be keyboard accessible', async () => {
        await page.goto('http://localhost:3000/form');
        
        // Tabキーでフォーカス移動をテスト
        const focusableElements = await page.evaluate(() => {
            const elements = [];
            const selector = 'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';
            document.querySelectorAll(selector).forEach((el, index) => {
                elements.push({
                    tagName: el.tagName,
                    type: el.type,
                    ariaLabel: el.getAttribute('aria-label'),
                    textContent: el.textContent?.trim().substring(0, 50)
                });
            });
            return elements;
        });
        
        console.log('Focusable elements:', focusableElements);
        expect(focusableElements.length).toBeGreaterThan(0);
        
        // Tabキーで全要素をフォーカスできるかテスト
        for (let i = 0; i < focusableElements.length; i++) {
            await page.keyboard.press('Tab');
            
            const focusedElement = await page.evaluate(() => {
                const el = document.activeElement;
                return {
                    tagName: el.tagName,
                    ariaLabel: el.getAttribute('aria-label'),
                    textContent: el.textContent?.trim().substring(0, 50)
                };
            });
            
            console.log(`Focus ${i + 1}:`, focusedElement);
        }
    });
    
    test('Images should have alt text', async () => {
        await page.goto('http://localhost:3000');
        
        const imagesWithoutAlt = await page.evaluate(() => {
            const images = Array.from(document.querySelectorAll('img'));
            return images
                .filter(img => !img.hasAttribute('alt'))
                .map(img => img.src);
        });
        
        expect(imagesWithoutAlt).toHaveLength(0);
        
        if (imagesWithoutAlt.length > 0) {
            console.log('Images without alt text:', imagesWithoutAlt);
        }
    });
    
    test('Page should have proper heading structure', async () => {
        await page.goto('http://localhost:3000');
        
        const headings = await page.evaluate(() => {
            const headingElements = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
            return headingElements.map(h => ({
                level: parseInt(h.tagName.substring(1)),
                text: h.textContent.trim()
            }));
        });
        
        console.log('Heading structure:', headings);
        
        // h1が1つだけあることを確認
        const h1Count = headings.filter(h => h.level === 1).length;
        expect(h1Count).toBe(1);
        
        // 見出しレベルがスキップされていないことを確認
        for (let i = 1; i < headings.length; i++) {
            const levelDiff = headings[i].level - headings[i - 1].level;
            if (levelDiff > 1) {
                console.warn(`Heading level skipped from h${headings[i - 1].level} to h${headings[i].level}`);
            }
        }
    });
    
    test('Color contrast should meet WCAG AA', async () => {
        await page.goto('http://localhost:3000');
        
        const results = await new AxePuppeteer(page)
            .withTags(['wcag2aa'])
            .disableRules(['color-contrast']) // 後で個別にチェック
            .analyze();
        
        const contrastResults = await new AxePuppeteer(page)
            .withRules(['color-contrast'])
            .analyze();
        
        expect(contrastResults.violations).toHaveLength(0);
        
        if (contrastResults.violations.length > 0) {
            console.log('Color contrast violations:');
            contrastResults.violations[0].nodes.forEach(node => {
                console.log(`  - ${node.html}`);
                console.log(`    ${node.failureSummary}`);
            });
        }
    });
});
```

```javascript
// package.json に追加
{
  "devDependencies": {
    "@axe-core/puppeteer": "^4.7.0",
    "puppeteer": "^21.0.0",
    "jest": "^29.0.0"
  },
  "scripts": {
    "test:a11y": "jest --testMatch='**/*.a11y.test.js'"
  }
}
```

### 参考文献・リソース

**スクリーンリーダー**
- NVDA: https://www.nvaccess.org/
- JAWS: https://www.freedomscientific.com/products/software/jaws/
- VoiceOver User Guide: https://support.apple.com/guide/voiceover/welcome/mac

**テストツール**
- axe DevTools: https://www.deque.com/axe/devtools/
- WAVE: https://wave.webaim.org/
- Lighthouse: https://developers.google.com/web/tools/lighthouse
- Pa11y: https://pa11y.org/

**ガイド**
- WebAIM Screen Reader Testing: https://webaim.org/articles/screenreader_testing/
- テストケース集: https://a11y-101.com/design/testing

---

## フレームワーク選択ガイド

| プロジェクトフェーズ | 推奨フレームワーク | 主な用途 |
|-----------------|-----------------|---------|
| **要件定義** | WCAG適合レベル選択、ユニバーサルデザイン原則 | 目標設定、法規制確認 |
| **設計** | インクルーシブデザイン、POUR原則、ユニバーサルデザイン | ワイヤーフレーム、プロトタイピング |
| **実装** | WCAG達成基準、ARIA、セマンティックHTML | コーディング、コンポーネント開発 |
| **テスト** | 支援技術テスト、自動テスト、手動テスト | 品質保証、問題発見 |
| **運用・改善** | ユーザーフィードバック、継続的テスト | 監視、インシデント対応 |

---

## 実践統合例

```typescript
// Next.js + TypeScript でのアクセシブルなWebアプリケーション

// components/AccessibleButton.tsx
import React from 'react';

interface AccessibleButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'icon';
  ariaLabel?: string;
  ariaExpanded?: boolean;
  ariaHaspopup?: boolean | 'menu' | 'dialog' | 'listbox';
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

export const AccessibleButton: React.FC<AccessibleButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  ariaLabel,
  ariaExpanded,
  ariaHaspopup,
  disabled = false,
  type = 'button',
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`accessible-button accessible-button--${variant}`}
      aria-label={ariaLabel}
      aria-expanded={ariaExpanded}
      aria-haspopup={ariaHaspopup}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

// components/AccessibleForm.tsx
import { useState } from 'react';

interface FormErrors {
  [key: string]: string;
}

export const AccessibleForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);
  
  const validate = () => {
    const newErrors: FormErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'お名前を入力してください';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'メールアドレスを入力してください';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = '正しいメールアドレス形式で入力してください';
    }
    
    if (!formData.message.trim()) {
      newErrors.message = 'メッセージを入力してください';
    }
    
    return newErrors;
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const newErrors = validate();
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      // フォーム送信処理
      console.log('Form submitted:', formData);
      setSubmitted(true);
    } else {
      // エラーサマリーにフォーカス
      document.getElementById('error-summary')?.focus();
    }
  };
  
  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* WCAG 3.3.1: エラー識別 */}
      {Object.keys(errors).length > 0 && (
        <div 
          id="error-summary"
          role="alert" 
          aria-live="assertive"
          tabIndex={-1}
          className="error-summary"
        >
          <h2>入力エラーがあります</h2>
          <ul>
            {Object.entries(errors).map(([field, message]) => (
              <li key={field}>
                <a href={`#${field}`}>{message}</a>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {submitted && (
        <div role="alert" aria-live="polite" className="success-message">
          お問い合わせを受け付けました。ありがとうございます。
        </div>
      )}
      
      {/* WCAG 1.3.1, 3.3.2: ラベルと説明 */}
      <div className="form-group">
        <label htmlFor="name" className="required-label">
          お名前
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
          aria-required="true"
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? 'name-error' : undefined}
          autoComplete="name"
        />
        {errors.name && (
          <div id="name-error" className="error-message" role="alert">
            {errors.name}
          </div>
        )}
      </div>
      
      <div className="form-group">
        <label htmlFor="email" className="required-label">
          メールアドレス
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
          autoComplete="email"
        />
        {errors.email && (
          <div id="email-error" className="error-message" role="alert">
            {errors.email}
          </div>
        )}
      </div>
      
      <div className="form-group">
        <label htmlFor="message" className="required-label">
          メッセージ
        </label>
        <textarea
          id="message"
          name="message"
          rows={5}
          value={formData.message}
          onChange={(e) => setFormData({ ...formData, message: e.target.value })}
          required
          aria-required="true"
          aria-invalid={!!errors.message}
          aria-describedby={errors.message ? 'message-error' : undefined}
        />
        {errors.message && (
          <div id="message-error" className="error-message" role="alert">
            {errors.message}
          </div>
        )}
      </div>
      
      <div className="form-actions">
        <button type="submit" className="btn-primary">
          送信する
        </button>
      </div>
    </form>
  );
};
```

---

## まとめ

アクセシビリティスペシャリストが活用する5つの主要フレームワーク：

1. **WCAG**: 国際標準、法規制準拠、POUR原則、3つの適合レベル
2. **ARIA**: 動的コンテンツ、複雑なUIコンポーネント、支援技術連携
3. **ユニバーサルデザイン7原則**: 製品・環境設計の基本思想
4. **インクルーシブデザイン**: ユーザー参加型設計、パーソナスペクトラム
5. **支援技術テスト**: スクリーンリーダー、拡大ツール、音声入力の実機検証

これらを組み合わせることで、すべての人が利用できる包括的なデジタル体験を実現できます。

---

## 参考文献

**書籍**
- Pickering, H. (2016). *Inclusive Design Patterns*. Smashing Magazine.
- Horton, S., & Quesenbery, W. (2013). *A Web for Everyone*. Rosenfeld Media.
- Holmes, K. (2018). *Mismatch: How Inclusion Shapes Design*. MIT Press.

**オンラインリソース**
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C ARIA: https://www.w3.org/WAI/ARIA/apg/
- Microsoft Inclusive Design: https://inclusive.microsoft.design/
- WebAIM: https://webaim.org/

**ツール**
- axe DevTools: https://www.deque.com/axe/devtools/
- NVDA: https://www.nvaccess.org/
- Color Contrast Checker: https://webaim.org/resources/contrastchecker/
