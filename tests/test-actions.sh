#!/bin/sh

srcdir=.
[ -r ./env.sh ] && . ./env.sh
. $srcdir/testlib.sh

tstart $srcdir/gallery.py

a=$(lca-tool --tracker --print an.image)
strstr "$a" '.*galleryserviceinterface' || exit 1
strstr "$a" '.*plainimageviewer' || exit 1

a=$(lca-tool --tracker --print an.image b.image)
strstr "$a" '.*galleryserviceinterface' || exit 1
strstr "$a" '.*plainimageviewer' || exit 1

a=$(lca-tool --tracker --print a.music)
strstr "$a" '.*plainmusicplayer' || exit 1

a=$(lca-tool --tracker --print a.music b.music)
strstr "$a" '.*plainmusicplayer' || exit 1

echo test > /tmp/test.html
atexit rm -f /tmp/test.html
uri="file:///tmp/test.html"
a=$(lca-tool --file --print $uri)
strstr "$a" '.*fixedparams' || exit 1

exit 0
