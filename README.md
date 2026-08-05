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
