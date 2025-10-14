# データサイエンティスト - 主要フレームワーク詳細

## フレームワーク1: CRISP-DM (Cross Industry Standard Process for Data Mining)

### 理論的背景

CRISP-DMは1996年に開発された、データマイニングプロジェクトの業界標準プロセスモデル。反復的・循環的アプローチにより、ビジネス課題とデータ分析を効果的に結びつける。

### 6つのフェーズ

**Phase 1: Business Understanding（ビジネス理解）**

**目的:** プロジェクトの目標と要件をビジネス視点で理解

**実施内容:**
- ビジネス目標の定義
- 状況評価（リソース、要件、リスク、コスト/ベネフィット）
- データマイニング目標の決定
- プロジェクト計画の策定

**成果物:**
```markdown
## ビジネス理解ドキュメント

### ビジネス目標
- 主目的: [売上20%向上等]
- 成功基準: [KPI指標]
- リスク: [想定リスクと影響度]

### データマイニング目標
- 予測対象: [離脱確率、売上予測等]
- 精度目標: [AUC 0.85以上等]
- 制約条件: [期限、予算、コンプライアンス]

### プロジェクト計画
- Phase 1: [期間、成果物]
- Phase 2: [期間、成果物]
...
```

**Phase 2: Data Understanding（データ理解）**

**目的:** データの収集、特性把握、品質評価

**実施内容:**
1. **初期データ収集**
   - データソース特定
   - アクセス権限取得
   - データ抽出

2. **データ記述**
   - データ量（行数、列数）
   - データ型
   - データ期間

3. **データ探索**
   - 記述統計量
   - 分布確認
   - 相関分析

4. **データ品質検証**
   - 欠損値（率、パターン）
   - 外れ値
   - 重複
   - 一貫性

**探索的データ分析チェックリスト:**
```python
# 基本情報
df.info()
df.describe()
df.head()

# 欠損値確認
df.isnull().sum() / len(df) * 100

# 重複確認
df.duplicated().sum()

# 数値変数の分布
df.hist(figsize=(15,10), bins=50)

# 相関分析
df.corr().style.background_gradient(cmap='coolwarm')

# カテゴリ変数の分布
for col in categorical_columns:
    print(df[col].value_counts())
```

**Phase 3: Data Preparation（データ準備）**

**目的:** モデリングに適したデータセット構築

**実施内容:**
1. **データ選択**
   - 分析対象データの決定
   - 不要列の除外

2. **データクレンジング**
   - 欠損値処理（削除、補完、フラグ化）
   - 外れ値処理
   - 重複削除
   - エラー修正

3. **特徴量エンジニアリング**
   - 新規特徴量作成
   - 特徴量変換
   - エンコーディング

4. **データ統合**
   - 複数ソースの結合
   - 集約

5. **フォーマット化**
   - データ分割（訓練/検証/テスト）
   - スケーリング

**データクレンジング戦略:**

| 問題 | 対処法 | 実装例 |
|------|--------|--------|
| 欠損値（少量） | 削除 | `df.dropna()` |
| 欠損値（多量） | 補完（平均、中央値、最頻値） | `df.fillna(df.mean())` |
| 欠損値（MNAR） | フラグ化 + 補完 | `df['col_missing'] = df['col'].isnull()` |
| 外れ値 | IQR法、Zスコア、ドメイン知識 | `Q1, Q3 = df.quantile([0.25, 0.75])` |
| 不均衡データ | SMOTE、アンダーサンプリング、重み付け | `from imblearn.over_sampling import SMOTE` |

**Phase 4: Modeling（モデリング）**

**目的:** 機械学習モデルの構築と最適化

**実施内容:**
1. **モデリング手法選択**
   - タスクタイプ（回帰、分類、クラスタリング）
   - データ特性（サイズ、次元、線形性）
   - ビジネス要件（精度、解釈性、速度）

2. **テスト設計**
   - 訓練/検証/テストデータ分割
   - 交差検証戦略
   - 評価指標選定

3. **モデル構築**
   - ベースラインモデル
   - 複数アルゴリズム試行
   - ハイパーパラメータチューニング

4. **モデル評価**
   - 性能指標計算
   - 過学習チェック
   - モデル比較

