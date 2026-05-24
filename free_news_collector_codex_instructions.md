# Codex開発指示書：無料情報ソース対応 マクロ・地政学ニュース収集要約アプリ

## 1. 開発目的

無料で取得できる公開情報のみを使い、以下の情報を自動収集・整理・要約するWebアプリを開発する。

対象テーマは以下。

- イラン・中東情勢
- 要人発言
- FRBの動向
- 米国経済の動向
- 為替市場
- 債券市場
- 株式市場
- 経済指標
- 原油・エネルギー

アプリは、外出先からでもスマートフォン・PCで閲覧できるようにする。初期リリースでは無料運用を最優先し、GitHub Pagesを第一候補、Google AI Studio / Google Cloud系の無料枠を第二候補として検討する。

## 2. 重要な前提

このアプリは投資判断を自動化するものではない。公開情報を収集し、要約・分類・重要度判定を行い、判断材料として提示する。

売買推奨、確定的な相場予測、投資助言は行わない。

ChatGPT Plusは、Codexによる開発支援、設計レビュー、手動分析、プロンプト改善に使う。ChatGPT Plus契約だけではOpenAI APIを無料で自動実行できるわけではないため、アプリのバックエンド処理には原則使わない。

Gemini APIは無料枠を使える可能性があるが、モデル別・地域別・時期別にクォータが変わるため、必ずAPI利用量を制御する。無料運用を維持するため、Gemini APIを使う場合は要約対象件数、実行回数、トークン量を制限する。

GitHub Pagesは静的ホスティングである。秘密情報を安全に保持できるサーバーではないため、APIキーをフロントエンドに直接埋め込んではならない。

## 3. 推奨アーキテクチャ

初期リリースでは以下を採用する。

```text
GitHub Actions
  ↓ 定期実行
Python collector
  ↓ API/RSS/Web取得
JSONデータ生成
  ↓
GitHubリポジトリに保存
  ↓
GitHub Pages
  ↓
React / Vite SPAで表示
```

この方式を第一候補とする理由は、無料運用しやすく、GitHub Pagesでどこからでも閲覧でき、GitHub Actionsにより定期実行が可能で、APIキーをGitHub Secretsに保存できるためである。

## 4. Google AI Studio案の位置づけ

Google AI Studioは、プロトタイプ作成やGemini連携アプリの試作に使う。特にGemini APIを使った要約UI、質問応答UI、レポート生成UIの試作に向いている。

ただし、初期版の本番運用先としてはGitHub Pagesを優先する。理由は以下。

- GitHub Pagesは静的サイトとして無料運用しやすい
- データ更新はGitHub Actionsで完結できる
- Gemini APIキーをクライアント側に露出せずに済む
- 収集済みJSONを表示するだけならバックエンドが不要
- 無料運用時の予期せぬ課金リスクを抑えやすい

Google AI Studio / Cloud Run / Firebase Hostingを使う場合は、APIキーの管理、課金設定、公開範囲、認証、無料枠超過時の挙動を別途確認すること。

## 5. 初期版のスコープ

### 5.1 必須機能

- 無料公開ソースからニュース・データを定期取得する
- 取得データをJSON形式で保存する
- 最新ニュース一覧をWeb画面で表示する
- テーマ別に分類して表示する
- 重要度A/B/Cを表示する
- ソースURL、公開日時、取得日時を表示する
- 1日分のサマリーを自動生成する
- スマートフォンで見やすい画面にする

### 5.2 初期版でやらないこと

- 有料ニュースAPIの利用
- リアルタイム株価配信
- 売買シグナル生成
- 自動売買
- ユーザー認証
- 複雑なDB運用
- 高頻度スクレイピング
- APIキーをブラウザに埋め込む実装

## 6. データソース一覧

### 6.1 地政学・イラン・中東情勢

