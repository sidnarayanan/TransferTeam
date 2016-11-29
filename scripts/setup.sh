cwd=$PWD
source ~/phedex/PHEDEX/etc/profile.d/env.sh
cd ~/CMSSW_7_4_15/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init -voms cms
cd $cwd
