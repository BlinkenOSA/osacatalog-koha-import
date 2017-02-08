SOLRMARC_PATH = /Users/Josh/dev/solrmarc
CURRENT_DIR=$(pwd)
$SOLRMARC_PATH/bin/indexfile $CURRENT_DIR/config-library.properties $CURRENT_DIR/koha-records-prep/output/koha-library*.mrc
