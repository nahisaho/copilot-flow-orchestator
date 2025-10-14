# DevOpsエンジニア - フレームワーク・理論詳解

## 概要

DevOpsエンジニアオーケストレーターは、CI/CD、Infrastructure as Code、SRE、可観測性など、現代のソフトウェアデリバリーに不可欠な包括的なプラクティスを統合した対話型AIシステムです。開発と運用の壁を打破し、高速で信頼性の高いデプロイメントを実現するための戦略を提供します。

### 特徴
- CI/CDパイプラインからGitOpsまで、自動化戦略の全領域をカバー
- Terraform、Kubernetes、Helmなど主要ツールの実装パターン
- Prometheus、Grafana、分散トレーシングによる包括的可観測性
- SLI/SLO/SLA、エラーバジェット、カオスエンジニアリングのSREプラクティス
- DevSecOps、コンプライアンスas Codeのセキュリティ統合
- 実装可能なYAML、HCL、Dockerfileなど実コード例を豊富に提供

---

## 組み込まれているフレームワーク・理論

### 1. CI/CD (Continuous Integration / Continuous Delivery)

#### 分類
- **ソフトウェアデリバリー自動化系**
- **DevOpsの中核プラクティス**

#### 出典・背景
- **CI提唱者**: Martin Fowler, Kent Beck (Extreme Programming)
- **出典**: Martin Fowler, "Continuous Integration" (2006)
- **CD標準化**: Jez Humble, David Farley, "Continuous Delivery" (Addison-Wesley, 2010)
- **背景**: 1990年代のExtreme Programming (XP) 運動の中で、頻繁な統合とテストの重要性が認識されました。Martin Fowlerらが2000年代初頭にCI概念を明確化し、Jez HumbleとDavid Farleyが2010年に出版した「Continuous Delivery」が現代のCD実践の基礎となりました。CI/CDは、DevOps文化の技術的基盤として不可欠です。

#### 理論の詳細

**継続的インテグレーション (CI) の原則**:

1. **単一のソースリポジトリ**: 全コードを1つのバージョン管理システムで管理
2. **ビルドの自動化**: コミット毎に自動ビルド
3. **自己テスト**: ビルドに自動テストを組み込み
4. **頻繁なコミット**: 最低1日1回はメインブランチに統合
5. **即座のフィードバック**: ビルド失敗を迅速に検知・通知
6. **本番環境に近いテスト環境**: ステージング環境でのテスト

**CIパイプラインの典型的なステージ**:

```
1. ソースチェックアウト (Git clone)
   ↓
2. 依存関係解決 (npm install, pip install)
   ↓
3. コンパイル/ビルド (mvn compile, go build)
   ↓
4. ユニットテスト (JUnit, pytest)
   ↓
5. 静的解析 (SonarQube, ESLint)
   ↓
6. セキュリティスキャン (SAST, dependency check)
   ↓
7. コードカバレッジ測定
   ↓
8. アーティファクト生成 (JAR, Docker image)
   ↓
9. アーティファクトリポジトリへのpush (Nexus, ECR)
```

**継続的デリバリー (CD) の原則**:

1. **デプロイ可能な状態の維持**: メインブランチは常にデプロイ可能
2. **デプロイの自動化**: ボタン1つでデプロイ可能
3. **環境の一貫性**: 開発・ステージング・本番で同一の方法でデプロイ
4. **ロールバック可能**: デプロイ失敗時の迅速なロールバック
5. **段階的リリース**: カナリアリリース、ブルーグリーンデプロイ

**CDパイプラインの典型的なステージ**:

```
1. CIパイプラインの成功
   ↓
2. 統合テスト (API test, E2E test)
   ↓
3. パフォーマンステスト (JMeter, k6)
   ↓
4. セキュリティスキャン (DAST, penetration test)
   ↓
5. ステージング環境へのデプロイ
   ↓
6. 受け入れテスト (UAT)
   ↓
7. 本番デプロイ承認 (手動ゲート)
   ↓
8. 本番環境へのデプロイ
   ↓
9. スモークテスト
   ↓
10. モニタリング・アラート
```

**デプロイ戦略**:

**1. ブルーグリーンデプロイ**:
- 青（現行）と緑（新バージョン）の2つの環境
- 緑環境にデプロイ→テスト→トラフィック切り替え
- ロールバックが瞬時（トラフィックを青に戻すだけ）
- リソースコストが2倍

**2. カナリアリリース**:
- 新バージョンに段階的にトラフィックを流す（例: 5% → 25% → 50% → 100%）
- 問題発生時は即座にロールバック
- リスク最小化、本番環境での実験

**3. ローリングデプロイ**:
- インスタンスを1つずつ更新
- ゼロダウンタイムデプロイ
- リソース効率的

**GitOps**:

Git を Single Source of Truth として、インフラとアプリケーションを宣言的に管理。

