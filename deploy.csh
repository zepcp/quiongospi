#! /bin/csh -f

set dir = "/home/pi/Documents/quiongospi"

echo `date`" - Moving to "$dir
cd $dir

echo `date`" - Pulling from github"
set result = `git pull`

if ("$result" == "Already up-to-date.") then
    echo `date`" - "$result
else
    echo `date`" - Restarting supervisor"
    sudo supervisorctl reread
    sudo service supervisor restart
endif

echo `date`" - Script finished successfully"