# FreeRDP GUI Wrapper
## Overview & User Guide

---

## 📋 Overview

The **FreeRDP GUI Wrapper** is a user-friendly cross-platform desktop application that provides a graphical interface for the powerful FreeRDP remote desktop client. Instead of memorizing complex command-line parameters, users can simply fill out forms and manage multiple connection profiles through an intuitive tabbed interface.

### Key Benefits
- **No command-line knowledge required** - Point-and-click interface for all FreeRDP features
- **Cross-platform compatibility** - Works seamlessly on Windows, Linux, and macOS
- **Connection management** - Save, load, and organize multiple RDP connection profiles
- **PuTTY-style interface** - Familiar workflow for IT professionals
- **Complete feature coverage** - Access to all major FreeRDP options through organized tabs
- **Portable** - Can be compiled to a single executable file

---

## 🚀 Features

### Connection Management
- **Save/Load Connections**: Store unlimited connection profiles with all settings
- **Quick Connect**: Fast one-time connections without saving
- **Import/Export**: Backup and share connection profiles
- **Auto-save**: Remembers your last-used settings

### Comprehensive Settings
- **Basic Settings**: Server, credentials, display resolution, color depth
- **Advanced Options**: Clipboard, drive redirection, performance tuning, gateway support
- **Expert Features**: Security protocols, graphics acceleration, custom parameters
- **Real-time Preview**: See the exact command that will be executed

### User Experience
- **Auto-detection**: Automatically finds wFreeRDP executable
- **Command Generation**: Shows the complete command for learning or manual execution
- **Error Handling**: Clear error messages and validation
- **Modern Interface**: Clean, professional GUI with organized tabs

---

## 📥 Installation & Setup

### Prerequisites
- **Python 3.6+** (for running the script directly)
- **FreeRDP** executable installed on your system

### FreeRDP Installation by Platform

#### **Windows**
- **wFreeRDP**: Download from GitHub releases or FreeRDP website
- **Package Managers**: `choco install freerdp` (Chocolatey) or `winget install FreeRDP`
- **Manual**: Extract to Program Files and add to PATH

#### **Linux** 
```bash
# Ubuntu/Debian (works on all desktop environments: GNOME, KDE, XFCE, etc.)
sudo apt update && sudo apt install freerdp2-x11

# CentOS/RHEL/Fedora
sudo dnf install freerdp        # Fedora
sudo yum install freerdp        # CentOS/RHEL

# Arch Linux
sudo pacman -S freerdp

# openSUSE
sudo zypper install freerdp
```

#### **macOS**
```bash
# Homebrew (recommended)
brew install freerdp

# MacPorts
sudo port install freerdp
```

### Option 1: Download Compiled Executable
1. Download the appropriate executable for your platform:
   - **Windows**: `FreeRDP_GUI.exe` 
   - **Linux**: `FreeRDP_GUI` (AppImage or native binary)
   - **macOS**: `FreeRDP_GUI.app` or native binary
2. Place it in any folder
3. Double-click to run - no installation required!

### Option 2: Run Python Script
1. Ensure Python 3.6+ is installed
2. Download `freerdp_gui.py`
3. Run: `python freerdp_gui.py`

### First-Time Setup
1. **Launch the application**
2. **Go to Expert tab** → FreeRDP Executable section
3. **Auto-detection**: The app automatically searches for FreeRDP executables:
   - **Windows**: `wfreerdp.exe`, `xfreerdp.exe`, `freerdp.exe`
   - **Linux**: `xfreerdp`, `freerdp`
   - **macOS**: `xfreerdp`, `freerdp`
4. **Manual selection**: Use Browse if auto-detection fails
5. **Test connection** with Quick Connect to verify setup

---

## 💻 User Guide

### Getting Started

#### Quick Connect (Fastest Method)
1. **Open the Connections tab**
2. **Enter Host**: Type server IP or hostname (e.g., `192.168.1.100`)
3. **Enter Username** (optional): Your login username
4. **Click "Quick Connect"** - Connects immediately without saving

#### Creating Your First Saved Connection
1. **Go to Basic tab**
2. **Fill in connection details**:
   - **Remote Host**: Server IP or hostname *(required)*
   - **Port**: Usually 3389 (default)
   - **Username**: Your login name
   - **Domain**: Windows domain (if applicable)
   - **Password**: Optional (can enter at connection time)

3. **Configure display** (optional):
   - **Resolution**: Set width/height or check fullscreen
   - **Color Depth**: 32-bit recommended for best quality

