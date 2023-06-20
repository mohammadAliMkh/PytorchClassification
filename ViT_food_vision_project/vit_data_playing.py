# import torch
# import torchvision
# import scipy
# import numpy
# import sklearn
# import pandas
# import matplotlib.pyplot as plt
# import os
# import timeit
# import random


# from torch.utils.data import DataLoader
# from torchvision import datasets
# from torchvision import transforms

# #load data
# test_data_path = "/content/Pytorch/ViT_food_vision_project/pizza_steak_sushi/test"
# train_data_path = "/content/Pytorch/ViT_food_vision_project/pizza_steak_sushi/train"

# #set image size and make transformer
# IM_SIZE = 224
# BATCH_SIZE = 32

# transformer = transforms.Compose([
#     transforms.Resize((IM_SIZE , IM_SIZE)),
#     transforms.ToTensor()
# ])

# #create test and train dataLoaders
# test_dataset = datasets.ImageFolder(test_data_path , transform = transformer)
# train_dataset = datasets.ImageFolder(train_data_path , transform = transformer)

# class_names = train_dataset.classes

# test_dataLoader = DataLoader(test_dataset, batch_size = BATCH_SIZE , shuffle = False , num_workers = torch.cuda.device_count())
# train_dataLoader = DataLoader(train_dataset, batch_size = BATCH_SIZE , shuffle = True , num_workers = torch.cuda.device_count())

# #show random images of data
# columns = 3
# rows = 4

# data = next(iter(train_dataLoader))

# rand = random.randint(0 , len(data[0]) - (columns * rows))

# images = data[0][rand:rand + (columns * rows)]
# targets = data[1][rand:rand + (columns * rows)]

# plt.figure(figsize = (10 , 7))
# for i in range(0 , (columns * rows)):
#   plt.subplot(columns , rows , i + 1)
#   plt.imshow(torch.permute(images[i] , dims = (1 , 2 , 0)))
#   plt.title(class_names[targets[i]])
#   plt.axis(False)


# #create a function to plot an image after empatching it
# def plot_patched_image(image , patch_size:int):
#   '''
#     plot an image after cropping image into patchs

#       inputs:
#         image: an torch permutetd image in shape (H , W , C)
#         patch_size : an integere odd number


#       output:
#         plot a figure with patched sub images
#   '''

#   patch_size = patch_size
#   sample_image = image
#   number_of_patches = int(sample_image.shape[0] / patch_size)
#   n_rows = number_of_patches
#   n_columns = n_rows

#   fig , axs = plt.subplots(n_rows , n_columns , sharex = True , sharey = True , figsize = (10 , 10))

#   for i in range(n_rows):
#     for j in range(n_columns):
#       axs[i , j].imshow(sample_image[i * patch_size: (i + 1) * patch_size , j * patch_size: (j + 1) * patch_size , :])
#       axs[i , j].set_xlabel(j+1)
#       axs[i , j].set_ylabel(i+1 , rotation  = "horizontal" , ha = "right")
#       axs[i , j].set_xticks([])
#       axs[i , j].set_yticks([])
#       axs[i , j].label_outer()
#   plt.show()

# #show the result
# image = torch.permute(images[0] , (1 , 2  , 0))
# plot_patched_image(image , patch_size= 16)

# create prepare method to make images in embedded form
# def prepare_embed_input(image):

#   '''prepare data embed for our transfomer in a apropriate shape

#       input: image torch.utils.data.Dataloder

#       output: array
#   '''
#   conv = torch.nn.Conv2d(in_channels = 3 , out_channels = 16 * 16 * 3 , kernel_size = 16 , stride = 16 , padding = 0)
#   x = conv(torch.unsqueeze(torch.permute(image , (2 , 0 , 1)) , dim = 0))
#   flat = torch.nn.Flatten(start_dim = 2 , end_dim = 3)
#   return torch.permute(flat(x) , (0 , 2 , 1))



# plot some embedded visually
# fig , axs = plt.subplots(3 , 3 , figsize = (5 , 5 ), sharex = True , sharey = True)
# n_fig = 0

# for i in range( 3):
#   for j in range(3):
#     axs[i , j].imshow(torch.reshape(torch.squeeze(torch.sigmoid(flatten_input) , dim = 0)[n_fig] , shape = (16 , 16 , 3)).detach().numpy())
#     n_fig = n_fig + 1
#     axs[i , j].set_xlabel(j + 1)
#     axs[i , j].set_ylabel(i + 1 , rotation = "horizontal" , ha = "right")
#     axs[i , j].set_xticks([])
#     axs[i , j].set_yticks([])
#     axs[i , j].label_outer()



# create Patching class befor adding class token and position embeddings
# class Patching(torch.nn.Module):


#   def __init__(self , in_channels = 3,
#                out_channels = 768,
#                kernel_size = 16,
#                stride = 16,
#                padding = 0):
   
#     super().__init__();
#     self.patches = torch.nn.Conv2d(in_channels = in_channels,
#                                    out_channels = out_channels,
#                                    kernel_size = kernel_size,
#                                    stride = stride,
#                                    padding = padding)
   
#     self.flat_patches = torch.nn.Flatten(start_dim = 2 , end_dim = 3)



#   def forward(self , x):
#     return torch.permute(self.flat_patches(self.patches(x)) , (0 , 2 , 1))