**GitOps の原則**:
1. **宣言的記述**: あるべき状態をYAMLで定義
2. **Git as Single Source of Truth**: Git が唯一の真実
3. **自動適用**: Git の状態とクラスターの状態を自動同期
4. **継続的な調整**: ドリフトを自動検知・修正

#### 実用例

**例1: GitHub Actions CI/CDパイプライン (Node.js アプリケーション)**

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18.x'
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # CI ステージ
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: npm run lint
    
    - name: Run unit tests
      run: npm run test:unit
    
    - name: Run integration tests
      run: npm run test:integration
    
    - name: Code coverage
      run: npm run test:coverage
      
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
    
    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    
    - name: Build application
      run: npm run build
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-artifacts
        path: dist/

  # セキュリティスキャン
  security-scan:
    runs-on: ubuntu-latest
    needs: build-and-test
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  # Docker イメージビルド
  build-docker-image:
    runs-on: ubuntu-latest
    needs: [build-and-test, security-scan]
    if: github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to GitHub Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.DOCKER_REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
          type=semver,pattern={{version}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Scan Docker image with Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-image-results.sarif'

  # CD ステージ: Staging デプロイ
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-docker-image
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --name staging-cluster --region us-west-2
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/myapp \
          myapp=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n staging
        kubectl rollout status deployment/myapp -n staging --timeout=5m
    
    - name: Run smoke tests
      run: |
        curl -f https://staging.example.com/health || exit 1
        npm run test:e2e -- --baseUrl=https://staging.example.com

  # CD ステージ: Production デプロイ (承認必要)
  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment:
      name: production
      url: https://example.com
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --name production-cluster --region us-west-2
    
    - name: Blue-Green Deployment
      run: |
        # 新バージョンをgreen環境にデプロイ
        kubectl apply -f k8s/deployment-green.yaml
        kubectl set image deployment/myapp-green \
          myapp=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n production
        kubectl rollout status deployment/myapp-green -n production --timeout=10m
        
        # スモークテスト (green環境)
        kubectl port-forward svc/myapp-green 8080:80 -n production &
        sleep 5
        curl -f http://localhost:8080/health || exit 1
        
        # トラフィック切り替え (Serviceのselectorを変更)
        kubectl patch service myapp -n production \
          -p '{"spec":{"selector":{"version":"green"}}}'
        
        # 旧バージョン (blue) を削除
        kubectl delete deployment myapp-blue -n production || true
    
    - name: Post-deployment monitoring
      run: |
        echo "Monitoring deployment for 5 minutes..."
        # Prometheus メトリクスをチェック
        # エラー率が閾値を超えたらアラート
```

**例2: GitOps with ArgoCD (Kubernetes マニフェスト管理)**

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  
  # ソース: Gitリポジトリ
  source:
    repoURL: https://github.com/myorg/myapp-config.git
    targetRevision: HEAD
    path: k8s/overlays/production
    
    # Kustomize設定
    kustomize:
      namePrefix: prod-
      commonLabels:
        env: production
  
  # デプロイ先: Kubernetesクラスター
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  # 同期ポリシー
  syncPolicy:
    automated:
      prune: true      # 不要なリソースを自動削除
      selfHeal: true   # ドリフトを自動修正
      allowEmpty: false
    
    syncOptions:
    - CreateNamespace=true
    - PruneLast=true
    
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  # ヘルスチェック
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas  # HPA管理のため無視

---
# k8s/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
- ../../base

replicas:
- name: myapp
  count: 5

images:
- name: myapp
  newName: ghcr.io/myorg/myapp
  newTag: v1.2.3

configMapGenerator:
- name: myapp-config
  literals:
  - LOG_LEVEL=info
  - MAX_CONNECTIONS=100

secretGenerator:
- name: myapp-secrets
  envs:
  - secrets.env
```

**例3: カナリアリリース (Flagger + Istio)**

```yaml
# canary-deployment.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
  namespace: production
spec:
  # デプロイメント参照
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  
  # プログレッシブデリバリー設定
  progressDeadlineSeconds: 600
  
  service:
    port: 80
    targetPort: 8080
    gateways:
    - public-gateway
    hosts:
    - myapp.example.com
  
  # カナリア分析
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    
    metrics:
    # リクエスト成功率
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    
    # レイテンシー (p99)
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
    
    # カスタムメトリクス (Prometheus)
    - name: error-rate
      templateRef:
        name: error-rate
        namespace: flagger-system
      thresholdRange:
        max: 1
      interval: 1m
    
    # Webhookテスト
    webhooks:
    - name: load-test
      url: http://flagger-loadtester/
      timeout: 5s
      metadata:
        type: cmd
        cmd: "hey -z 1m -q 10 -c 2 http://myapp-canary.production:80/"
    
    - name: smoke-test
      url: http://flagger-loadtester/
      timeout: 15s
      metadata:
        type: cmd
        cmd: "curl -f http://myapp-canary.production:80/health"

# カナリアリリースの進行:
# 1. 0% → 10% → 20% → 30% → 40% → 50%
# 2. 各ステップで1分間メトリクスを監視
# 3. 閾値超過でロールバック、成功で次のステップへ
# 4. 50%到達後、問題なければ100%へ
```

#### 参考文献・リソース
- Martin Fowler, "Continuous Integration" (2006) - https://martinfowler.com/articles/continuousIntegration.html
- Jez Humble, David Farley, "Continuous Delivery" (Addison-Wesley, 2010)
- The DevOps Handbook (Gene Kim, et al., 2016)
- GitOps Principles - https://www.gitops.tech/

---

### 2. Infrastructure as Code (IaC)

#### 分類
- **インフラ自動化系**
- **宣言的インフラ管理**

#### 出典・背景
- **IaC概念**: 2000年代後半、クラウドコンピューティングの普及とともに登場
- **Terraform**: HashiCorp, Mitchell Hashimoto (2014)
- **背景**: 従来の手動によるインフラ構築は、再現性の欠如、設定ドリフト、スケーラビリティの制約という課題を抱えていました。Infrastructure as Codeは、インフラをコードとして管理することで、バージョン管理、自動化、再現性を実現します。

#### 理論の詳細

**IaCの原則**:

1. **宣言的定義**: あるべき状態を記述 (手順ではなく)
2. **バージョン管理**: Git でインフラコードを管理
3. **冪等性**: 何度実行しても同じ結果
4. **Immutable Infrastructure**: 変更ではなく再作成
5. **自己文書化**: コードがドキュメント

**IaCツールの比較**:

| ツール | アプローチ | 言語 | 対象 | 特徴 |
|--------|----------|------|------|------|
| Terraform | 宣言的 | HCL | マルチクラウド | 状態管理、プラン/適用分離 |
| Ansible | 手続き的 | YAML | 構成管理 | エージェントレス、シンプル |
| CloudFormation | 宣言的 | JSON/YAML | AWS専用 | ネイティブ統合、スタック管理 |
| Pulumi | 宣言的 | 汎用言語 | マルチクラウド | TypeScript/Python等で記述 |
| Chef | 手続き的 | Ruby DSL | 構成管理 | エージェント型、強力 |
| Puppet | 宣言的 | Puppet DSL | 構成管理 | エージェント型、成熟 |

**Terraformの核心概念**:

**1. プロバイダー (Provider)**: クラウドAPI接続
```hcl
provider "aws" {
  region = "us-west-2"
}
```

**2. リソース (Resource)**: インフラコンポーネント
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}
```

**3. データソース (Data Source)**: 既存リソース参照
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
}
```

