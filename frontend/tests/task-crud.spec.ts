import { test, expect } from '@playwright/test'

async function createTask(page, title: string, extra?: { status?: string }) {
  await page.getByRole('button', { name: '＋ 新規' }).click()
  await page.getByLabel('タイトル').fill(title)
  if (extra?.status) {
    await page.getByLabel('ステータス').selectOption(extra.status)
  }
  await page.getByRole('button', { name: /作成|更新/ }).click()
  await expect(page.getByText(title)).toBeVisible()
}

async function changeFirstTaskStatus(page, status: string) {
  const firstSelect = page.locator('li select').first()
  await firstSelect.selectOption(status)
  await expect(firstSelect).toHaveValue(status)
}

test.describe('Task CRUD', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    // 一覧ロード待機
    await expect(page.getByText('タスクがありません').or(page.locator('li').first())).toBeVisible({ timeout: 5000 })
  })

  test('create task', async ({ page }) => {
    await createTask(page, 'タスクA')
  })

  test('edit task', async ({ page }) => {
    await createTask(page, 'タスク編集前')
    await page.getByRole('button', { name: '編集' }).first().click()
    await page.getByLabel('タイトル').fill('タスク編集後')
    await page.getByRole('button', { name: '更新' }).click()
    await expect(page.getByText('タスク編集後')).toBeVisible()
  })

  test('filter by status', async ({ page }) => {
    await createTask(page, 'タスクTodo1', { status: 'todo' })
    await changeFirstTaskStatus(page, 'doing')
    // filter doing
    await page.getByLabel('ステータス:').selectOption('doing')
    await expect(page.locator('li')).toHaveCount(1)
  })

  test('delete task', async ({ page }) => {
    await createTask(page, '削除対象')
    const item = page.getByText('削除対象')
    await page.getByRole('button', { name: '削除' }).first().click()
    // confirm 自動OK（Playwright デフォルト）
    await expect(item).not.toBeVisible()
  })
})
