#!/bin/bash
# UniFlow Install Script

echo "Downloading UniFlow..."

DOWNLOAD_URL="https://uniflow-seven.vercel.app/uniflow"

# Download the executable to a temporary location
if ! curl -# -f -L -o /tmp/uniflow_download "$DOWNLOAD_URL"; then
    echo "❌ Error: Failed to download UniFlow from $DOWNLOAD_URL"
    exit 1
fi

echo "Installing to /usr/local/bin..."
# Move it to the system PATH so it can be run from anywhere. 
# We use sudo because /usr/local/bin requires admin privileges.
sudo mv /tmp/uniflow_download /usr/local/bin/uniflow

# Make sure it is executable
sudo chmod +x /usr/local/bin/uniflow

echo ""
echo "✅ UniFlow has been successfully installed!"
echo "You can now run it from any terminal by typing: uniflow"