**4. 変数 (Variables)**: パラメータ化
```hcl
variable "instance_type" {
  type    = string
  default = "t3.micro"
}
```

**5. 出力 (Outputs)**: 情報の公開
```hcl
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

**6. モジュール (Modules)**: 再利用可能なコンポーネント

**Terraformワークフロー**:

```
1. terraform init    # プロバイダープラグインのダウンロード
   ↓
2. terraform plan    # 変更のプレビュー（差分表示）
   ↓
3. terraform apply   # 変更の適用
   ↓
4. terraform destroy # リソースの削除
```

**状態管理 (State Management)**:

Terraformは `terraform.tfstate` ファイルで実際のインフラ状態を追跡。

**ベストプラクティス**:
- リモートステート (S3 + DynamoDB ロック)
- ステートファイルの暗号化
- バックアップ
- ワークスペース分離 (dev/staging/prod)

#### 実用例

**例1: Terraform マルチクラウドインフラ (AWS + GCP)**

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  
  # リモートステート (S3バックエンド)
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

# AWS プロバイダー
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}

# GCP プロバイダー
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-west1"
}

# modules/vpc/main.tf (再利用可能なVPCモジュール)
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.name_prefix}-vpc"
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.name_prefix}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "${var.name_prefix}-private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.name_prefix}-igw"
  }
}

resource "aws_nat_gateway" "main" {
  count         = length(var.public_subnet_cidrs)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name = "${var.name_prefix}-nat-${count.index + 1}"
  }
}

resource "aws_eip" "nat" {
  count  = length(var.public_subnet_cidrs)
  domain = "vpc"
  
  tags = {
    Name = "${var.name_prefix}-nat-eip-${count.index + 1}"
  }
}

# モジュール使用
module "vpc" {
  source = "./modules/vpc"
  
  name_prefix          = "myapp-${var.environment}"
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24"]
}

# EKS クラスター
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  
  cluster_name    = "myapp-${var.environment}"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  cluster_endpoint_public_access = true
  
  eks_managed_node_groups = {
    general = {
      min_size     = 2
      max_size     = 10
      desired_size = 3
      
      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
      
      labels = {
        role = "general"
      }
      
      tags = {
        NodeGroup = "general"
      }
    }
  }
  
  # IRSA (IAM Roles for Service Accounts) 有効化
  enable_irsa = true
}

# outputs.tf
output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "configure_kubectl" {
  description = "Configure kubectl command"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}
```

