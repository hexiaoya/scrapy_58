#!/bin/bash
apt update && apt install -y wget bzip2
ANACONDA_URL="https://repo.continuum.io/archive/"
ANACONDA_VERSION=`wget --no-check-certificate -qO- $ANACONDA_URL | grep -o '"Anaconda3.*-Linux-x86_64.sh"' | cut -d '"' -f 2 | sort -r | head -n 1`
wget --no-check-certificate $ANACONDA_URL$ANACONDA_VERSION -O anaconda3-install.sh
echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh
/bin/bash anaconda3-install.sh -b -p /opt/conda
rm -f anaconda3-install.sh
#export PATH=/opt/conda/bin:$PATH
#source /etc/profile