**モデル選択フローチャート:**
```
目的: 回帰 or 分類 or クラスタリング？
  ├─ 回帰
  │   ├─ 線形関係あり → 線形回帰（Ridge, Lasso, ElasticNet）
  │   ├─ 非線形複雑 → Random Forest, Gradient Boosting
  │   └─ 大規模データ → LightGBM, XGBoost
  │
  ├─ 分類
  │   ├─ 解釈性重視 → ロジスティック回帰、決定木
  │   ├─ 精度重視 → Random Forest, Gradient Boosting, XGBoost
  │   ├─ 非線形境界 → SVM (RBFカーネル)
  │   └─ 画像・テキスト → ニューラルネットワーク
  │
  └─ クラスタリング
      ├─ クラスタ数既知 → K-means
      ├─ クラスタ数未知 → DBSCAN, 階層的クラスタリング
      └─ 可視化目的 → PCA, t-SNE, UMAP
```

**Phase 5: Evaluation（評価）**

**目的:** ビジネス目標達成度の検証

**実施内容:**
1. **結果評価**
   - ビジネス基準での評価
   - モデル性能の解釈
   - デプロイ判断

2. **プロセスレビュー**
   - 見落としたステップの確認
   - 品質保証

3. **次ステップ決定**
   - デプロイ or 反復 or 中止

**評価基準マトリクス:**

| 観点 | 基準 | 目標値 |
|------|------|--------|
| 技術性能 | AUC-ROC, F1-Score等 | ビジネス要件による |
| ビジネス価値 | ROI, コスト削減額 | 投資回収1年以内等 |
| 運用性 | 予測速度、再学習頻度 | 100ms以内等 |
| 解釈性 | SHAP値、特徴量重要度 | ステークホルダー理解可能 |
| 公平性 | 各セグメントでの性能 | グループ間差10%以内等 |

**Phase 6: Deployment（展開）**

**目的:** モデルの本番環境への展開と運用

**実施内容:**
1. **デプロイ計画**
   - 展開方法（バッチ、リアルタイム、エッジ）
   - インフラ設計
   - モニタリング設計

2. **実装**
   - モデルのパッケージ化
   - API開発
   - 統合テスト

3. **モニタリングと保守**
   - 性能モニタリング
   - データドリフト検知
   - 再学習トリガー設定

**デプロイメントチェックリスト:**
- [ ] モデルのシリアライズ（pickle, joblib, ONNX）
- [ ] API実装（FastAPI, Flask）
- [ ] Dockerコンテナ化
- [ ] CI/CD パイプライン構築
- [ ] A/Bテスト設計
- [ ] モニタリングダッシュボード
- [ ] 再学習パイプライン
- [ ] ロールバック手順
- [ ] ドキュメント整備

### CRISP-DM活用のベストプラクティス

1. **反復的アプローチ**: 各フェーズは固定順序ではなく、必要に応じて前のフェーズに戻る
2. **ステークホルダー巻き込み**: ビジネス理解と評価フェーズで密接に連携
3. **早期プロトタイプ**: データ理解段階で簡易モデル構築し、フィージビリティ確認
4. **ドキュメント化**: 各フェーズの成果物を記録し、再現性を確保
5. **ビジネス価値優先**: 技術的洗練よりもビジネス目標達成を優先

---

## フレームワーク2: 探索的データ分析 (Exploratory Data Analysis)

### 理論的背景

EDAは1977年にJohn Tukeyが提唱したデータ分析アプローチ。仮説検証に先立ち、データの特性、パターン、異常を視覚的・統計的に探索する。

### 記述統計による理解

**中心傾向**
- **平均**: 算術平均、外れ値に敏感
- **中央値**: 50パーセンタイル、頑健な指標
- **最頻値**: 最も頻出する値、カテゴリデータに有用

**ばらつき**
- **標準偏差**: 平均からの散らばり度合い
- **分散**: 標準偏差の2乗
- **四分位範囲(IQR)**: Q3 - Q1、外れ値に頑健
- **変動係数(CV)**: 標準偏差/平均、スケール異なる変数の比較

