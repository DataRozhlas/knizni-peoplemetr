Dlouhodobé sledování české knižní produkce. Časem z toho půjdou říkat věci, např. do jakých období směrují nakladatelství novinky, která předvánoční anketa knihám pomáhá nejvíc, jak se liší popisy knih psanými muži a ženami atd.

Současná pipeline: novinky z Martinusu → JSON (momentálně v ```.gitignore```) → ISBNs nepřekladových knih vydaných v letech 2023 a 2024 periodicky do Goodreads a Databáze knih → JSON (ve složce ```data```).

Todo:

- Scrapovat toho z Martinusu víc: ukázky e-booků, info o bestsellerech, čtenářské hodnocení.

- Zlepšit filtrování novinek pro sledování.

- Pokusit se získat informace o přesných datech vydání (něco je na Goodreads, ne moc spolehlivé).

- Napojit další zdroje dat: [Národní knihovna](https://text.nkp.cz/o-knihovne/odborne-cinnosti/otevrena-data).

- Dashboard s trendy.