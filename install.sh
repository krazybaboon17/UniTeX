#!/bin/bash
# UniTeX Install Script

echo "Downloading UniTeX..."

DOWNLOAD_URL="https://unitex-seven.vercel.app/unitex"

# Download the executable to a temporary location
if ! curl -# -f -L -o /tmp/unitex_download "$DOWNLOAD_URL"; then
    echo "❌ Error: Failed to download UniTeX from $DOWNLOAD_URL"
    exit 1
fi

echo "Installing to /usr/local/bin..."
# Move it to the system PATH so it can be run from anywhere. 
# We use sudo because /usr/local/bin requires admin privileges.
sudo mv /tmp/unitex_download /usr/local/bin/unitex

# Make sure it is executable
sudo chmod +x /usr/local/bin/unitex

echo ""
echo "✅ UniTeX has been successfully installed!"
echo "You can now run it from any terminal by typing: unitex"