**分布の形状**
- **歪度(Skewness)**: 分布の非対称性（0=対称、正=右裾、負=左裾）
- **尖度(Kurtosis)**: 裾の重さ（3=正規分布、>3=重い裾、<3=軽い裾）

**実装例:**
```python
import pandas as pd
import numpy as np

# 記述統計量の算出
summary = df.describe(include='all')

# 詳細統計量
def advanced_stats(series):
    return pd.Series({
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'var': series.var(),
        'cv': series.std() / series.mean(),
        'skew': series.skew(),
        'kurtosis': series.kurtosis(),
        'min': series.min(),
        'max': series.max(),
        'range': series.max() - series.min(),
        'iqr': series.quantile(0.75) - series.quantile(0.25),
        'missing': series.isnull().sum()
    })

numerical_stats = df.select_dtypes(include=[np.number]).apply(advanced_stats)
```

### 可視化技法

**単変量分析**

| グラフタイプ | 用途 | 適用データ |
|------------|------|-----------|
| ヒストグラム | 分布の形状確認 | 連続変数 |
| 箱ひげ図 | 分布と外れ値 | 連続変数 |
| 棒グラフ | カテゴリ別頻度 | カテゴリ変数 |
| 円グラフ | 構成比 | カテゴリ変数（5個以下） |
| バイオリンプロット | 分布の詳細 | 連続変数 |

**多変量分析**

| グラフタイプ | 用途 | 適用データ |
|------------|------|-----------|
| 散布図 | 2変数の関係 | 連続 x 連続 |
| 散布図行列 | 多変数の関係 | 複数連続変数 |
| 相関ヒートマップ | 相関構造 | 複数連続変数 |
| 箱ひげ図（グループ別） | グループ間比較 | カテゴリ x 連続 |
| ペアプロット | 多変数探索 | 複数連続 + カテゴリ |

**実装例:**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# 分布の可視化
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# ヒストグラム
df['column'].hist(bins=50, ax=axes[0,0])
axes[0,0].set_title('Histogram')

# 箱ひげ図
df.boxplot(column='column', ax=axes[0,1])
axes[0,1].set_title('Boxplot')

# Q-Qプロット（正規性確認）
from scipy import stats
stats.probplot(df['column'], dist="norm", plot=axes[1,0])
axes[1,0].set_title('Q-Q Plot')

# カーネル密度推定
df['column'].plot(kind='kde', ax=axes[1,1])
axes[1,1].set_title('KDE')

plt.tight_layout()
plt.show()

# 相関ヒートマップ
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0,
            fmt='.2f', square=True, linewidths=1)
plt.title('Correlation Heatmap')
plt.show()

# ペアプロット
sns.pairplot(df, hue='target_variable', diag_kind='kde')
plt.show()
```

### 外れ値検出

**統計的手法**

**1. IQR法（四分位範囲法）**
```python
Q1 = df['column'].quantile(0.25)
Q3 = df['column'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['column'] < lower_bound) | (df['column'] > upper_bound)]
```

**2. Zスコア法**
```python
from scipy import stats

z_scores = np.abs(stats.zscore(df['column']))
outliers = df[z_scores > 3]  # 3σ以上を外れ値とする
```

**3. Isolation Forest（機械学習ベース）**
```python
from sklearn.ensemble import IsolationForest

clf = IsolationForest(contamination=0.1, random_state=42)
outlier_labels = clf.fit_predict(df[numerical_columns])
outliers = df[outlier_labels == -1]
```

### 相関分析

**相関係数の種類**

| 係数 | 適用条件 | 範囲 | 特徴 |
|------|----------|------|------|
| Pearson | 線形関係、正規分布 | -1 ~ 1 | 線形相関のみ検出 |
| Spearman | 単調関係 | -1 ~ 1 | 順位相関、非線形にも対応 |
| Kendall | 順序データ | -1 ~ 1 | サンプルサイズ小で正確 |

**実装と解釈:**
```python
# Pearson相関
pearson_corr = df.corr(method='pearson')

# Spearman相関
spearman_corr = df.corr(method='spearman')

# Kendall相関
kendall_corr = df.corr(method='kendall')

# 相関係数と有意性
from scipy.stats import pearsonr, spearmanr

