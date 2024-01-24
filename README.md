
<div align="center">

  <img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/Logo.png?raw=true?raw=true" alt="logo" width="180px"/>

  ![Version](https://img.shields.io/badge/node_version-0.1.4-green?style=for-the-badge&labelColor=darkgreen)

  [![Commit activity](https://img.shields.io/github/commit-activity/t/abdozmantar/ComfyUI-InstaSwap/main?cacheSeconds=0)](https://github.com/Gourieff/comfyui-reactor-node/commits/main)
  ![Last commit](https://img.shields.io/github/last-commit/abdozmantar/ComfyUI-InstaSwap/main?cacheSeconds=0)
  [![Opened issues](https://img.shields.io/github/issues/abdozmantar/ComfyUI-InstaSwap?color=red)](https://github.com/Gourieff/comfyui-reactor-node/issues?cacheSeconds=0)
  [![Closed issues](https://img.shields.io/github/issues-closed/abdozmantar/ComfyUI-InstaSwap?color=green&cacheSeconds=0)](https://github.com/Gourieff/comfyui-reactor-node/issues?q=is%3Aissue+is%3Aclosed)
  ![License](https://img.shields.io/github/license/abdozmantar/ComfyUI-InstaSwap)

# InstaSwap Face Swap Node for ComfyUI
</div>

### Fastest Face Swap Extension Node for ComfyUI, Single node and FastTrack: Lightning-Speed Facial Transformation for your projects.

<div align="center">

---
[**Installation**](#installation) | [**Usage**](#usage) | [**Troubleshooting**](#troubleshooting)  | [**Disclaimer**](#disclaimer)

---
## Demo
</div>
<div align="center">
  <img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/help/Promo.gif?raw=true" alt="demo" width="100%"/>
</div>

## Installation


1. Clone this repository to your ComfyUI custom nodes folder. There is two way :  
- A) Download this repository  as a zip file and extract files in to `comfyui\custom_nodes\ComfyUI-InstaSwap` folder.

- B) Go to `comfyui\custom_nodes\` folder open a terminal window here and run `git clone https://github.com/abdozmantar/ComfyUI-InstaSwap` command.

2. Go to `comfyui\custom_nodes\ComfyUI-InstaSwap` folder and open a terminal window and run `python install.py` command. If you using windows you can double click `install.bat` alternatively. 

3. Wait patiently installation to finish.

4. If you are using Windows operating system you have to install C++ build tools for build InsightFace library on your computer.  To do this:
   - Install [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/) Communty version (skip this if you installed already)
   - Install [VS C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 
   - Open Visual Studio under `Workloads -> Desktop & Mobile` menu select `Desktop Development with C++`
   
5. In order to use face restorer feature you have to download and place face restorer models:
    - Download these models below and move to them to `comfyui\custom_nodes\ComfyUI-InstaSwap\models\facerestore_models` directory : 
https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth
https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth

6. Run the ComfyUI. 

7.  Double click anywhere in ComfyUI and search InstaSwap node by typing it or right click anywhere and select `Add Node > InstaSwap > InstaSwap Fast Face Swap` node to using it.

<img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/help/Location.jpg?raw=true" alt="webui-demo" width="100%"/>

## Usage

InstaFaceSwap node is very easy to use.  In order to get a result, you have to connect a couple of mandatory slots. 

<img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/help/Usage.jpg?raw=true" alt="webui-demo" width="100%"/>

### Inputs

- (1) `input_image` - is your source image/video file that be processed.
    <img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/help/NodeTypes.jpg?raw=true" alt="webui-demo" width="100%"/>
	#### Supported Nodes
	- Image Files :
	For `processing` single image files you can use Comfy's default `Load Image Node` 
	
	- Video Files :
	 For `processing` video files you have to use third-party video helper library. Most known video library for Comfy is [VHS Video Helper Suite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)  You have to download and install it. If you use Manager plugin you can install it easly from there :
   <img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/help/vhs.jpg?raw=true" alt="webui-demo" width="100%"/>
   
- (2) `source_image` - Your input images or videos will swap faces with this source image. You can use a single image file with Comfy's default `Load Image Node`
   <img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/help/SourceImage.jpg?raw=true" alt="webui-demo" width="100%"/>
   
	- `face_model` (Optional) This is an optional node, you can use your previously created face models with saved using the `Save Face Model` node

### Outputs

- (3) `IMAGE` - this is processed face swap image/video file 
    <img src="https://github.com/abdozmantar/ComfyUI-InstaSwap/blob/main/help/Output.jpg?raw=true" alt="webui-demo" width="100%"/>
	#### Supported Nodes
	Image File :
	- For `preview` processed image files you can use Comfy's default `Preview Image Node`
	- For `save` processed image files on the disk you can use Comfy's default `Save Image Node`
	
	Video File :
	- For `preview` processed video file as an image sequence, you can use Comfy's default `Preview Image Node`
	- For `preview` processed video file as a video clip, you can use [VHS Video Helper Suite's](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)  `Video Combine Node`
	- For `save` processed video file as an image sequence, you can use Comfy's default `Save Image Node`
	- For `save` processed video file as a video clip, you can use [VHS Video Helper Suite's](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)  `Video Combine Node`
	
- `FACE_MODEL` (Optional) - This output delivers the model of the source face, which is constructed throughout the face swapping procedure. You can use it later as an input `face_model` For saving model to disk for later use you can connect and use `Save Face Model node`


### Restoration
After the face swapping process, the resulting image can sometimes be of low resolution. To prevent this and achieve ultra-high quality results, we can utilize Face Restoration models. We provided detailed information about downloading and correctly placing thesemodels during the [Installation](#installation) phase. If everything is in place, all you need to do is select your desired restorer from the InstaSwap main nodes *(4)

### Gender Detection

You have the ability to designate a specific gender for detection in images. InstaSwap will only execute a face swap if the detected face fulfills this specified condition

### Face Indexes

InstaSwap identifies faces within images sequentially, starting from left to right and then from top to bottom. To target specific faces, you have the option to assign indexes to both source and input images. The indexing begins with 0 for the first face detected. You are free to arrange the indexes in your preferred sequence. For example, using 0,1,2 for the Source and 1,0,2 for the Input indicates that the face at index 1 in the Input image (the second face) will swap with the face at index 0 in the Source image (the first face), and so on.

### Face Models

You have the option to save face models as `safetensors` files, which are stored in the `ComfyUI\models\reactor\faces` directory. These files can be loaded into InstaSwap for various scenarios while maintaining extremely compact models of the faces you work with.

To have newly created models show up in the `Load Face Model` Node's list, simply refresh your ComfyUI web application page. It's advisable to use ComfyUI Manager to avoid losing your workflow upon refreshing, especially if you haven't saved your work prior to the refresh.

## Troubleshooting

<a name="insightfacebuild">

### **I. If you encounter the error 'AttributeError: ‘NoneType’ object has no attribute ‘get’**

This likely due to an issue with the `inswapper_128.onnx` model file. To resolve this, consider downloading the file manually from the provided this [link](https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx) Once downloaded, replace the existing file in the `ComfyUI\models\insightface` directory with the newly downloaded one.

### **II. "instaswap.execute() got an unexpected keyword argument 'reference_image'"**

That indicates that the input parameters have been altered in the most recent update. To rectify this, you should remove the existing InstaSwap Node from your workflow and then add it back again.

### **III. "ModuleNotFoundError: No module named 'basicsr'" or "subprocess-exited-with-error" during future-0.18.3 installation**

- Download [this](https://github.com/Gourieff/Assets/raw/main/comfyui-reactor-node/future-0.18.3-py3-none-any.whl) file
- Put it to ComfyUI root folder and run this command:
      `python_embeded\python.exe -m pip install future-0.18.3-py3-none-any.whl`
- Then run this command:
      `python_embeded\python.exe -m pip install basicsr`
### **IV. "fatal: fetch-pack: invalid index-pack output" when you try to `git clone` the repository"**

Try to clone with `--depth=1` (last commit only):

     git clone --depth=1 https://github.com/abdozmantar/ComfyUI-InstaSwap

Then retrieve the rest (if you need):

     git fetch --unshallow

## Disclaimer

This software is designed as a constructive tool in the burgeoning field of AI-generated media, aiding artists in tasks like animating custom characters or using them as models for apparel design, among others.

The creators of this software acknowledge the potential for unethical use and are dedicated to implementing measures to prevent such misuse. We are committed to developing this project in a positive direction, ensuring compliance with legal and ethical standards.

Users of this software are expected to employ it responsibly and in accordance with local laws. When using a real person's face, it is advisable to obtain their consent and to clearly label the content as a deepfake when publishing it online. The developers and contributors of this software bear no responsibility for the actions of its users.

By using this extension, you agree not to create content that:

-   Violates any laws;
-   Causes harm to individuals;
-   Disseminates harmful information or images, whether public or private;
-   Spreads misinformation;
-   Targets vulnerable groups.

This software employs the pre-trained models 'buffalo_l' and 'inswapper_128.onnx' from InsightFace, subject to the following terms:

-   According to the InsightFace license, their pre-trained models are solely for non-commercial research purposes, which applies to both auto-downloaded and manually downloaded models.

Users must strictly comply with these usage conditions. The developers and maintainers of this software are not liable for any misuse of InsightFace’s pre-trained models.

Please be aware that commercial use of this software requires you to train your own models or find commercially permissible models.

### Models Hashes

#### You can safely use models have these hashes:

inswapper_128.onnx
```
MD5:a3a155b90354160350efd66fed6b3d80
SHA256:e4a3f08c753cb72d04e10aa0f7dbe3deebbf39567d4ead6dce08e98aa49e16af
```

1k3d68.onnx

```
MD5:6fb94fcdb0055e3638bf9158e6a108f4
SHA256:df5c06b8a0c12e422b2ed8947b8869faa4105387f199c477af038aa01f9a45cc
```

2d106det.onnx

```
MD5:a3613ef9eb3662b4ef88eb90db1fcf26
SHA256:f001b856447c413801ef5c42091ed0cd516fcd21f2d6b79635b1e733a7109dbf
```

det_10g.onnx

```
MD5:4c10eef5c9e168357a16fdd580fa8371
SHA256:5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91
```

genderage.onnx

```
MD5:81c77ba87ab38163b0dec6b26f8e2af2
SHA256:4fde69b1c810857b88c64a335084f1c3fe8f01246c9a191b48c7bb756d6652fb
```

w600k_r50.onnx

```
MD5:80248d427976241cbd1343889ed132b3
SHA256:4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43
```

**Please check hashsums if you download these models from unverified (or untrusted) sources**


