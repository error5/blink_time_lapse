# you need to install 'apt install ffmpeg' and adjust frame rate according to image frequency 

ffmpeg -loglevel debug -framerate 8 -pattern_type glob -i '*.jpg' -c:v libx264 -pix_fmt yuv420p output_video.mp4 -y
