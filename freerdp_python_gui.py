#!/usr/bin/env python3
r"""
FreeRDP GUI Wrapper
A user-friendly cross-platform interface for FreeRDP with connection management
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter import LEFT, RIGHT, TOP, BOTTOM, BOTH, X, Y, W, E, NORMAL, DISABLED
import json
import os
import subprocess
import sys
from pathlib import Path


class FreeRDPGUI:
    def __init__(self, root):
        self.password_var = None
        self.domain_var = None
        self.username_var = None
        self.port_var = None
        self.server_var = None
        self.freerdp_path_var = None
        self.notebook = None
        self.root = root
        self.root.title("FreeRDP GUI Wrapper")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Configuration file for saved connections
        self.config_file = Path.home() / ".freerdp_connections.json"
        self.connections = self.load_connections()

        # Variables for form fields
        self.setup_variables()

        # Create the GUI
        self.create_widgets()

        # Find FreeRDP executable
        self.find_freerdp()

        # Load last used settings
        self.load_last_settings()

    def setup_variables(self):
        """Initialize all tkinter variables"""
        # Basic tab variables
        self.server_var = tk.StringVar()
        self.port_var = tk.StringVar(value="3389")
        self.username_var = tk.StringVar()
        self.domain_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.width_var = tk.StringVar(value="1920")
        self.height_var = tk.StringVar(value="1080")
        self.fullscreen_var = tk.BooleanVar()
        self.color_depth_var = tk.StringVar(value="32")

        # Advanced tab variables
        self.clipboard_var = tk.BooleanVar()
        self.drive_redirect_var = tk.StringVar()
        self.printers_var = tk.BooleanVar()
        self.microphone_var = tk.BooleanVar()
        self.compression_var = tk.BooleanVar()
        self.fonts_var = tk.BooleanVar()
        self.aero_var = tk.BooleanVar(value=True)
        self.themes_var = tk.BooleanVar(value=True)
        self.wallpaper_var = tk.BooleanVar(value=True)
        self.gateway_var = tk.StringVar()
        self.gateway_user_var = tk.StringVar()

        # Expert tab variables
        self.freerdp_path_var = tk.StringVar()
        self.security_var = tk.StringVar()
        self.cert_ignore_var = tk.BooleanVar()
        self.admin_session_var = tk.BooleanVar()
        self.gdi_mode_var = tk.StringVar()
        self.remotefx_var = tk.BooleanVar()
        self.multimon_var = tk.BooleanVar()
        self.custom_params_var = tk.StringVar()

        # Connection management variables
        self.connection_name_var = tk.StringVar()
        self.quick_server_var = tk.StringVar()
        self.quick_user_var = tk.StringVar()

    def create_widgets(self):
        """Create the main GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.create_basic_tab()
        self.create_advanced_tab()
        self.create_expert_tab()
        self.create_connections_tab()

        # Create bottom button frame
        self.create_bottom_buttons()

    def create_connections_tab(self):
        """Create the connections management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Connections")

        # Saved connections section
        connections_frame = ttk.LabelFrame(frame, text="Saved Connections", padding=10)
        connections_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Connection list and buttons
        list_frame = ttk.Frame(connections_frame)
        list_frame.pack(fill=BOTH, expand=True)

        # Listbox with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(side=tk.LEFT, fill=BOTH, expand=True)

        self.connection_listbox = tk.Listbox(list_container, height=8, font=("Courier", 10))
        self.connection_listbox.pack(side=tk.LEFT, fill=BOTH, expand=True)
        self.connection_listbox.bind('<<ListboxSelect>>', self.on_connection_select)

        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.connection_listbox.yview)
        scrollbar.pack(side="right", fill=tk.Y)
        self.connection_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons frame
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.pack(side="right", fill=tk.Y, padx=(10, 0))

        self.load_btn = ttk.Button(buttons_frame, text="Load", command=self.load_connection, state=tk.DISABLED)
        self.load_btn.pack(fill=tk.X, pady=2)

        ttk.Button(buttons_frame, text="Save As...", command=self.save_connection).pack(fill=tk.X, pady=2)

        self.delete_btn = ttk.Button(buttons_frame, text="Delete", command=self.delete_connection, state=tk.DISABLED)
        self.delete_btn.pack(fill=tk.X, pady=2)

        self.rename_btn = ttk.Button(buttons_frame, text="Rename", command=self.rename_connection, state=tk.DISABLED)
        self.rename_btn.pack(fill=tk.X, pady=2)

        # Connection name entry
        name_frame = ttk.Frame(connections_frame)
        name_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(name_frame, text="Connection Name:").pack(side=tk.LEFT)
        ttk.Entry(name_frame, textvariable=self.connection_name_var, width=30).pack(side=tk.LEFT, padx=(10, 0))

        # Quick connect section
        quick_frame = ttk.LabelFrame(frame, text="Quick Connect", padding=10)
        quick_frame.pack(fill=tk.X, padx=10, pady=5)

        quick_fields = ttk.Frame(quick_frame)
        quick_fields.pack(fill=tk.X)

        ttk.Label(quick_fields, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(quick_fields, textvariable=self.quick_server_var, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(quick_fields, text="Username:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        ttk.Entry(quick_fields, textvariable=self.quick_user_var, width=20).grid(row=0, column=3, padx=5)

        quick_buttons = ttk.Frame(quick_frame)
        quick_buttons.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(quick_buttons, text="Quick Connect", command=self.quick_connect).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_buttons, text="Save & Connect", command=self.save_and_connect).pack(side=tk.LEFT)

        self.update_connection_list()

    def create_basic_tab(self):
        """Create the basic settings tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Basic")

        # Connection details
        conn_frame = ttk.LabelFrame(frame, text="Connection Details", padding=10)
        conn_frame.pack(fill=tk.X, padx=10, pady=5)

        # Server and port
        server_frame = ttk.Frame(conn_frame)
        server_frame.pack(fill=tk.X, pady=2)
        ttk.Label(server_frame, text="Remote Host *:").pack(side=tk.LEFT)
        ttk.Entry(server_frame, textvariable=self.server_var, width=30).pack(side=tk.LEFT, padx=(10, 20))
        ttk.Label(server_frame, text="Port:").pack(side=tk.LEFT)
        ttk.Entry(server_frame, textvariable=self.port_var, width=8).pack(side=tk.LEFT, padx=(5, 0))

        # Username and domain
        user_frame = ttk.Frame(conn_frame)
        user_frame.pack(fill=tk.X, pady=2)
        ttk.Label(user_frame, text="Username:").pack(side=tk.LEFT)
        ttk.Entry(user_frame, textvariable=self.username_var, width=20).pack(side=tk.LEFT, padx=(10, 20))
        ttk.Label(user_frame, text="Domain:").pack(side=tk.LEFT)
        ttk.Entry(user_frame, textvariable=self.domain_var, width=15).pack(side=tk.LEFT, padx=(5, 0))

        # Password
        pass_frame = ttk.Frame(conn_frame)
        pass_frame.pack(fill=tk.X, pady=2)
        ttk.Label(pass_frame, text="Password:").pack(side=tk.LEFT)
        ttk.Entry(pass_frame, textvariable=self.password_var, width=30, show="*").pack(side=tk.LEFT, padx=(10, 0))

        # Display settings
        display_frame = ttk.LabelFrame(frame, text="Display Settings", padding=10)
        display_frame.pack(fill=tk.X, padx=10, pady=5)

        # Resolution
        res_frame = ttk.Frame(display_frame)
        res_frame.pack(fill=tk.X, pady=2)
        ttk.Label(res_frame, text="Width:").pack(side=tk.LEFT)
        ttk.Entry(res_frame, textvariable=self.width_var, width=8).pack(side=tk.LEFT, padx=(5, 20))
        ttk.Label(res_frame, text="Height:").pack(side=tk.LEFT)
        ttk.Entry(res_frame, textvariable=self.height_var, width=8).pack(side=tk.LEFT, padx=(5, 20))

        ttk.Checkbutton(res_frame, text="Fullscreen", variable=self.fullscreen_var).pack(side=tk.LEFT, padx=(20, 0))

        # Color depth
        color_frame = ttk.Frame(display_frame)
        color_frame.pack(fill=tk.X, pady=2)
        ttk.Label(color_frame, text="Color Depth:").pack(side=tk.LEFT)
        color_combo = ttk.Combobox(color_frame, textvariable=self.color_depth_var, width=15, state="readonly")
        color_combo['values'] = ("32", "24", "16", "15", "8")
        color_combo.pack(side=tk.LEFT, padx=(5, 0))

    def create_advanced_tab(self):
        """Create the advanced settings tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Advanced")

        # Redirection options
        redirect_frame = ttk.LabelFrame(frame, text="Redirection Options", padding=10)
        redirect_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Checkbutton(redirect_frame, text="Clipboard redirection", variable=self.clipboard_var).pack(anchor=tk.W,
                                                                                                        pady=2)
        ttk.Checkbutton(redirect_frame, text="Printer redirection", variable=self.printers_var).pack(anchor=tk.W,
                                                                                                     pady=2)
        ttk.Checkbutton(redirect_frame, text="Microphone redirection", variable=self.microphone_var).pack(anchor=tk.W,
                                                                                                          pady=2)

        drive_frame = ttk.Frame(redirect_frame)
        drive_frame.pack(fill=tk.X, pady=2)
        ttk.Label(drive_frame, text="Drive/Folder:").pack(side=tk.LEFT)
        ttk.Entry(drive_frame, textvariable=self.drive_redirect_var, width=40).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(drive_frame, text="Browse", command=self.browse_drive).pack(side=tk.LEFT)

        # Performance & Visual
        perf_frame = ttk.LabelFrame(frame, text="Performance & Visual", padding=10)
        perf_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Checkbutton(perf_frame, text="Enable compression", variable=self.compression_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(perf_frame, text="Smooth fonts (ClearType)", variable=self.fonts_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(perf_frame, text="Desktop composition (Aero)", variable=self.aero_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(perf_frame, text="Enable themes", variable=self.themes_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(perf_frame, text="Show wallpaper", variable=self.wallpaper_var).pack(anchor=tk.W, pady=2)

        # Gateway settings
        gateway_frame = ttk.LabelFrame(frame, text="Gateway Settings", padding=10)
        gateway_frame.pack(fill=tk.X, padx=10, pady=5)

        gw_fields = ttk.Frame(gateway_frame)
        gw_fields.pack(fill=tk.X)
        ttk.Label(gw_fields, text="Gateway Host:").pack(side=tk.LEFT)
        ttk.Entry(gw_fields, textvariable=self.gateway_var, width=25).pack(side=tk.LEFT, padx=(5, 20))
        ttk.Label(gw_fields, text="Gateway User:").pack(side=tk.LEFT)
        ttk.Entry(gw_fields, textvariable=self.gateway_user_var, width=20).pack(side=tk.LEFT, padx=(5, 0))

    def create_expert_tab(self):
        """Create the expert settings tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Expert")

        # FreeRDP executable
        exe_frame = ttk.LabelFrame(frame, text="FreeRDP Executable", padding=10)
        exe_frame.pack(fill=tk.X, padx=10, pady=5)

        path_frame = ttk.Frame(exe_frame)
        path_frame.pack(fill=tk.X)
        ttk.Label(path_frame, text="Path:").pack(side=tk.LEFT)
        ttk.Entry(path_frame, textvariable=self.freerdp_path_var, width=50).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(path_frame, text="Browse", command=self.browse_freerdp).pack(side=tk.LEFT)

        # Security & Protocol
        security_frame = ttk.LabelFrame(frame, text="Security & Protocol", padding=10)
        security_frame.pack(fill=tk.X, padx=10, pady=5)

        sec_combo_frame = ttk.Frame(security_frame)
        sec_combo_frame.pack(fill=tk.X, pady=2)
        ttk.Label(sec_combo_frame, text="Security Protocol:").pack(side=tk.LEFT)
        sec_combo = ttk.Combobox(sec_combo_frame, textvariable=self.security_var, width=15, state="readonly")
        sec_combo['values'] = ("", "rdp", "tls", "nla", "ext")
        sec_combo.pack(side=tk.LEFT, padx=(5, 0))

        ttk.Checkbutton(security_frame, text="Ignore certificate errors", variable=self.cert_ignore_var).pack(
            anchor=tk.W, pady=2)
        ttk.Checkbutton(security_frame, text="Admin/Console session", variable=self.admin_session_var).pack(anchor=tk.W,
                                                                                                            pady=2)

        # Advanced Graphics
        graphics_frame = ttk.LabelFrame(frame, text="Advanced Graphics", padding=10)
        graphics_frame.pack(fill=tk.X, padx=10, pady=5)

        gdi_frame = ttk.Frame(graphics_frame)
        gdi_frame.pack(fill=tk.X, pady=2)
        ttk.Label(gdi_frame, text="GDI Rendering:").pack(side=tk.LEFT)
        gdi_combo = ttk.Combobox(gdi_frame, textvariable=self.gdi_mode_var, width=15, state="readonly")
        gdi_combo['values'] = ("", "sw", "hw")
        gdi_combo.pack(side=tk.LEFT, padx=(5, 0))

        ttk.Checkbutton(graphics_frame, text="Enable RemoteFX", variable=self.remotefx_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(graphics_frame, text="Multi-monitor support", variable=self.multimon_var).pack(anchor=tk.W,
                                                                                                       pady=2)

        # Custom parameters
        custom_frame = ttk.LabelFrame(frame, text="Custom Parameters", padding=10)
        custom_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(custom_frame, text="Additional Parameters:").pack(anchor=tk.W)
        ttk.Entry(custom_frame, textvariable=self.custom_params_var, width=60).pack(fill=tk.X, pady=(5, 0))

    def create_bottom_buttons(self):
        """Create the bottom button frame"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(button_frame, text="Show Command", command=self.show_command).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Connect", command=self.connect).pack(side="right")

        # Status label
        self.status_label = ttk.Label(button_frame, text="Ready", foreground="green")
        self.status_label.pack(side=tk.LEFT)

    def find_freerdp(self):
        """Try to find FreeRDP executable automatically (cross-platform)"""
        # Platform-specific executable names and paths
        if sys.platform == "win32":
            exe_names = ["wfreerdp.exe", "xfreerdp.exe", "freerdp.exe"]
            common_paths = [
                "./wfreerdp.exe",
                "./xfreerdp.exe",
                "C:\\Program Files\\FreeRDP\\wfreerdp.exe",
                "C:\\Program Files (x86)\\FreeRDP\\wfreerdp.exe",
                "C:\\Program Files\\FreeRDP\\xfreerdp.exe",
                "C:\\Program Files (x86)\\FreeRDP\\xfreerdp.exe",
                "C:\\Program Files\\wfreerdp\\wfreerdp.exe"
            ]
        else:
            # Linux/Mac - xfreerdp is most common
            exe_names = ["xfreerdp", "freerdp", "wfreerdp"]
            common_paths = [
                "/usr/bin/xfreerdp",
                "/usr/local/bin/xfreerdp",
                "/usr/bin/freerdp",
                "/usr/local/bin/freerdp",
                "/opt/freerdp/bin/xfreerdp",
                "/snap/bin/freerdp"  # Snap packages
            ]

        # Check common paths first
        for path in common_paths:
            if os.path.exists(path):
                self.freerdp_path_var.set(path)
                return

        # Check PATH for any of the executable names
        for exe_name in exe_names:
            found_path = self.which(exe_name)
            if found_path:
                self.freerdp_path_var.set(found_path)
                return

    def which(self, program):
        """Find executable in PATH (cross-platform)"""

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
                # Also check with .exe extension on Windows
                if sys.platform == "win32":
                    exe_file_with_ext = exe_file + ".exe"
                    if is_exe(exe_file_with_ext):
                        return exe_file_with_ext
        return None

    def browse_freerdp(self):
        """Browse for FreeRDP executable (cross-platform)"""
        if sys.platform == "win32":
            title = "Select FreeRDP executable"
            filetypes = [
                ("FreeRDP executables", "wfreerdp.exe;xfreerdp.exe;freerdp.exe"),
                ("Executable files", "*.exe"),
                ("All files", "*.*")
            ]
        else:
            title = "Select FreeRDP executable (xfreerdp, freerdp)"
            filetypes = [("All files", "*")]

        filename = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if filename:
            self.freerdp_path_var.set(filename)

    def browse_drive(self):
        """Browse for drive/folder to redirect"""
        folder = filedialog.askdirectory(title="Select folder to redirect")
        if folder:
            self.drive_redirect_var.set(folder)

    def load_connections(self):
        """Load saved connections from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading connections: {e}")
        return {}

    def save_connections(self):
        """Save connections to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.connections, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save connections: {e}")

    def update_connection_list(self):
        """Update the connection listbox"""
        self.connection_listbox.delete(0, tk.END)
        for name, conn in self.connections.items():
            server = conn.get('server', 'No server')
            self.connection_listbox.insert(tk.END, f"{name} ({server})")

    def on_connection_select(self, event):
        """Handle connection selection"""
        selection = event.widget.curselection()
        if selection:
            # Enable buttons
            self.load_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            self.rename_btn.config(state=tk.NORMAL)

            # Set connection name
            conn_name = list(self.connections.keys())[selection[0]]
            self.connection_name_var.set(conn_name)
        else:
            # Disable buttons
            self.load_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
            self.rename_btn.config(state=tk.DISABLED)

    def get_current_settings(self):
        """Get all current form settings as a dictionary"""
        return {
            'server': self.server_var.get(),
            'port': self.port_var.get(),
            'username': self.username_var.get(),
            'domain': self.domain_var.get(),
            'password': self.password_var.get(),
            'width': self.width_var.get(),
            'height': self.height_var.get(),
            'fullscreen': self.fullscreen_var.get(),
            'color_depth': self.color_depth_var.get(),
            'clipboard': self.clipboard_var.get(),
            'drive_redirect': self.drive_redirect_var.get(),
            'printers': self.printers_var.get(),
            'microphone': self.microphone_var.get(),
            'compression': self.compression_var.get(),
            'fonts': self.fonts_var.get(),
            'aero': self.aero_var.get(),
            'themes': self.themes_var.get(),
            'wallpaper': self.wallpaper_var.get(),
            'gateway': self.gateway_var.get(),
            'gateway_user': self.gateway_user_var.get(),
            'wfreerdp_path': self.freerdp_path_var.get(),
            'security': self.security_var.get(),
            'cert_ignore': self.cert_ignore_var.get(),
            'admin_session': self.admin_session_var.get(),
            'gdi_mode': self.gdi_mode_var.get(),
            'remotefx': self.remotefx_var.get(),
            'multimon': self.multimon_var.get(),
            'custom_params': self.custom_params_var.get(),
        }

    def load_settings(self, settings):
        """Load settings into the form"""
        self.server_var.set(settings.get('server', ''))
        self.port_var.set(settings.get('port', '3389'))
        self.username_var.set(settings.get('username', ''))
        self.domain_var.set(settings.get('domain', ''))
        self.password_var.set(settings.get('password', ''))
        self.width_var.set(settings.get('width', '1920'))
        self.height_var.set(settings.get('height', '1080'))
        self.fullscreen_var.set(settings.get('fullscreen', False))
        self.color_depth_var.set(settings.get('color_depth', '32'))
        self.clipboard_var.set(settings.get('clipboard', False))
        self.drive_redirect_var.set(settings.get('drive_redirect', ''))
        self.printers_var.set(settings.get('printers', False))
        self.microphone_var.set(settings.get('microphone', False))
        self.compression_var.set(settings.get('compression', False))
        self.fonts_var.set(settings.get('fonts', False))
        self.aero_var.set(settings.get('aero', True))
        self.themes_var.set(settings.get('themes', True))
        self.wallpaper_var.set(settings.get('wallpaper', True))
        self.gateway_var.set(settings.get('gateway', ''))
        self.gateway_user_var.set(settings.get('gateway_user', ''))
        self.freerdp_path_var.set(settings.get('wfreerdp_path', ''))
        self.security_var.set(settings.get('security', ''))
        self.cert_ignore_var.set(settings.get('cert_ignore', False))
        self.admin_session_var.set(settings.get('admin_session', False))
        self.gdi_mode_var.set(settings.get('gdi_mode', ''))
        self.remotefx_var.set(settings.get('remotefx', False))
        self.multimon_var.set(settings.get('multimon', False))
        self.custom_params_var.set(settings.get('custom_params', ''))

    def save_connection(self):
        """Save current settings as a new connection"""
        name = self.connection_name_var.get().strip()
        if not name:
            server = self.server_var.get().strip()
            if server:
                name = server
                self.connection_name_var.set(name)
            else:
                messagebox.showerror("Error", "Please enter a connection name")
                return

        if name in self.connections:
            if not messagebox.askyesno("Confirm", f"Connection '{name}' already exists. Overwrite?"):
                return

        self.connections[name] = self.get_current_settings()
        self.save_connections()
        self.update_connection_list()
        self.status_label.config(text=f"Connection '{name}' saved", foreground="green")

    def load_connection(self):
        """Load selected connection"""
        selection = self.connection_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a connection to load")
            return

        conn_name = list(self.connections.keys())[selection[0]]
        settings = self.connections[conn_name]
        self.load_settings(settings)
        self.notebook.select(0)  # Switch to Basic tab
        self.status_label.config(text=f"Connection '{conn_name}' loaded", foreground="green")

    def delete_connection(self):
        """Delete selected connection"""
        selection = self.connection_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a connection to delete")
            return

        conn_name = list(self.connections.keys())[selection[0]]
        if messagebox.askyesno("Confirm", f"Delete connection '{conn_name}'?"):
            del self.connections[conn_name]
            self.save_connections()
            self.update_connection_list()
            self.connection_name_var.set("")
            self.status_label.config(text=f"Connection '{conn_name}' deleted", foreground="green")

    def rename_connection(self):
        """Rename selected connection"""
        selection = self.connection_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a connection to rename")
            return

    def rename_connection(self):
        """Rename selected connection"""
        selection = self.connection_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a connection to rename")
            return

        old_name = list(self.connections.keys())[selection[0]]
        new_name = simpledialog.askstring("Rename Connection", f"Enter new name for '{old_name}':",
                                          initialvalue=old_name)

        if new_name and new_name.strip() and new_name != old_name:
            new_name = new_name.strip()
            if new_name in self.connections:
                messagebox.showerror("Error", f"Connection '{new_name}' already exists")
                return

            self.connections[new_name] = self.connections.pop(old_name)
            self.save_connections()
            self.update_connection_list()
            self.connection_name_var.set(new_name)
            self.status_label.config(text=f"Connection renamed to '{new_name}'", foreground="green")

    def quick_connect(self):
        """Quick connect using minimal settings"""
        server = self.quick_server_var.get().strip()
        user = self.quick_user_var.get().strip()

        if not server:
            messagebox.showerror("Error", "Please enter a server address")
            return

        # Set basic settings and connect
        self.server_var.set(server)
        if user:
            self.username_var.set(user)

        self.connect()

    def save_and_connect(self):
        """Save quick connect settings and connect"""
        server = self.quick_server_var.get().strip()
        user = self.quick_user_var.get().strip()

        if not server:
            messagebox.showerror("Error", "Please enter a server address")
            return

        # Set basic settings
        self.server_var.set(server)
        if user:
            self.username_var.set(user)

        # Generate connection name and save
        name = f"{user}@{server}" if user else server
        self.connection_name_var.set(name)
        self.save_connection()

        # Connect
        self.connect()

    def build_command(self):
        """Build the FreeRDP command line (cross-platform)"""
        freerdp_path = self.freerdp_path_var.get().strip()
        server = self.server_var.get().strip()

        if not freerdp_path:
            messagebox.showerror("Error", "Please specify the path to FreeRDP executable")
            return None

        if not server:
            messagebox.showerror("Error", "Please enter a server hostname or IP address")
            return None

        # Start building command
        cmd = [freerdp_path]

        # Basic connection
        port = self.port_var.get().strip()
        if port and port != "3389":
            cmd.append(f"/v:{server}:{port}")
        else:
            cmd.append(f"/v:{server}")

        # Authentication
        username = self.username_var.get().strip()
        domain = self.domain_var.get().strip()
        password = self.password_var.get().strip()

        if username:
            if domain:
                cmd.append(f"/u:{domain}\\{username}")
            else:
                cmd.append(f"/u:{username}")
        elif domain:
            cmd.append(f"/d:{domain}")

        if password:
            cmd.append(f"/p:{password}")

        # Display settings
        if self.fullscreen_var.get():
            cmd.append("/f")
        else:
            width = self.width_var.get().strip()
            height = self.height_var.get().strip()
            if width and height:
                cmd.append(f"/size:{width}x{height}")

        color_depth = self.color_depth_var.get().strip()
        if color_depth:
            cmd.append(f"/bpp:{color_depth}")

        # Advanced options
        if self.clipboard_var.get():
            cmd.append("+clipboard")

        drive_redirect = self.drive_redirect_var.get().strip()
        if drive_redirect:
            cmd.append(f"/drive:share,{drive_redirect}")

        if self.microphone_var.get():
            cmd.append("/mic")

        if self.compression_var.get():
            cmd.append("+compression")

        if self.fonts_var.get():
            cmd.append("+fonts")

        if self.aero_var.get():
            cmd.append("+aero")
        else:
            cmd.append("-aero")

        if not self.themes_var.get():
            cmd.append("-themes")

        if not self.wallpaper_var.get():
            cmd.append("-wallpaper")

        # Gateway
        gateway = self.gateway_var.get().strip()
        if gateway:
            cmd.append(f"/g:{gateway}")
            gateway_user = self.gateway_user_var.get().strip()
            if gateway_user:
                cmd.append(f"/gu:{gateway_user}")

        # Expert options
        security = self.security_var.get().strip()
        if security:
            cmd.append(f"/sec:{security}")

        if self.cert_ignore_var.get():
            cmd.append("/cert-ignore")

        if self.admin_session_var.get():
            cmd.append("/admin")

        gdi_mode = self.gdi_mode_var.get().strip()
        if gdi_mode:
            cmd.append(f"/gdi:{gdi_mode}")

        if self.remotefx_var.get():
            cmd.append("/rfx")

        if self.multimon_var.get():
            cmd.append("/multimon")

        # Custom parameters
        custom_params = self.custom_params_var.get().strip()
        if custom_params:
            # Split custom parameters and add them
            cmd.extend(custom_params.split())

        return cmd

    def show_command(self):
        """Display the generated command"""
        cmd = self.build_command()
        if cmd:
            command_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in cmd)

            # Create a new window to show the command
            cmd_window = tk.Toplevel(self.root)
            cmd_window.title("Generated Command")
            cmd_window.geometry("800x300")

            # Text widget with scrollbars
            text_frame = ttk.Frame(cmd_window)
            text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
            text_widget.pack(side=tk.LEFT, fill=BOTH, expand=True)

            scrollbar_y = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            scrollbar_y.pack(side="right", fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar_y.set)

            scrollbar_x = ttk.Scrollbar(cmd_window, orient=tk.HORIZONTAL, command=text_widget.xview)
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X, padx=10)
            text_widget.config(xscrollcommand=scrollbar_x.set)

            text_widget.insert(tk.END, command_str)
            text_widget.config(state=tk.DISABLED)

            # Copy button
            button_frame = ttk.Frame(cmd_window)
            button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

            def copy_command():
                cmd_window.clipboard_clear()
                cmd_window.clipboard_append(command_str)
                copy_btn.config(text="Copied!")
                cmd_window.after(2000, lambda: copy_btn.config(text="Copy to Clipboard"))

            copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", command=copy_command)
            copy_btn.pack(side="right")

            self.status_label.config(text="Command generated successfully", foreground="green")

    def connect(self):
        """Execute the FreeRDP command"""
        cmd = self.build_command()
        if cmd:
            try:
                self.status_label.config(text="Connecting...", foreground="blue")
                self.root.update()

                # Save current settings as last used
                self.save_last_settings()

                # Execute the command and capture output
                if sys.platform == "win32":
                    # On Windows, capture stderr to get error details
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    if result.returncode != 0:
                        # Connection failed, show error details
                        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                        if not error_msg:
                            error_msg = f"FreeRDP exited with code {result.returncode}"

                        self.show_connection_error(error_msg)
                        self.status_label.config(text="Connection failed", foreground="red")
                    else:
                        # Success case - launch in background for ongoing connection
                        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                        self.status_label.config(text="Connection launched", foreground="green")
                else:
                    # On Linux/Mac, also capture output
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    if result.returncode != 0:
                        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                        if not error_msg:
                            error_msg = f"FreeRDP exited with code {result.returncode}"

                        self.show_connection_error(error_msg)
                        self.status_label.config(text="Connection failed", foreground="red")
                    else:
                        # Launch in background for ongoing connection
                        subprocess.Popen(cmd)
                        self.status_label.config(text="Connection launched", foreground="green")

            except subprocess.TimeoutExpired:
                # If it takes longer than 10 seconds, assume it's connecting successfully
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
                self.status_label.config(text="Connection launched", foreground="green")
            except FileNotFoundError:
                error_msg = f"FreeRDP executable not found: {cmd[0]}\n\nPlease check the Expert tab and verify the executable path."
                self.show_connection_error(error_msg)
                self.status_label.config(text="Executable not found", foreground="red")
            except Exception as e:
                self.show_connection_error(f"Failed to launch connection: {str(e)}")
                self.status_label.config(text="Connection failed", foreground="red")

    def show_connection_error(self, error_message):
        """Display connection error details in a popup window"""
        error_window = tk.Toplevel(self.root)
        error_window.title("Connection Error")
        error_window.geometry("600x400")
        error_window.transient(self.root)
        error_window.grab_set()

        # Main frame
        main_frame = ttk.Frame(error_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Error message
        ttk.Label(main_frame, text="Connection Failed", font=("TkDefaultFont", 12, "bold")).pack(anchor=tk.W,
                                                                                                 pady=(0, 10))

        # Scrollable text area for error details
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        error_text = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 9), height=15)
        error_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=error_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        error_text.config(yscrollcommand=scrollbar.set)

        # Insert error message
        error_text.insert(tk.END, error_message)
        error_text.config(state=tk.DISABLED)

        # Common solutions section
        solutions_text = """
    Common Solutions:
    - Check server address and port
    - Verify username and password
    - Ensure RDP is enabled on target server
    - Check firewall settings
    - Try different security protocol in Expert tab
    - For gateway connections, verify gateway settings
    """

        ttk.Label(main_frame, text="Troubleshooting Tips:", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W,
                                                                                                     pady=(10, 5))
        solutions_label = ttk.Label(main_frame, text=solutions_text, justify=tk.LEFT)
        solutions_label.pack(anchor=tk.W, fill=tk.X)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        def copy_error():
            error_window.clipboard_clear()
            error_window.clipboard_append(error_message)
            copy_btn.config(text="Copied!")
            error_window.after(2000, lambda: copy_btn.config(text="Copy Error"))

        copy_btn = ttk.Button(button_frame, text="Copy Error", command=copy_error)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="Close", command=error_window.destroy).pack(side=tk.RIGHT)

    def save_last_settings(self):
        """Save current settings as last used"""
        settings = self.get_current_settings()
        try:
            last_settings_file = Path.home() / ".freerdp_last_settings.json"
            with open(last_settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving last settings: {e}")

    def load_last_settings(self):
        """Load last used settings"""
        try:
            last_settings_file = Path.home() / ".freerdp_last_settings.json"
            if last_settings_file.exists():
                with open(last_settings_file, 'r') as f:
                    settings = json.load(f)
                    self.load_settings(settings)
        except Exception as e:
            print(f"Error loading last settings: {e}")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FreeRDPGUI(root)

    # Set window icon if available
    try:
        if sys.platform == "win32":
            root.iconbitmap(default="python.ico")
    except (tk.TclError, FileNotFoundError):
        pass

    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()