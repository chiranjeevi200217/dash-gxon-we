# Vercel Deployment Quick Reference

## 🚀 One-Command Deployment

```bash
# Push to GitHub (Vercel auto-deploys)
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

Then go to: https://vercel.com/new

---

## 📋 Essential Environment Variables

**For Production:**
```
DATABASE_URL = [your_production_db_url]
JWT_SECRET = [your_secret_key]
NEXT_PUBLIC_API_URL = https://yourdomain.com/api
```

**For Development:**
```
DATABASE_URL = [your_local_db_url]
JWT_SECRET = [your_secret_key]
NEXT_PUBLIC_API_URL = http://localhost:3000/api
```

---

## ✅ Pre-Deployment Checks

```bash
# 1. Build locally
npm run build

# 2. Test production build
npm start

# 3. Run linter
npm run lint

# 4. Check git status
git status
```

---

## 🔗 Important Links

| Action | Link |
|--------|------|
| **Deploy** | https://vercel.com/new |
| **Dashboard** | https://vercel.com/dashboard |
| **Docs** | https://vercel.com/docs |
| **GitHub Integration** | https://vercel.com/integrations/github |

---

## 📍 After Deployment

1. ✓ Visit your deployment: `https://[project-name].vercel.app`
2. ✓ Add environment variables: Settings → Environment Variables
3. ✓ Trigger redeploy (automatic after adding env vars)
4. ✓ Configure custom domain (optional): Settings → Domains
5. ✓ Enable analytics: Settings → Analytics

---

## 🆘 Need Help?

- Build fails? → Check [Build Logs](https://vercel.com/dashboard/[project]/logs)
- Env vars not working? → Redeploy after adding them
- Domain not working? → DNS takes 24-48 hours
- Performance issue? → Check [Analytics](https://vercel.com/dashboard/[project]/analytics)

See **VERCEL_DEPLOYMENT_GUIDE.md** for complete instructions.
