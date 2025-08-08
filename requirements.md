# TODOリスト Webサービス 要件定義書（確定版）

## 1. 概要
シンプルなタスク管理（CRUD）を行う OSS の Web アプリケーション。認証未実装の単一テナントMVPを1日で構築し、将来のユーザー認証・拡張を容易にする基盤を用意する。

## 2. 目的
- 個人/軽量業務のタスク整理を支援する最小機能セットの提供
- 将来的な認証・共有・通知・タグ付けなど拡張の土台
- 公開OSSとして外部コントリビュートを受け入れやすい構造

## 3. ユーザー
MVP: 認証なし・全タスク共通領域（擬似シングルユーザ）  
将来: userテーブル + tasks.user_id 追加によるマルチユーザ化（論理的マルチテナント）

## 4. スコープ（MVP）
必須機能:
- タスク CRUD（作成 / 一覧 / 取得 / 更新 / 削除）
- ステータス（todo / doing / done）変更
- 優先度（high / medium / low）必須入力（デフォルト: medium）
- 期限（日時型、過去日時も許容）
- ステータス簡易フィルタ（一覧）
- モバイル対応（レスポンシブ）
- 日本語UI
- E2Eテスト（主要ユーザーフロー）

除外（MVPでは実装しない）:
- 認証/認可
- タグ/検索（全文/タイトル）
- 通知/リマインダ
- 論理削除（物理削除のみ）
- 共有/権限管理
- ダークモード（将来UIテーマ拡張で対応可）

## 5. 画面一覧
| ID | 画面 | 内容 | 備考 |
|----|------|------|------|
| G01 | タスク一覧 | 一覧表示 / statusフィルタ / 新規ボタン / 編集・削除 | メイン画面 |
| G02 | タスク作成 | フォーム（タイトル/説明/期限/優先度/作成） | ステータスは初期 todo |
| G03 | タスク編集 | 既存値編集 / 更新 / 削除 | 一覧から遷移 |
| (省略可) | 詳細 | 一覧→編集で代替 | MVPでは未実装 |

## 6. データモデル
Task:
| 項目 | 型 | 必須 | デフォルト | 備考 |
|------|----|------|------------|------|
| id | UUID | ○ | 生成 | 主キー |
| title | string | ○ |  - | 1..100文字 |
| description | string | 任意 | - | 最大1000文字 |
| status | enum(todo/doing/done) | ○ | todo | |
| priority | enum(high/medium/low) | ○ | medium | |
| dueDate | datetime | 任意 | null | 過去可 |
| createdAt | datetime | ○ | now | サーバ生成 |
| updatedAt | datetime | ○ | now/update | サーバ更新 |

削除: 物理削除のみ。将来的論理削除導入時は deletedAt 追加予定。

## 7. API仕様（FastAPI REST）
| メソッド | パス | 説明 | クエリ/ボディ | 成功レスポンス |
|----------|------|------|----------------|----------------|
| GET | /api/tasks | タスク一覧取得 | status(任意) | 200 JSON配列 |
| POST | /api/tasks | タスク作成 | JSON body | 201 JSON(作成) |
| GET | /api/tasks/{id} | 単一取得 | id | 200 JSON |
| PUT | /api/tasks/{id} | 全更新 | JSON body | 200 JSON |
| PATCH | /api/tasks/{id} | 部分更新（時間余裕時） | JSON body | 200 JSON |
| DELETE | /api/tasks/{id} | 物理削除 | id | 204 空 |

レスポンス例（GET /api/tasks/xxx）:
```json
{
  "id": "3c8c9e9a-...",
  "title": "買い物",
  "description": "牛乳と卵",
  "status": "todo",
  "priority": "medium",
  "dueDate": "2025-08-08T12:30:00Z",
  "createdAt": "2025-08-08T09:00:00Z",
  "updatedAt": "2025-08-08T09:00:00Z"
}
```

### バリデーション
- title: 空白トリム後1..100
- description: 0..1000
- status: enum以外400
- priority: enum以外400
- dueDate: ISO8601文字列（無効値400）

### 並び順 / フィルタ
- デフォルト: createdAt DESC
- フィルタ: status（完全一致）

