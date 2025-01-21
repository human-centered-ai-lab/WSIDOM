#!/bin/bash

#wget https://gdc.cancer.gov/system/files/public/file/gdc-client_v1.6.1_Ubuntu_x64.zip
#unzip gdc-client_v1.6.1_Ubuntu_x64.zip
#chmod +x ./gdc-client
./../examples/gdc-client download -m gdc_manifest_TCGA_slides.tsv
#./gdc-client download -m gdc_manifest_TCGA_test_slides.tsv
