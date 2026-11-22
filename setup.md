# Setup

## 🔧 .venv

### Creating virtual environments

```bash
python -m venv .venv
```

### Command to activate virtual environment

```bash
source .venv/Scripts/activate    # bash
.venv/Scripts/activate.bat       # cmd
.venv/Scripts/Activate.ps1       # PowerShell
```

## 🧩 VS Code

### Select Interpreter

1. Enter <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> in your vscode.

2. Locate your Virtual Environment:  
   **Python: Select Interpreter > Enter interpreter path... > _select_**

3. Once you locate your virtual env select your python version:  
   **.venv\Scripts\python.exe**.

4. Now in your project you will see `.vscode` directory created open `settings.json` inside of it and add:  
   **"python.terminal.activateEnvironment": true**

5. Now restart the terminal.

### Extensions

- [Python Environments](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Qt for Python](https://marketplace.visualstudio.com/items?itemName=seanwu.vscode-qt-for-python)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Sort CSS](https://marketplace.visualstudio.com/items?itemName=piyushsarkar.sort-css-properties)
- [Terminals Manager](https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-terminals)

## ⚙️ .vscode

### settings.json

```json
{
  "search.exclude": {
    "**/.venv": true
  },
  "workbench.editorAssociations": {
    "*.svg": "default"
  },
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true,
  "editor.rulers": [125],
  "python.testing.unittestArgs": ["-v", "-s", "./tests", "-p", "test_*.py"],
  "python.testing.pytestEnabled": false,
  "python.testing.unittestEnabled": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "ruff.lineLength": 125,
  "ruff.organizeImports": true,
  "ruff.configuration": {
    "lint": {
      "ignore": ["BLE001", "D202", "UP035", "UP045", "TRY002", "PLW1510"],
      "isort": {
        "lines-after-imports": 2
      }
    },
    "format": {
      "quote-style": "double"
    }
  },
  "sortcss.sortingStrategy": "concentric-css"
}
```

### terminals.json

- [Terminals Manager](https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-terminals)
- [Integrated Terminal colors](https://code.visualstudio.com/api/references/theme-color?color-formats#integrated-terminal-colors)

```json
{
  "autorun": true,
  "autokill": true,
  "terminals": [
    {
      "name": "app",
      "icon": "terminal",
      "color": "terminal.ansiMagenta",
      "commands": ["source .venv/Scripts/activate", "python src/main.py"],
      "execute": true,
      "shellPath": "C:\\Program Files\\Git\\bin\\bash.exe"
    },
    {
      "name": "root",
      "icon": "file-directory",
      "color": "terminal.ansiGreen",
      "shellPath": "C:\\Program Files\\Git\\bin\\bash.exe"
    }
  ]
}
```

### launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "python src/main.py",
      "type": "debugpy",
      "request": "launch",
      "program": "src/main.py",
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```
