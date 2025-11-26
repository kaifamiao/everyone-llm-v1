# Everyone-LLM Frontend

Nuxt4 前端应用

## 环境要求

- Node.js 18+
- npm 或 yarn

## 安装

```bash
npm install
```

## 配置

在 `nuxt.config.ts` 中配置后端 API 地址，或设置环境变量：

```bash
export API_BASE_URL=http://localhost:8000
```

## 开发

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

## 构建

```bash
npm run build
npm run preview
```

## 主要功能

- ✅ 响应式布局（PC 和移动端）
- ✅ 对话管理（创建、选择、删除、搜索）
- ✅ 7种对话模式（AI、文档、知识库、数据库、Web、图片、MCP）
- ✅ SSE 流式响应
- ✅ Markdown 渲染
- ✅ 积分显示和扣除
- ✅ 设置面板（主题、API 配置、AI 参数）
- ✅ 对话导出（JSON 格式）

