fileName=$1

sed 's/^/block:/' ${fileName} > ${fileName}.block

#~/TransferTeam/phedex/FileDeleteTMDB -db ~/param/DBParam:Prod/OPSNARAYANAN -list ${fileName}.block -invalidate
for b in $(cat ${fileName}); do
  ~/TransferTeam/dbs/DBS3SetFileStatus.py --url=https://cmsweb.cern.ch/dbs/prod/global/DBSWriter --status=invalid --recursive=False --block=$b
done
