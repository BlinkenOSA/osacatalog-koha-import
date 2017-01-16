CURRENT_DIR=$(pwd)
PYTHON="/opt/python/bin/python"

KOHA_URL='http://koha:8080'
KOHA_USER='koha_user'
KOHA_PASS='koha_pass'
SOLR_URL='http://localhost:8983/solr/osacatalog'

KOHA_AUTH=$KOHA_URL+'/cgi-bin/koha/svc/authentication?userid='+$KOHA_USER+'&password='+$KOHA_PASS
KOHA_EXPORT=$KOHA_URL+'/cgi-bin/koha/tools/export.pl'

mkdir -p $CURRENT_DIR/koha-records-prep/input
mkdir -p $CURRENT_DIR/koha-records-prep/output
rm $CURRENT_DIR/koha-records-prep/input/koha-library.mrc
rm $CURRENT_DIR/koha-records-prep/output/koha-library.mrc
rm $CURRENT_DIR/koha-records-prep/input/koha-filmlibrary.mrc
rm $CURRENT_DIR/koha-records-prep/output/koha-library.mrc
curl $KOHA_AUTH --cookie-jar $CURRENT_DIR/koha-export.cookies
curl -X POST -F "record_type=bibs" -F "op=export" -F "branch=OSA" -F "output_format=iso2709" -F "filename=koha_library.mrc" --cookie $CURRENT_DIR/koha-export.cookies $KOHA_EXPORT > $CURRENT_DIR/koha-records-prep/input/koha-library.mrc
curl -X POST -F "record_type=bibs" -F "op=export" -F "branch=FL" -F "output_format=iso2709" -F "filename=koha_filmlibrary.mrc" --cookie $CURRENT_DIR/koha-export.cookies $KOHA_EXPORT > $CURRENT_DIR/koha-records-prep/input/koha-filmlibrary.mrc
$PYTHON $CURRENT_DIR/koha-records-prep/update_hashids_marc.py
curl $SOLR_URL+'/update?commit=true' -d '<delete><query>record_origin_facet:"Library"</query></delete>'
curl $SOLR_URL+'/update?commit=true' -d '<delete><query>record_origin_facet:"Film Library"</query></delete>'
$CURRENT_DIR/solrmarc/bin/indexfile config-library.properties $CURRENT_DIR/koha-records-prep/output/koha-library*.mrc
$CURRENT_DIR/solrmarc/bin/indexfile config-filmlibrary.properties $CURRENT_DIR/koha-records-prep/output/koha-filmlibrary*.mrc
rm $CURRENT_DIR/koha-export.cookies