corr_coef, p_value = pearsonr(df['var1'], df['var2'])
print(f"Correlation: {corr_coef:.3f}, p-value: {p_value:.3f}")

# 解釈ガイドライン
# |r| = 0.0 - 0.3: 弱い相関
# |r| = 0.3 - 0.7: 中程度の相関
# |r| = 0.7 - 1.0: 強い相関
```

**注意点:**
- 相関 ≠ 因果関係
- 外れ値の影響（Pearson）
- 非線形関係の見逃し（Pearson）
- 交絡変数の存在

---

## フレームワーク3: 特徴量エンジニアリング

### 理論的背景

Andrew Ng: "Applied machine learning is basically feature engineering."
特徴量エンジニアリングは、生データからモデルに有用な特徴量を作成・選択するプロセス。

### 数値特徴量の処理

**スケーリング**

| 手法 | 変換式 | 用途 |
|------|--------|------|
| 標準化 | (x - μ) / σ | 平均0、標準偏差1。距離ベースアルゴリズム |
| 正規化（Min-Max） | (x - min) / (max - min) | [0,1]範囲。ニューラルネットワーク |
| Robust Scaler | (x - median) / IQR | 外れ値に頑健 |
| Max Abs Scaler | x / max(abs(x)) | [-1,1]範囲。スパースデータ |

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# 標準化
scaler = StandardScaler()
df['column_scaled'] = scaler.fit_transform(df[['column']])

# 正規化
scaler = MinMaxScaler()
df['column_normalized'] = scaler.fit_transform(df[['column']])

# Robust Scaler
scaler = RobustScaler()
df['column_robust'] = scaler.fit_transform(df[['column']])
```

**変換**

**1. 対数変換（右裾の分布を正規化）**
```python
df['log_column'] = np.log1p(df['column'])  # log(1+x)、0対応
```

**2. Box-Cox変換（最適なλを自動決定）**
```python
from scipy.stats import boxcox

df['boxcox_column'], lambda_param = boxcox(df['column'])
```

**3. Yeo-Johnson変換（負の値にも対応）**
```python
from sklearn.preprocessing import PowerTransformer

pt = PowerTransformer(method='yeo-johnson')
df['yj_column'] = pt.fit_transform(df[['column']])
```

**ビニング（離散化）**

```python
# 等幅ビニング
df['age_binned'] = pd.cut(df['age'], bins=5, labels=['very young', 'young', 'middle', 'senior', 'elderly'])

# 等頻度ビニング
df['income_binned'] = pd.qcut(df['income'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

# カスタムビン
bins = [0, 18, 30, 50, 100]
df['age_custom'] = pd.cut(df['age'], bins=bins, labels=['child', 'young', 'adult', 'senior'])
```

### カテゴリカル特徴量の処理

**エンコーディング手法比較**

| 手法 | 適用場面 | メリット | デメリット |
|------|----------|----------|-----------|
| Label Encoding | 順序あり変数 | シンプル、次元増えない | 順序情報を誤って学習 |
| One-Hot Encoding | カーディナリティ低い | 順序情報なし、解釈容易 | 高次元、多重共線性 |
| Target Encoding | カーディナリティ高い | 次元増えない、予測力高い | リーク、過学習リスク |
| Frequency Encoding | 頻度が情報 | シンプル | 情報損失 |

**実装例:**

```python
# Label Encoding
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['education_encoded'] = le.fit_transform(df['education'])

# One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=['category'], prefix='cat')

# Target Encoding（過学習対策：CV内で実施）
def target_encode(train, test, column, target, smoothing=1):
    # 訓練データでの平均計算
    means = train.groupby(column)[target].mean()
    global_mean = train[target].mean()

    # スムージング適用
    counts = train.groupby(column).size()
    smooth_means = (counts * means + smoothing * global_mean) / (counts + smoothing)

    # テストデータに適用
    train_encoded = train[column].map(smooth_means)
    test_encoded = test[column].map(smooth_means).fillna(global_mean)

    return train_encoded, test_encoded

# Frequency Encoding
freq_map = df['category'].value_counts() / len(df)
df['category_freq'] = df['category'].map(freq_map)
```

