cd src

for FILE in *
do
  if [ "$FILE" = *.nim ]
  then
    nim c --threads:on --app:lib --out:${FILE%.nim}.so $FILE
  fi
done

cd ..
