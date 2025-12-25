# Vercel-Only Deployment Guide

Deploy both frontend and backend to **Vercel** for a simple, single-platform deployment.

---

## ⚠️ Important Limitations

This lightweight serverless approach has some tradeoffs:

| Feature | Status | Notes |
|---------|--------|-------|
| **Cold Start Time** | 30-60 seconds | First request after 15min inactivity |
| **Vector Store** | Rebuilds on cold start | 5,810 chunks loaded from files |
| **Database (Sessions)** | Ephemeral | Resets on deployment/cold start |
| **Response Time** | 2-5 seconds | After cold start |
| **Cost** | 100% FREE | No credit card required |

**Best For**: Demos, portfolios, testing, personal projects
**Not For**: Production apps requiring persistent sessions

---

## Prerequisites

1. **GitHub Account** with your code pushed
2. **HuggingFace API Token** from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. **Vercel Account** - Sign up at [vercel.com](https://vercel.com) (free)

---

## Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

---

## Step 2: Deploy Backend to Vercel

### 2.1 Import Project

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **Add New...** → **Project**
3. Import your GitHub repository
4. Vercel will detect it as a monorepo

### 2.2 Configure Backend

**Project Settings:**
- **Framework Preset**: Other
- **Root Directory**: `backend`
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)

**Environment Variables** - Click "Environment Variables" and add:

| Key | Value |
|-----|-------|
| `HF_TOKEN` | `hf_your_actual_token_here` |
| `DEFAULT_MODEL` | `meta-llama/Llama-3.2-3B-Instruct` |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` |
| `DEBUG` | `false` |
| `CORS_ORIGINS` | `*` (we'll update this after frontend deployment) |

### 2.3 Deploy Backend

1. Click **Deploy**
2. Wait 3-5 minutes for deployment
3. **Copy your backend URL** (e.g., `https://your-backend-abc123.vercel.app`)

**Note**: First deployment might take longer as it installs all dependencies.

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Create New Project

1. In Vercel dashboard, click **Add New...** → **Project**
2. Select **same repository** again
3. Vercel will auto-detect Vite

### 3.2 Configure Frontend

**Project Settings:**
- **Framework Preset**: Vite (auto-detected)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)

**Environment Variables:**

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://your-backend-abc123.vercel.app` |

**Replace** with your actual backend URL from Step 2.3.

### 3.3 Deploy Frontend

1. Click **Deploy**
2. Wait 1-2 minutes for build
3. **Copy your frontend URL** (e.g., `https://classical-music-qa.vercel.app`)

---

## Step 4: Update CORS on Backend

1. Go back to your **backend project** in Vercel
2. Click **Settings** → **Environment Variables**
3. Find `CORS_ORIGINS` and click **Edit**
4. Change value to your frontend URL:
   ```
   https://classical-music-qa.vercel.app
   ```
5. Click **Save**
6. Click **Redeploy** to apply changes

---

## Step 5: Test Your Application

1. Open your Vercel frontend URL
2. Wait 30-60 seconds on first visit (cold start loading vector store)
3. Try asking: **"Who was Johann Sebastian Bach?"**

**What to Expect:**
- ✅ First request: 30-60 seconds (cold start)
- ✅ Subsequent requests: 2-5 seconds (warm)
- ✅ AI responds with composer information
- ✅ Sources show composer biographies
- ⚠️ After 15 minutes of inactivity: cold start again

---

## Understanding Cold Starts

### What Happens on Cold Start:

1. **Database Initialization**: Creates SQLite tables (~1 second)
2. **Vector Store Initialization**: Loads 107 composer files into ChromaDB (~20-40 seconds)
3. **Embedding Model Load**: Loads sentence-transformers model (~5-10 seconds)

**Total Cold Start**: 30-60 seconds

### When Cold Starts Occur:

- First request after deployment
- After 15 minutes of inactivity (Vercel free tier limit)
- After redeployment

### How to Minimize Impact:

- **Keep It Warm**: Visit your site every 10-15 minutes
- **Pre-Load**: Add a `/health` endpoint check via external monitoring (UptimeRobot, etc.)
- **Upgrade**: Vercel Pro removes cold starts ($20/month)

---

## Troubleshooting

### Frontend shows "Network Error"

**Cause**: CORS not configured or backend is down

**Fix**:
1. Check `CORS_ORIGINS` in backend environment variables
2. Must match frontend URL exactly (no trailing slash)
3. Try `*` for testing (not recommended for production)

### Backend shows "Function execution timeout"

**Cause**: Cold start taking longer than 60 seconds

**Fix**:
1. Check Vercel function logs for specific error
2. Increase timeout in `backend/vercel.json` (max 60s on free tier)
3. Consider reducing number of composer files in `/data/composer_sources/`

