if [ -d ".venv" ]; then
    if [ -d ".venv/bin" ]; then
        .venv/bin/python main.py
    elif [ -d ".venv/Scripts" ]; then
        .venv/Scripts/python main.py
    fi
else
    python -m venv .venv
    if [ -d ".venv/bin" ]; then
        .venv/bin/pip install -r requirements.txt
    elif [ -d ".venv/Scripts" ]; then
        .venv/Scripts/pip install -r requirements.txt
    fi
fi
