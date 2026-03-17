# NBS System Admin Guide — Contributor Workflow

## Setup

1. Install [VS Code](https://code.visualstudio.com/download)
2. Install the [GitHub Repositories extension](https://marketplace.visualstudio.com/items?itemName=GitHub.remotehub), if you don't have it already.
3. Open VS Code and select **Clone Git Repository** on the splash page
4. Paste `https://github.com/CDCgov/NEDSS-SystemAdminGuide` and press Enter
5. Choose your root user folder as the location
6. Select **Yes** when prompted to open the repo folder
7. Open a terminal: **Terminal > New Terminal**

Your prompt should look something like:
```
admin@your-MacBook-Pro NEDSS-SystemAdminGuide %
```

### One-time git configuration

Run these once on your machine after setup:

**Auto-track remote branches** — lets you run `git push` on a new branch without needing `-u origin branchname`:
```bash
git config --global push.autoSetupRemote true
```

**Tab completion for branch names** — press Tab after `git checkout ` or `git merge ` to autocomplete branch names.

- **macOS (zsh, the default shell):** zsh includes git completion but it must be initialized. Add these lines to your `~/.zshrc` if they aren't already there:
  ```bash
  autoload -Uz compinit && compinit
  ```
  Then reload your shell or open a new terminal:
  ```bash
  source ~/.zshrc
  ```
- **macOS (bash):**
  ```bash
  brew install bash-completion
  ```
  Then add this line to your `~/.bash_profile`:
  ```bash
  [[ -r "$(brew --prefix)/etc/profile.d/bash_completion.sh" ]] && . "$(brew --prefix)/etc/profile.d/bash_completion.sh"
  ```
- **Windows (Git Bash):** included with [Git for Windows](https://git-scm.com/download/win) — no action needed.


## Branch Naming

Prefix with your initials and use a descriptive name:
```
js/add-authentication-docs
js/STLT-123-authentication
```


## Daily Workflow

### 1. Start from an up-to-date `main`

```bash
git checkout main
git pull
git checkout -b your-initials/short-description
```

### 2. Make your changes and commit

```bash
git add <changed files>
git commit -m "Describe what you changed"
```

Repeat as needed. Push your feature branch to keep it backed up on remote:

```bash
git push -u origin your-initials/short-description
```

### 3. Stage for stakeholder review

Sync `preview` with `main` first to avoid conflicts, then merge your feature branch in:

```bash
git checkout preview
git pull origin preview
git merge main
git merge your-initials/short-description
```

If there are merge conflicts, resolve them before continuing. Then push to trigger the preview site deploy:

```bash
git push origin preview
```

The preview site will update within a minute or two:
https://jburgh.github.io/CDCgov-NEDSS-SystemAdminGuide-preview/

Share that URL with stakeholders and collect feedback.

### 4. Iterate

For each round of revisions, update your feature branch and re-push to `preview`:

```bash
git checkout your-initials/short-description
# make edits
git add <changed files>
git commit -m "Updates from review"
git checkout preview
git merge your-initials/short-description
```

Resolve any conflicts, then push:

```bash
git push origin preview
```

### 5. Merge to `main` when approved

Open a PR on GitHub from your **feature branch** to `main` — not from `preview` to `main`.

Go to https://github.com/CDCgov/NEDSS-SystemAdminGuide — GitHub will show a prompt to open a PR for your recently pushed branch.

After the PR is approved and merged, the production site updates automatically:
https://cdcgov.github.io/NEDSS-SystemAdminGuide/

### 6. Clean up

```bash
git checkout main
git pull
git branch -d your-initials/short-description
git push origin --delete your-initials/short-description
```


## Useful Commands

| Command | What it does |
|---------|--------------|
| `git status` | Show current branch and any uncommitted changes |
| `git branch` | List all local branches |
| `git checkout branchname` | Switch to an existing branch |
| `git pull` | Pull latest changes from remote |
| `git log --oneline -10` | See last 10 commits |


## Further Reading

- [Five rules of Git hygiene](https://cbea.ms/git-commit/)
- [GitHub Docs](https://docs.github.com)