| ソース | 用途 | 取得方法 | 優先度 |
|---|---|---|---|
| GDELT | 世界ニュース横断監視、イラン・イスラエル・ホルムズ海峡関連ニュース | API | A |
| ACLED | 紛争イベント、政治暴力イベント、抗議、発生日、場所、当事者 | API / Data Export | A |
| U.S. Department of State | 外交声明、制裁、中東関連発言 | RSS / Web | B |
| White House | 大統領発言、声明、ファクトシート | Web / RSS相当 | B |
| U.S. Treasury / OFAC | 制裁、財務省発表、金融制裁 | RSS / Web | B |
| IAEA | イラン核関連、査察、声明 | Web / RSS相当 | B |
| UN Press / Security Council | 安保理、国連声明 | Web / RSS相当 | C |

### 6.2 FRB・金融政策

| ソース | 用途 | 取得方法 | 優先度 |
|---|---|---|---|
| FRB Feeds | FRBニュース、スピーチ、証言、プレスリリース、統計 | RSS | A |
| FRB FOMCページ | FOMC声明、議事要旨、カレンダー、政策決定 | Web | A |
| FRB H.15 | 政策金利、米国債利回り、各種金利 | Data / RSS / FRED | A |
| FRB H.10 | 為替レート | Data / RSS / FRED | A |
| FRED | FRB関連指標、政策金利、金利系列、金融環境 | API | A |

### 6.3 米国経済指標

| ソース | 用途 | 取得方法 | 優先度 |
|---|---|---|---|
| FRED | マクロ経済時系列全般 | API | A |
| BLS API | CPI、PPI、雇用統計、失業率、平均時給、JOLTS | API | A |
| BEA API | GDP、PCE、個人所得、個人消費 | API | A |
| Census API | 小売売上、住宅着工、建設支出、貿易統計 | API | B |
| University of Michigan / FRED | 消費者信頼感、期待インフレ | FRED / Web | B |

### 6.4 市場データ

| ソース | 用途 | 取得方法 | 優先度 |
|---|---|---|---|
| FRED | S&P500、VIX、一部為替・金利・商品関連系列 | API | A |
| FRB H.15 | 米2年債、10年債、30年債、利回り曲線 | Data / RSS / FRED | A |
| FRB H.10 | 為替レート | Data / RSS / FRED | A |
| EIA Open Data | 原油、天然ガス、在庫、需給、エネルギー価格 | API | A |
| Alpha Vantage | 株価指数、FX、商品データの補助 | API無料枠 | B |

## 7. データ取得方針

### 7.1 取得頻度

| 対象 | 取得頻度 |
|---|---|
| GDELTニュース | 1〜3時間ごと |
| FRB RSS | 3〜6時間ごと |
| State / Treasury / White House | 3〜6時間ごと |
| FRED / BLS / BEA / Census | 1日1回、重要指標日は追加取得 |
| FRB H.15 / H.10 | 1日1回 |
| EIA | 1日1回、在庫発表日は追加取得 |
| ACLED | 1日1回 |
| Alpha Vantage | 1日1回、無料枠内 |

### 7.2 収集キーワード

初期版では以下のキーワードを使用する。

```text
Iran
Israel
Middle East
Strait of Hormuz
Hormuz
Tehran
nuclear facility
IAEA
sanctions
missile attack
oil supply
ceasefire
retaliation
Federal Reserve
FOMC
Jerome Powell
inflation
rate cut
rate hike
Treasury yield
USD JPY
S&P 500
Nasdaq
VIX
WTI
Brent
```

日本語表示用には以下の分類ラベルを使う。

```text
イラン・中東情勢
要人発言
FRB
米国経済
為替
債券
株式
原油・エネルギー
経済指標
その他
```

## 8. データモデル

### 8.1 news_items.json

ニュース・発言・公式発表は以下の形式で保存する。

```json
{
  "generated_at": "2026-05-24T07:00:00+09:00",
  "items": [
    {
      "id": "sha256_hash",
      "source": "GDELT",
      "source_type": "news_api",
      "title": "...",
      "summary": "...",
      "url": "https://...",
      "published_at": "2026-05-23T22:10:00Z",
      "fetched_at": "2026-05-24T07:00:00+09:00",
      "language": "en",
      "country": "US",
      "category": "イラン・中東情勢",
      "importance": "A",
      "confidence": "medium",
      "market_impact": {
        "fx": "ドル円はリスク回避の円買いとドル買いが交錯する可能性",
        "bonds": "米国債はリスク回避で買われる可能性",
        "stocks": "株式にはリスクオフ圧力",
        "commodities": "原油・金には上昇圧力"
      },
      "tags": ["Iran", "Middle East", "oil"]
    }
  ]
}
```

