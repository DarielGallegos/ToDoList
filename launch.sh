#! /bin/bash

echo "Launching the program..."
if [ ! -d "repositories" ]; then
    mkdir repositories
    touch repositories/todolist.db3
fi
python3 main.py
echo "Program finished."