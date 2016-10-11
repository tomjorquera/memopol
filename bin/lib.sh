if [ -n "$OPENSHIFT_HOMEDIR" ]; then
    source ${OPENSHIFT_HOMEDIR}app-root/runtime/dependencies/python/virtenv/bin/activate
fi

function parltrack_download_pipe() {
    if [ -n "$OPENSHIFT_DATA_DIR" ]; then
        cd $OPENSHIFT_DATA_DIR
    fi

    [ -n "$CLEAN" ] && rm -rf $1
    [ -f "$1" ] || wget http://parltrack.euwiki.org/dumps/$1 || exit 1

    if [ -n "$OPENSHIFT_REPO_DIR" ]; then
        cd $OPENSHIFT_REPO_DIR
    fi

    export DJANGO_SETTINGS_MODULE=memopol.settings
    unxz -c ${OPENSHIFT_DATA_DIR}$1 | $2
    [ -n "$CLEAN" ] && rm -rf $1
}

function francedata_download_pipe() {
    if [ -n "$OPENSHIFT_DATA_DIR" ]; then
        cd $OPENSHIFT_DATA_DIR
    fi

    [ -n "$CLEAN" ] && rm -rf $1
    [ -f "$1" ] || wget https://francedata-njoyard.rhcloud.com/$1 || exit 1

    if [ -n "$OPENSHIFT_REPO_DIR" ]; then
        cd $OPENSHIFT_REPO_DIR
    fi

    export DJANGO_SETTINGS_MODULE=memopol.settings
    gunzip -c ${OPENSHIFT_DATA_DIR}$1 | $2
    [ -n "$CLEAN" ] && rm -rf $1
}

function refresh_scores() {
    if [ -n "$OPENSHIFT_REPO_DIR" ]; then
        cd $OPENSHIFT_REPO_DIR
    fi

    export DJANGO_SETTINGS_MODULE=memopol.settings
    memopol refresh_scores
}