### 時系列特徴量

**日時から特徴量抽出**

```python
df['date'] = pd.to_datetime(df['date'])

# 基本的な時間特徴量
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek  # 0=月曜
df['quarter'] = df['date'].dt.quarter
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)

# 周期性の表現（円環的エンコーディング）
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

# 祝日フラグ
from pandas.tseries.holiday import USFederalHolidayCalendar
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=df['date'].min(), end=df['date'].max())
df['is_holiday'] = df['date'].isin(holidays).astype(int)
```

**ラグ特徴量と移動統計量**

```python
# ラグ特徴量
for lag in [1, 7, 30]:
    df[f'sales_lag_{lag}'] = df.groupby('store_id')['sales'].shift(lag)

# ローリング統計量
window_sizes = [7, 30]
for window in window_sizes:
    df[f'sales_rolling_mean_{window}'] = df.groupby('store_id')['sales'].transform(
        lambda x: x.rolling(window, min_periods=1).mean()
    )
    df[f'sales_rolling_std_{window}'] = df.groupby('store_id')['sales'].transform(
        lambda x: x.rolling(window, min_periods=1).std()
    )

# 差分
df['sales_diff_1'] = df.groupby('store_id')['sales'].diff(1)
df['sales_pct_change'] = df.groupby('store_id')['sales'].pct_change()
```

### 特徴量選択

**フィルタ法（統計ベース）**

```python
# 分散による選択（低分散特徴量を除去）
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0.1)
X_selected = selector.fit_transform(X)

# 相関による選択
corr_matrix = X.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]
X_selected = X.drop(columns=to_drop)

# 統計検定による選択
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(score_func=f_classif, k=10)
X_selected = selector.fit_transform(X, y)
```

**ラッパー法（モデルベース）**

```python
# Recursive Feature Elimination (RFE)
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
rfe = RFE(estimator=model, n_features_to_select=10, step=1)
rfe.fit(X, y)
selected_features = X.columns[rfe.support_]
```

**組み込み法**

```python
# Lasso（L1正則化）による特徴量選択
from sklearn.linear_model import LassoCV

lasso = LassoCV(cv=5, random_state=42).fit(X, y)
importance = np.abs(lasso.coef_)
selected_features = X.columns[importance > 0]

# Tree-based Feature Importance
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
```

---

## フレームワーク4: 機械学習モデリング

### モデル選択ガイド

**タスクタイプ別推奨アルゴリズム**

**回帰タスク:**

| シナリオ | 推奨アルゴリズム | 理由 |
|----------|-----------------|------|
| 線形関係、解釈性重視 | 線形回帰、Ridge、Lasso | シンプル、係数で解釈可能 |
| 非線形、中規模データ | Random Forest | 非線形対応、特徴量重要度 |
| 高精度、大規模データ | XGBoost, LightGBM | 最高精度、高速 |
| 時系列予測 | ARIMA, Prophet, LSTM | 時間依存性考慮 |

**分類タスク:**

| シナリオ | 推奨アルゴリズム | 理由 |
|----------|-----------------|------|
| 解釈性重視 | ロジスティック回帰、決定木 | 透明性、説明可能 |
| 高精度、表データ | XGBoost, LightGBM | 最高精度クラス |
| 非線形、複雑な境界 | SVM（RBFカーネル） | 非線形対応 |
| 画像分類 | CNN（ResNet, EfficientNet） | 画像特徴抽出 |
| テキスト分類 | BERT, RoBERTa | 文脈理解 |
| 不均衡データ | XGBoost（scale_pos_weight） | 重み付け対応 |

### 交差検証戦略

**K-Fold Cross-Validation**

```python
from sklearn.model_selection import cross_val_score, KFold

kfold = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kfold, scoring='accuracy')

print(f"CV Accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

**Stratified K-Fold（分類、不均衡データ）**

```python
from sklearn.model_selection import StratifiedKFold

skfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skfold, scoring='roc_auc')
```

**Time Series Split（時系列データ）**

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_index, test_index in tscv.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    # モデル訓練と評価
```

### ハイパーパラメータチューニング

**Grid Search（全探索）**

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=2
)

