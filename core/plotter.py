import csv
from datetime import datetime
import os
import tkinter.messagebox as messagebox

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