---
description: Run the frontend and backend concurrently
---

This workflow starts both the React frontend and the FastAPI backend using the `concurrently` package defined in the frontend's `package.json`.

// turbo
1. Run the application:
```bash
cd frontend && npm run dev
```

The application will be available at:
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:8000](http://localhost:8000)
