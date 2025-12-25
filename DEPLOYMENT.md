# Deployment Guide - Classical Music Q&A

This guide covers deploying your application with the **best free setup**:
- **Frontend**: Vercel (fast, excellent CDN)
- **Backend**: Render (supports long-running FastAPI operations)

Both platforms offer 100% free tiers - no credit card required!

---

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **HuggingFace Account** - Get free API token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. **Vercel Account** - Sign up at [vercel.com](https://vercel.com) (free)
4. **Render Account** - Sign up at [render.com](https://render.com) (free)

---

## Step 1: Push Code to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Ready for deployment"

# Add remote and push
git remote add origin https://github.com/yourusername/classical-music-qa.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render

### 2.1 Create Web Service

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure service:

**Basic Settings:**
- **Name**: `classical-music-backend`
- **Region**: Oregon (US West) - or closest to you
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

**Build & Start:**
- **Build Command**:
  ```bash
  pip install -r requirements.txt && python init_vector_store.py
  ```
- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select: `Free`

### 2.2 Set Environment Variables

Click **Environment** tab and add:

| Key | Value |
|-----|-------|
| `HF_TOKEN` | `hf_your_actual_token_here` |
| `DEFAULT_MODEL` | `meta-llama/Llama-3.2-3B-Instruct` |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` |
| `DEBUG` | `false` |
| `CORS_ORIGINS` | `https://your-vercel-app.vercel.app` (update after frontend deployment) |

### 2.3 Deploy

1. Click **Create Web Service**
2. Wait 5-10 minutes for initial deployment
3. Monitor logs for any errors
4. Once deployed, **copy your backend URL** (e.g., `https://classical-music-backend.onrender.com`)

**Important Notes:**
- First request after 15 minutes of inactivity has a ~30-60 second cold start
- Vector store initializes automatically on startup (5,810 chunks)
- Check logs to verify vector store loaded successfully

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Import Project

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **Add New...** → **Project**
3. Import your GitHub repository
4. Vercel will auto-detect it's a Vite project

### 3.2 Configure Project

**Framework Preset:** Vite (auto-detected)

**Root Directory:** `frontend`

**Build Settings:**
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### 3.3 Set Environment Variable

Click **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://your-backend-url.onrender.com` |

**Replace** `your-backend-url.onrender.com` with your actual Render backend URL from Step 2.3.

### 3.4 Deploy

1. Click **Deploy**
2. Wait 1-2 minutes for build
3. Once deployed, **copy your frontend URL** (e.g., `https://your-app.vercel.app`)

---

## Step 4: Update CORS on Backend

Now that you have your frontend URL, update the backend CORS settings:

1. Go back to Render dashboard
2. Open your backend service
3. Go to **Environment** tab
4. Update `CORS_ORIGINS` to your Vercel URL:
   ```
   https://your-app.vercel.app
   ```
5. Save (backend will automatically redeploy in ~2 minutes)

---

## Step 5: Test Your Application

1. Open your Vercel URL: `https://your-app.vercel.app`
2. Try asking a question: "Who was Johann Sebastian Bach?"
3. Verify:
   - ✅ Chat interface loads
   - ✅ Message sends successfully
   - ✅ AI responds with composer information
   - ✅ Sources show composer biographies

**First Request:** May take 30-60 seconds if backend was sleeping (cold start)
**Subsequent Requests:** Should be fast (2-5 seconds)

---

## Troubleshooting

### Frontend shows "Network Error"

**Cause:** CORS not configured correctly or backend is down

**Fix:**
1. Check `CORS_ORIGINS` in Render environment variables
2. Make sure it matches your Vercel URL **exactly** (no trailing slash)
3. Verify backend is running: Visit `https://your-backend.onrender.com/health`

### Backend won't start

**Cause:** Missing HF_TOKEN or dependency errors

**Fix:**
1. Check Render logs for specific error
2. Verify `HF_TOKEN` is set correctly in environment variables
3. Make sure all environment variables are set

### Chat returns empty responses

**Cause:** HuggingFace API token invalid or rate limited

**Fix:**
1. Verify HF_TOKEN is valid: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Check backend logs for API errors
3. HuggingFace free tier has rate limits - wait and retry

### Vector store not loading

**Cause:** Build command didn't run `init_vector_store.py`

**Fix:**
1. Check Render logs for "Checking vector store..."
2. Should see "Loading XX composer files"
3. If not, rebuild with correct build command:
   ```bash
   pip install -r requirements.txt && python init_vector_store.py
   ```

### Slow first response (30-60 seconds)

**Expected Behavior:** Render free tier spins down after 15 minutes of inactivity

**Not a Bug:** This is normal for free tier. Upgrade to paid tier for always-on service.

---

## Custom Domain (Optional)

### Add Domain to Vercel

1. Go to your Vercel project settings
2. Click **Domains**
3. Add your custom domain
4. Follow DNS configuration instructions

### Update CORS

After adding custom domain, update backend `CORS_ORIGINS`:
```
https://yourdomain.com
```

---

## Monitoring & Logs

### Vercel Logs
- Go to your project → **Deployments** → Click deployment → **Logs**
- See build logs and runtime logs

### Render Logs
- Go to your service → **Logs** tab
- See real-time application logs
- Monitor API requests, vector store initialization, errors

---

## Cost Breakdown

| Service | Tier | Cost | Limits |
|---------|------|------|--------|
| **Vercel** | Free | $0/month | 100GB bandwidth, unlimited requests |
| **Render** | Free | $0/month | 750 hours/month, 512MB RAM |
| **HuggingFace** | Free | $0/month | Rate limited (generous) |
| **Total** | | **$0/month** | Perfect for demos & personal use |

---

## Alternative: Both on Render

If you prefer a single platform:

### Frontend on Render

1. Create **Static Site** instead of Web Service
2. Use same repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add environment variable: `VITE_API_URL`

**Pros:** Single platform, simpler management
**Cons:** Slower than Vercel's global CDN

---

## Updating Your Deployment

### Update Frontend (Vercel)
```bash
git add .
git commit -m "Update frontend"
git push origin main
```
Vercel auto-deploys on push to main branch.

### Update Backend (Render)
```bash
git add .
git commit -m "Update backend"
git push origin main
```
Render auto-deploys on push to main branch.

### Force Rebuild
- **Vercel**: Go to deployment → **...** → **Redeploy**
- **Render**: Go to service → **Manual Deploy** → **Deploy latest commit**

---

## Next Steps

- ✅ Application deployed and working
- 📊 Monitor usage in Vercel/Render dashboards
- 🎨 Customize branding and styling
- 📚 Add more composers to knowledge base
- 🔒 Consider rate limiting for production use

---

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Render Docs**: [render.com/docs](https://render.com/docs)
- **HuggingFace Docs**: [huggingface.co/docs](https://huggingface.co/docs)

**Enjoy your free Classical Music Q&A application! 🎵**
