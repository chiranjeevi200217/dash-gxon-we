# Vercel Deployment Guide for Next.js

## Prerequisites
- [ ] GitHub account with your repository pushed
- [ ] Vercel account (create at https://vercel.com/signup)
- [ ] Git installed and configured locally
- [ ] Node.js 18+ installed

---

## Step 1: Prepare Your Repository

### 1.1 Ensure Repository is Up-to-Date
```bash
# Check git status
git status

# Commit all changes
git add .
git commit -m "Prepare for Vercel deployment"

# Push to GitHub
git push origin main
```

### 1.2 Verify Build Configuration
Your `package.json` scripts are properly configured:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint"
  }
}
```

### 1.3 Check for `.gitignore`
Ensure your `.gitignore` includes:
```
node_modules/
.next/
.env.local
.env.*.local
*.log
.DS_Store
```

---

## Step 2: Connect Repository to Vercel

### 2.1 Create/Login to Vercel
1. Go to https://vercel.com
2. Click "Log in" or "Sign up"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub account

### 2.2 Import Your Project
1. After login, click **"Add New..."** → **"Project"**
2. Select **"Import Git Repository"**
3. Paste your GitHub repository URL or search for it:
   - Format: `https://github.com/username/repo-name`
4. Click **"Import"**

### 2.3 Grant Permissions
- Click **"Authorize Vercel"** if prompted
- Select repository access (allow Vercel to access your repo)
- You can restrict to specific repositories for security

---

## Step 3: Configure Build Settings

### 3.1 Project Settings
On the Vercel import page, you should see:

| Setting | Value | Notes |
|---------|-------|-------|
| **Framework** | Next.js | Auto-detected |
| **Build Command** | `npm run build` or `next build` | Should auto-fill |
| **Output Directory** | `.next` | Auto-detected |
| **Install Command** | `npm install` | Auto-detected |
| **Development Command** | `next dev` | Optional |

### 3.2 Root Directory
- If your `next.config.mjs` is in the root: **Leave as `.`**
- If in a subdirectory: **Set to the subdirectory path**

### 3.3 Recommended `vercel.json` Configuration
Place this in your project root:
```json
{
  "buildCommand": "npm run build",
  "devCommand": "next dev",
  "installCommand": "npm install",
  "framework": "nextjs"
}
```

---

## Step 4: Set Environment Variables

### 4.1 Configure Variables in Vercel Dashboard
1. After project import, go to **Settings** → **Environment Variables**
2. Add variables for each environment (Production, Preview, Development):

**Common Variables:**
```
DATABASE_URL=your_database_connection_string
API_KEY=your_api_key
NEXT_PUBLIC_API_ENDPOINT=https://api.example.com
```

### 4.2 Environment Variable Best Practices
- **Prefix `NEXT_PUBLIC_`** for client-side variables (publicly exposed)
- **No prefix** for server-side only variables
- Use **separate values** for production/staging/development
- Never commit `.env.local` to Git

### 4.3 Add Variables Example
```
NEXT_PUBLIC_API_URL = https://api.yourdomain.com  [✓] Production [✓] Preview
DATABASE_URL = postgresql://user:pass@host/db      [✓] Production [✗] Preview
JWT_SECRET = your_secret_key                       [✓] Production [✓] Preview
```

---

## Step 5: Enable Automatic Deployments

### 5.1 Git Integration (Already Enabled!)
Vercel automatically deploys when you push to GitHub:
- **Push to `main`** → Deploy to Production
- **Push to other branches** → Deploy to Preview
- **Create Pull Request** → Get Preview URL in PR comments

### 5.2 Deployment Rules (Optional)
Go to **Settings** → **Git** to configure:
- **Production Branch**: Set to `main` (or your default branch)
- **Ignored Build Step**: Skip deployments if specific files change
  ```bash
  # Example: Don't redeploy on README changes
  git diff --quiet HEAD^ HEAD -- ./README.md
  ```

### 5.3 Automatic Rollback
- Vercel keeps deployment history
- Click previous deployment to rollback instantly
- No re-build required

