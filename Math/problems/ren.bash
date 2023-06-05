i=1
for file in "Screenshot from"*; do
   new_name="S$i.png"
   mv "$file" "$new_name"
   ((i=i+1))
done