**例2: Ansible プレイブック (Webサーバー構成管理)**

```yaml
# playbook.yml
---
- name: Configure Web Servers
  hosts: webservers
  become: yes
  vars:
    nginx_version: "1.24"
    app_user: "webapp"
    app_directory: "/var/www/myapp"
  
  tasks:
  - name: Update apt cache
    apt:
      update_cache: yes
      cache_valid_time: 3600
  
  - name: Install required packages
    apt:
      name:
        - nginx
        - python3-pip
        - git
        - ufw
      state: present
  
  - name: Create application user
    user:
      name: "{{ app_user }}"
      shell: /bin/bash
      create_home: yes
  
  - name: Create application directory
    file:
      path: "{{ app_directory }}"
      state: directory
      owner: "{{ app_user }}"
      group: "{{ app_user }}"
      mode: '0755'
  
  - name: Configure firewall
    ufw:
      rule: allow
      port: "{{ item }}"
      proto: tcp
    loop:
      - '22'   # SSH
      - '80'   # HTTP
      - '443'  # HTTPS
  
  - name: Enable firewall
    ufw:
      state: enabled
  
  - name: Configure Nginx
    template:
      src: templates/nginx.conf.j2
      dest: /etc/nginx/sites-available/myapp
      owner: root
      group: root
      mode: '0644'
    notify: Restart Nginx
  
  - name: Enable Nginx site
    file:
      src: /etc/nginx/sites-available/myapp
      dest: /etc/nginx/sites-enabled/myapp
      state: link
    notify: Restart Nginx
  
  - name: Start and enable Nginx
    systemd:
      name: nginx
      state: started
      enabled: yes
  
  handlers:
  - name: Restart Nginx
    systemd:
      name: nginx
      state: restarted

# templates/nginx.conf.j2
server {
    listen 80;
    server_name {{ ansible_fqdn }};
    
    root {{ app_directory }}/public;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location /api {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    access_log /var/log/nginx/myapp_access.log;
    error_log /var/log/nginx/myapp_error.log;
}

# inventory.ini
[webservers]
web1.example.com ansible_host=192.168.1.10
web2.example.com ansible_host=192.168.1.11
web3.example.com ansible_host=192.168.1.12

[webservers:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

#### 参考文献・リソース
- HashiCorp, "Terraform: Up & Running" (O'Reilly, 2022)
- Kief Morris, "Infrastructure as Code" (O'Reilly, 2nd Edition, 2020)
- Terraform Documentation - https://developer.hashicorp.com/terraform/docs
- Ansible Documentation - https://docs.ansible.com/

---

### 3. Site Reliability Engineering (SRE)

#### 分類
- **信頼性エンジニアリング系**
- **運用の科学的アプローチ**

#### 出典・背景
- **提唱組織**: Google
- **出典**: Betsy Beyer, et al., "Site Reliability Engineering: How Google Runs Production Systems" (O'Reilly, 2016)
- **背景**: Googleが2003年頃に確立した、ソフトウェアエンジニアリングの原則を運用に適用する実践。Ben Treynor Slossが初代SREディレクター。従来の運用 (Ops) がスケールしない問題を、自動化とエンジニアリング文化で解決します。

#### 理論の詳細

**SREの核心原則**:

1. **Toil の最小化**: 手動作業を50%未満に
2. **エラーバジェット**: 信頼性と速度のバランス
3. **SLI/SLO/SLA**: 測定可能な信頼性目標
4. **自動化**: 手動作業の排除
5. **Blameless Postmortem**: 人ではなくシステムを改善
6. **段階的ロールアウト**: リスク管理

**SLI (Service Level Indicator)**:

サービスレベルの測定指標。

**主要なSLI**:
- **可用性 (Availability)**: 成功したリクエスト / 全リクエスト
- **レイテンシ (Latency)**: リクエスト応答時間のパーセンタイル (p50, p95, p99)
- **エラー率 (Error Rate)**: エラーレスポンス / 全リクエスト
- **スループット (Throughput)**: 単位時間あたりの処理量

**SLO (Service Level Objective)**:

SLIの目標値。内部目標。

**例**:
- 可用性: 99.9% (月間43.8分のダウンタイム許容)
- レイテンシ: p99 < 200ms
- エラー率: < 0.1%

**SLA (Service Level Agreement)**:

顧客との契約上の保証。SLOより緩い値を設定。

**例**:
- SLO: 99.9%、SLA: 99.5% (補償発生)

**エラーバジェット (Error Budget)**:

許容される障害の量。イノベーションの余地。

```
エラーバジェット = 100% - SLO

