#!/bin/bash
# run phoenix interactive or smoke test
. ./setup.sh
set -eu
# usage function
function usage()
{
   cat << HEREDOC
   Usage: $progname

   run phoenix container . default interactive
   Optional arguments:
     -h, --help      show this help message and exit
     -s, --smoke     run container and do a smoke test
     -t, --tshark    run container with privileged mode for tshark
HEREDOC
}


# initialize variables
progname=$(basename $0)
smoke=0
tshark=0
tshark_args=""

OPTS=$(getopt -o "hst" --long "help,smoke,tshark" -n "$progname" -- "$@")
if [ $? != 0 ] ; then echo "Error in command line arguments." >&2 ; usage; exit 1 ; fi
eval set -- "$OPTS"

while true; do
  case "$1" in
    -h | --help ) usage; exit; ;;
    -s | --smoke ) smoke=1; shift ;;
    -t | --tshark ) tshark=1; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

if [ $tshark != 0 ]
then
  tshark_args="--privileged --network=host"
fi

function run(){
    rm -rf $git_root/../tmp_phn
    mkdir $git_root/../tmp_phn
    chmod 777 $git_root/../tmp_phn
    docker rm $cnt_phn --force 2>/dev/null || true
    docker run -d \
        --name  $cnt_phn \
        -p     5432:5432 \
        -p     15432:5432 \
        -p     13306:5432 \
        -e POSTGRES_PASSWORD=pass1 \
        $tshark_args \
        --cap-add=SYS_PTRACE \
        --mount type=bind,source=$git_root/code,target=/$cnt_user/code \
        --mount type=bind,source=$git_root/../tmp_phn,target=/$cnt_user/tmp_phn \
        $image_phn
}

function exec_interactive(){
    docker exec -t $cnt_phn /bin/bash -c 'pg_stop   '
    docker exec -t $cnt_phn /bin/bash -c 'pg_init  '
    # docker exec -t $cnt_phn /bin/bash -c 'pg_start '
    docker exec -it $cnt_phn /bin/bash
}

function exec_smoke(){

    # stop/reinit /start /simple select
    docker exec -t $cnt_phn /bin/bash -c 'pg_stop   '
    docker exec -t $cnt_phn /bin/bash -c 'pg_init && pg_start '
    docker exec -t $cnt_phn /bin/bash -c 'psql -c "select 1" '
    rc=$?
}

run

retc=0
# continue regardless of errors
set +eu
if [ $smoke != 0 ]
then
    exec_smoke
else
    exec_interactive
fi
echo "return code ======= $rc"