### 8.2 market_snapshot.json

市場データは以下の形式で保存する。

```json
{
  "generated_at": "2026-05-24T07:00:00+09:00",
  "items": [
    {
      "symbol": "DGS10",
      "name": "米10年債利回り",
      "source": "FRED",
      "value": 4.45,
      "unit": "%",
      "date": "2026-05-23",
      "change_1d": 0.05,
      "category": "債券"
    }
  ]
}
```

### 8.3 daily_report.json

日次レポートは以下の形式で保存する。

```json
{
  "date": "2026-05-24",
  "generated_at": "2026-05-24T07:05:00+09:00",
  "headline": "中東情勢と米金利が市場の主な焦点",
  "executive_summary": "...",
  "sections": [
    {
      "title": "イラン・中東情勢",
      "summary": "...",
      "importance": "A",
      "source_item_ids": ["..."]
    },
    {
      "title": "FRB動向",
      "summary": "...",
      "importance": "B",
      "source_item_ids": ["..."]
    }
  ],
  "watch_points": [
    "米10年債利回りの変化",
    "原油価格の反応",
    "FRB高官発言"
  ]
}
```

## 9. 重要度判定ロジック

初期版ではルールベースで重要度を判定する。AI判定は補助扱いとする。

### 9.1 重要度A

以下のいずれかに該当する場合は重要度A。

- イラン、イスラエル、米国、ホルムズ海峡、核施設、制裁、報復、停戦に関する重大ニュース
- FRB議長、FOMC声明、FOMC議事要旨、政策金利に関するニュース
- CPI、PCE、雇用統計、GDP、小売売上など主要指標の発表
- 米10年債利回りが前日比10bp以上変化
- USD/JPYが前日比1%以上変化
- S&P500またはNasdaqが前日比1.5%以上変化
- WTIまたはBrentが前日比2%以上変化

### 9.2 重要度B

- FRB高官発言
- 米政府・財務省・国務省の中東関連声明
- 原油在庫、EIA関連データ
- 中東情勢の続報
- 米国経済指標の予想比乖離

### 9.3 重要度C

- 通常の周辺ニュース
- 既報の焼き直し
- 市場影響が限定的なコメント

## 10. AI要約方針

無料運用を重視するため、AI要約は必須処理ではなく拡張処理とする。

初期版では以下の優先順位で実装する。

1. ルールベース分類・テンプレート要約
2. Gemini API無料枠による重要ニュースのみの要約
3. Local LLM / Ollamaによるローカル要約
4. 手動でChatGPT Plusへ貼り付けて詳細分析

### 10.1 Gemini APIを使う場合の制限

- 重要度Aのみ要約対象にする
- 1回の実行で最大20件まで
- 同一URLは再要約しない
- 要約結果をキャッシュする
- API失敗時もアプリ表示は継続する
- APIキーはGitHub Secretsに保存する
- フロントエンドにAPIキーを出さない

### 10.2 要約プロンプト

```text
あなたはマクロ経済・地政学リスクのアナリストです。
以下の公開情報を日本語で要約してください。

条件：
- 事実と推測を分ける
- 投資助言ではなく、判断材料として書く
- 市場への影響は仮説として書く
- 為替、債券、株式、原油への影響を簡潔に整理する
- 不明点は不明と書く
- 誇張しない

出力JSON：
{
  "summary": "...",
  "facts": ["..."],
  "uncertain_points": ["..."],
  "market_impact": {
    "fx": "...",
    "bonds": "...",
    "stocks": "...",
    "commodities": "..."
  },
  "importance_reason": "..."
}

入力：
{input}
```

## 11. 画面仕様

### 11.1 画面一覧

初期版は1つのSPAでよい。

- ダッシュボード
- ニュース一覧
- 市場データ
- 日次レポート
- ソース一覧
- 設定表示

### 11.2 ダッシュボード

表示項目。

