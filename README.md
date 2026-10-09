# 我们的时光地图

一个给情侣共同记录日常、照片和旅行足迹的全栈网页应用。

- 前端：Vue 3 + Vite + Element Plus + Leaflet
- 后端：FastAPI + Python 3.12
- 数据库：SQLite
- 图片：本地文件系统
- 地图：Leaflet + OpenStreetMap，不需要地图 API Key

## 当前功能

- 首次设置两个人的昵称和纪念日。
- 添加、编辑、删除恋爱日记。
- 日记包含日期、标题、内容、心情和多张照片。
- 按心情和日期范围筛选日记。
- 在 Leaflet 地图上点击位置并保存地点。
- 地点可以关联日记并上传照片。
- 首页显示在一起的天数、下一个纪念日倒计时和统计数据。
- SQLite 数据库和上传文件都保存在本地，适合个人或家庭使用。

## 项目结构

```text
love-map/
├── backend/
│   ├── app/
│   │   ├── api/routes.py
│   │   ├── core/db.py
│   │   ├── crud/diary.py
│   │   ├── crud/place.py
│   │   ├── schemas/models.py
│   │   ├── service/stats.py
│   │   └── main.py
│   ├── uploads/
│   ├── requirements.txt
│   └── schema.sql
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── composables/
│   │   └── services/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 启动后端

要求 Python 3.12 或更高版本。

PowerShell：

```powershell
cd love-map/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Linux/macOS：

```bash
cd love-map/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

后端启动后可以访问：

- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/api/health

## 启动前端

另开一个终端：

```powershell
cd love-map/frontend
npm install
npm run dev
```

浏览器打开：

http://localhost:5173

## 数据文件位置

第一次启动后会自动生成：

- backend/data/love-map.db：SQLite 数据库。
- backend/uploads/：上传的照片。

这些运行数据已经在 .gitignore 中忽略，不会被提交到 GitHub。备份项目时请单独备份这两个位置。

## API 概览

- GET/POST /api/couple
- GET/POST /api/diary
- GET/PUT/DELETE /api/diary/{id}
- POST /api/diary/{id}/photo
- GET/POST /api/place
- PUT/DELETE /api/place/{id}
- POST /api/place/{id}/photo
- GET /api/stats

日记筛选示例：

```text
GET /api/diary?mood=happy&start_date=2026-01-01&end_date=2026-12-31
```

## 上传到 GitHub

在 love-map 目录执行：

```powershell
git init -b main
git add .
git commit -m "feat: create love map app"
git branch -M main
git remote add origin git@github.com:haijunlia/love-map.git
git push -u origin main
```

建议不要提交：

- backend/.venv/
- backend/data/love-map.db
- backend/uploads/ 中的照片
- .env 和任何密码、Token

## 发布版本

第一次上传成功后，可以在确认前后端启动方式和文档都没问题后发布版本：

```powershell
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

以后有新功能时，先修改代码、测试并提交，再使用新的版本号，例如 `v0.2.0`。不要重复使用已经推送过的 Tag。

## 后续可扩展功能

- 登录或邀请机制。
- 云端对象存储和数据库。
- 日记导出 PDF。
- 地点路线和旅行相册。
- 更完整的统计图表。
