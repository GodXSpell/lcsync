#!/bin/bash
# LeetCode Sync Setup Script for Unix/Linux/Mac

echo "🚀 Setting up LeetCode Sync (lcsync) for Unix/Linux/Mac..."

# Make the shell script executable
chmod +x lcsync.sh
echo "✅ Made lcsync executable"

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found: $(python3 --version)"
else
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    python3 -m pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️  requirements.txt not found"
fi

# Test the installation
echo "🧪 Testing installation..."
./lcsync help

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Quick usage:"
echo "  ./lcsync init      # Initialize project"
echo "  ./lcsync user      # Set up user"
echo "  ./lcsync cookie    # Add LeetCode session"
echo "  ./lcsync fetch     # Fetch submissions"
echo "  ./lcsync push      # Push to GitHub"
echo ""
echo "💡 To use from anywhere, add this directory to your PATH:"
echo "   export PATH=\"\$PATH:$(pwd)\""