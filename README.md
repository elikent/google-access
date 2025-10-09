
## 🔐 Secrets & Credentials

This repo uses a Google **service account** key for automation.

### How we store it
- The key file lives **outside of version control** in `configs\.secrets\`.
- An environment variable points to it:
  - `GA_LEROF_SERVICE_ACCOUNT=/absolute/path/to/.secrets/ga-service.json`

### Permissions
- The service account has **least-privilege** roles (Drive/Shares as needed; Sheets read-only if applicable).

### Local setup
1. Create `.secrets/<file-name>.json` (gitignored).
2. Set env var (Windows PowerShell):
   ```powershell
   [Environment]::SetEnvironmentVariable("GA_WORK_SERVICE_ACCOUNT","D:\path\to\.secrets\<file-name>.json","User")
