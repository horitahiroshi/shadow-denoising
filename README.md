# **Shadow removing for image segmentation in forest ground image**

**Luiz Alberto Hiroshi Horita**

**Nº USP: 6882704**

## **Abstract**

Image processing is an interesting and very challenging subject that can be used in many different applications such as security cameras, robotization of industries, autonomous vehicles in many different environments indoor and outdoor. Independently of the application, in real life one of the main causes of environment noise is shadow, which can heavily distort both image intensity (luminance) and color (chrominance). With this in mind, this project's goal is to treat this problem specificaly in forests ground images aiming offroad mobile robotization. For that, the focus is to detect the shadows and remove them, so the objects can clearly be seen and segmented.

## **1. Main objective**

Given the eucalyptus plantation scenario, this work's goal is to treat the shadow noise problem that occur in some specific period of a sunny day, for example at noon when the sun light is strong enough to project shadow spots all over the road, which difficult the image segmentation for object detection.

For this work, it is important to notice that as its goal is to detect and remove the shadow spots not worrying with performance for video frame processing, so every processing here will be done in a single image at a time.

The input images of this program must be from eucalyptus plantation's streets (see example on Figure1 below). All images used in this project was acquired by the author.

![eucalyptus](/images/shadowE.jpg)
**Figure 1** - Example of shadow noise on an eucalyptus plantation's street.

## **2. The shadow**

"Shadows will occur when direct light from a light source is partially or totally occluded. Shadow can be divided into two types: self shadow and cast shadow.
The self shadow is the part of an object that is not illuminated by direct light; the cast shadow is the dark area projected by an object on the background" [1].

![shadow](/bibliography/shadow_explanation.jpg)

**Figure 2** - Explanation of shadow (picture from [2]).

The shadow of an object is partioned into umbra and panunbra regions. The umbra region is the part of the shadowed surface in which the direct light source is completely obscured by the occluding object. The penumbra is the part of the surface where the light source is only partially occluded, and it occurs when the light source is not a point source or due to diffraction of light rays [2].

## **3. Methodes**

### **3.1. Detecting the shadows**

Shadow detection algorithm must find the image regions in which there are shadows, based on pixel light intensity.

For that the following methods will be implemented: 
- color analysis (*HSV* color space might be used);
- segmentation using adaptive thresholding.
<!-- and running a limiarization based on layer $V$ (value) thresholding. -->

Then, the output of this step must be the mask with all shadow regions in the image.

### **3.2. Removing the shadows**

Once the shadow regions are found, it is possible to restore them as if there is no shadow in the scenario.

With this in mind, it is necessary to:
- analyse the color in non-shadowed regions;
- re-ranging the shadowed region's color intensities;
- filter to remove the edges between the unshadowed regions and the non-shadowed regions.
<!-- enhance them by reranging the pixel intensities according to non-shadow regions histogram. -->

P.S.: unshadowed regions are the shadowed regions with shadow removed; and non-shadowed regions are the regions in which there have never been shadow from the beginning.

## **Bibliography**
[1] [TIAN, Jiandong; SUN, Jing; TANG, Yandong. *Tricolor Attenuation Model for Shadow Detection*. IEEE TRANSACTIONS ON IMAGE PROCESSING, vol. 18, pp.2355-2363. 2009.](/bibliography/Tricolor_Attenuation_Model_for_Shadow_Detection.pdf)

[2] [ARBEL, Eli; HEL-OR, Hagit. *Shadow Removal Using Intensity Surfaces and Texture Anchor Points*. IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, vol. 33, pp. 1202-1216. 2011.](bibliography/Shadow_Removal_Using_Intensity_Surfaces_and_Texture_Anchor_Points.pdf)