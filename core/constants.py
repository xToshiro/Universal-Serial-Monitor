import os

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