grid_search.fit(X_train, y_train)
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")
```

**Random Search（ランダム探索）**

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(5, 30),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': uniform(0.1, 0.9)
}

random_search = RandomizedSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_distributions=param_dist,
    n_iter=50,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)
```

**Bayesian Optimization（ベイズ最適化）**

```python
from skopt import BayesSearchCV
from skopt.space import Real, Integer

search_spaces = {
    'n_estimators': Integer(100, 500),
    'max_depth': Integer(5, 30),
    'min_samples_split': Integer(2, 20),
    'learning_rate': Real(0.01, 0.3, prior='log-uniform')
}

bayes_search = BayesSearchCV(
    estimator=XGBClassifier(random_state=42),
    search_spaces=search_spaces,
    n_iter=50,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    random_state=42
)

bayes_search.fit(X_train, y_train)
```

### 評価指標の選択

**回帰指標:**

| 指標 | 式 | 特徴 | 使用場面 |
|------|----|----|---------|
| MAE | Σ\|y-ŷ\|/n | 外れ値に頑健 | 外れ値が多い |
| MSE | Σ(y-ŷ)²/n | 大きな誤差にペナルティ | 大きな誤差を避けたい |
| RMSE | √MSE | MSEと同じ単位 | 標準的 |
| R² | 1 - SS_res/SS_tot | 説明力 | モデル比較 |
| MAPE | Σ\|y-ŷ\|/y/n | %誤差 | 相対誤差重視 |

**分類指標（二値分類）:**

| 指標 | 式 | 特徴 | 使用場面 |
|------|----|----|---------|
| Accuracy | (TP+TN)/(TP+FP+TN+FN) | 全体正解率 | 均衡データ |
| Precision | TP/(TP+FP) | 陽性予測の正確さ | FP削減重視 |
| Recall | TP/(TP+FN) | 陽性の検出率 | FN削減重視（医療等） |
| F1-Score | 2PR/(P+R) | Precision-Recallの調和平均 | 不均衡データ |
| AUC-ROC | ROC曲線下面積 | 閾値に依存しない | 総合評価 |
| AUC-PR | PR曲線下面積 | 不均衡データに適切 | 不均衡データ |

**多クラス分類:**
- Macro-averaged: 各クラスの平均（クラス不均衡考慮しない）
- Micro-averaged: 全サンプルで計算（多数派クラス優先）
- Weighted-averaged: クラス数で重み付け

**実装例:**

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                            f1_score, roc_auc_score, classification_report,
                            confusion_matrix)

# 予測
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# 指標計算
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall: {recall_score(y_test, y_pred):.3f}")
print(f"F1-Score: {f1_score(y_test, y_pred):.3f}")
print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.3f}")

# 詳細レポート
print(classification_report(y_test, y_pred))

# 混同行列
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()
```

---

## フレームワーク5: 実験設計と因果推論

### A/Bテスト設計

**サンプルサイズ計算**

```python
from statsmodels.stats.power import tt_ind_solve_power

# 必要サンプルサイズの計算
effect_size = 0.2  # Cohen's d
alpha = 0.05  # 有意水準
power = 0.8  # 検出力

n_per_group = tt_ind_solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    alternative='two-sided'
)

print(f"Required sample size per group: {int(n_per_group)}")
```

**統計検定**

```python
from scipy.stats import ttest_ind, mannwhitneyu, chi2_contingency

# t検定（連続変数、正規分布前提）
statistic, pvalue = ttest_ind(group_a, group_b)

# Mann-Whitney U検定（連続変数、分布前提なし）
statistic, pvalue = mannwhitneyu(group_a, group_b, alternative='two-sided')

# カイ二乗検定（カテゴリ変数）
contingency_table = pd.crosstab(df['group'], df['conversion'])
chi2, pvalue, dof, expected = chi2_contingency(contingency_table)

