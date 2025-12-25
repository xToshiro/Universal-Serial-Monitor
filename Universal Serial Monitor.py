import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import serial
import serial.tools.list_ports
import threading
from datetime import datetime
import time
import csv
import multiprocessing
import os
import json
import sys
 

# --- Dicionários de Tradução e Temas ---
LANGUAGES = {
    "pt": {
        "title": "Monitor Serial Universal v1.2",
        "port": "Porta:",
        "baud": "Baud:",
        "connect": "Iniciar",
        "disconnect": "Parar",
        "tx_enable": "Habilitar TX",
        "idle": "| Ocioso:",
        "avg": "Média:",
        "plot": "📈 Gráficos",
        "file_menu": "Arquivo",
        "load_log": "Carregar Log Antigo...",
        "set_folder": "Definir Pasta de Logs...",
        "exit": "Sair",
        "tools_menu": "Ferramentas",
        "config_filters": "Configurar Filtros...",
        "clear_screen": "Limpar Tela",
        "view_menu": "Exibir",
        "theme": "Tema",
        "lang": "Idioma",
        "help_menu": "Ajuda",
        "about": "Sobre",
        "hist_title": "Histórico de Eventos",
        "tx_label": "Enviar comando (TX):",
        "send_btn": "Enviar",
        "status_folder": "Pasta de Logs: {}",
        "status_view": "Visualizando: {}",
        "status_monitor": "Gravando em: {}",
        "status_stopped": "Parado.",
        "err_select_port": "Selecione uma porta.",
        "err_connection": "Erro de Conexão",
        "err_tx": "Não conectado.",
        "warn_stop_load": "Parar monitoramento atual para carregar log?",
        "success_load": "Log carregado e analisado.",
        "err_read_log": "Falha ao ler log: {}",
        "about_msg": "Universal Serial Monitor v1.2\n\nDesenvolvido por: Jairo Ivo Castro Brito\nDep. Engenharia de Transportes - UFC\n\nLicença: GNU GPLv3",
        "boots": "Boots",
        "panics": "Panics",
        "errors": "Erros"
    },
    "en": {
        "title": "Universal Serial Monitor v1.2",
        "port": "Port:",
        "baud": "Baud:",
        "connect": "Start",
        "disconnect": "Stop",
        "tx_enable": "Enable TX",
        "idle": "| Idle:",
        "avg": "Avg:",
        "plot": "📈 Charts",
        "file_menu": "File",
        "load_log": "Load Old Log...",
        "set_folder": "Set Log Folder...",
        "exit": "Exit",
        "tools_menu": "Tools",
        "config_filters": "Configure Filters...",
        "clear_screen": "Clear Screen",
        "view_menu": "View",
        "theme": "Theme",
        "lang": "Language",
        "help_menu": "Help",
        "about": "About",
        "hist_title": "Event History",
        "tx_label": "Send Command (TX):",
        "send_btn": "Send",
        "status_folder": "Log Folder: {}",
        "status_view": "Viewing: {}",
        "status_monitor": "Recording to: {}",
        "status_stopped": "Stopped.",
        "err_select_port": "Select a port.",
        "err_connection": "Connection Error",
        "err_tx": "Not connected.",
        "warn_stop_load": "Stop current monitoring to load log?",
        "success_load": "Log loaded and analyzed.",
        "err_read_log": "Failed to read log: {}",
        "about_msg": "Universal Serial Monitor v1.2\n\nDeveloped by: Jairo Ivo Castro Brito\nTransport Engineering Dept - UFC\n\nLicense: GNU GPLv3",
        "boots": "Boots",
        "panics": "Panics",
        "errors": "Errors"
    }
}

THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "black",
        "top_bg": "#f0f0f0",
        "text_bg": "white",
        "text_fg": "black",
        "list_bg": "#f8f8f8",
        "list_fg": "black",
        "panel_bg": "#e0e0e0",
        "stats_bg": "#e0e0e0",
        "entry_bg": "white",
        "entry_fg": "black",
        "btn_bg": "#dddddd",
        "btn_fg": "black"
    },
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "top_bg": "#3e3e3e",
        "text_bg": "#1e1e1e",
        "text_fg": "#00ff00", # Terminal style
        "list_bg": "#1e1e1e",
        "list_fg": "#e0e0e0",
        "panel_bg": "#3e3e3e",
        "stats_bg": "#4e4e4e",
        "entry_bg": "#505050",
        "entry_fg": "white",
        "btn_bg": "#505050",
        "btn_fg": "white"
    }
}

