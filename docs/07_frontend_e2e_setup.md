# 07 フロント E2E テスト (Playwright)

## 概要
主要ユーザーフロー自動化テスト。

## タスクリスト
- [x] Playwright 初期化 (`npx playwright init` カスタム)
- [x] 環境設定 (baseURL)
- [x] テスト: タスク作成 -> 一覧に表示
- [x] テスト: 編集 -> 変更反映
- [x] テスト: ステータスフィルタ適用
- [x] テスト: 削除 -> 一覧から消える
- [x] 期待待機: networkidle or locator assertions
- [x] CI 用 headless 実行設定（GitHub Actions想定）
- [x] スクリーンショット/trace 失敗時保存

## 完了条件
- 全 E2E テスト成功
- CI でも同様に成功

## メモ
バックエンド API をテスト前にシードしても良いが、UI操作で作成する方針。
