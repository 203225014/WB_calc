#!/bin/bash
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd backend && pip install -e .