4. **Go to Connections tab**
5. **Enter Connection Name**: Give it a memorable name
6. **Click "Save As..."**
7. **Click "Connect"** or select from list and "Load" → "Connect"

---

### Tab-by-Tab Guide

#### 🔗 Connections Tab
**Purpose**: Manage and organize your connection profiles

**Saved Connections Section**:
- **Connection List**: Shows all saved connections with server info
- **Load**: Loads selected connection settings into all tabs
- **Save As...**: Saves current form settings as new connection
- **Delete**: Removes connection (with confirmation)
- **Rename**: Changes connection name
- **Connection Name Field**: Name for new connections (auto-filled if empty)

**Quick Connect Section**:
- **Host**: Server address for one-time connections
- **Username**: Optional username
- **Quick Connect**: Connect without saving
- **Save & Connect**: Save as new connection and connect immediately

**💡 Pro Tips**:
- Double-click connections to load them quickly
- Use descriptive names like "Work Server" or "Home PC"
- Quick Connect is perfect for temporary or one-off connections

#### 🖥️ Basic Tab
**Purpose**: Essential connection settings that most users need

**Connection Details**:
- **Remote Host**: Server IP address or hostname *(required)*
- **Port**: RDP port (3389 is standard)
- **Username**: Login username
- **Domain**: Windows domain (use DOMAIN\username format)
- **Password**: Can be left blank to prompt at connection time

**Display Settings**:
- **Width/Height**: Custom resolution (e.g., 1920x1080)
- **Fullscreen**: Uses entire screen (press Ctrl+Alt+Enter to exit)
- **Color Depth**: 32-bit for best quality, lower for slower connections

**💡 Pro Tips**:
- Leave password blank for security - you'll be prompted
- Use fullscreen for immersive experience
- Try 16-bit color depth for slow networks

#### ⚙️ Advanced Tab  
**Purpose**: Performance tuning, redirection, and gateway settings

**Redirection Options**:
- **Clipboard**: Copy/paste between local and remote computers
- **Drive/Folder**: Share local folders with remote session
- **Printer**: Access local printers from remote session
- **Microphone**: Use local microphone in remote session

**Performance & Visual**:
- **Compression**: Reduces bandwidth usage (enable for slow connections)
- **Smooth Fonts**: ClearType font rendering
- **Desktop Composition**: Aero glass effects (disable for performance)
- **Themes**: Windows visual themes (disable for performance)
- **Wallpaper**: Desktop background (disable for performance)

**Gateway Settings**:
- **Gateway Host**: RD Gateway server for secure external connections
- **Gateway User**: Username for gateway authentication

**💡 Pro Tips**:
- Enable clipboard for easy file transfer via copy/paste
- Disable visual effects (Aero, themes, wallpaper) for slow connections
- Use drive redirection to access local files remotely

#### 🔧 Expert Tab
**Purpose**: Advanced security, graphics, and customization options

**FreeRDP Executable**:
- **Path**: Location of FreeRDP executable (auto-detected for most installations)
- **Browse**: Manually locate the executable
- **Supported executables**: 
  - **Windows**: `wfreerdp.exe`, `xfreerdp.exe`, `freerdp.exe`
  - **Linux/Mac**: `xfreerdp`, `freerdp`

**Security & Protocol**:
- **Security Protocol**: Force specific authentication (usually auto is best)
- **Ignore Certificate Errors**: Skip SSL certificate validation
- **Admin/Console Session**: Connect to console session

**Advanced Graphics**:
- **GDI Rendering**: Software vs hardware graphics rendering
- **RemoteFX**: Advanced graphics acceleration (if supported)
- **Multi-monitor**: Span session across multiple monitors

**Custom Parameters**:
- **Additional Parameters**: Any extra wfreerdp command-line options

**💡 Pro Tips**:
- Only change security settings if you understand the implications
- Try hardware GDI rendering for better graphics performance
- Use custom parameters for advanced features not in the GUI

---

### Common Workflows

#### Setting Up a Work Connection
1. **Basic Tab**: Enter server, username, domain
2. **Advanced Tab**: Enable clipboard, disable visual effects for performance
3. **Connections Tab**: Save as "Work Server"

#### Configuring Home PC Access
1. **Basic Tab**: Enter home IP, credentials
2. **Advanced Tab**: Enable full visual effects, drive redirection
3. **Expert Tab**: Set up gateway if connecting from outside network
4. **Connections Tab**: Save as "Home PC"

