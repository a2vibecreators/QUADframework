#!/bin/bash
#
# QUAD CLI Installer
# ==================
# Installs QUAD CLI commands
#
# Usage: curl -fsSL https://quad-downloads-b0c99.web.app/install.sh | bash
#
# Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.

set -e

QUAD_VERSION="0.1.0"
DOWNLOAD_BASE="https://quad-downloads-b0c99.web.app"
QUAD_DIR="$HOME/.quad"

echo ""
echo "  ╔═══════════════════════════════════════════╗"
echo "  ║     QUAD - Quick Unified Agentic Dev      ║"
echo "  ║         CLI Installer v$QUAD_VERSION            ║"
echo "  ╚═══════════════════════════════════════════╝"
echo ""

# ─────────────────────────────────────────────────
# Check Prerequisites
# ─────────────────────────────────────────────────
echo "→ Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  ✗ Python 3 not found!"
    echo "    Install: brew install python@3.11"
    exit 1
fi
echo "  ✓ Python 3 found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "  ✗ pip3 not found!"
    exit 1
fi
echo "  ✓ pip3 found"

# ─────────────────────────────────────────────────
# Install QUAD CLI
# ─────────────────────────────────────────────────
echo ""
echo "→ Installing QUAD CLI..."

mkdir -p "$QUAD_DIR"
cd "$QUAD_DIR"

# Download and extract
curl -fsSL "$DOWNLOAD_BASE/quad-cli-$QUAD_VERSION.tar.gz" -o quad-cli.tar.gz
tar -xzf quad-cli.tar.gz
rm quad-cli.tar.gz

# Install
cd quad-cli
pip3 install --user --break-system-packages . 2>/dev/null || \
pip3 install --user . 2>/dev/null || \
pip3 install .

cd "$HOME"

# ─────────────────────────────────────────────────
# Update PATH
# ─────────────────────────────────────────────────
echo ""
echo "→ Updating PATH..."

# Get Python user bin directory (handles macOS Library/Python/x.x/bin)
PYTHON_USER_BASE=$(python3 -m site --user-base 2>/dev/null)
PYTHON_BIN="$PYTHON_USER_BASE/bin"

# Also check common locations
LOCAL_BIN="$HOME/.local/bin"

# Determine which bin directory has quad
if [ -f "$PYTHON_BIN/quad" ]; then
    TARGET_BIN="$PYTHON_BIN"
elif [ -f "$LOCAL_BIN/quad" ]; then
    TARGET_BIN="$LOCAL_BIN"
else
    TARGET_BIN="$PYTHON_BIN"
fi

# Add to PATH if not already there
if [[ ":$PATH:" != *":$TARGET_BIN:"* ]]; then
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        # Check if already in shell rc
        if ! grep -q "$TARGET_BIN" "$SHELL_RC" 2>/dev/null; then
            echo "export PATH=\"$TARGET_BIN:\$PATH\"" >> "$SHELL_RC"
            echo "  ✓ Added $TARGET_BIN to $SHELL_RC"
        fi
    fi
    export PATH="$TARGET_BIN:$PATH"
fi

# ─────────────────────────────────────────────────
# Verify
# ─────────────────────────────────────────────────
echo ""
echo "→ Verifying installation..."

if command -v quad &> /dev/null; then
    echo "  ✓ quad command available"
    quad --version
else
    echo "  ✓ Installation complete"
    echo "  → Run this to use quad now:"
    echo "    export PATH=\"$TARGET_BIN:\$PATH\""
    echo ""
    echo "  → Or restart your terminal"
fi

# ─────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────
echo ""
echo "  ═══════════════════════════════════════════════"
echo "  ✓ QUAD CLI Installed!"
echo "  ═══════════════════════════════════════════════"
echo ""
echo "  Quick Start:"
echo "  ────────────"
echo "    quad login                 # Login"
echo "    quad init banking-portal   # Create new project"
echo "    cd banking-portal"
echo "    quad story create          # Generate user stories"
echo "    quad code generate         # Generate code"
echo "    quad test                  # Run tests"
echo ""
echo "  Help: quad --help"
echo "  Docs: https://quadframe.work/docs"
echo ""
