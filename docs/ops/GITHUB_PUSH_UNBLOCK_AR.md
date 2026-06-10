# إلغاء حظر git push (403)

إذا ظهر `Permission denied to VoXc2 (403)`:

```powershell
gh auth login -h github.com -p https -s repo
gh auth setup-git
powershell -File scripts/push_main_with_gh.ps1
```

بديل API:

```powershell
py -3 scripts/push_via_gh_api.py
```

تحقق: `git fetch origin && git log origin/main -1 --oneline`
