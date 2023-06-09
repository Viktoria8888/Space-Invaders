i=1
for file in "Problem"*; do
   name="Problem$i.png"
   convert $name -resize 65% $name
   ((i=i+1))
done