例: SLO 99.9% の場合
エラーバジェット = 0.1%
月間: 43.8分のダウンタイム
```

**エラーバジェットの活用**:
- **バジェット残あり**: 新機能リリース、リスクある変更OK
- **バジェット使い果たし**: 新機能凍結、安定性改善に集中

**Toilの定義と削減**:

**Toil**: 
- 手動
- 反復的
- 自動化可能
- 戦術的 (戦略的価値なし)
- O(n)でスケール (線形増加)

**Toil削減戦略**:
1. 自動化 (スクリプト、ツール)
2. セルフサービス化 (ユーザーが自分で実行)
3. プロセス改善
4. 製品改善 (根本原因の解消)

**目標**: Toil < 50%の時間

**On-Call体制**:

**ベストプラクティス**:
- ローテーション: 負担分散 (週単位)
- エスカレーションポリシー: 1次→2次→3次
- アラート品質: 実行可能、緊急、ノイズ削減
- Runbook: 対応手順書
- ポストモーテム: 障害から学ぶ

#### 実用例

**例1: SLI/SLO定義とPrometheusクエリ**

```yaml
# slo-definition.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: slo-definition
data:
  slo.yaml: |
    # サービスレベル目標定義
    service: myapp-api
    
    slos:
    # 可用性 SLO
    - name: availability
      objective: 99.9  # 99.9%
      description: "API availability measured by successful requests"
      sli:
        metric: availability
        query: |
          sum(rate(http_requests_total{job="myapp-api",code!~"5.."}[5m]))
          /
          sum(rate(http_requests_total{job="myapp-api"}[5m]))
      window: 30d  # 30日間のローリングウィンドウ
      
      error_budget:
        remaining_query: |
          1 - (
            (1 - (sum(rate(http_requests_total{code!~"5.."}[30d])) / sum(rate(http_requests_total[30d]))))
            / (1 - 0.999)
          )
    
    # レイテンシ SLO (p99 < 200ms)
    - name: latency
      objective: 0.99  # 99% of requests
      description: "99th percentile latency under 200ms"
      sli:
        metric: latency
        query: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{job="myapp-api"}[5m])) by (le)
          ) < 0.2
      window: 30d
    
    # エラー率 SLO (< 0.1%)
    - name: error_rate
      objective: 99.9
      description: "Error rate below 0.1%"
      sli:
        metric: error_rate
        query: |
          sum(rate(http_requests_total{job="myapp-api",code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{job="myapp-api"}[5m]))
      threshold: 0.001
      window: 30d

# Prometheus アラートルール
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-alerts
spec:
  groups:
  - name: slo-violations
    interval: 1m
    rules:
    # エラーバジェット消費速度アラート
    - alert: ErrorBudgetBurn
      expr: |
        (
          sum(rate(http_requests_total{job="myapp-api",code=~"5.."}[1h]))
          /
          sum(rate(http_requests_total{job="myapp-api"}[1h]))
        ) > (0.001 * 14.4)  # 0.1%の14.4倍 = 2%の1時間エラー率
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error budget burn rate"
        description: "Error budget will be exhausted in < 2 days at current rate"
    
    # SLO違反アラート
    - alert: SLOViolation
      expr: |
        (
          sum(rate(http_requests_total{job="myapp-api",code!~"5.."}[30d]))
          /
          sum(rate(http_requests_total{job="myapp-api"}[30d]))
        ) < 0.999
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "SLO availability target missed"
        description: "30-day availability is below 99.9% target"
    
    # レイテンシSLO違反
    - alert: LatencySLOViolation
      expr: |
        histogram_quantile(0.99,
          sum(rate(http_request_duration_seconds_bucket{job="myapp-api"}[5m])) by (le)
        ) > 0.2
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "p99 latency exceeds 200ms"
        description: "99th percentile latency is {{ $value }}s"

# Grafana ダッシュボード (JSON抜粋)
{
  "dashboard": {
    "title": "SLO Dashboard",
    "panels": [
      {
        "title": "30-Day Availability",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{code!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d]))"
          }
        ],
        "thresholds": [
          {"value": 0.999, "color": "green"},
          {"value": 0.995, "color": "yellow"},
          {"value": 0, "color": "red"}
        ]
      },
      {
        "title": "Error Budget Remaining",
        "targets": [
          {
            "expr": "1 - ((1 - (sum(rate(http_requests_total{code!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d])))) / (1 - 0.999))"
          }
        ]
      }
    ]
  }
}
```

**例2: Blameless Postmortem テンプレート**

```markdown
# インシデントポストモーテム

## 基本情報
- **インシデントID**: INC-2025-001
- **発生日時**: 2025-01-15 14:32 UTC
- **検知日時**: 2025-01-15 14:35 UTC
- **解決日時**: 2025-01-15 15:47 UTC
- **影響時間**: 1時間15分
- **重要度**: P1 (Critical)
- **担当SRE**: Alice, Bob

## エグゼクティブサマリー
API サービスで504 Gateway Timeout エラーが大量発生。
全リクエストの約30%が失敗し、月間エラーバジェットの40%を消費。
根本原因はデータベース接続プールの枯渇。

## 影響
- **ユーザー影響**: 約10,000ユーザーがサービス利用不可
- **エラー率**: 30% (通常0.1%)
- **エラーバジェット消費**: 40% (月間許容の40%を1時間で消費)
- **SLO違反**: 可用性SLO (99.9%) を下回る

