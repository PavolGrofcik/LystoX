# LystoX
## Deep neural networks with computer vision methods applied to medical data

*Biosegmentation of T-lymphocytes from histological images affected by cancer*

![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/Logo.png)

## Dataset
Dataset consists of histological images of human body, specifically from
colon, breast, prostate tissues. The tissue was marked with CD-3 and CD-8 marker,
so that T-lymphocytes had been highlighted as brown cells with brighter blue nuclues.
All images have size 299x299 pixels in *.png* format. 

Examples of dataset with highlihted borders 15x15 pixels (yellow).  
Note that borders exclude objects of interest.  


![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_11.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_14.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_135.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_402.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_5.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_417.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_1687.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_2510.png) 
<!-- ![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/lysto_pilot_412.png)  -->


## Data pipeline process 
At first it includes downloading data, then create binary mask for some of them
using implemented tool **LystoX**.
After creating correspondig masks we convert source images also to HSV and LAB color
space. There were a hypothesis that differenct color spaces can have higher final
test score as result to have more range in representing colors and therefore our model
can better catch the trend during trainig. 
Secondly follows augmentation using rotation, horizontal/vertical flipping (masks also!)

Finally we train our model (UNET), validate and test on final dataset. Validation
also consists of postprocesing our predicted images using thresholding and 
morphological operations such as opening/closing in order to delete noisy and
incorrect predictions so that we achieve higher final test score

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


In coclusion we can accept that converting images to different color space such as HSV/LAB
has an effect on our final prediction. It is shown below that training models with these type of
images resulted to better score with comparison to the RGB model. 
## Final segmented T-lymphocytes

*Best RGB model*  
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/0_test_data_rgb0.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/4_test_data_rgb4.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/*_test_data_rgb8.png)

*Best HSV model*  
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/0_test_data_hsv0.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/4_test_data_hsv4.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/8_test_data_hsv8.png)

*Best LAB model*  
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/0_test_data_lab0.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/4_test_data_lab4.png)
![Logo](https://github.com/PavolGrofcik/LystoX/blob/master/figures/8_test_data_lab8.png)


## Future work

Future work can include normalization using standard Z-mean normalization or more sophisticated
stain normalizations for instance Macenko/Vahadane method. Since our images are stained,
normalization of the specific stain could help both pathologist (humans) and our AI models
to better segment and be more robust towards T-lymphocytes and 
artifacts that resemble similar in some cases. This could be demonstrated as a future work
with model accuracy and conclude if the normalization has great advantage over none.


## Resources
Data can be downloaded after registration from:  

https://lysto.grand-challenge.org/

All rights reserved! 
® Registered 
Bachelor thesis 

**FIIT STU 2020**  
**Pavol Grofčík**  


*Please do not copy anything from these repositary,
you can have high similarity coefficient
and fail during final examination!*
