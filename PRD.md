# PRD — Al-La'eeb (AI Football Talent Intelligence Platform)

## 1. نظرة عامة
منصة كشف مواهب كرة القدم بالذكاء الاصطناعي: تحليل فيديو (CV)، مدرب افتراضي (NLP عربي/إنجليزي)، سوق كشّافين. معمارية microservices بواجهة FastAPI Gateway.

## 2. المستخدمون
- لاعب (يسجّل، يرفع فيديو، يستلم تقارير وتمارين)
- مدرب افتراضي/بشري (خطط تدريب)
- كشّاف (بحث عن مواهب، مفضلة، توصيات)

## 3. الميزات الأساسية (قابلة للاختبار)
1. تسجيل/دخول/تحديث JWT + بيانات المستخدم (`POST /register|/login|/refresh`, `GET /me`, `POST /logout|/change-password`)
2. تحقق وجه بيومتري + حالة اللاعب (`POST /face`, `GET /status/{player_id}`)
3. رفع فيديو تحليل + تتبع الحالة والطابور (`POST /upload`, `GET /status/{video_id}`, `GET /queue/status`, `POST /consents/video-analysis/{player_id}`)
4. مقاييس أداء وتقرير تدريبي وخط زمني (`GET /metrics/{video_id}`, `GET /report/{video_id}`, `GET /timeline/{video_id}`)
5. مدرب محادثة + مكتبة تمارين + توليد تقرير (`POST /chat`, `GET /drills`, `POST /generate-report`)
6. ملفات لاعبين وبحث وإحصائيات (`GET /api/v1/players/search`, `GET /api/v1/players/{player_id}[ /stats|/timeline]`)
7. بحث كشّافين وتفاصيل وتوصيات ومفضلة (`POST /api/v1/scout/search`, `GET /api/v1/scout/player/{player_id}/detailed`, `GET /api/v1/scout/recommendations`, `POST /api/v1/scout/favorite/{player_id}`)
8. رفع/بث فيديو (`POST /api/v1/videos/upload`, `GET /api/v1/videos/{video_id}/stream`)

## 4. API endpoints الحقيقية (من الكود فقط)
- Auth: `POST /register|/login|/refresh|/logout|/change-password`, `GET /me`, `POST /face`, `GET /status/{player_id}`, `GET /health|/ready|/metrics`
- AI-Engine: `POST /upload`, `GET /status/{video_id}|/queue/status|/metrics/{video_id}|/report/{video_id}|/timeline/{video_id}`
- NLP-Coach: `POST /chat|/generate-report`, `GET /drills`
- Player: `GET /api/v1/players/search|/{player_id}|/{player_id}/stats|/{player_id}/timeline`
- Scout: `POST /api/v1/scout/search|/favorite/{player_id}`, `GET /api/v1/scout/player/{player_id}/detailed|/recommendations`
- Video: `POST /api/v1/videos/upload`, `GET /api/v1/videos/{video_id}/stream`
- Gateway: `GET /health`, `GET /api/v1/health/all`

## 5. بيانات الدخول/الإعداد للاختبار
- `cp .env.example .env` ثم `docker-compose up --build`؛ Gateway: `http://localhost:8000`، Auth: `:8001`، AI-Engine: `:8003`، NLP-Coach: `:8004`
- فحوص الصحة: `/api/v1/health/` على كل خدمة؛ لا توجد بيانات دخول افتراضية في الكود — يُنشأ مستخدم عبر `POST /register`

## 6. خارج النطاق (mocked/simulated)
- Qdrant (مقارنة 10,000+ لاعب)، GPT-4o/Claude/Gemini، InsightFace/OCR، دفع RTMP — لا أساس كودي حي تم التحقق منه هنا؛ أي ادعاء SLA (< 2s، 30 FPS، 47 مقياسا) تسويقي من README وغير قابل للاختبار كعقد API.
