#!/bin/bash

# A script that is used to check for late submissions. This script will prompt
# the user before deleting any symbolic links, so it is safe to run. It also 
# does a quick check on the entered deadline. 
#
# Author: Ivan Gozali

if [ -z $1 ]; then
    echo
    echo "Usage                       : ./checklate.sh deadline"
    echo "Format of deadline argument : yyyymmddHHMM"
    echo
    echo "Example                     : ./checklate.sh 201209080100"
    echo
    echo "Homework 1 deadline, for example (in GMT, to maintain compatibility with get-submissions):"
    echo "HW1 : 201301282000"

    exit 1
fi

deadline=$1

echo "Entered deadline is ${deadline:4:2}-${deadline:6:2}-${deadline:0:4} ${deadline:8:2}:${deadline:10:2}. Ensure deadline is correct before proceeding."
echo -n "Is deadline correct? [y/n]"
read YN

case $YN in
[yY]*) 
    ;;
[nN]*) echo "Incorrect deadline entered."
    exit 1
    ;;
esac

for file in $(ls)
do
    login=${file%%.*}
    timestamp=${file##*.}

    if [[ ${login:0:4} == "cs70" ]]; then
        if [[ "$timestamp" > "$deadline" ]]; then
            echo
            echo "File: " $file
            echo "Login: " $login
            echo "Timestamp: " ${timestamp:4:2}-${timestamp:6:2}-${timestamp:0:4} ${timestamp:8:2}:${timestamp:10:2}

            echo -n "This submission is past the deadline ($deadline). Would you like to delete the symbolic link? [y/n]"
            read YN

            case $YN in
            [yY]*) rm -fv $file
                ;;
            [nN]*) echo "Skipping file $file"
                ;;
            esac
        fi
    fi
done