## 8. 非機能要件
| 分類 | 要件 |
|------|------|
| パフォーマンス | 小規模（<1000件）で一覧応答 <300ms（ローカル） |
| 可用性 | シングルインスタンス運用 |
| セキュリティ | CORS許可Origin制限 / 基本的なヘッダ設定 / XSS対策（エスケープ） |
| ログ | アクセス（メソッド, パス, ステータス, 所要時間）, エラー例外 |
| i18n | 日本語固定（将来拡張でi18n層差し替え） |
| モバイル | 最小幅360px想定、テーブルはカード表示へ切替（将来） |
| ライセンス | MIT |

## 9. 技術スタック
| レイヤ | 選定 | 備考 |
|--------|------|------|
| フロント | Vue 3 + Vite + TypeScript | Composition API |
| UI | Tailwind CSS | Utility-first |
| 状態管理 | 必要最小: ローカル状態 + composables / fetch | 規模拡大時 Pinia検討 |
| テスト（E2E） | Playwright | CI headless |
| バックエンド | FastAPI | Uvicorn ASGI |
| DB | SQLite | 開発/小規模運用 |
| ORM/モデル | SQLModel | Pydantic + SQLAlchemy融合 |
| マイグレーション | Alembic | 自動生成支援 |
| コンテナ | Docker / docker-compose | API + SQLite永続ボリューム |
| デプロイ(フロント) | Vercel | 静的/SPA |
| デプロイ(API) | Railway | Dockerコンテナとしてデプロイ |
| Lint(Backend) | Ruff | フォーマット & 静的チェック |
| Lint(Frontend) | ESLint + Prettier | 標準設定拡張 |
| ライセンス | MIT | LICENSE添付 |

## 10. テスト範囲
| 種別 | 内容 |
|------|------|
| ユニット | バリデーション / モデルスキーマ |
| API | CRUD正常 / 誤ID 404 / バリデーション400 |
| E2E | 1) タスク作成→一覧反映 2) 編集→値更新 3) 削除→消失確認 4) ステータスフィルタ動作 |

## 11. 開発ステップ（1日目標）
| 順序 | 作業 | 目安 |
|------|------|------|
| 1 | リポジトリ初期構成 / ライセンス / README | 0.5h |
| 2 | backend: FastAPI雛形 / SQLModel Task / マイグレーション | 1h |
| 3 | CRUDエンドポイント実装 & pytest | 1.5h |
| 4 | frontend: Vite+Vue+Tailwind セットアップ | 0.5h |
| 5 | 一覧/取得/作成フォーム | 1h |
| 6 | 更新/削除/フィルタ | 1h |
| 7 | E2E (Playwright) / Lint整備 | 1h |
| 8 | ドキュメント整備 / 動作最終確認 | 0.5h |
| (余裕) | PATCH対応 / UI改善 | - |

## 12. リスクと対策
| リスク | 影響 | 対策 |
|--------|------|------|
| 時間超過 | 機能未完 | 詳細画面省略 / PATCH後回し |
| デプロイ設定遅延 | 公開遅れ | 早期Railwayサービス作成 |
| 将来認証導入改修コスト | 大規模差分 | スキーマ/サービス層分離で吸収 |

## 13. 受け入れ基準
- CRUD APIが仕様通り(201/200/204/404/400)動作
- Lint & フォーマットエラーなし
- フロントUIでタスクの作成/編集/削除/フィルタが動作
- E2Eシナリオ成功（CI or ローカル）
- READMEにセットアップ/起動/テスト方法明記

## 14. ライセンス
MIT（`LICENSE`ファイル配置）

## 15. 将来拡張
| 項目 | 概要 |
|------|------|
| 認証 | OAuth2 / OIDC / 外部IdP（Auth0/Supabase） |
| タグ | tagsテーブル + 中間テーブル task_tags |
| 検索 | SQLite FTS5 / PostgreSQL移行時にGINなど |
| 通知 | 期限前ジョブ（Celery/リマインダ） |
| PWA | オフラインキャッシュ / push通知 |
| 論理削除 | deletedAt列追加 / 復元機能 |

## 16. 補足アーキメモ
- API層は service / repository レイヤ分離想定（MVP段階はfat router可、将来抽出）
- user_id追加時: Taskテーブルに NOT NULL user_id（FK）後付→既存行はマイグレーション時デフォルトユーザーに割当
- CORS: Vercelデプロイドメインのみ許可

---
最終更新日: 2025-08-08
