pylint approvaltests --disable=C0103,W0703,C0415,W1514,R0913

:: W1514 - Unsure how to fix this, as google answer breaks code ( https://stackoverflow.com/questions/54835232/python-codec-error-during-file-write-with-utf-8-string )
:: R0913 - at some point break back compatibility and clean up API
:: pylint --disable=all --enable=C0103 .\approvaltests\
