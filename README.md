# Cheating Model Project

This repository contains the project files for the `cheating_model` notebook and related outputs.

What's included:
- `cheating_model.ipynb` — main notebook
- `cheating_model_best.pt` — local model artifact (ignored by .gitignore by default)
- `runs/` — detection/prediction outputs (ignored by .gitignore)

Quick local setup

1. Initialize git (already done by this script):
   - `git init`
2. Create a GitHub repository on the website or with the GitHub CLI:
   - Website: create a new repo at https://github.com/new and copy the repository URL.
   - gh CLI: `gh repo create <OWNER>/<REPO> --public --source=. --remote=origin --push`

How to add a remote and push (example):

```powershell
# replace USERNAME/REPO with your GitHub repo URL
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main
```

Notes

- Large model files are ignored by default. If you want to include the model in the repo, remove `*.pt` from `.gitignore` or use Git LFS.
- If `git commit` fails due to missing user name/email, configure them:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

If you'd like, I can:
- Add the remote and push for you if you provide the GitHub remote URL, or
- Create the GitHub repository for you if you provide a personal access token (PAT) and confirm you want me to do that.