# --- Configurações Padrão ---
DEFAULT_CONFIG = {
    "log_folder": os.getcwd(),
    "baud_rate": 115200,
    "language": "pt",
    "theme": "light",
    "filters": [
        {"keyword": "rst:", "type": "boots"},
        {"keyword": "boot:", "type": "boots"},
        {"keyword": "ets jul", "type": "boots"},
        {"keyword": "panic", "type": "panics"},
        {"keyword": "guru meditation", "type": "panics"},
        {"keyword": "error", "type": "errors"},
        {"keyword": "fail", "type": "errors"},
        {"keyword": "exception", "type": "errors"}
    ]
}

CONFIG_FILE = "monitor_config.json"

# --- Funções Auxiliares ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar config: {e}")

# --- Processo de Plotagem ---
def plot_worker(filename):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        
 
 
 
 
 
 
 
        times, deltas, avgs, errors = [], [], [], []

        if not os.path.exists(filename):
 
            return

        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    t = datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                    times.append(t)
                    deltas.append(float(row['IdleTime']))
                    avgs.append(float(row['AvgInterval']))
                    total_err = int(row['Boots']) + int(row['Panics']) + int(row['Errors'])
                    errors.append(total_err)
                except ValueError:
                    continue

        if not times:
            print("Sem dados suficientes.")
            return
        
        # Tema escuro para plots se o sistema estiver escuro (opcional, aqui fixo)
        plt.style.use('bmh')

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        fig.canvas.manager.set_window_title("Metrics Analysis")
        
        ax1.set_title('Jitter / Stability')
        ax1.plot(times, deltas, label='Idle (s)', color='blue', alpha=0.3)
        ax1.plot(times, avgs, label='Avg (s)', color='green', linewidth=2)
        ax1.set_ylabel('Seconds')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.set_title('Accumulated Events')
        ax2.plot(times, errors, label='Total Errors', color='red', linewidth=2)
        ax2.set_ylabel('Count')
        ax2.fill_between(times, errors, color='red', alpha=0.1)
        ax2.grid(True, alpha=0.3)

        formatter = mdates.DateFormatter('%H:%M:%S')
        ax2.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except ImportError:
        messagebox.showerror("Erro", "Matplotlib not found.\npip install matplotlib")
    except Exception as e:
        print(f"Erro plot: {e}")

