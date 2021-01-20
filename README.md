# LystoX
## Deep neural networks with computer vision methods applied to medical data

*Biosegmentation of T-lymphocytes from histological images affected by cancer*

![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/Logo.png)

## Dataset
Dataset consists of histological data of human body, specifically from
colon, breast, prostate tissues. The tissue was marked with CD3 and CD8 marker,
so T-lymphocytes were highlithed as brown cells with brigher blue nuclues.
All images have size 299x299 pixels in *.png* format. 

Examples of dataset with highlihted borders with no objects of interest.

![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_11.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_14.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_135.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_402.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_5.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_417.png)


## Data pipeline process 
It includes at first downloading data, then create binary mask for some of them.
After creating correspondig masks we convert source images to HSV and LAB color
space. There were a hypothesis that differenct color spaces can adjust final
test score as result to have more range in representing colors and our model
can better catch the trend during trainig. 
Secondly augmentation using rotation, horizontal/vertical flipping (mask also!)

Finally we train our model, validate and test on finale dataset. Validation
also consists of postprocesing our predicted images using thresholdin and 
morphological operations such as opening/closing in order to delete noisy and
incorrect prediction so that we achieve higher model score

*Activity diagram*  

![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/activity_diagram.png)


*Architecture diagram*  

![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/Architecture_diagram.png)

## Model of our DNN

Model represents recent state-of-the art UNET architecture. However image sizes
are different as shown in image (299x299px)  


![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/Unet.PNG)

## Final score  

**Final predictions**  

Here are tables of best model with achieved score and using postprocessing 
operations as thresholding (Thresh) and morphological opening using structural element (SE)
with specific size.


**Table of best models in thesis**
| Model        | Thresh | SE | Dice           | Jaccard  | 
| ------------- |:-------------:| -----:| -----:| -----:| 
| RGB     | 0.1 | 7 | .5902 | .4998 |
| HSV     | .0.1|   7 | .6506  | .5688 |
| LAB | 0.1      |    7 | .6563 | .5742 |



**Table of best models after thesis evaluation with additional training**
| Model        | Thresh | SE | Dice           | Jaccard  | 
| ------------- |:-------------:| -----:| -----:| -----:| 
| RGB     | .15 | 9 | .6032 | .5146 |
| HSV     | .2|   7 | .6870  | .6061 |
| LAB | .15      |    9 | .6919 | .6145 |


##Final segmented T-lymphocytes##

*Best RGB model*  
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/0_test_data_rgb0.png)

*Best HSV model*  
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/0_test_data_hsv0.png)

*Best LAB model*  
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/0_test_data_lab0.png)
