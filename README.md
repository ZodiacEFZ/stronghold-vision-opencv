# stronghold-vision-opencv

Vision process with OpenCV by Zodiac.

## License

MIT

声明：我们允许组织以及个人将此项目用于商业行为，没有任何限制。
但**请带上本项目的许可证 `MIT`**，并**附上原作者以及项目的地址**。我们保留对该项目的最终解释权。

## Install

`Python3`, `numpy`, `cv2`, `matplotlib` are required to run this script.
To communicate with roboRIO, you also need `pynetworktables`.

Install OpenCV 3.1 for Python3, and then install other requirements:

```
git clone https://github.com/ZodiacEFZ/stronghold-vision-opencv && cd stronghold-vision-opencv

pip install -r requirements.txt
```

## Analyze

Put all test images in `./TestData/RealFullField` folder, then run `./analyze.py`.
Then there will be a window showing analyze result.

Uncomment `cv2.imwrite("TestData/Result/res%d.png" % (i), img)` then result images
will be put in `./TestData/Result` with contours drawn on.

## Production

Run `./video.py`, then OpenCV will read data from the default camera and analyze data.
With NetworkTables you can enable/disable vision process, manual exposure. And
this vision daemon will report target data to NetworkTables. Also an mjpeg server will
be set up to transfer **processed** image stream.

## Structure

`detect` folder stores detect algorithm.

`grip` folder stores origin grip solution.

## Config

Create `config.py`. Here's an example.

```
server = {
    "host": "",
    "port": 8080,
    "rioAddress": "roboRIO-9036-FRC.local"
}
camera = {
    "width": 640,
    "height": 480,
    "fps": 30,
    "r_width": 322,
    "r_height": 245,
    "cX": 320,
    "cY": 240,
    "id": 0
}
```

## How to use

After running `./video.py`, vision daemon will start an http server serving
mjpeg stream at specified port. Because this server only support one connection,
You should use a mjpeg [proxy](https://github.com/ZodiacEFZ/stronghold-vision-mjpeg-proxy)
to transfer video data.

If you want to view vision settings, deploy a
[WebDashboard](https://github.com/ZodiacEFZ/stronghold-vision-webdashboard).
