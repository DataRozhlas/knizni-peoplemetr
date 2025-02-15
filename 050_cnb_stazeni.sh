# Skript stáhne z webu Národní knihovny následující data:
# - Česká národní bibliografie (cnb.xml)
# - Databáze národních autorit NK ČR (aut.xml)
# - Souborný katalog ČR (skc.xml -- bacha, 27 GB)
rm "./downloads/smazat_cnb.xml.gz"
rm "./downloads/smazat_aut.xml.gz"
rm "./downloads/smazat_skc.xml.gz"
mv "./downloads/cnb.xml.gz" "./downloads/smazat_cnb.xml.gz"
mv "./downloads/aut.xml.gz" "./downloads/smazat_aut.xml.gz"
mv "./downloads/skc.xml.gz" "./downloads/smazat_skc.xml.gz"
wget --tries=5 --waitretry=10 --timeout=30 --continue -O ./downloads/cnb.xml.gz https://aleph.nkp.cz/data/cnb.xml.gz
wget --tries=5 --waitretry=10 --timeout=30 --continue -O ./downloads/aut.xml.gz https://aleph.nkp.cz/data/aut.xml.gz
wget --tries=5 --waitretry=10 --timeout=30 --continue -O ./downloads/skc.xml.gz https://aleph.nkp.cz/data/skc.xml.gz
gunzip -c --force ./downloads/cnb.xml.gz > ./downloads/cnb.xml
gunzip -c --force ./downloads/aut.xml.gz > ./downloads/aut.xml
gunzip -c --force ./downloads/skc.xml.gz > ./downloads/skc.xml