### Chat returns empty or error responses

**Cause**: HuggingFace API token invalid or rate limited

**Fix**:
1. Verify `HF_TOKEN` in environment variables
2. Check HuggingFace token is valid: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. HuggingFace free tier has rate limits - wait and retry

### Sessions don't persist

**Expected Behavior**: SQLite database is ephemeral in serverless

**Not a Bug**: Sessions reset on:
- Cold starts
- Redeployments
- Every ~15-20 minutes

**Solution**: This is a limitation of the lightweight approach. For persistent sessions, use Vercel Postgres (requires upgrade) or deploy backend to Render.

### Vector store empty

**Cause**: Composer files not included in deployment

**Fix**:
1. Check `backend/.vercelignore` includes `!data/composer_sources/`
2. Verify files exist in `backend/data/composer_sources/`
3. Check Vercel build logs for "Vector store initialized with XXXX chunks"

---

## Monitoring & Logs

### View Backend Logs

1. Go to Vercel dashboard → Backend project
2. Click **Deployments** → Latest deployment
3. Click **View Function Logs**
4. See real-time logs including:
   - Database initialization
   - Vector store loading progress
   - API requests
   - Errors

### View Frontend Logs

1. Go to Vercel dashboard → Frontend project
2. Click **Deployments** → Latest deployment
3. Build logs show npm install and build process

---

## Performance Optimization

### Reduce Cold Start Time

1. **Reduce Composer Files**: Remove less popular composers to decrease initialization time
2. **Optimize Embeddings**: Use smaller embedding model (though quality may decrease)
3. **Pre-warm Function**: Use external service to ping `/health` every 10 minutes

### Improve Response Time

1. **Smaller Model**: Consider switching to smaller LLM (faster but less accurate)
2. **Reduce Retrieval**: Lower `RETRIEVAL_K` in config (fewer chunks = faster)
3. **Cache Results**: Add client-side caching for repeated questions

---

## Cost Breakdown

| Service | Tier | Cost | Limits |
|---------|------|------|--------|
| **Vercel Frontend** | Free | $0/month | 100GB bandwidth |
| **Vercel Backend** | Free | $0/month | 100GB bandwidth, 100GB-hrs compute |
| **HuggingFace API** | Free | $0/month | Rate limited |
| **Total** | | **$0/month** | Perfect for demos! |

### Vercel Free Tier Limits

- **Functions**: 100GB-Hrs serverless compute/month
- **Bandwidth**: 100GB/month
- **Executions**: Unlimited
- **Timeout**: 10 seconds (hobby), 60 seconds with Pro
- **Cold Start**: After 15 minutes of inactivity

---

## Upgrading to Production

If you need better performance, consider:

### Option 1: Vercel Pro ($20/month)
- ✅ No cold starts
- ✅ Longer timeouts (300 seconds)
- ✅ More compute hours
- ❌ Still ephemeral database

### Option 2: Hybrid (Vercel + Render)
- ✅ Frontend on Vercel (fast CDN)
- ✅ Backend on Render (persistent database)
- ✅ Both can stay free
- ✅ Better for production

### Option 3: Add Vercel Postgres
- ✅ Persistent sessions
- ✅ Stay on Vercel
- ❌ Requires Vercel Pro ($20/month)

---

## Updating Your Deployment

### Update Code

```bash
git add .
git commit -m "Update application"
git push origin main
```

Vercel automatically redeploys on push to `main` branch.

### Update Environment Variables

1. Go to project **Settings** → **Environment Variables**
2. Edit values
3. Click **Redeploy** to apply changes

### Rollback Deployment

1. Go to **Deployments**
2. Find previous working deployment
3. Click **...** → **Promote to Production**

---

## Custom Domain (Optional)

### Add Domain to Vercel

1. Go to project **Settings** → **Domains**
2. Add your custom domain
3. Configure DNS as instructed
4. SSL certificate auto-generated

### Update CORS

After adding custom domain to frontend:
1. Update backend `CORS_ORIGINS` to your new domain
2. Redeploy backend

---

## Next Steps

- ✅ Application deployed on Vercel
- 📊 Monitor usage in Vercel dashboard
- 🎨 Customize branding and styling
- 🔍 Monitor function logs for errors
- 📈 Consider upgrading if traffic grows

---

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **HuggingFace Docs**: [huggingface.co/docs](https://huggingface.co/docs)
- **Mangum (ASGI adapter)**: [github.com/jordaneremieff/mangum](https://github.com/jordaneremieff/mangum)

**Enjoy your free Classical Music Q&A on Vercel! 🎵**
