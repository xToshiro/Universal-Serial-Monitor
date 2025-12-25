import multiprocessing
import tkinter as tk
from core.gui import SerialMonitorApp

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