---

## Step 6: Set Up Custom Domain

### 6.1 Connect Custom Domain
1. Go to your project in Vercel dashboard
2. Click **Settings** → **Domains**
3. Click **"Add"** → **"Add Custom Domain"**
4. Enter your domain (e.g., `yourdomain.com`)
5. Choose DNS configuration method

### 6.2 DNS Configuration Options

#### Option A: Nameserver Transfer (Recommended)
1. Point your domain registrar's nameservers to Vercel:
   - `ns1.vercel-dns.com`
   - `ns2.vercel-dns.com`
   - `ns3.vercel-dns.com`
   - `ns4.vercel-dns.com`
2. Wait 24-48 hours for DNS propagation
3. Vercel auto-issues SSL certificate

#### Option B: CNAME Record
1. Add CNAME record in your DNS provider:
   - **Name**: `www` (or subdomain)
   - **Value**: `cname.vercel-dns.com`
2. For root domain (@), add A record:
   - **Name**: `@`
   - **Value**: `76.76.19.124`

### 6.3 SSL Certificate
- Vercel auto-generates free SSL certificate (Let's Encrypt)
- Usually issues within 5 minutes
- Automatic renewal

### 6.4 Redirect www to Non-www (or vice versa)
In Vercel dashboard:
1. **Settings** → **Domains**
2. Add both `domain.com` and `www.domain.com`
3. Click three dots on one → **"Edit"** → **"Redirect to"**

---

## Best Practices

### 1. Branch Strategy
```
main (production) → Auto-deploys to vercel.app
staging → Deploy to staging.vercel.app
feature-* → Preview deployments (auto-deleted after PR merge)
```

### 2. Environment Configuration
```javascript
// next.config.mjs
const nextConfig = {
  swcMinify: true,              // Enable SWC minification (faster)
  compress: true,               // Enable gzip compression
  productionBrowserSourceMaps: false,  // Disable source maps in production
  
  // Performance optimizations
  images: {
    domains: ['cdn.example.com'],
    unoptimized: false,
  },
};

export default nextConfig;
```

### 3. Performance Optimization
- Use **Image Optimization** with `<Image>` component
- Enable **Compression** in next.config.mjs
- Configure **Caching** headers
- Use **ISR** (Incremental Static Regeneration) for dynamic content
- Implement **API routes** on Vercel Functions

### 4. Security Best Practices
- **Never** commit `.env.local` or secrets to Git
- Use Vercel's **"Sensitive" toggle** for sensitive variables
- Implement **API authentication** on serverless functions
- Use **CORS headers** appropriately
- Enable **HTTPS only** (default in Vercel)

### 5. Monitoring & Analytics
```
Vercel Dashboard:
- Analytics (real-time metrics)
- Logs (function and build logs)
- Speed Insights (Core Web Vitals)
- Performance metrics
```

### 6. Cost Optimization
- Use **ISR/SSG** instead of **SSR** when possible
- Minimize **Serverless Function** execution time
- Cache API responses
- Use **Edge Middleware** for simple transformations
- Monitor **bandwidth** usage

---

## Troubleshooting

### Issue 1: Build Fails with "Command npm run build exited with 1"

**Solutions:**
```bash
# 1. Check for Node version mismatch
node --version  # Should be 18+

# 2. Install dependencies locally and test
npm install
npm run build

# 3. Check for missing environment variables
# Add all required ENV vars in Vercel dashboard

# 4. Clear cache and redeploy
# In Vercel: Settings → Deployments → "Redeploy"
```

### Issue 2: Environment Variables Not Working

**Solutions:**
```javascript
// Verify you're accessing correctly:

// For public variables (client-side)
const API_URL = process.env.NEXT_PUBLIC_API_URL;  // ✓ Correct

// For server-side only
export async function getServerSideProps() {
  const SECRET = process.env.DATABASE_URL;  // ✓ Correct
}

// Wrong: accessing server vars on client
const SECRET = process.env.DATABASE_URL;  // ✗ Won't work in browser
```

**Debug:**
1. Restart build after adding ENV vars
2. Check **Settings** → **Environment Variables** → Variable shows in all environments
3. Verify variable name matches exactly (case-sensitive)
4. Rebuild project after changes

### Issue 3: Custom Domain Not Working

**Solutions:**
```bash
# Check DNS propagation (takes 24-48 hours)
nslookup yourdomain.com
dig yourdomain.com

# Verify CNAME/A records
nslookup www.yourdomain.com
# Should resolve to cname.vercel-dns.com

# Clear browser cache (Ctrl+Shift+Del or Cmd+Shift+Del)
# Try incognito/private window
```

**Common Mistakes:**
- Pointing to wrong CNAME value
- Not waiting for DNS propagation (24-48 hours)
- Mixing A and CNAME records incorrectly
- SSL certificate not auto-issued (can take 5+ minutes)

### Issue 4: 404 Errors on Deployed Site

**Solution:** Your `vercel.json` rewrites configuration:
```json
{
  "rewrites": [
    {"source": "/(.*)","destination": "/"}
  ]
}
```
This is correct for client-side routing. Verify:
1. Pages exist in `/app` directory
2. Routes are properly defined in Next.js
3. No conflicting API routes

### Issue 5: Slow Performance After Deployment

**Solutions:**
```javascript
// next.config.mjs
const nextConfig = {
  swcMinify: true,  // Enable SWC minifier
  compress: true,   // Enable compression
  
  // Image optimization
  images: {
    unoptimized: false,
    formats: ['image/avif', 'image/webp'],
  },
};

export default nextConfig;
```

**Check:**
1. Use **Analytics** tab in Vercel dashboard
2. Check **Function Logs** for slow API calls
3. Review **Rebuild Logs** for compilation issues
4. Use Next.js built-in optimization: `<Image>` component

### Issue 6: Preview Deployments Not Generating

**Solutions:**
1. Go to **Settings** → **Git** in Vercel dashboard
2. Verify **"Deploy on Push"** is enabled
3. Check **"Ignored Build Step"** - ensure PR branch is not ignored
4. Make sure GitHub integration is properly authorized
5. Try pushing again with a new commit

### Issue 7: Database Connection Timeout

**Solutions:**
```javascript
// Increase timeout for database connections
// In API routes or getServerSideProps:
const client = new DatabaseClient({
  timeout: 30000,  // 30 seconds
  connectionString: process.env.DATABASE_URL,
});

// Verify connection string format
// DATABASE_URL must include all connection params
```

---

## Quick Checklist

### Before Deploying
- [ ] All code committed and pushed to GitHub
- [ ] No `.env.local` in Git history
- [ ] `npm run build` works locally
- [ ] No console errors or warnings
- [ ] Package.json has correct build script
- [ ] All dependencies listed in package.json

### Vercel Configuration
- [ ] Project imported and connected to GitHub
- [ ] Build command: `npm run build`
- [ ] Framework: Next.js (auto-detected)
- [ ] Production branch: `main`
- [ ] All environment variables added
- [ ] Sensitive variables marked as "Sensitive"

### After First Deployment
- [ ] Verify site works at `project-name.vercel.app`
- [ ] Check for console errors in browser DevTools
- [ ] Test all pages and API routes
- [ ] Review **Build Logs** for warnings
- [ ] Monitor **Analytics** for performance

### Custom Domain Setup
- [ ] Domain purchased and accessible
- [ ] DNS configured (nameservers or CNAME)
- [ ] SSL certificate issued (status: "Ready")
- [ ] Domain redirects working
- [ ] Test at custom domain

---

## Deployment Complete! 🎉

Your Next.js project is now live on Vercel with:
- ✓ Automatic deployments from GitHub
- ✓ Preview URLs for pull requests
- ✓ Environment-specific variables
- ✓ Custom domain with SSL
- ✓ Global edge network
- ✓ Automatic scaling

**Useful Links:**
- [Vercel Dashboard](https://vercel.com/dashboard)
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
- [Vercel Monitoring](https://vercel.com/analytics)
