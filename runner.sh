#!/bin/sh
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh

bash ~/miniconda.sh -b -p ~/miniconda

export PATH="$HOME/miniconda/bin":$PATH
pip install Streamlit
conda install git

git clone https://https://github.com/Asad1287/Reliability_Analyzer.git
cd reliability_analyzer

pip install -r src/requirements.txt
sudo yum install tmux
tmux
streamlit run src/main.py 