## タイムライン
| 時刻 (UTC) | イベント | アクション |
|-----------|---------|----------|
| 14:32 | データベースレスポンス遅延開始 | - |
| 14:35 | PagerDuty アラート発火 | Alice が On-Call 対応開始 |
| 14:40 | 504エラー急増を確認 | Bob が合流、調査開始 |
| 14:50 | DB接続プール枯渇を特定 | 接続プールサイズ拡大を決定 |
| 15:00 | 接続プールサイズを50→200に変更 | Kubernetes Deployment更新 |
| 15:05 | 新Podがロールアウト完了 | モニタリング継続 |
| 15:15 | エラー率が正常化 (< 0.1%) | 継続監視 |
| 15:47 | インシデントクローズ宣言 | ポストモーテム作成開始 |

## 根本原因
新機能リリース (v2.3.0) で、各リクエストが平均2クエリ→5クエリに増加。
データベース接続プールサイズ (50) が不足し、接続待機によりタイムアウト。

**技術的詳細**:
- 接続プール設定: `maxConnections: 50, maxIdleTime: 30s`
- トラフィック: 500 req/s × 5 queries/req = 2500 DB queries/s
- 接続不足: 2500 queries/s ÷ 50 connections = 50 queries/connection/s
- クエリ実行時間: 平均100ms → 接続待機発生

## 検知と対応
### 何がうまく機能したか
- ✅ Prometheus アラートが3分以内に発火
- ✅ PagerDuty エスカレーションが正常動作
- ✅ Grafana ダッシュボードで迅速に原因特定
- ✅ Runbook に従った対応

### 何がうまく機能しなかったか
- ❌ ステージング環境でのロードテスト不足
- ❌ データベース接続プール監視が未実装
- ❌ 接続プール設定の自動スケーリング未実装

## アクションアイテム
| アクション | 担当者 | 期限 | 優先度 |
|----------|-------|------|-------|
| DB接続プール監視を追加 (Prometheus metrics) | Alice | 2025-01-20 | P0 |
| ステージング環境でのロードテストを必須化 | Bob | 2025-01-25 | P0 |
| 接続プール自動スケーリング実装 (HPA連動) | Charlie | 2025-02-01 | P1 |
| Runbook 更新 (DB接続プール対応) | Alice | 2025-01-18 | P1 |
| 新機能リリース前のDB影響分析チェックリスト作成 | David | 2025-01-30 | P2 |

## 学んだ教訓
1. **リソース容量計画の重要性**: クエリ数増加の影響を事前評価すべきだった
2. **可観測性のギャップ**: DB接続プール使用率の監視が欠如
3. **ロードテストの不足**: ステージングでの負荷テストでは検出できず

## 再発防止策
- データベース接続プール使用率のダッシュボード追加
- CI/CDパイプラインに性能回帰テスト組み込み
- リリース前のアーキテクチャレビュー必須化
```

**例3: カオスエンジニアリング実験 (Chaos Mesh)**

```yaml
# chaos-experiment.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-failure-experiment
  namespace: chaos-testing
spec:
  action: pod-failure
  mode: fixed-percent
  value: "20"  # 20% のPodを障害させる
  duration: "30s"
  
  selector:
    namespaces:
      - production
    labelSelectors:
      app: myapp
  
  scheduler:
    cron: "@every 1h"  # 1時間ごとに実行

---
# ネットワーク遅延実験
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay-experiment
spec:
  action: delay
  mode: all
  
  selector:
    namespaces:
      - production
    labelSelectors:
      app: myapp
  
  delay:
    latency: "100ms"
    correlation: "50"
    jitter: "10ms"
  
  duration: "5m"
