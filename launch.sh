#! /bin/bash

if [ ! -d "repositories" ]; then
    mkdir repositories
    touch repositories/todolist.db3
fi

if ! command -v pip &> /dev/null ; then
    echo "Pip is not installed."
    echo "Installing pip..."
    sudo apt update && sudo apt upgrade
    #sudo apt install libncurses5-dev libncursesw5-dev -y
    pip install textual
    sudo apt-get install python3-pip -y
fi

if ! command pip list | grep textual &> /dev/null ; then
    echo "Textual is not installed."
    echo "Installing textual..."
    pip install textual
fi

# Run the program
python3 main.py

# Run the program in dev mode