# XR Development Monitor

Unity と Meta Quest 向け XR 開発情報を、公式情報を優先して収集・差分検知するツールです。
正確性を優先し、取得失敗を「変更なし」とは扱いません。

## 現在の範囲

Phase 0 と Phase 1 の基礎実装です。設定、HTML 収集、正規化、スナップショット、
差分検知、取得状態、CLI、テストを含みます。

| Source | 状態 | 理由 |
| --- | --- | --- |
| Unity Editor Release Notes | 有効 | robots.txt とHTML本文領域を確認済み。 |
| Unity OpenXR Plugin | 保留 | currentページが動的に本文を生成するため、HTML Collectorでは正確に収集できない。 |
| Meta Horizon Developer Release Notes | 保留 | Meta Developersのrobots.txtが書面許可なしの自動収集を禁止している。 |

## セットアップ

```powershell
$env:XR_MONITOR_UV_CACHE = "$PWD/.uv-cache"
uv sync --group dev
uv run python -m xr_monitor --help
uv run pytest
uv run ruff check .
uv run mypy src
```

## CLI

```powershell
uv run python -m xr_monitor collect --source unity_editor_release_notes
uv run python -m xr_monitor collect --schedule daily
uv run python -m xr_monitor diff --source unity_editor_release_notes
```

`--schedule daily` は有効なソースだけを収集します。未有効化のソースを個別に指定した場合は、
明確にエラーで終了します。取得・解析に失敗した場合、既存のスナップショットは変更しません。

## 日次収集

GitHub Actionsの `collect-daily` は毎日 09:00 JST（00:00 UTC）に実行されます。Snapshotと
Source Healthに変更があった場合だけ、`data: collect updates YYYY-MM-DD` というコミットを作成します。
取得ログは肥大化を避け、Gitへは保存しません。

日次収集の前にUnity公式サイトマップを確認し、Unity 6の新しいリリースノートURLを検出します。現在は
検出したURL一覧を保持する段階であり、個別リリースノートの自動収集は次の段階で追加します。

## 静的サイト

更新レコード、公式本文、システム判定、Source Healthを静的HTMLに出力します。

```powershell
uv run python -m xr_monitor build-site
```

生成先は `site/index.html` です。`Deploy static site` ワークフローは `main` へのpush時に
GitHub Pagesへデプロイします。初回のみリポジトリの **Settings → Pages** で、Sourceを
**GitHub Actions** に設定してください。

システム判定はキーワード規則にもとづく補助情報であり、公式発表ではありません。根拠が弱い場合は
`documentation / info` として表示します。

公開用のSnapshotと更新レコードには、公式本文の最大1,500文字の抜粋だけを保存します。完全な本文は
Gitへ保存・公開しません。
