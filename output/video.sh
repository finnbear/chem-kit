yes y | ffmpeg -framerate 25 -i frame%05d.png -c:v libx264 -r 30 -pix_fmt yuv420p Chem-Output.mp4
rm ./*.png
