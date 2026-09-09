#!/bin/bash
# QUAD CLI Build and Deploy Script
# ==================================
#
# Builds QUAD CLI package and deploys to Firebase hosting.
#
# Usage:
#   ./build-and-deploy.sh            # Build and deploy
#   ./build-and-deploy.sh --build    # Build only
#   ./build-and-deploy.sh --deploy   # Deploy only
#
# Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper functions
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${YELLOW}→ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

header() {
    echo ""
    echo "═══════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════"
    echo ""
}

# Parse arguments
BUILD_ONLY=false
DEPLOY_ONLY=false

if [ "$1" == "--build" ]; then
    BUILD_ONLY=true
elif [ "$1" == "--deploy" ]; then
    DEPLOY_ONLY=true
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ─────────────────────────────────────────────────────────────
# 1. BUILD
# ─────────────────────────────────────────────────────────────

if [ "$DEPLOY_ONLY" == false ]; then
    header "Building QUAD CLI Package"

    # Check Python version
    info "Checking Python version..."
    python3 --version || error "Python 3 not found. Install Python 3.10+"
    success "Python found"

    # Clean previous builds
    info "Cleaning previous builds..."
    rm -rf build/ dist/ *.egg-info
    success "Cleaned"

    # Build source distribution
    info "Building source distribution..."
    python3 setup.py sdist || error "Source distribution build failed"
    success "Source distribution created"

    # Build wheel distribution
    info "Building wheel distribution..."
    python3 setup.py bdist_wheel || error "Wheel distribution build failed"
    success "Wheel distribution created"

    # Show build artifacts
    echo ""
    info "Build artifacts:"
    ls -lh dist/
    echo ""

    # Get version
    VERSION=$(python3 -c "from quad_cli import __version__; print(__version__)")
    success "Built QUAD CLI v${VERSION}"
fi

# ─────────────────────────────────────────────────────────────
# 2. DEPLOY
# ─────────────────────────────────────────────────────────────

if [ "$BUILD_ONLY" == false ]; then
    header "Deploying to Firebase"

    # Check if dist/ exists
    if [ ! -d "dist" ]; then
        error "dist/ folder not found. Run with --build first."
    fi

    # Check firebase CLI
    info "Checking Firebase CLI..."
    if ! command -v firebase &> /dev/null; then
        error "Firebase CLI not found. Install with: npm install -g firebase-tools"
    fi
    success "Firebase CLI found"

    # Check login status
    info "Checking Firebase login..."
    firebase projects:list > /dev/null 2>&1 || error "Not logged into Firebase. Run: firebase login"
    success "Firebase authenticated"

    # Prepare deployment directory
    info "Preparing deployment files..."

    # Create public directory structure
    mkdir -p public/dist

    # Copy build artifacts
    cp -r dist/* public/dist/
    success "Build artifacts copied"

    # Create/update install script
    info "Creating install script..."

    cat > public/install.sh << 'EOF'
#!/bin/bash
# QUAD CLI Installation Script
# =============================
#
# Installs QUAD CLI from downloads.quadframe.work
#
# Usage:
#   curl -fsSL https://downloads.quadframe.work/install.sh | bash
#
# Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${YELLOW}→ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

echo ""
echo "═══════════════════════════════════════"
echo "  QUAD CLI Installation"
echo "═══════════════════════════════════════"
echo ""

# Check Python
info "Checking Python..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 not found. Install Python 3.10+ first."
fi
success "Python 3 found"

# Get latest version
info "Fetching latest version..."
LATEST_VERSION=$(curl -s https://downloads.quadframe.work/latest.txt || echo "0.1.0")
success "Latest version: v${LATEST_VERSION}"

# Download and install
info "Downloading QUAD CLI..."
pip3 install "quad-cli==${LATEST_VERSION}" || \
    pip3 install --upgrade "https://downloads.quadframe.work/dist/quad-cli-${LATEST_VERSION}.tar.gz"

success "QUAD CLI installed successfully!"

# Verify installation
info "Verifying installation..."
quad --version || error "Installation verification failed"

echo ""
echo "═══════════════════════════════════════"
echo "  Installation Complete!"
echo "═══════════════════════════════════════"
echo ""
echo "Quick Start:"
echo "  quad login                    # Login to QUAD"
echo "  quad init my-project          # Create new project"
echo "  quad story create             # Generate stories"
echo "  quad code generate            # Generate code"
echo ""
echo "Documentation: https://quadframe.work/docs"
echo ""
EOF

    chmod +x public/install.sh
    success "Install script created"

    # Create version file
    echo "$VERSION" > public/latest.txt
    success "Version file created"

    # Create index page
    info "Creating landing page..."

    cat > public/index.html << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QUAD CLI Downloads</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            max-width: 800px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        h1 { font-size: 3em; margin-bottom: 20px; }
        p { font-size: 1.2em; margin-bottom: 30px; opacity: 0.9; }
        .version { font-size: 0.9em; opacity: 0.7; margin-bottom: 40px; }
        .install-box {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            margin: 30px 0;
        }
        code {
            display: block;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 1.1em;
            padding: 15px;
            background: rgba(0,0,0,0.4);
            border-radius: 5px;
            overflow-x: auto;
        }
        .links {
            display: flex;
            gap: 20px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        a {
            color: #fff;
            text-decoration: none;
            padding: 12px 24px;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
            transition: all 0.3s;
        }
        a:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 QUAD CLI</h1>
        <p>Quick Unified Agentic Development</p>
        <div class="version">Latest Version: v${VERSION}</div>

        <h2 style="margin-bottom: 15px;">Installation</h2>
        <div class="install-box">
            <code>curl -fsSL https://downloads.quadframe.work/install.sh | bash</code>
        </div>

        <h2 style="margin: 30px 0 15px;">Quick Start</h2>
        <div class="install-box">
            <code>quad login<br>quad init my-project<br>quad story create<br>quad code generate</code>
        </div>

        <div class="links">
            <a href="https://quadframe.work">Website</a>
            <a href="https://quadframe.work/docs">Documentation</a>
            <a href="https://github.com/a2vibes/QUAD">GitHub</a>
            <a href="dist/">Download Files</a>
        </div>

        <p style="margin-top: 40px; font-size: 0.9em; opacity: 0.6;">
            © 2026 Gopi Suman Addanke. All Rights Reserved.
        </p>
    </div>
</body>
</html>
EOF

    success "Landing page created"

    # Deploy to Firebase
    info "Deploying to Firebase..."
    firebase deploy --only hosting || error "Firebase deployment failed"

    success "Deployed to Firebase!"

    echo ""
    success "QUAD CLI v${VERSION} is now live at:"
    info "  https://downloads.quadframe.work"
    info "  https://downloads.quadframe.work/install.sh"
    info "  https://downloads.quadframe.work/dist/"
fi

# ─────────────────────────────────────────────────────────────
# DONE!
# ─────────────────────────────────────────────────────────────

header "Build and Deploy Complete!"

if [ "$BUILD_ONLY" == false ] && [ "$DEPLOY_ONLY" == false ]; then
    echo "Next steps:"
    echo "  1. Test installation: curl -fsSL https://downloads.quadframe.work/install.sh | bash"
    echo "  2. Announce release on GitHub"
    echo "  3. Update documentation"
    echo ""
fi