#### Quick Troubleshooting Connection
1. **Connections Tab**: Quick Connect with just IP address
2. **Test basic connectivity first**
3. **If successful, use "Save & Connect" to create permanent profile**

---

## 🔧 Advanced Usage

### Command Preview
- **Click "Show Command"** to see the exact FreeRDP command
- **Copy to clipboard** for manual execution or scripting
- **Learn command-line syntax** for advanced usage

### File Locations
**Windows:**
- **Connections**: `C:\Users\[username]\.freerdp_connections.json`
- **Last Settings**: `C:\Users\[username]\.freerdp_last_settings.json`

**Linux/macOS:**
- **Connections**: `~/.freerdp_connections.json`
- **Last Settings**: `~/.freerdp_last_settings.json`

**Backup**: Copy JSON files to preserve connections across systems

### Fullscreen Mode Tips
- **Enter**: Check fullscreen option or press Ctrl+Alt+Enter
- **Exit**: Press Ctrl+Alt+Enter to toggle back to windowed
- **Access local desktop**: Press Ctrl+Alt+Home for connection bar
- **Force exit**: Alt+Tab to local desktop, then close RDP window

---

## 🛠️ Troubleshooting

### Common Issues

**"FreeRDP executable not found"**
- Go to Expert tab → Browse for FreeRDP executable
- Install FreeRDP package for your operating system:
  - **Windows**: Download wFreeRDP or use package manager
  - **Linux**: `sudo apt install freerdp2-x11` (Ubuntu/Debian)
  - **macOS**: `brew install freerdp`
- Check if FreeRDP is in your system PATH
- Try different executable names (xfreerdp vs freerdp vs wfreerdp)

**"Can't connect to server"**
- Verify server IP/hostname is correct
- Check port 3389 is open (or custom port)
- Ensure RDP is enabled on target server
- Test with Quick Connect first

**"Connection works but no clipboard/drives"**
- Enable specific redirection options in Advanced tab
- Some servers disable redirection for security
- Try different security protocol in Expert tab

**Application won't start**
- Ensure Python 3.6+ is installed (for script version)
- **Linux**: Install tkinter: `sudo apt install python3-tk` (Ubuntu/Debian)
- **macOS**: Use system Python or install tkinter support
- Check antivirus isn't blocking the executable

### Performance Optimization
- **Slow connections**: Disable Aero, themes, wallpaper; enable compression
- **Fast local network**: Enable all visual effects for best experience
- **Multiple monitors**: Enable multi-monitor support in Expert tab

---

## 🔐 Security Notes

### Password Security
- **Avoid saving passwords** in connection profiles when possible
- **Use domain authentication** when available
- **Consider certificate-based authentication** for high-security environments

### Network Security
- **Use RD Gateway** for external connections instead of direct RDP
- **Enable NLA security** protocol when supported
- **Don't ignore certificate errors** unless you understand the risks

---

## 📚 Additional Resources

### Learning More
- **FreeRDP Documentation**: [Official FreeRDP Wiki](https://github.com/FreeRDP/FreeRDP/wiki)
- **Cross-platform support**: Works on Windows, Linux (all DEs), and macOS
- **RDP Protocol**: Microsoft Remote Desktop Protocol documentation
- **Security Best Practices**: Microsoft RDP security guidelines

### Getting Help
- **Test with command preview**: Use "Show Command" to debug issues
- **Check FreeRDP logs**: Run command manually to see detailed error messages
- **Verify server settings**: Ensure target server has RDP enabled and configured
- **Platform-specific issues**: Check FreeRDP installation for your OS

---

## 🌍 Platform-Specific Notes

### **Windows**
- Supports all FreeRDP variants (wFreeRDP, standard FreeRDP builds)
- Auto-detects installations in Program Files
- Executable extensions: `.exe`

### **Linux** 
- Works on all desktop environments (GNOME, KDE, XFCE, MATE, Cinnamon, Unity)
- Package `freerdp2-x11` provides `xfreerdp` command
- Supports Snap packages and Flatpak installations
- No executable extensions needed

### **macOS**
- Supports Homebrew and MacPorts installations  
- May require granting accessibility permissions
- Works with both Intel and Apple Silicon Macs

---

## 📄 License & Credits

This GUI wrapper is designed to make FreeRDP more accessible to users who prefer graphical interfaces over command-line tools. The underlying remote desktop functionality is provided by the excellent FreeRDP project.

**FreeRDP GUI Wrapper** - Making cross-platform remote desktop connections simple and manageable.
