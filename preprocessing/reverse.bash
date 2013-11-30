file=$1

if [ -e .reverse_temp ]
then
    rm .reverse_temp
fi

if [ -e .reverse_body ] 
then
    rm .reverse_body
fi

# Just so this works on mac too, since mac 
# doesn't have 'tac'
head -1 $file >> .reverse_temp
tail -n +2 $file >> .reverse_body
sed '1!G;h;$!d' .reverse_body >> .reverse_temp

rm .reverse_body
mv .reverse_temp $file
