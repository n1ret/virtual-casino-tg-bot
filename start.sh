if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    if [ -d ".venv/bin" ]; then
        .venv/bin/pip install -r requirements.txt
    elif [ -d ".venv/Scripts" ]; then
        .venv/Scripts/pip install -r requirements.txt
    fi
fi

if [ -d ".venv/bin" ]; then
    .venv/bin/python main.py
elif [ -d ".venv/Scripts" ]; then
    .venv/Scripts/python main.py
fi