# 効果量の計算（Cohen's d）
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / pooled_std
```

### 因果推論

**傾向スコアマッチング (Propensity Score Matching)**

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

# 傾向スコアの推定
ps_model = LogisticRegression()
ps_model.fit(X_confounders, treatment)
propensity_scores = ps_model.predict_proba(X_confounders)[:, 1]

# マッチング（最近傍法）
treated = df[df['treatment'] == 1]
control = df[df['treatment'] == 0]

nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
nn.fit(control[['propensity_score']].values)
distances, indices = nn.kneighbors(treated[['propensity_score']].values)

# マッチされたサンプルで効果測定
matched_control = control.iloc[indices.flatten()]
ate = treated['outcome'].mean() - matched_control['outcome'].mean()
print(f"Average Treatment Effect: {ate:.3f}")
```

**差分の差分法 (Difference-in-Differences)**

```python
import statsmodels.formula.api as smf

# DiDモデルの推定
formula = 'outcome ~ treatment * post_period + controls'
model = smf.ols(formula, data=df).fit()

# DiD推定量（交互作用項の係数）
did_estimate = model.params['treatment:post_period']
print(f"DiD Estimate: {did_estimate:.3f}")
print(model.summary())
```

---

## フレームワーク6: モデル解釈性と説明

### SHAP (SHapley Additive exPlanations)

```python
import shap

# モデル訓練
model = XGBClassifier().fit(X_train, y_train)

# SHAP Explainer作成
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary Plot（全体の特徴量重要度）
shap.summary_plot(shap_values, X_test)

# Force Plot（個別予測の説明）
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])

# Dependence Plot（特徴量と予測の関係）
shap.dependence_plot("feature_name", shap_values, X_test)

# Waterfall Plot（個別予測の詳細）
shap.waterfall_plot(shap.Explanation(
    values=shap_values[0],
    base_values=explainer.expected_value,
    data=X_test.iloc[0],
    feature_names=X_test.columns.tolist()
))
```

### LIME (Local Interpretable Model-agnostic Explanations)

```python
import lime
import lime.lime_tabular

# LIME Explainer作成
explainer = lime.lime_tabular.LimeTabularExplainer(
    X_train.values,
    feature_names=X_train.columns.tolist(),
    class_names=['class_0', 'class_1'],
    mode='classification'
)

# 個別予測の説明
i = 0
exp = explainer.explain_instance(
    X_test.iloc[i].values,
    model.predict_proba,
    num_features=10
)

exp.show_in_notebook()
exp.as_pyplot_figure()
```

---

## 参考文献・リソース

### 書籍

**基礎:**
- Géron, A. (2019). "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow." O'Reilly.
- VanderPlas, J. (2016). "Python Data Science Handbook." O'Reilly.
- McKinney, W. (2017). "Python for Data Analysis." O'Reilly.

**統計・数理:**
- James, G. et al. (2021). "An Introduction to Statistical Learning." Springer.
- Hastie, T. et al. (2009). "The Elements of Statistical Learning." Springer.

**実務:**
- Zheng, A. & Casari, A. (2018). "Feature Engineering for Machine Learning." O'Reilly.
- Provost, F. & Fawcett, T. (2013). "Data Science for Business." O'Reilly.
- Huyen, C. (2022). "Designing Machine Learning Systems." O'Reilly.

### オンラインコース

- **Coursera**: Machine Learning (Andrew Ng), Deep Learning Specialization
- **fast.ai**: Practical Deep Learning for Coders
- **Kaggle Learn**: Pandas, Machine Learning, Feature Engineering
- **DataCamp**: Data Scientist with Python Career Track

### ツール・ライブラリ

- **pandas**: データ操作 (https://pandas.pydata.org/)
- **scikit-learn**: 機械学習 (https://scikit-learn.org/)
- **XGBoost**: 勾配ブースティング (https://xgboost.readthedocs.io/)
- **LightGBM**: 高速勾配ブースティング (https://lightgbm.readthedocs.io/)
- **SHAP**: モデル解釈 (https://shap.readthedocs.io/)
- **MLflow**: 実験管理 (https://mlflow.org/)

### コミュニティ・カンファレンス

- **Kaggle**: データサイエンスコンペティション (https://www.kaggle.com/)
- **KDD**: ACM SIGKDD Conference
- **NeurIPS**: Neural Information Processing Systems
- **ICML**: International Conference on Machine Learning

---

**更新日**: 2025-01-14
**対象**: データ分析・機械学習プロジェクト全般