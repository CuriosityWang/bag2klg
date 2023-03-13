# 使用自制离线数据跑通ElasticFusion

## 实验环境及设备

实验环境：

- Ubuntu22.04 
- RTX3060

实验设备：

- 小米13（Android）
- Realsense D455

一句话总结就是，使用**我的手机连接realsense**去室外录制相关离线数据(**.bag**格式)，然后转换成ElasticiFusion的.**klg**格式进行三维重建。

<img src="http://49.235.90.42:800/images/2023/03/13/138_1678672876_hd.jpg" alt="138_1678672876_hd" style="zoom: 33%;" />

过程中还是遇到了不少坑的，比如深度图的尺度以及编码问题，导致一开始的重建总是不顺利。

## 代码

目录组织：

![image-20230313112427061](https://img2023.cnblogs.com/blog/1906082/202303/1906082-20230313163719930-334082053.png)

## Env

#### 编译`png_to_klg`

这里的代码主要参考了https://github.com/HTLife/png_to_klg

  - CMake
  - Boost
  - zlib
  - libjpeg
  - OpenCV

**==在编译之前要修改 `main.cpp` 下第45行的 depth_scale 为1000，realsense默认是1000==**

![image-20230313114213147](https://img2023.cnblogs.com/blog/1906082/202303/1906082-20230313163721920-468072754.png)

**build**

```bash
cd png_to_klg
mkdir build
cd build
cmake ..
make
```

#### ros相关库

建议使用虚拟环境

**numpy**

```bash
pip install numpy
```

**rosbag**

```bash
pip install --extra-index-url https://rospypi.github.io/simple/ rosbag
pip install roslz4 --extra-index-url https://rospypi.github.io/simple/
```

**cv_bridge**

1. 下载源码https://codeload.github.com/ros-perception/vision_opencv/zip/refs/heads/noetic

2. cd至cv_bridge文件夹

3. 然后命令行安装

   ```bash
   python setup.py install
   ```

**sensor_image and geometry_msgs**

```bash
pip install sensor_msgs --extra-index-url https://rospypi.github.io/simple/
pip install geometry_msgs --extra-index-url https://rospypi.github.io/simple/
```

**rospy**

```bash
pip install -i https://pypi.douban.com/simple rospy
```

**cv_bridge.boost**

在这里下载 https://github.com/rospypi/simple/raw/any/cv-bridge/cv_bridge-1.13.0.post0-py2.py3-none-any.whl

```bash
pip install cv_bridge-1.13.0.post0-py2.py3-none-any.whl
```

## Usage

1. run read_bag.py

```bash
python read_bad.py -n YourBagFile -d YourDepthTopic -r YourRGBTopic 
```

2. 根据提示修改 png2klg.sh相关参数

```ba
cd png_to_klg
# set  the path for the depth.txt and rgb.txt.  ** feed the depth file first and then rgb file **
python associate.py ../bag_data/600/depth.txt ../bag_data/600/rgb.txt > associations.txt 
# to copy the associations.txt to your your_bag_data's path
cp associations.txt ../bag_data/600/associations.txt

cd build
# -w is the extracted rgb and depth images's path -o is the output
./pngtoklg -w ../../bag_data/600 -o ../../bag_data/600/600.klg -t

```

2. run png2klg.sh

```bash
sh png2klg.sh
```

最后的目录应该是这样：

<img src="http://49.235.90.42:800/images/2023/03/13/image-20230313162714627.png" alt="image-20230313162714627" style="zoom: 67%;" />

3. 使用编译好的 ElasticFusion运行

```
./ElasticFusion -l 600.klg
```

## Refer

https://github.com/HTLife/png_to_klg
