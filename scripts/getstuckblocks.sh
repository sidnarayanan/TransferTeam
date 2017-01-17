wget -O - "https://cmsweb.cern.ch/phedex/datasvc/perl/prod/blockarrive?block=${1}%23*&to_node=${2}" | grep "NAME" | sed "s?.*'/?\/?" | sed "s?.*NAME.*??g" | sed "s?',??g" | grep / 2>/dev/null