- 今日の総括
- 重要度Aニュース
- イラン・中東情勢
- FRB動向
- 為替・債券・株式・原油のスナップショット
- 今日・今週の注目点
- 最終更新時刻

### 11.3 ニュース一覧

機能。

- カテゴリフィルタ
- 重要度フィルタ
- キーワード検索
- ソース表示
- 公開日時順ソート
- URLを新規タブで開く

### 11.4 市場データ

表示項目。

- USD/JPY
- DXY相当データが取得できる場合は表示
- 米2年債利回り
- 米10年債利回り
- 米30年債利回り
- S&P500
- Nasdaq
- VIX
- WTI
- Brent
- Gold

無料で取得できない項目は「未取得」と表示し、アプリを落とさない。

## 12. 技術スタック

### 12.1 フロントエンド

- React
- TypeScript
- Vite
- Tailwind CSS
- Recharts
- date-fns

### 12.2 データ収集

- Python 3.11以上
- requests
- feedparser
- pandas
- pydantic
- python-dateutil
- beautifulsoup4

### 12.3 CI/CD

- GitHub Actions
- GitHub Pages

### 12.4 任意

- Gemini API
- Ollama
- Google Apps Script

## 13. ディレクトリ構成

```text
macro-geopolitical-brief/
  README.md
  package.json
  vite.config.ts
  index.html
  src/
    App.tsx
    main.tsx
    components/
      Dashboard.tsx
      NewsList.tsx
      MarketSnapshot.tsx
      DailyReport.tsx
      SourceBadge.tsx
      ImportanceBadge.tsx
    lib/
      types.ts
      format.ts
      filters.ts
  public/
    data/
      news_items.json
      market_snapshot.json
      daily_report.json
      sources.json
  collector/
    requirements.txt
    main.py
    config.py
    models.py
    sources/
      gdelt.py
      acled.py
      frb.py
      fred.py
      bls.py
      bea.py
      census.py
      eia.py
      us_state.py
      us_treasury.py
      whitehouse.py
      alpha_vantage.py
    processing/
      classify.py
      dedupe.py
      importance.py
      summarize.py
      report.py
    tests/
      test_classify.py
      test_dedupe.py
      test_importance.py
  .github/
    workflows/
      collect.yml
      deploy.yml
```

## 14. GitHub Actions仕様

### 14.1 collect.yml

目的：定期的にデータを取得し、public/data配下のJSONを更新する。

実行タイミング。

```yaml
on:
  schedule:
    - cron: '0 22 * * *'   # JST 07:00
    - cron: '0 4 * * *'    # JST 13:00
    - cron: '0 10 * * *'   # JST 19:00
  workflow_dispatch:
```

処理内容。

