#!/bin/sed -f
# sed script made using suggestions from  http://tvtropes.org/pmwiki/pmwiki.php/Main/Hulkspeak
s/ing\>//g
s/\<I\>/Me/g
s/\<i\>/me/g
s/\<[Tt]he\> //g
s/\<[Tt]o\> //g
s/\<[Aa]\> //g
s/\<[Aa]n\> //g
s/\<[Aa]re\> //g
s/\<[Aa]m\> //g
s/\<[Dd]o\> //g
s/\<[Dd]oes\> //g
y/abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ/
