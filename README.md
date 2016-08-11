# stronghold-vision-opencv

Vision process with OpenCV. By Team 9036.

## License

MIT

## Analyze

Put all test images in `./TestData/RealFullField` folder, then run `./analyze.py`.
Then there will be a window showing analyze result.

Uncomment `cv2.imwrite("TestData/Result/res%d.png" % (i), img)` then result images
will be put in `./TestData/Result` with contours drawn on.

## Production

Run `./video.py`, then OpenCV will read data from the default camera and analyze data.
With NetworkTables you can enable/disable vision process, manual exposure. And
this vision daemon will report target data to NetworkTables.

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

After running `./video.py`, vision daemon will start an http server at specified port.
You should use a [proxy](https://github.com/SkyZH/stronghold-vision-mjpeg-proxy) and
[webdashboard](https://github.com/SkyZH/stronghold-vision-webdashboard) to see vision data.
