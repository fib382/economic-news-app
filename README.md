# Macro Geopolitical Brief

無料公開情報を収集し、マクロ経済・FRB・地政学・市場データを日本語で閲覧するための静的Webアプリです。投資判断の自動化、売買推奨、確定的な相場予測は行いません。

## 構成

- React + TypeScript + Vite + Tailwind CSS
- `public/data/*.json` を読み込むGitHub Pages向けSPA
- Python collectorでGDELT、FRB RSS、FREDを取得
- GitHub Actionsで1日3回のデータ更新とGitHub Pagesデプロイ

## 対象テーマ

- イラン・中東情勢
- 要人発言
- FRB
- 米国経済
- 為替、債券、株式
- 経済指標
- 原油・エネルギー

## ローカル実行

```powershell
npm install
npm run dev
```

ビルド確認:

```powershell
npm run build
```

collector実行:

```powershell
python -m pip install -r collector/requirements.txt
python collector/main.py
```

## GitHub Secrets

以下は任意です。未設定のソースはスキップされ、アプリ全体は停止しません。

- `FRED_API_KEY`
- `BEA_API_KEY`
- `EIA_API_KEY`
- `ALPHA_VANTAGE_API_KEY`
- `ACLED_API_KEY`
- `ACLED_EMAIL`
- `GEMINI_API_KEY`

APIキーはブラウザ側へ埋め込まず、GitHub ActionsのSecretsで扱います。

## GitHub Pages

`deploy.yml` は `main` ブランチへのpushまたは手動実行で `npm run build` を行い、`dist` をGitHub Pagesへデプロイします。Repository settingsのPagesでSourceをGitHub Actionsに設定してください。

Private repositoryでGitHub Pagesを使う場合、GitHub Pagesがprivate repositoryに対応するGitHubプランである必要があります。対応していない場合はworkflow自体は実行できますが、Pagesの公開で失敗または利用不可になります。

Public repositoryとして運用する場合、リポジトリのコード、commit履歴、`public/data/*.json`、`logs/latest.json` は誰でも閲覧できます。APIキーやローカル `.env` はcommitせず、GitHub Secretsだけに保存してください。

`main` はforce pushとbranch deletionを禁止し、通常のデータ更新commitはGitHub Actions botが行う想定です。直接pushできるのはリポジトリのwrite権限を持つユーザーだけです。

## データ更新

`collect.yml` はUTC 22:00、04:00、10:00に実行します。これはJST 07:00、13:00、19:00相当です。Actionsタブから手動実行も可能です。

collectorは `public/data/*.json` と `logs/latest.json` の生成差分だけをbot名義でcommitします。APIキーやローカルの `.env` はcommitせず、必要な値はGitHub Secretsに登録してください。collectorのcommitが `main` にpushされると、通常のpushと同じく `deploy.yml` が動き、最新データを含む静的サイトを再デプロイします。

## 免責

このアプリは公開情報の収集、分類、要約、重要度判定を行う情報整理ツールです。投資助言、売買推奨、自動売買、確定的な市場予測を目的としません。
