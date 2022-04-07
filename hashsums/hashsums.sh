#!/bin/sh

set -e

build_hash_for_files() {
    # build hash file with $1 in $2 into $3
    # return 0 on success
    [ ! -d "$2" ] && printf "$2 is not dir." && return 1
    for f in $2/*; do
        if [ -d "$f" ]; then
            build_hash_for_files "$1" "$f" "$3" || return $?
        else
            $1 $f >> $3 || return $?
        fi
    done
    return 0

}

# build hash file with $1 in $2 into $3.
# Removes initial dir from the hashfile to simulate relative paths without
# having to deal with relative paths byitself.
# return 0 on success

echo "building $1 hashfile ($3) for $2"

rm -f $3

build_hash_for_files "$1" "$2" "$3" || return $?

# remove initial path to simulate relative paths
sed -i -e "s|$2[/]*||g" "$3"
return $?
