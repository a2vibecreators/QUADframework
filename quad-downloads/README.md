# QUAD Downloads Site

**URL:** https://quad-downloads-b0c99.web.app
**Custom Domain (pending):** https://downloads.quadframe.work

Static file hosting for QUAD CLI installer.

## Files

| File | Purpose |
|------|---------|
| `install.sh` | Installer script |
| `quad-cli-X.X.X.tar.gz` | CLI package |

## Deploy

```bash
cd QUAD/quad-downloads
firebase deploy --only hosting
```

## Update CLI Package

```bash
# 1. Build new package (auto-copies to quad-downloads/public/)
cd QUAD/quad-cli
./build-package.sh

# 2. Update version in install.sh if needed
# Edit quad-downloads/public/install.sh → QUAD_VERSION="X.X.X"

# 3. Deploy
cd ../quad-downloads
firebase deploy --only hosting
```

## Hosted by

Firebase Hosting (project: quad-downloads-b0c99)
