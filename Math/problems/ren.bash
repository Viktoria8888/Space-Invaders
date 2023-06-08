i=1
for file in "S"*; do
   new_name="Problem$i.png"
   mv "$file" "$new_name"
   ((i=i+1))
done