1. Pythonセットアップ
2. 依存関係インストール
3. collector/main.pyを実行
4. public/data/*.jsonを更新
5. 変更があればコミット
6. deployワークフローまたはGitHub Pagesビルドを実行

### 14.2 deploy.yml

目的：ReactアプリをGitHub Pagesへデプロイする。

実行タイミング。

- mainブランチへのpush
- workflow_dispatch

## 15. 環境変数・Secrets

GitHub Secretsに保存する候補。

```text
FRED_API_KEY
BEA_API_KEY
EIA_API_KEY
ALPHA_VANTAGE_API_KEY
ACLED_API_KEY
ACLED_EMAIL
GEMINI_API_KEY
```

必須にするのは最小限にする。キーが未設定のソースはスキップし、アプリ全体は正常終了させる。

## 16. ソース別実装指示

### 16.1 GDELT

- APIで指定キーワードのニュースを取得する
- イラン、中東、ホルムズ海峡、核施設、制裁関連を対象にする
- title、url、published_at、source_country、languageを保存する
- 同じURLは重複排除する

### 16.2 FRB RSS

- FRB公式RSSからスピーチ、証言、プレスリリース、統計更新を取得する
- Powell、FOMC、inflation、employment、rate、balance sheetを含むものを優先する
- FRB関連は一次情報として重要度を高める

### 16.3 FRED

初期取得系列候補。

```text
DGS2      米2年債利回り
DGS10     米10年債利回り
DGS30     米30年債利回り
FEDFUNDS  FF金利
CPIAUCSL  CPI
PCEPI     PCE価格指数
UNRATE    失業率
PAYEMS    非農業部門雇用者数
SP500     S&P500
VIXCLS    VIX
DEXJPUS   USD/JPY
DCOILWTICO WTI原油
```

### 16.4 BLS

初期取得系列候補。

```text
CUSR0000SA0     CPI All Urban Consumers
CES0000000001   Nonfarm Payrolls
LNS14000000     Unemployment Rate
CES0500000003   Average Hourly Earnings
```

### 16.5 BEA

- GDP
- PCE
- Personal Income
- Personal Consumption Expenditures

初期版ではFRED経由で代替できる系列はFREDを優先してもよい。

### 16.6 EIA

- WTI
- Brent
- 原油在庫
- ガソリン在庫
- 天然ガス在庫

初期版ではWTIとBrentだけでもよい。

### 16.7 Alpha Vantage

無料枠制限があるため、初期版では以下だけ取得する。

- USD/JPY
- NASDAQまたはQQQ
- SPY
- GLD
- USO

取得頻度は1日1回に制限する。

## 17. エラー処理

- ソース単位でtry/exceptする
- 1つのソースが失敗しても全体を止めない
- エラー内容はlogs/latest.jsonに保存する
- フロントエンドでは「一部ソース取得失敗」と表示する
- APIキー未設定はエラーではなくスキップ扱いにする
- rate limit時は再試行しすぎない

## 18. 重複排除

以下の順で重複を排除する。

1. URL完全一致
2. タイトル正規化後一致
3. タイトル類似度
4. 同一ソース・同一公開時刻・同一タイトル

idは以下から生成する。

```text
sha256(source + normalized_title + published_at + url)
```

## 19. 分類ロジック

初期版ではキーワードベースで分類する。

```text
Iran, Israel, Hormuz, missile, nuclear, sanctions → イラン・中東情勢
FOMC, Federal Reserve, Powell, rate cut, rate hike → FRB
CPI, PCE, GDP, payrolls, unemployment, retail sales → 経済指標
Treasury yield, bond, 10-year, 2-year → 債券
USD, JPY, currency, exchange rate → 為替
S&P, Nasdaq, Dow, equities, stocks → 株式
WTI, Brent, oil, gas, EIA → 原油・エネルギー
White House, Treasury, State Department, remarks, speech → 要人発言
```

## 20. セキュリティ要件

- APIキーをフロントエンドに出さない
- public/dataに秘密情報を保存しない
- GitHub Secretsを使う
- 取得元URLと公開日時を必ず保存する
- 生成AI要約には根拠URLを紐づける
- 不明確な情報を断定しない
- Webスクレイピングは利用規約を尊重する

## 21. READMEに記載する内容

READMEには以下を記載する。

- アプリ概要
- 無料運用前提の制約
- 対象情報
- 使用データソース
- セットアップ手順
- GitHub Secrets設定
- ローカル実行方法
- GitHub Pagesデプロイ方法
- GitHub Actionsの手動実行方法
- データ更新頻度
- 免責事項

## 22. Codexへの実装タスク分解

Codexには一度に全部作らせず、以下の順で依頼する。

### Task 1：プロジェクト雛形作成

依頼内容。

```text
React + TypeScript + Vite + Tailwind CSSのSPAを作成してください。
GitHub Pagesで配信できる構成にしてください。
public/data配下のJSONを読み込んで、ダッシュボード、ニュース一覧、市場データ、日次レポートを表示する最小実装を作ってください。
まだ実データ取得は不要です。サンプルJSONを作ってください。
```

受け入れ条件。

- npm install / npm run devで起動する
- npm run buildが成功する
- スマホ表示で崩れない
- public/data/*.jsonを読み込む

### Task 2：データモデルとサンプルデータ

依頼内容。

```text
news_items.json、market_snapshot.json、daily_report.json、sources.jsonのスキーマをTypeScript型とPython pydanticモデルで定義してください。
サンプルデータも作成してください。
```

受け入れ条件。

- TypeScript型がsrc/lib/types.tsにある
- Pythonモデルがcollector/models.pyにある
- JSON構造が一致している

### Task 3：GDELT collector

依頼内容。

```text
collector/sources/gdelt.pyを実装してください。
GDELTからIran、Israel、Hormuz、sanctions、nuclear関連ニュースを取得し、標準NewsItem形式に変換してください。
重複排除とエラー処理も実装してください。
```

受け入れ条件。

- API失敗時に全体が落ちない
- NewsItem形式で返る
- URL重複が排除される

### Task 4：FRB RSS collector

依頼内容。

```text
FRB公式RSSを取得するcollector/sources/frb.pyを実装してください。
スピーチ、証言、プレスリリース、FOMC関連を取得してNewsItem形式にしてください。
```

受け入れ条件。

- RSS取得できる
- FRBカテゴリに分類される
- Powell、FOMC、inflationなどは重要度が上がる

### Task 5：FRED market collector

依頼内容。

```text
FRED APIからDGS2、DGS10、DGS30、FEDFUNDS、SP500、VIXCLS、DEXJPUS、DCOILWTICOを取得し、market_snapshot.jsonを生成してください。
APIキーがない場合はスキップしてください。
```

受け入れ条件。

- FRED_API_KEY未設定でも落ちない
- 取得成功時はmarket_snapshot.jsonに反映される
- 前日比を計算する

### Task 6：分類・重要度判定

依頼内容。

```text
collector/processing/classify.pyとimportance.pyを実装してください。
キーワードベースでカテゴリ分類し、ルールベースで重要度A/B/Cを判定してください。
```

受け入れ条件。

- 主要カテゴリに分類される
- 重要度A/B/Cが付く
- テストがある

### Task 7：日次レポート生成

依頼内容。

```text
取得済みnews_items.jsonとmarket_snapshot.jsonからdaily_report.jsonを生成してください。
AI APIを使わず、テンプレートベースで日次サマリーを生成してください。
```

受け入れ条件。

- 重要度Aを優先して要約する
- セクション別に整理する
- watch_pointsを出す

### Task 8：GitHub Actions

依頼内容。

```text
collect.ymlとdeploy.ymlを作成してください。
collect.ymlは1日3回と手動実行でcollectorを動かし、JSONが変わった場合だけcommitしてください。
deploy.ymlはmainブランチ更新時にGitHub PagesへReactアプリをデプロイしてください。
```

受け入れ条件。

- workflow_dispatchで手動実行できる
- Secrets未設定でも失敗しない
- GitHub Pagesにデプロイできる

### Task 9：Gemini要約オプション

依頼内容。

```text
GEMINI_API_KEYが設定されている場合だけ、重要度Aニュースに対してGemini APIで日本語要約を生成するsummarize.pyを実装してください。
同一URLは再要約しないキャッシュを実装してください。
APIキーがない場合はテンプレート要約にフォールバックしてください。
```

受け入れ条件。

- APIキー未設定で正常動作する
- API失敗時にテンプレート要約へ戻る
- public/dataにAPIキーが含まれない

### Task 10：UI改善

依頼内容。

```text
ダッシュボードUIを改善してください。
カテゴリフィルタ、重要度フィルタ、検索、最終更新時刻、ソースURLリンク、モバイル表示を実装してください。
```

受け入れ条件。

- スマホで見やすい
- フィルタが動作する
- 重要度Aが目立つ
- ソースを確認できる

## 23. 最初の完成定義

初期リリースは以下を満たせば完成とする。

- GitHub Pagesでアプリが閲覧できる
- GitHub Actionsで1日3回データ更新される
- GDELTとFRB RSSが取得できる
- FREDが取得できる
- market_snapshot.jsonが表示される
- daily_report.jsonが表示される
- ニュース一覧でカテゴリ・重要度フィルタが使える
- 重要ニュースにソースURLが付く
- APIキーが公開されていない
- 無料枠内で運用できる

## 24. 将来拡張

- ACLED連携
- BLS / BEA / EIA連携
- Google Apps ScriptによるGoogle Sheets出力
- NotebookLM投入用Markdown出力
- Ollamaによるローカル要約
- LINE / Slack / Gmail通知
- 類似ニュース統合
- 過去相場反応との照合
- 経済指標カレンダー
- PWA化

## 25. 開発時の注意

Codexには、大きすぎるタスクを一度に投げない。必ず小さなPR単位にする。

各タスクでは以下を明示する。

- 目的
- 変更対象ファイル
- やってよいこと
- やってはいけないこと
- 受け入れ条件
- テスト方法

実装時は、まずAIなしで動く構成を完成させる。その後、Gemini APIやOllamaによる要約をオプションとして追加する。

最初から完璧なAI要約を狙わず、まず「正しいソースから、毎日、同じ形式で情報が集まる状態」を完成させる。

## 26. 最初にCodexへ渡すプロンプト

以下をCodexの最初のタスクとして使用する。

```text
無料公開情報だけを使って、マクロ経済・FRB・地政学・市場データを収集し、日本語で閲覧できるWebアプリを作ります。

まず、React + TypeScript + Vite + Tailwind CSSでGitHub Pages向けのSPAを作成してください。

要件：
- public/data/news_items.jsonを読み込む
- public/data/market_snapshot.jsonを読み込む
- public/data/daily_report.jsonを読み込む
- ダッシュボードを表示する
- ニュース一覧を表示する
- 市場スナップショットを表示する
- 日次レポートを表示する
- カテゴリフィルタ、重要度フィルタ、キーワード検索を実装する
- スマートフォンでも見やすくする
- APIキーや外部API呼び出しはまだ実装しない
- サンプルJSONをpublic/data配下に作成する
- npm run devとnpm run buildが成功するようにする

やってはいけないこと：
- 有料APIを前提にしない
- Gemini APIキーをブラウザ側に置かない
- 自動売買や投資助言機能を作らない
- バックエンドやDBを最初から作り込まない

完了条件：
- ローカルで画面が表示される
- サンプルデータが表示される
- buildが成功する
- GitHub Pagesへデプロイ可能な構成になっている
```

## 27. 次にCodexへ渡すプロンプト

UI雛形が完成した後、以下を依頼する。

```text
次にcollectorディレクトリを作成し、Pythonで無料公開ソースからデータを取得する処理を実装してください。

最初の対象は以下です。
- GDELT
- FRB RSS
- FRED

要件：
- collector/main.pyから実行できる
- 取得結果をpublic/data/news_items.json、market_snapshot.json、daily_report.jsonに出力する
- APIキーが未設定でも落ちない
- ソース単位でエラー処理する
- URL重複を排除する
- カテゴリ分類と重要度A/B/C判定を行う
- pytestで最低限のテストを作る

完了条件：
- python collector/main.pyでJSONが生成される
- npm run buildが成功する
- 生成されたJSONがフロントエンドに表示される
```

## 28. 運用設計

初期運用は以下とする。

- GitHub PagesでWeb画面を公開する
- GitHub Actionsで1日3回データを更新する
- GDELT、FRB RSS、FREDを最初に稼働させる
- BLS、BEA、EIA、ACLEDは第2段階で追加する
- Gemini API要約は第3段階で追加する
- 無料枠超過を避けるため、Gemini要約は重要度Aのみ対象にする
- APIキーはGitHub Secretsに保存する
- フロントエンドから直接APIキーを使わない

## 29. 最終判断

このアプリの初期版は、Google AI StudioよりもGitHub Pages + GitHub Actionsで進める方がよい。

理由は以下。

- 静的サイトとして無料運用しやすい
- 定期実行をGitHub Actionsに任せられる
- 収集済みJSONを表示するだけならバックエンド不要
- APIキーをGitHub Secretsで管理できる
- CodexとGitHubの開発フローに乗せやすい
- あとからGemini API、Google Apps Script、NotebookLM、Ollamaを追加しやすい

したがって、最初のリリース方針は以下。

```text
Phase 1：GitHub Pages + サンプルJSON + UI
Phase 2：GitHub Actions + Python collector + GDELT/FRB/FRED
Phase 3：BLS/BEA/EIA/ACLED追加
Phase 4：Gemini APIまたはOllamaによる要約強化
Phase 5：通知、PWA、Google Sheets/NotebookLM連携
```

