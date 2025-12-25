# Universal Serial Monitor

![License](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-green.svg)

> **Advanced Logging & Analysis Tool for Embedded Systems**
>
> *Ferramenta Avançada de Log e Análise para Sistemas Embarcados*

---

## 📋 Table of Contents / Índice

1. [About the Project / Sobre o Projeto](#about-the-project--sobre-o-projeto)
2. [Key Features / Funcionalidades](#key-features--funcionalidades)
3. [Installation / Instalação](#installation--instalação)
4. [Usage / Como Usar](#usage--como-usar)
5. [Repository Structure / Estrutura](#repository-structure--estrutura)
6. [Author & License / Autor & Licença](#author--license--autor--licença)

---

## <a name="about"></a> 🇺🇸 About the Project

The **Universal Serial Monitor** is a robust, lightweight, and cross-platform desktop application designed to facilitate the monitoring, logging, and analysis of serial data from embedded devices (ESP32, Arduino, Raspberry Pi, STM32).

It was developed to support research on air quality monitoring and vehicular emissions at the **Federal University of Ceará (UFC)**. Unlike standard serial monitors, this tool provides real-time stability metrics, automatic error detection (panics, resets), and persistent logging without requiring a heavy IDE installation.

## <a name="sobre"></a> 🇧🇷 Sobre o Projeto

O **Monitor Serial Universal** é uma aplicação desktop robusta, leve e multiplataforma, projetada para facilitar o monitoramento, registro e análise de dados seriais de dispositivos embarcados (ESP32, Arduino, Raspberry Pi, STM32).

Foi desenvolvido para apoiar pesquisas de monitoramento da qualidade do ar e emissões veiculares na **Universidade Federal do Ceará (UFC)**. Diferente de monitores seriais padrão, esta ferramenta fornece métricas de estabilidade em tempo real, detecção automática de erros (panics, resets) e registro persistente em arquivos, sem a necessidade de instalar uma IDE pesada.

---

## ✨ Key Features / Funcionalidades

| Feature | Description (EN) | Descrição (PT) |
| :--- | :--- | :--- |
| **Real-time Metrics** | Monitors connection stability (jitter), idle time, and average message intervals. | Monitora estabilidade da conexão (jitter), tempo ocioso e intervalos médios. |
| **Dual Logging** | Automatically saves raw serial output to `.txt` and structured metrics to `.csv`. | Salva automaticamente saída bruta em `.txt` e métricas estruturadas em `.csv`. |
| **Data Plotting** | Integrated graphing tool to visualize stability and error accumulation over time. | Ferramenta gráfica integrada para visualizar estabilidade e acúmulo de erros. |
| **Smart Filters** | Detects keywords like "Panic", "Error", "Boot". Allows custom filters via JSON config. | Detecta palavras-chave como "Panic", "Error", "Boot". Permite filtros personalizados via JSON. |
| **TX Capability** | Send commands to your device via serial interface. | Envie comandos para seu dispositivo via interface serial. |
| **Customization** | Dark Mode, English/Portuguese languages, and adjustable Baud Rates. | Modo Escuro, idiomas Inglês/Português e Baud Rates ajustáveis. |

---

## 🚀 Installation / Instalação

### Pre-requisites / Pré-requisitos
* **Windows/Linux/macOS**
* **Drivers:** Ensure your USB-Serial drivers (CH340, CP210x, etc.) are installed. / *Certifique-se de que os drivers USB-Serial estão instalados.*

### Running the Executable / Executando
No Python installation is required if you use the executable. / *Não é necessário instalar Python se usar o executável.*

1.  Navigate to the `dist` folder. / *Navegue até a pasta `dist`.*
2.  Run `Universal Serial Monitor.exe`. / *Execute `Universal Serial Monitor.exe`.*

### Running from Source / Rodando do Código Fonte
If you prefer to run or modify the Python script: / *Se preferir rodar ou modificar o script Python:*

```bash
# 1. Install dependencies
pip install pyserial matplotlib

# 2. Run the script
python "Universal Serial Monitor.py"
```

---

## 📖 Usage / Como Usar

1.  **Connect Device:** Plug your microcontroller into the USB port.
2.  **Select Port:** Click the refresh button (`↻`) and select the COM port.
3.  **Config:** Set the Baud Rate (Default: 115200).
4.  **Start:** Click **Start/Iniciar**.
    * 🟢 **RX LED (Green/Blinking):** Data receiving successfully.
    * 🔴 **RX LED (Red):** Connection error.
5.  **Analyze:**
    * Click **Charts/Gráficos** to open the real-time analysis window.
    * Check the sidebar for a history of Boot/Panic events.

---

## 📂 Repository Structure / Estrutura

```text
.
├── .gitignore                  # Git configuration / Configuração Git
├── LICENSE                     # GNU GPLv3 License / Licença
├── monitor_config.json         # User settings (auto-generated) / Configurações (auto-gerado)
├── README.md                   # Project Documentation / Documentação
├── Universal Serial Monitor.py # Main Source Code / Código Fonte Principal
├── Universal Serial Monitor.spec # PyInstaller Build Spec / Especificação de Build
└── Universal Serial Monitor.exe  # Executable File / Execultavel
```

---

## 👤 Author & License / Autor & Licença

**Developer:** Jairo Ivo Castro Brito  
*PhD Student at Federal University of Ceará (UFC)* *Department of Transport Engineering* This project is licensed under the **GNU GPLv3 License**.  
*Este projeto está licenciado sob a **Licença GNU GPLv3**.*

> "Software for a cleaner future."
```