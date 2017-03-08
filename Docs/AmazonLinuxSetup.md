

## Install basics
sudo yum -y update
sudo yum -y upgrade
sudo yum -y install python34
sudo yum -y install python34-virtualenv
sudo alternatives --set python /usr/bin/python3.4
sudo yum -y install blas lapack atlas-sse3-devel gcc

## Create Venv
virtualenv-3.4 stack
source ~/stack/bin/activate

## Setup Python
pip install --upgrade pip
pip3 install numpy
pip3 install scipy
pip3 install sklearn
pip3 install pandas
pip3 install flask
pip3 install boto

## Upload Flask API & Test
It worked...