```

#### 参考文献・リソース
- Betsy Beyer, et al., "Site Reliability Engineering" (O'Reilly, 2016)
- Betsy Beyer, et al., "The Site Reliability Workbook" (O'Reilly, 2018)
- Alex Hidalgo, "Implementing Service Level Objectives" (O'Reilly, 2020)
- Google SRE Books - https://sre.google/books/

---

### 4. 可観測性 (Observability)

#### 分類
- **監視・診断系**
- **システム理解の3本柱**

#### 出典・背景
- **可観測性概念**: 制御理論から派生 (Rudolf Kalman, 1960年代)
- **現代の適用**: Charity Majors, Liz Fong-Jones, George Miranda
- **出典**: "Observability Engineering" (O'Reilly, 2022)
- **背景**: マイクロサービス、分散システムの普及により、従来の監視 (既知の障害を検知) では不十分に。可観測性は「システムの内部状態を外部出力から推測できる能力」を指します。

#### 理論の詳細

**可観測性の3本柱 (Three Pillars of Observability)**:

**1. メトリクス (Metrics)**:
- 定義: 時系列の数値データ
- 特徴: 集約可能、低コスト、長期保存
- 用途: システム状態の概観、アラート
- 例: CPU使用率、リクエスト数、エラー率

**2. ログ (Logs)**:
- 定義: イベントの詳細記録
- 特徴: 構造化/非構造化、高コスト
- 用途: 詳細調査、デバッグ
- 例: アプリケーションログ、エラーログ、監査ログ

**3. トレース (Traces)**:
- 定義: リクエストのエンドツーエンド経路
- 特徴: 分散システムの可視化
- 用途: パフォーマンス分析、依存関係理解
- 例: マイクロサービス間の呼び出しチェーン

**メトリクスパターン**:

**RED Method** (リクエスト駆動サービス):
- **Rate**: リクエスト数 (req/s)
- **Errors**: エラー数・率
- **Duration**: レイテンシ (p50, p95, p99)

**USE Method** (リソース駆動システム):
- **Utilization**: 使用率 (%)
- **Saturation**: 飽和度 (キュー長)
- **Errors**: エラー数

**Four Golden Signals** (Google SRE):
- Latency (レイテンシ)
- Traffic (トラフィック)
- Errors (エラー)
- Saturation (飽和)

**構造化ログ**:

JSON形式でログを出力し、検索・集計を容易にします。

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "error",
  "service": "order-service",
  "trace_id": "a1b2c3d4e5f6",
  "span_id": "f6e5d4c3b2a1",
  "user_id": "12345",
  "message": "Failed to process order",
  "error": {
    "type": "DatabaseConnectionError",
    "message": "Connection timeout",
    "stack_trace": "..."
  },
  "context": {
    "order_id": "ORD-98765",
    "payment_method": "credit_card"
  }
}
```

**分散トレーシングの構成要素**:

- **Trace**: 1つのリクエストの全体
- **Span**: Trace内の1つの操作 (例: DBクエリ)
- **Context Propagation**: Trace IDをサービス間で伝播

```
Trace: ユーザーが注文を作成

Frontend (100ms)
  ├─ API Gateway (50ms)
  │   ├─ Order Service (30ms)
  │   │   ├─ DB Query: Insert Order (10ms)
  │   │   └─ DB Query: Update Inventory (5ms)
  │   └─ Payment Service (20ms)
  │       └─ External API: Stripe (15ms)
  └─ Notification Service (10ms)
      └─ Send Email (8ms)
```

#### 実用例

