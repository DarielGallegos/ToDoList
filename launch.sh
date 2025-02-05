#! /bin/bash

if [ ! -d "repositories" ]; then
    mkdir repositories
    touch repositories/todolist.db3
fi

if ! command -v pip &> /dev/null ; then
    echo "Pip is not installed."
    echo "Installing pip..."
    sudo apt update && sudo apt upgrade
    sudo apt install libncurses5-dev libncursesw5-dev -y
    sudo apt-get install python3-pip -y
fi

python3 main.py