#!/bin/bash
echo "Removing Match Reports:..."
rm -rf ../Report/*
echo "Removing Match Reports: Done"
wait
echo "Generating New Players"
python3 player_gen.py
echo "Generating New Players: Done"
wait
echo "Generating Tournament Schedule"
python3 league.py
echo "Generating Tournament Schedule: Done"
wait
echo "Ready for python simManager.py"