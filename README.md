## 构成

| 工具                                                     | 作用                                                         |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| adb command                                              | 基本上都是通过调用adb命令来完成手指类的操作                  |
| OpenCV                                                   | 使用模板匹配来定位某些动态元素                               |
| [→PaddleOCR←](https://github.com/PaddlePaddle/PaddleOCR) | 文字识别及提取                                               |
| [→ADBKeyBoard←](https://github.com/senzhk/ADBKeyBoard)   | 由于adb命令是无法输入某些文字的，用该工具代替adb原始输入操作 |
| [→clipper←](https://github.com/majido/clipper)           | 经测试，由于提取所在页面的链接时会复制到手机剪贴板，但是当量过多时就出错了，用该工具代替了原始的剪贴版 |

## 使用

测试环境为小米8 Lite，Android：9

```bash
pip install paddlepaddle
pip install paddleocr

pip uninstall numpy
pip install -U numpy==1.23
```

由于不同手机的像素及颜色深度可能不同，为此，需做以下修改。

- 由于用到了图片模板匹配，img目录下的图片，需要手动更换一遍。

- `config.py`文件中的button_location区域的坐标位置也需手动修改，可通过(Appium与Appium Inspector)进行定位，或其他UI元素定位软件

详细内容见代码注释。
