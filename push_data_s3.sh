s3cmd put scores.html  's3://geoguessr'
s3cmd setacl s3://geoguessr/scores.html --acl-public
