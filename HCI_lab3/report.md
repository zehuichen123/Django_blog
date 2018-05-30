# Image Search Console Report

*Zehui Chen 1652763*

## Introduction

This image search console can return back similiar images of your uploading images, which performs a simple image search task. The whole process of the task includes the following steps:
- Check the image size for preventing malicious attacks
- Predict the category of the image
- List the same category images in the order of similiarity of uploading images

To give a better interaction with users, five-stage search framework is practiced in this project, which helps to coordinate design practices and satisfy the needs of all users.  

## Five-stage Search Framework Practice

### Formulation

A filter is utilized when showing results, and the filter helps to form the function of advanced search. In this project, I provide three filter options for you to choose:  
- **Image Size** (three options: `390*190`,`1080*720`,`1920*1080`) (Attention here, if you choose to show large images from local image library, no images will meet the need since all image size in the local image library is quite small).
- **Image Source** (three options: local,Baidu,Google). Since all image links to Baidu Image library are banned, I downloaded these images first in another folder.  
- **Image Type** (three option: `.png`,`.jpeg/.jpg`,'`.gif`) Again, here if you choose to show `.png` in the local image library, no images will meets the requirements because all images are in the format of `.jpg`.
<center>
<img src="filter.png" height="150px"> 
</center>
Of course, you can choose not to use any filters, and we will show you the search results from local library.

### Intiation of action

Explicit actions are initiated by buttons in the homepage with consistent labels, such as `Upload` and `Start Search!` button. And `Advanced Search Options` are designed as a toggle one, and it will remain folded if you do not click it. The reason we choose to design it in this way is because not everyone want to do advance search. 
<center>
<img src="search_console.png" height="200px">
</center>

### Review of results

In the results page, a related word list will be shown in the top of image results. The list consists of predicted suggested words. If you click them, they will redirect your to Baidu Baike (2333, maybe not so cool). 

And all search images are shown in the whole pages. One thing to emphasize is if your mouse hover the image, if will automatically become bigger. The purpose of this function is to help users see image clearly and easily if they are interested in this image, which gives them a better use experience.   

Of course, a back to search button is fixed to the top of the page, which is convenient for your to back to homepage to start your second search.  

<center>
<img src="result.png" height="300px">
</center>

### Refinement

Refinement means to guide users in progressive refinement with meaningful messages, and make search parameters convenient and provide suggestions for error correction. Part of refinement are practiced in my project mentioned above, such as suggested words for search task.  

### Use

To achieve a better user experience, imbaded actions in results should be added and allow users to favorite their interested images, or collect user feedback, such as rating, reiviews and likes for one image. However, with the limit time of this project, I can not make all this functions available in my project. But these elements are really important in the HCI when designing such tasks.  

## Features of this project

- A web based application for convenient usage
- Extremely accurate search results (I will give you an explanation of my customed search engine)
- Quite simple User Interface but useful and clearly
- Advanced Search with Three Filters
- Automatically magnify the images when mouse hovers it
- Suggested words list in the result page

## My Customed Search Engine

In my perspective, only to compute image similarity is not enough for us to give a satisfying results. Thus, I try a two step search workflow: 1) predict the upload image category 2) List the corresponding images in the order of similiarity based on Hash value.

### Prediction with Inception V3

The origin image library has 716 images with 12 different categories. Since convoluntional neural network does a gogerous job on image classication tasks, I decided to use CNN as my predict model. However, only 716 images is not enough for a CNN training since it is a data-hunger for NN training process. Thus, I try to do a transfer learning on Inception_V3 (GoogleNet) and add several layers in the end of original net. The final neural network has an output of 12 units to give the probability of each category based on uploading image. Here we use a pre-trained model of Inception V3 and the accuracy on our original image dataset reaches about 95% in only 20 epochs! 
<center>
<img src="train_result.png" height="200px">
</center>

### DHash Value for similarity computation

To list the result in the order of image similiarity, I did a DHash computation in consideration of search speed. Since we have already known the category in the prediction part, all image comparsion is based on the same category images. And if you upload an image that is already in the original image library, and search results in the local library, you will find the first image of the result is the image you upload, since they are the same image and have the highest similiarity value. You can refer to <a href="https://www.jianshu.com/p/193f0089b7a2">this page</a> to get a understanding on how do DHash computation on images.  

## Conclusion

In this lab, I've tried to practice five-stage search framework on my project and got a basic understanding on it. This lab is quite fun and meaningful which helps us to go deeper to consider how to design user interface and how to interact with users.

## Reference

- <a href="https://www.jianshu.com/p/193f0089b7a2">相似图片检测：感知哈希算法之dHash的Python实现</a>
- <a href="https://arxiv.org/abs/1512.00567">Rethinking the Inception Architecture for Computer Vision</a>

