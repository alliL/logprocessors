#!/bin/bash


directory="branchjson"
gitbranch="EPC"

if [  -d "$directory" ]; then
	
	rm -rf ~/$directory
fi


cd ~/logprocessors
	rm -rf ~/logprocessors/branchjson
cd .
echo "Getting Git logs"

mkdir ~/$directory
cd ~/$gitbranch/
for branch in $(git branch --all | grep '^\s*remotes' | egrep --invert-match '(:?HEAD|master)$'); do
    echo "${branch##*/}"
    git checkout  "${branch##*/}"
    
    git log master..."${branch##*/}"\
    --date=local --after="2017-06-01T16:36:00-07:00" \
    --pretty=format:'{%n  "commit": "%H",%n  "author": "%aN <%aE>",%n  "date": "%ad",%n  "message": "%f"%n},' \
    $@ | \
    perl -pe 'BEGIN{print "["}; END{print "]\n"}' | \
    perl -pe 's/},]/}]/'> log.json
    sed 's/\\/\\\\/g' log.json > newlog
    
    git log master..."${branch##*/}"\
     --date=local --after="2017-06-01T16:36:00-07:00" \
    --numstat \
    --format='%H' \
    $@ | \
    perl -lawne '
        if (defined $F[1]) {
            print qq#{"insertions": "$F[0]", "deletions": "$F[1]", "path": "$F[2]"},#
        } elsif (defined $F[0]) {
            print qq#],\n"$F[0]": [#
        };
        END{print qq#],#}' | \
    tail -n +2 | \
    perl -wpe 'BEGIN{print "{"}; END{print "}"}' | \
    tr '\n' ' ' | \
    perl -wpe 's#(]|}),\s*(]|})#$1$2#g' | \
    perl -wpe 's#,\s*?}$#}#'> stat.json

    sed 's/\\/\\\\/g' stat.json > statlog

	
     jq --slurp '.[1] as $logstat | .[0] | map(.paths = $logstat[.commit])' newlog statlog > "${branch##*/}".json
	rm -rf log.json newlog statlog stat.json
	
	mv "${branch##*/}".json ~/$directory
			
done
mv ~/$directory ~/logprocessors

echo "Git logs Done"

