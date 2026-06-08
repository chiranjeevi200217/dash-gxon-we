# Pre-Deployment Checklist for Vercel

## ✅ Code Quality & Preparation

- [ ] All changes committed to Git
  ```bash
  git status  # Should show "nothing to commit"
  ```

- [ ] No console.log() statements or debug code
  - Search for: `console.log`, `debugger`, `alert()`

- [ ] All imports are correct (no missing dependencies)
  ```bash
  npm run lint
  ```

- [ ] Build completes successfully locally
  ```bash
  npm run build  # No errors
  npm start      # Site loads at http://localhost:3000
  ```

- [ ] No TypeScript/ESLint errors
  ```bash
  npm run lint
  ```

- [ ] API routes and endpoints tested
  - Test all database connections
  - Test all external API calls
  - Verify error handling

- [ ] Environment variables documented
  - Create `.env.example` (without sensitive values)
  - List all required variables in README.md

## ✅ Project Structure

- [ ] `next.config.mjs` is properly configured
- [ ] `package.json` has correct build scripts
- [ ] `vercel.json` is properly configured
- [ ] `.gitignore` includes `.env.local`
- [ ] No `node_modules/` in Git
- [ ] No `.next/` build artifacts in Git

## ✅ GitHub Repository

- [ ] Repository is public or GitHub integration granted
- [ ] All code pushed to main branch
  ```bash
  git push origin main
  ```

- [ ] No sensitive data in Git history
  ```bash
  git log --all --oneline | head -20
  ```

- [ ] README.md updated with:
  - [ ] Project description
  - [ ] Setup instructions
  - [ ] Required environment variables
  - [ ] Deployment instructions

## ✅ Pre-Vercel Configuration

- [ ] Create `.env.example`
  ```
  NEXT_PUBLIC_API_URL=https://api.example.com
  DATABASE_URL=your_database_url_here
  JWT_SECRET=your_secret_here
  ```

- [ ] Update README with env vars section
- [ ] Delete any local database files
- [ ] Clear cache if needed
  ```bash
  rm -rf .next/
  npm install  # Clean reinstall
  npm run build
  ```

## ✅ Deployment Steps

### Step 1: Create Vercel Account
- [ ] Go to https://vercel.com/signup
- [ ] Sign up with GitHub account
- [ ] Authorize Vercel to access GitHub

### Step 2: Import Project
- [ ] Click "Add New" → "Project"
- [ ] Select "Import Git Repository"
- [ ] Choose your GitHub repository
- [ ] Review import settings

### Step 3: Configure Build Settings
- [ ] **Framework**: Next.js (auto-detected ✓)
- [ ] **Build Command**: `npm run build`
- [ ] **Output Directory**: `.next`
- [ ] **Install Command**: `npm install`
- [ ] **Root Directory**: `.` (if project is in root)
- [ ] **Environment Variables**: SKIP FOR NOW (add after first deploy)

### Step 4: Deploy First Version
- [ ] Click "Deploy"
- [ ] Wait for build to complete (5-10 minutes)
- [ ] Verify deployment at `project-name.vercel.app`
- [ ] Test all pages and routes
- [ ] Check browser console for errors

### Step 5: Add Environment Variables (After First Deploy)
- [ ] Go to **Settings** → **Environment Variables**
- [ ] Add each variable:
  - [ ] `NEXT_PUBLIC_API_URL`
  - [ ] `DATABASE_URL`
  - [ ] `JWT_SECRET` (mark as "Sensitive")
  - [ ] Any other required variables
- [ ] Select environments: Production / Preview / Development
- [ ] **Trigger Redeploy** (automatic after save)

### Step 6: Test After Redeploy
- [ ] Visit deployed site at `project-name.vercel.app`
- [ ] Verify environment variables are working
- [ ] Test API routes
- [ ] Check database connections

### Step 7: Set Up Custom Domain (Optional)
- [ ] Purchase domain (e.g., yourdomain.com)
- [ ] In Vercel: **Settings** → **Domains**
- [ ] Click **"Add"** → **"Add Custom Domain"**
- [ ] Enter domain name
- [ ] Choose DNS setup method:
  - [ ] **Nameserver Transfer** (recommended)
    - Update registrar nameservers to Vercel
    - Wait 24-48 hours
  - OR
  - [ ] **CNAME Record**
    - Add CNAME: `www` → `cname.vercel-dns.com`
    - Add A record: `@` → `76.76.19.124`
    - Wait for SSL certificate (5 minutes)

### Step 8: Enable Git Integration Features (After Deploy)
- [ ] Go to **Settings** → **Git**
- [ ] Verify **"Deploy on Push"** is enabled
- [ ] Check **"Deploy on Pull Requests"** is enabled
- [ ] Set **"Production Branch"** to `main`

## ✅ Post-Deployment Testing

### Functional Testing
- [ ] Homepage loads
- [ ] Navigation works
- [ ] All pages accessible
- [ ] API endpoints respond correctly
- [ ] Database queries work
- [ ] Forms submit successfully
- [ ] Error pages display (404, 500, etc.)

### Performance Testing
- [ ] Page load time < 3 seconds
- [ ] No JavaScript errors in console
- [ ] Images load properly
- [ ] CSS/styling correct
- [ ] Responsive design works on mobile
- [ ] No CORS errors

### Security Testing
- [ ] No hardcoded secrets visible in code
- [ ] HTTPS is enforced
- [ ] API authentication working
- [ ] Environment variables not exposed

### Mobile Testing
- [ ] Responsive layout correct
- [ ] Touch interactions work
- [ ] Fonts readable at small sizes
- [ ] No horizontal scroll

## ✅ Monitoring Setup

- [ ] Set up error tracking (optional)
  - Sentry, LogRocket, or similar
- [ ] Enable Vercel Analytics
  - **Settings** → **Analytics** → Enable
- [ ] Monitor build times
  - Target: < 5 minutes
- [ ] Set up alerts for failed deployments
- [ ] Review first week of analytics

## ✅ Maintenance

- [ ] Set up monitoring alerts
- [ ] Plan update schedule
- [ ] Document deployment process
- [ ] Create rollback procedure
- [ ] Schedule performance reviews

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Build fails | Check build logs, ensure all deps in package.json |
| Env vars not working | Redeploy after adding, verify variable names |
| 404 errors | Check route configuration, verify files exist |
| Slow performance | Enable caching, optimize images, check function logs |
| Domain not resolving | Wait 24-48h for DNS, verify CNAME/A records |

## Emergency Contacts & Resources

- **Vercel Support**: https://vercel.com/support
- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Status Page**: https://vercel-status.com

---

## Quick Links

- [Vercel Dashboard](https://vercel.com/dashboard)
- [Your Project Deployments](https://vercel.com/dashboard/projects)
- [Project Settings](https://vercel.com/dashboard/[project]/settings)
- [Analytics](https://vercel.com/dashboard/[project]/analytics)

---

**Last Updated**: June 8, 2026
**Next Review**: After first deployment
