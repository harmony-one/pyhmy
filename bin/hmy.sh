#!/usr/bin/env bash

BUCKET='pub.harmony.one'
OS="$(uname -s)"

usage () {
    cat << EOT
Usage: $0 [option] command

Options:
   -d          download all the binaries
   -h          print this help
Note: Arguments must be passed at the end for ./hmy to work correctly.
For instance: ./hmy.sh balances <one-address> --node=https://api.s0.p.hmny.io/

EOT
}

set_download () {
    local rel='mainnet'
    case "$OS" in
	Darwin)
	    FOLDER=release/darwin-x86_64/${rel}/
	    BIN=( hmy libbls384_256.dylib libcrypto.1.0.0.dylib libgmp.10.dylib libgmpxx.4.dylib libmcl.dylib )
	    ;;
	Linux)
	    FOLDER=release/linux-x86_64/${rel}/
	    BIN=( hmy )
	    ;;
	*)
	    echo "${OS} not supported."
	    exit 2
	    ;;
    esac
}

do_download () {
    # download all the binaries
    for bin in "${BIN[@]}"; do
	rm -f ${bin}
	curl http://${BUCKET}.s3.amazonaws.com/${FOLDER}${bin} -o ${bin}
    done
    chmod +x hmy
}

while getopts "dh" opt; do
    case ${opt} in
        d)
            set_download
            do_download
            exit 0
            ;;
        h|*)
            usage
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))

if [ "$OS" = "Linux" ]; then
    ./hmy "$@"
else
    DYLD_FALLBACK_LIBRARY_PATH="$(pwd)" ./hmy "$@"
fi
