cd png_to_klg
# set  the path for the depth.txt and rgb.txt.  ** feed the depth file first and then rgb file **
python associate.py ../bag_data/600/depth.txt ../bag_data/600/rgb.txt > associations.txt 
# to copy the associations.txt to your your_bag_data_name's path
cp associations.txt ../bag_data/600/associations.txt

cd build

./pngtoklg -w ../../bag_data/600 -o ../../bag_data/600/600.klg -t