# --- Janela de Edição de Filtros ---
class FilterEditor(tk.Toplevel):
    def __init__(self, parent, config, on_save, theme_name="light"):
        super().__init__(parent)
        self.title("Filter Editor")
        self.geometry("400x400")
        self.config = config
        self.on_save = on_save
        self.theme = THEMES[theme_name]
        
        self.configure(bg=self.theme["bg"])
        
        frame = tk.Frame(self, padx=10, pady=10, bg=self.theme["bg"])
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Keyword:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=0, column=0, sticky="w")
        self.entry_keyword = tk.Entry(frame, bg=self.theme["entry_bg"], fg=self.theme["entry_fg"], insertbackground=self.theme["fg"])
        self.entry_keyword.grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(frame, text="Type:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=1, column=0, sticky="w")
        self.combo_type = ttk.Combobox(frame, values=["boots", "panics", "errors"], state="readonly")
        self.combo_type.current(2)
        self.combo_type.grid(row=1, column=1, sticky="ew", padx=5)

        btn_add = tk.Button(frame, text="Add / Adicionar", command=self.add_filter, bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        btn_add.grid(row=2, column=1, sticky="e", pady=5)

        self.listbox = tk.Listbox(frame, bg=self.theme["list_bg"], fg=self.theme["list_fg"])
        self.listbox.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)
        
        btn_remove = tk.Button(frame, text="Remove Selected", command=self.remove_filter, fg="red", bg=self.theme["btn_bg"])
        btn_remove.grid(row=4, column=0, columnspan=2, sticky="ew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for f in self.config['filters']:
            self.listbox.insert(tk.END, f"{f['keyword']}  ->  [{f['type'].upper()}]")

    def add_filter(self):
        kw = self.entry_keyword.get().strip().lower()
        cat = self.combo_type.get()
        if kw:
            self.config['filters'].append({"keyword": kw, "type": cat})
            save_config(self.config)
            self.refresh_list()
            self.entry_keyword.delete(0, tk.END)
            self.on_save(self.config)

    def remove_filter(self):
        sel = self.listbox.curselection()
        if sel:
            idx = sel[0]
            del self.config['filters'][idx]
            save_config(self.config)
            self.refresh_list()
            self.on_save(self.config)

# --- App Principal ---
class SerialMonitorApp:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.current_lang = self.config.get("language", "pt")
        self.current_theme = self.config.get("theme", "light")
        
        self.root.geometry("1100x750")
        
        self.serial_port = None
        self.is_monitoring = False
        self.connection_error = False # Flag para RX LED vermelho
        self.log_file = None
        self.metrics_file = None
        self.metrics_writer = None
        self.metrics_filename_full = ""
        self.baud_rate = self.config.get("baud_rate", 115200)
        self.MAX_GUI_LINES = 2000
        
        self.last_data_time = 0
        self.seconds_since_last = 0
        self.interval_sum = 0
        self.interval_count = 0
        self.current_avg = 0.0
        self.stats = {"boots": 0, "panics": 0, "errors": 0}

        self.setup_ui()
        self.apply_theme()
        self.apply_language()
        
        self.update_ports()
        self.check_led_status()
        self.update_timer_loop()

    def setup_ui(self):
        # --- Menu ---
        self.menubar = tk.Menu(self.root)
        
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(command=self.load_old_log)
        self.file_menu.add_command(command=self.select_log_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(command=self.root.quit)
        self.menubar.add_cascade(menu=self.file_menu)

        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.tools_menu.add_command(command=self.open_filter_editor)
        self.tools_menu.add_command(command=self.clear_screen)
        self.menubar.add_cascade(menu=self.tools_menu)
        
        # Menu Exibir (Temas e Idiomas)
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        
        self.theme_menu = tk.Menu(self.view_menu, tearoff=0)
        self.theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))
        self.view_menu.add_cascade(menu=self.theme_menu)
        
        self.lang_menu = tk.Menu(self.view_menu, tearoff=0)
        self.lang_menu.add_command(label="Português", command=lambda: self.change_lang("pt"))
        self.lang_menu.add_command(label="English", command=lambda: self.change_lang("en"))
        self.view_menu.add_cascade(menu=self.lang_menu)
        
        self.menubar.add_cascade(menu=self.view_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(command=self.show_about)
        self.menubar.add_cascade(menu=self.help_menu)
        self.root.config(menu=self.menubar)

        # --- Topo ---
        self.top_frame = tk.Frame(self.root, pady=5, bd=1, relief=tk.RAISED)
        self.top_frame.pack(fill=tk.X, side=tk.TOP)

        # LEDs
        self.led_rx_canvas = tk.Canvas(self.top_frame, width=20, height=20, highlightthickness=0)
        self.led_rx_oval = self.led_rx_canvas.create_oval(2, 2, 18, 18, fill="gray")
        self.led_rx_canvas.pack(side=tk.LEFT, padx=(10, 2))
        self.lbl_rx = tk.Label(self.top_frame, text="RX")
        self.lbl_rx.pack(side=tk.LEFT, padx=(0, 10))

        self.led_log_canvas = tk.Canvas(self.top_frame, width=20, height=20, highlightthickness=0)
        self.led_log_oval = self.led_log_canvas.create_oval(2, 2, 18, 18, fill="gray")
        self.led_log_canvas.pack(side=tk.LEFT, padx=(5, 2))
        self.lbl_log = tk.Label(self.top_frame, text="LOG")
        self.lbl_log.pack(side=tk.LEFT, padx=(0, 10))

        # Controles
        self.lbl_port = tk.Label(self.top_frame, text="Porta:")
        self.lbl_port.pack(side=tk.LEFT)
        self.combo_ports = ttk.Combobox(self.top_frame, width=15)
        self.combo_ports.pack(side=tk.LEFT, padx=5)
        self.btn_refresh = tk.Button(self.top_frame, text="↻", command=self.update_ports, width=3)
        self.btn_refresh.pack(side=tk.LEFT)

        self.lbl_baud = tk.Label(self.top_frame, text="Baud:")
        self.lbl_baud.pack(side=tk.LEFT, padx=(10, 2))
        
        # Baud Rate com Combobox Editável
        baud_rates = ["9600", "19200", "38400", "57600", "74880", "115200", "230400", "460800", "921600"]
        self.combo_baud = ttk.Combobox(self.top_frame, values=baud_rates, width=8)
        self.combo_baud.set(str(self.baud_rate))
        self.combo_baud.pack(side=tk.LEFT, padx=5)

        self.btn_connect = tk.Button(self.top_frame, text="Iniciar", command=self.toggle_connection, width=10)
        self.btn_connect.pack(side=tk.LEFT, padx=10)

        self.show_tx = tk.BooleanVar()
        self.chk_tx = tk.Checkbutton(self.top_frame, variable=self.show_tx, command=self.toggle_tx_panel)
        self.chk_tx.pack(side=tk.LEFT, padx=5)

        # Métricas
        self.lbl_idle_title = tk.Label(self.top_frame, text="| Ocioso:")
        self.lbl_idle_title.pack(side=tk.LEFT, padx=(5,0))
        self.lbl_timer = tk.Label(self.top_frame, text="0s", fg="blue", width=5, font=("Arial", 10, "bold"))
        self.lbl_timer.pack(side=tk.LEFT)
        
        self.lbl_avg_title = tk.Label(self.top_frame, text="Média:")
        self.lbl_avg_title.pack(side=tk.LEFT, padx=(5,0))
        self.lbl_avg = tk.Label(self.top_frame, text="0.0s", fg="blue", width=6, font=("Arial", 10, "bold"))
        self.lbl_avg.pack(side=tk.LEFT)

        self.btn_plot = tk.Button(self.top_frame, text="📈", command=self.launch_plotter)
        self.btn_plot.pack(side=tk.RIGHT, padx=10)

        # --- Painéis Principais ---
        self.main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        self.frame_log = tk.Frame(self.main_pane)
        self.text_area = scrolledtext.ScrolledText(self.frame_log, state='disabled', font=("Consolas", 10))
        self.text_area.pack(expand=True, fill='both')
        self.main_pane.add(self.frame_log, minsize=500)

        self.frame_side = tk.Frame(self.main_pane)
        
        # Stats
        self.frame_stats = tk.Frame(self.frame_side, pady=5, relief=tk.RAISED, bd=1)
        self.frame_stats.pack(fill=tk.X)
        self.lbl_stat_boots = tk.Label(self.frame_stats, text="Boots: 0", fg="red", font=("Arial", 9, "bold"))
        self.lbl_stat_boots.grid(row=0, column=0, padx=5)
        self.lbl_stat_panics = tk.Label(self.frame_stats, text="Panics: 0", fg="darkred", font=("Arial", 9, "bold"))
        self.lbl_stat_panics.grid(row=0, column=1, padx=5)
        self.lbl_stat_errors = tk.Label(self.frame_stats, text="Errors: 0", fg="orange", font=("Arial", 9, "bold"))
        self.lbl_stat_errors.grid(row=0, column=2, padx=5)

        # Lista de Eventos
        self.lbl_hist_title = tk.Label(self.frame_side, relief=tk.RIDGE)
        self.lbl_hist_title.pack(fill=tk.X, pady=(5,0))
        
        self.frame_hist_container = tk.Frame(self.frame_side)
        self.frame_hist_container.pack(fill=tk.BOTH, expand=True)
        self.list_boot = tk.Listbox(self.frame_hist_container, font=("Consolas", 9))
        self.list_boot.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Painel TX
        self.frame_tx = tk.Frame(self.frame_side, bd=1, relief=tk.GROOVE, pady=5)
        self.lbl_tx_title = tk.Label(self.frame_tx, font=("Arial", 8, "bold"))
        self.lbl_tx_title.pack(anchor="w", padx=5)
        
        tx_input_frame = tk.Frame(self.frame_tx)
        tx_input_frame.pack(fill=tk.X, padx=5)
        
        self.entry_tx = tk.Entry(tx_input_frame)
        self.entry_tx.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_tx.bind("<Return>", lambda e: self.send_serial())
        
        self.btn_send = tk.Button(tx_input_frame, command=self.send_serial)
        self.btn_send.pack(side=tk.LEFT, padx=(5,0))

        self.main_pane.add(self.frame_side, minsize=300)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Tema e Idioma ---
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.config["theme"] = theme_name
        save_config(self.config)
        self.apply_theme()

    def apply_theme(self):
        t = THEMES[self.current_theme]
        
        self.root.configure(bg=t["bg"])
        self.top_frame.configure(bg=t["top_bg"])
        self.lbl_port.configure(bg=t["top_bg"], fg=t["fg"])
        self.lbl_baud.configure(bg=t["top_bg"], fg=t["fg"])
        self.lbl_rx.configure(bg=t["top_bg"], fg=t["fg"])
        self.lbl_log.configure(bg=t["top_bg"], fg=t["fg"])
        self.chk_tx.configure(bg=t["top_bg"], fg=t["fg"], selectcolor=t["entry_bg"])
        self.lbl_idle_title.configure(bg=t["top_bg"], fg=t["fg"])
        self.lbl_avg_title.configure(bg=t["top_bg"], fg=t["fg"])
        self.lbl_timer.configure(bg=t["top_bg"])
        self.lbl_avg.configure(bg=t["top_bg"])
        
        # Botões do Topo
        for btn in [self.btn_refresh, self.btn_connect, self.btn_plot]:
             btn.configure(bg=t["btn_bg"], fg=t["btn_fg"])

        # Log
        self.text_area.configure(bg=t["text_bg"], fg=t["text_fg"], insertbackground=t["fg"])
        
        # Painel Lateral
        self.frame_side.configure(bg=t["bg"])
        self.frame_stats.configure(bg=t["stats_bg"])
        self.lbl_stat_boots.configure(bg=t["stats_bg"])
        self.lbl_stat_panics.configure(bg=t["stats_bg"])
        self.lbl_stat_errors.configure(bg=t["stats_bg"])
        
        self.lbl_hist_title.configure(bg=t["panel_bg"], fg=t["fg"])
        self.list_boot.configure(bg=t["list_bg"], fg=t["list_fg"])
        
        # TX
        self.frame_tx.configure(bg=t["panel_bg"])
        self.lbl_tx_title.configure(bg=t["panel_bg"], fg=t["fg"])
        self.frame_tx.winfo_children()[1].configure(bg=t["panel_bg"]) # tx_input_frame
        self.entry_tx.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["fg"])
        self.btn_send.configure(bg=t["btn_bg"], fg=t["btn_fg"])
        
        self.status_bar.configure(bg=t["top_bg"], fg=t["fg"])

    def change_lang(self, lang_code):
        self.current_lang = lang_code
        self.config["language"] = lang_code
        save_config(self.config)
        self.apply_language()

    def apply_language(self):
        L = LANGUAGES[self.current_lang]
        self.root.title(L["title"])
        
        # Menu
        self.menubar.entryconfigure(1, label=L["file_menu"])
        self.file_menu.entryconfigure(0, label=L["load_log"])
        self.file_menu.entryconfigure(1, label=L["set_folder"])
        self.file_menu.entryconfigure(3, label=L["exit"])
        
        self.menubar.entryconfigure(2, label=L["tools_menu"])
        self.tools_menu.entryconfigure(0, label=L["config_filters"])
        self.tools_menu.entryconfigure(1, label=L["clear_screen"])
        
        self.menubar.entryconfigure(3, label=L["view_menu"])
        self.view_menu.entryconfigure(0, label=L["theme"])
        self.view_menu.entryconfigure(1, label=L["lang"])
        
        self.menubar.entryconfigure(4, label=L["help_menu"])
        self.help_menu.entryconfigure(0, label=L["about"])
        
        # Labels
        self.lbl_port.configure(text=L["port"])
        self.lbl_baud.configure(text=L["baud"])
        self.chk_tx.configure(text=L["tx_enable"])
        self.lbl_idle_title.configure(text=L["idle"])
        self.lbl_avg_title.configure(text=L["avg"])
        self.btn_plot.configure(text=L["plot"])
        self.lbl_hist_title.configure(text=L["hist_title"])
        self.lbl_tx_title.configure(text=L["tx_label"])
        self.btn_send.configure(text=L["send_btn"])
        
        # Connection button state text
        if self.is_monitoring:
            self.btn_connect.configure(text=L["disconnect"])
        else:
            self.btn_connect.configure(text=L["connect"])
            
        # Status
        folder = self.config['log_folder']
        self.status_var.set(L["status_folder"].format(folder))
        
        # Stats update labels too
        self.update_stats_labels()

    # --- Lógica ---
    def toggle_tx_panel(self):
        if self.show_tx.get():
            self.frame_tx.pack(side=tk.BOTTOM, fill=tk.X, pady=(5,0))
        else:
            self.frame_tx.pack_forget()

    def send_serial(self):
        if not self.serial_port or not self.serial_port.is_open:
            messagebox.showwarning("Aviso", LANGUAGES[self.current_lang]["err_tx"])
            return
        
        data = self.entry_tx.get()
        if data:
            try:
                msg = data + "\n"
                self.serial_port.write(msg.encode('utf-8'))
                self.entry_tx.delete(0, tk.END)
                
                ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                log_entry = f"[{ts}] [TX] >> {data}\n"
                self.append_text(log_entry)
                if self.log_file:
                    self.log_file.write(log_entry)
                    self.log_file.flush()
                    self.flash_log_led(True)
            except Exception as e:
                self.flash_log_led(False)
                print(f"Erro TX: {e}")

    def load_old_log(self):
        L = LANGUAGES[self.current_lang]
        if self.is_monitoring:
            if not messagebox.askyesno("Confirmar", L["warn_stop_load"]):
                return
            self.stop_monitoring()
            
        filename = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not filename:
            return
            
        self.clear_screen()
        self.stats = {"boots": 0, "panics": 0, "errors": 0}
        self.update_stats_labels()
        self.list_boot.delete(0, tk.END)
        
        self.status_var.set(L["status_view"].format(filename))
        
        try:
            folder = os.path.dirname(filename)
            basename = os.path.basename(filename)
            csv_name = basename.replace("log_serial_", "metrics_").replace(".txt", ".csv")
            csv_full = os.path.join(folder, csv_name)
            
            if os.path.exists(csv_full):
                self.metrics_filename_full = csv_full
                self.btn_plot.config(state="normal")
            else:
                self.metrics_filename_full = ""
            
            with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                display_lines = lines if len(lines) < 5000 else lines[-5000:]
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, "".join(display_lines))
                self.text_area.config(state='disabled')
                
                for line in lines:
                    line_lower = line.lower()
                    ts_display = line.split(']')[0].replace('[', '') if '[' in line else "?"
                    for filter_rule in self.config['filters']:
                        if filter_rule['keyword'] in line_lower:
                            f_type = filter_rule['type']
                            if f_type in self.stats:
                                self.stats[f_type] += 1
                                self.add_boot_event(ts_display, line.strip())
                            break
                
                self.update_stats_labels()
                messagebox.showinfo("Sucesso", L["success_load"])

        except Exception as e:
            messagebox.showerror("Erro", L["err_read_log"].format(e))

    def flash_log_led(self, success=True):
        color = "#00ff00" if success else "#ff0000"
        self.led_log_canvas.itemconfig(self.led_log_oval, fill=color)
        if success:
            self.root.after(100, lambda: self.led_log_canvas.itemconfig(self.led_log_oval, fill="gray"))

    def show_about(self):
        messagebox.showinfo(LANGUAGES[self.current_lang]["about"], LANGUAGES[self.current_lang]["about_msg"])

    def select_log_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.config['log_folder'] = folder
            save_config(self.config)
            self.status_var.set(LANGUAGES[self.current_lang]["status_folder"].format(folder))

    def open_filter_editor(self):
        FilterEditor(self.root, self.config, self.reload_config, self.current_theme)

    def reload_config(self, new_config):
        self.config = new_config

    def update_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [f"{p.device} - {p.description}" for p in ports]
        self.combo_ports['values'] = port_list
        if port_list: self.combo_ports.current(0)

    def toggle_connection(self):
        if not self.is_monitoring: self.start_monitoring()
        else: self.stop_monitoring()

    def start_monitoring(self):
        L = LANGUAGES[self.current_lang]
        selection = self.combo_ports.get()
        if not selection:
            messagebox.showerror("Erro", L["err_select_port"])
            return

        port = selection.split(' - ')[0]
        try:
            self.baud_rate = int(self.combo_baud.get())
            self.config['baud_rate'] = self.baud_rate
            save_config(self.config)

            self.serial_port = serial.Serial(port, self.baud_rate, timeout=1)
            self.connection_error = False # Reset error flag
            
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_dir = self.config['log_folder']
            if not os.path.exists(log_dir): os.makedirs(log_dir)

            log_name = os.path.join(log_dir, f"log_serial_{ts}.txt")
            self.metrics_filename_full = os.path.join(log_dir, f"metrics_{ts}.csv")
            
            self.log_file = open(log_name, 'a', encoding='utf-8')
            self.metrics_file = open(self.metrics_filename_full, 'w', newline='', encoding='utf-8')
            self.metrics_writer = csv.writer(self.metrics_file)
            self.metrics_writer.writerow(['Timestamp', 'IdleTime', 'AvgInterval', 'Boots', 'Panics', 'Errors'])
            
            self.is_monitoring = True
            self.seconds_since_last = 0
            self.interval_sum = 0
            self.interval_count = 0
            self.last_data_time = 0
            self.current_avg = 0.0
            self.stats = {"boots": 0, "panics": 0, "errors": 0}
            self.update_stats_labels()
            self.list_boot.delete(0, tk.END)
            
            self.btn_connect.config(text=L["disconnect"], bg="#ffcccc")
            self.status_var.set(L["status_monitor"].format(log_name))
            
            self.thread = threading.Thread(target=self.read_serial_loop)
            self.thread.daemon = True
            self.thread.start()
            
        except Exception as e:
            messagebox.showerror(L["err_connection"], str(e))

    def stop_monitoring(self):
        self.is_monitoring = False
        self.connection_error = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        if self.log_file: self.log_file.close()
        if self.metrics_file: self.metrics_file.close()
        
        self.btn_connect.config(text=LANGUAGES[self.current_lang]["connect"], bg="#dddddd")
        if self.current_theme == "dark": self.btn_connect.config(bg="#505050")
            
        self.status_var.set(LANGUAGES[self.current_lang]["status_stopped"])

    def read_serial_loop(self):
        while self.is_monitoring and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting:
                    self.connection_error = False # RX OK
                    current_time_epoch = time.time()
                    delta_t = 0.0
                    
                    if self.last_data_time > 0:
                        delta_t = current_time_epoch - self.last_data_time
                        if delta_t > 0.01:
                            self.interval_sum += delta_t
                            self.interval_count += 1
                            self.current_avg = self.interval_sum / self.interval_count
                            # ATUALIZADO: Atualiza label de Média
                            self.root.after(0, lambda a=self.current_avg: self.lbl_avg.config(text=f"{a:.2f}s"))
                    
                    self.last_data_time = current_time_epoch
                    self.seconds_since_last = 0
                    self.root.after(0, lambda: self.lbl_timer.config(text="0s", fg="blue"))
                    
                    line = self.serial_port.readline().decode('utf-8', errors='replace').strip()
                    if line:
                        now_obj = datetime.now()
                        ts_display = now_obj.strftime('%H:%M:%S.%f')[:-3]
                        ts_csv = now_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
                        
                        metrics_str = f"[DT:{delta_t:.2f}s AVG:{self.current_avg:.2f}s]"
                        log_entry = f"[{ts_display}] {metrics_str} {line}\n"
                        
                        line_lower = line.lower()
                        is_significant = False
                        
                        for filter_rule in self.config['filters']:
                            if filter_rule['keyword'] in line_lower:
                                f_type = filter_rule['type']
                                if f_type in self.stats:
                                    self.stats[f_type] += 1
                                    is_significant = True
                                break 

                        if self.metrics_writer:
                            self.metrics_writer.writerow([
                                ts_csv, f"{delta_t:.4f}", f"{self.current_avg:.4f}",
                                self.stats['boots'], self.stats['panics'], self.stats['errors']
                            ])
                            self.metrics_file.flush()

                        if is_significant:
                            self.root.after(0, self.update_stats_labels)
                            self.root.after(0, self.add_boot_event, ts_display, line)

                        self.root.after(0, self.append_text, log_entry)
                        
                        try:
                            if self.log_file:
                                self.log_file.write(log_entry)
                                self.log_file.flush()
                                self.root.after(0, lambda: self.flash_log_led(True))
                        except Exception:
                             self.root.after(0, lambda: self.flash_log_led(False))

            except Exception as e:
                # Se der erro no loop de leitura, marca flag para LED Vermelho
                self.connection_error = True
                print(f"Erro serial: {e}")
                break

    def update_stats_labels(self):
        L = LANGUAGES[self.current_lang]
        self.lbl_stat_boots.config(text=f"{L['boots']}: {self.stats['boots']}")
        self.lbl_stat_panics.config(text=f"{L['panics']}: {self.stats['panics']}")
        self.lbl_stat_errors.config(text=f"{L['errors']}: {self.stats['errors']}")

    def append_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text)
        num_lines = int(self.text_area.index('end-1c').split('.')[0])
        if num_lines > self.MAX_GUI_LINES:
            diff = num_lines - self.MAX_GUI_LINES
            self.text_area.delete("1.0", f"{diff}.0")
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def clear_screen(self):
        self.text_area.config(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.config(state='disabled')

    def add_boot_event(self, timestamp, line):
        short_line = line[:35] + "..." if len(line) > 35 else line
        self.list_boot.insert(0, f"[{timestamp}] Evento!")
        self.list_boot.insert(1, f"   {short_line}")
        self.list_boot.itemconfig(0, {'fg': 'red'})

    def check_led_status(self):
        # Lógica RX LED
        if self.is_monitoring:
            if self.connection_error:
                # Vermelho fixo se falhou
                self.led_rx_canvas.itemconfig(self.led_rx_oval, fill="#ff0000")
            elif (time.time() - self.last_data_time < 0.2):
                # Piscando verde se recebendo
                self.led_rx_canvas.itemconfig(self.led_rx_oval, fill="#00ff00")
            else:
                self.led_rx_canvas.itemconfig(self.led_rx_oval, fill="#555555")
        else:
            self.led_rx_canvas.itemconfig(self.led_rx_oval, fill="#555555")
            
        self.root.after(100, self.check_led_status)
    
    def update_timer_loop(self):
        if self.is_monitoring and not self.connection_error:
            self.seconds_since_last += 1
            self.lbl_timer.config(text=f"{self.seconds_since_last}s")
            if self.seconds_since_last > 10:
                self.lbl_timer.config(fg="red")
            else:
                self.lbl_timer.config(fg="blue")
        self.root.after(1000, self.update_timer_loop)

    def launch_plotter(self):
 
        if not self.metrics_filename_full or not os.path.exists(self.metrics_filename_full):
            messagebox.showinfo("Aviso", "Nenhum arquivo de métricas disponível.")
            return
        if self.metrics_file:
            self.metrics_file.flush()
        
        # Correção para Linux: Forçar contexto 'spawn' ao invés de 'fork'
        ctx = multiprocessing.get_context('spawn')
        p = ctx.Process(target=plot_worker, args=(self.metrics_filename_full,))
        p.start()
 
 
if __name__ == "__main__":
    # Necessário para PyInstaller no Windows com multiprocessing
    multiprocessing.freeze_support()
    
    try:
        multiprocessing.set_start_method('spawn')
    except RuntimeError:
        pass
    
 
    root = tk.Tk()
    app = SerialMonitorApp(root)
    root.mainloop()
 