**例1: Prometheus + Grafana スタック構築**

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
      external_labels:
        cluster: 'production'
        region: 'us-west-2'
    
    # アラートマネージャー設定
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093
    
    # アラートルール読み込み
    rule_files:
    - /etc/prometheus/rules/*.yml
    
    # スクレイプ設定
    scrape_configs:
    # Kubernetes APIサーバー
    - job_name: 'kubernetes-apiservers'
      kubernetes_sd_configs:
      - role: endpoints
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https
    
    # Kubernetes Nodes
    - job_name: 'kubernetes-nodes'
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - target_label: __address__
        replacement: kubernetes.default.svc:443
      - source_labels: [__meta_kubernetes_node_name]
        regex: (.+)
        target_label: __metrics_path__
        replacement: /api/v1/nodes/${1}/proxy/metrics
    
    # Kubernetes Pods (アプリケーションメトリクス)
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name

---
# アプリケーション Deployment (Prometheusメトリクス公開)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: OTEL_EXPORTER_PROMETHEUS_PORT
          value: "8080"

---
# Grafana ダッシュボード (ConfigMap)
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-myapp
data:
  myapp-dashboard.json: |
    {
      "dashboard": {
        "title": "MyApp Metrics",
        "panels": [
          {
            "title": "Request Rate (req/s)",
            "targets": [{
              "expr": "sum(rate(http_requests_total{job=\"myapp\"}[5m]))"
            }]
          },
          {
            "title": "Error Rate (%)",
            "targets": [{
              "expr": "sum(rate(http_requests_total{job=\"myapp\",code=~\"5..\"}[5m])) / sum(rate(http_requests_total{job=\"myapp\"}[5m])) * 100"
            }]
          },
          {
            "title": "Request Duration (p50, p95, p99)",
            "targets": [
              {"expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))", "legendFormat": "p50"},
              {"expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))", "legendFormat": "p95"},
              {"expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))", "legendFormat": "p99"}
            ]
          }
        ]
      }
    }
```

**例2: 分散トレーシング (OpenTelemetry + Jaeger)**

```python
# Python アプリケーション: OpenTelemetry 計装
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from flask import Flask
import requests

# トレーサー設定
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Jaeger エクスポーター
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

app = Flask(__name__)

# 自動計装
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route('/api/orders', methods=['POST'])
def create_order():
    # カスタムスパン作成
    with tracer.start_as_current_span("create_order") as span:
        # スパン属性追加
        span.set_attribute("user_id", "12345")
        span.set_attribute("order_total", 99.99)
        
        # データベース操作 (自動計装)
        order_id = save_order_to_db()
        span.set_attribute("order_id", order_id)
        
        # 外部サービス呼び出し (自動計装)
        try:
            payment_result = process_payment(order_id)
            span.set_attribute("payment_status", "success")
        except Exception as e:
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            span.record_exception(e)
            raise
        
        # 通知送信
        send_notification(order_id)
        
        return {"order_id": order_id, "status": "created"}

def process_payment(order_id):
    # 新しいスパン作成
    with tracer.start_as_current_span("process_payment") as span:
        span.set_attribute("payment_provider", "stripe")
        
        # Stripe API呼び出し (自動計装されたrequests)
        response = requests.post(
            "https://api.stripe.com/v1/charges",
            data={"amount": 9999, "currency": "usd"}
        )
        
        return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

```yaml
# Jaeger デプロイ (Kubernetes)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:1.50
        env:
        - name: COLLECTOR_ZIPKIN_HOST_PORT
          value: ":9411"
        - name: COLLECTOR_OTLP_ENABLED
          value: "true"
        ports:
        - containerPort: 5775
          protocol: UDP
        - containerPort: 6831
          protocol: UDP
        - containerPort: 6832
          protocol: UDP
        - containerPort: 5778
          protocol: TCP
        - containerPort: 16686
          protocol: TCP  # Jaeger UI
        - containerPort: 14250
          protocol: TCP
        - containerPort: 14268
          protocol: TCP
        - containerPort: 14269
          protocol: TCP
        - containerPort: 9411
          protocol: TCP
        - containerPort: 4317
          protocol: TCP  # OTLP gRPC
        - containerPort: 4318
          protocol: TCP  # OTLP HTTP
```

#### 参考文献・リソース
- Charity Majors, et al., "Observability Engineering" (O'Reilly, 2022)
- Brendan Gregg, "Systems Performance" (Pearson, 2nd Edition, 2020)
- Prometheus Documentation - https://prometheus.io/docs/
- OpenTelemetry - https://opentelemetry.io/

---

## DevOps戦略選択ガイド

| DevOps目標 | 推奨フレームワーク（優先順） | 適用場面 |
|-----------|---------------------------|---------|
| **デプロイ自動化** | CI/CD → GitOps → カナリアリリース | 全プロジェクト、頻繁なリリース |
| **インフラ自動化** | Terraform → Kubernetes → Helm | クラウド環境、マイクロサービス |
| **信頼性向上** | SRE (SLI/SLO/SLA) → エラーバジェット → ポストモーテム | プロダクション、ミッションクリティカル |
| **可視化強化** | 可観測性 (Prometheus + Grafana) → 分散トレーシング → ログ集約 | 複雑なシステム、マイクロサービス |
| **コンテナ化** | Docker → Kubernetes → Service Mesh | モダンアプリケーション |

---

## 統合的な活用例: マイクロサービスの包括的DevOps実装

### レイヤー1: コード管理・CI
- **GitOps**: Git as Single Source of Truth
- **GitHub Actions**: 自動ビルド・テスト・セキュリティスキャン

### レイヤー2: インフラ自動化
- **Terraform**: VPC、EKS、RDS のプロビジョニング
- **Kubernetes**: コンテナオーケストレーション
- **Helm**: アプリケーションパッケージ管理

### レイヤー3: デプロイ自動化
- **ArgoCD**: Kubernetes マニフェストの自動同期
- **Flagger**: カナリアリリース

### レイヤー4: 可観測性
- **Prometheus**: メトリクス収集
- **Grafana**: ダッシュボード
- **Jaeger**: 分散トレーシング
- **ELK**: ログ集約

### レイヤー5: SRE実践
- **SLI/SLO定義**: 可用性99.9%、p99レイテンシ<200ms
- **エラーバジェット**: 新機能リリースとのバランス
- **On-Call体制**: インシデント対応

---

## 参考資料

### 書籍
1. "The DevOps Handbook" (Gene Kim, et al., 2016)
2. "Site Reliability Engineering" (Betsy Beyer, et al., 2016)
3. "Continuous Delivery" (Jez Humble, David Farley, 2010)
4. "Infrastructure as Code" (Kief Morris, 2020)
5. "Observability Engineering" (Charity Majors, et al., 2022)

### オンラインリソース
- Kubernetes Documentation: https://kubernetes.io/docs/
- Terraform Documentation: https://developer.hashicorp.com/terraform
- Prometheus Documentation: https://prometheus.io/docs/
- Google SRE Books: https://sre.google/books/

---

## まとめ

DevOpsは、開発と運用の壁を打破し、高速で信頼性の高いソフトウェアデリバリーを実現する文化と実践の集合体です。本ドキュメントで紹介した4つのフレームワーク——CI/CD、Infrastructure as Code、SRE、可観測性——は、現代のDevOps実践の基盤です。

- **CI/CD**で高速かつ安全なデプロイメント
- **IaC**でインフラの再現性と自動化
- **SRE**で信頼性とイノベーションのバランス
- **可観測性**でシステムの深い理解

これらを組み合わせ、段階的に導入し、継続的に改善することが重要です。
