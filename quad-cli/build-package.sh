#!/bin/bash
#
# Build QUAD CLI Package for Downloads
# =====================================
# Creates quad-cli-X.X.X.tar.gz for downloads.quadframe.work
#
# Usage: ./build-package.sh
#
# Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION="0.1.0"
PACKAGE_NAME="quad-cli-$VERSION"
OUTPUT_DIR="$SCRIPT_DIR/dist"

echo ""
echo "Building QUAD CLI Package v$VERSION"
echo "═══════════════════════════════════"
echo ""

# Clean
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Create temp directory for packaging
TEMP_DIR=$(mktemp -d)
PACKAGE_DIR="$TEMP_DIR/quad-cli"

echo "→ Copying files..."
mkdir -p "$PACKAGE_DIR"

# Copy required files
cp -r "$SCRIPT_DIR/quad_cli" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/setup.py" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/pyproject.toml" "$PACKAGE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/README.md" "$PACKAGE_DIR/" 2>/dev/null || true

# Remove __pycache__ and .pyc files
find "$PACKAGE_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true

echo "→ Creating tarball..."
cd "$TEMP_DIR"
tar -czf "$OUTPUT_DIR/$PACKAGE_NAME.tar.gz" quad-cli

# Cleanup
rm -rf "$TEMP_DIR"

# Copy to quad-downloads for deployment
DOWNLOADS_DIR="$SCRIPT_DIR/../quad-downloads/public"
if [ -d "$DOWNLOADS_DIR" ]; then
    cp "$OUTPUT_DIR/$PACKAGE_NAME.tar.gz" "$DOWNLOADS_DIR/"
    echo "→ Copied to quad-downloads/public/"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "✓ Package created: $OUTPUT_DIR/$PACKAGE_NAME.tar.gz"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Deploy to downloads.quadframe.work:"
echo ""
echo "  cd ../quad-downloads"
echo "  firebase deploy --only hosting"
echo ""
