#!/bin/bash

if (-not (Test-Path -Path "venv")) {
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt 
} else {
    .\venv\Scripts\Activate.ps1
}

python -m src.game.TestReflexesGame @args