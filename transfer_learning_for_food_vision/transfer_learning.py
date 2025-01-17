import torchvision
import torch
import matplotlib.pyplot as plt
import os
import numpy as np
import shutil
import torchinfo
import data_setup, engine, fetch_data, model, predict, train

from pathlib import Path
from torchvision import transforms

#get efficient weights
efficient_weight = torchvision.models.EfficientNet_B0_Weights.DEFAULT
efficient_transformer = efficient_weight.transforms()

#define train and test data directory
TRAIN_IMAGE_DIR = "/content/food_vision_project/pizza_steak_sushi/train"
TEST_IMAGE_DIR = "/content/food_vision_project/pizza_steak_sushi/test"

#make train , test data loaders using our last data_setup.py file
train_dataLoader , test_dataLoader , class_names = data_setup.create_dataLoader(TRAIN_IMAGE_DIR,
                             TEST_IMAGE_DIR,
                             batch_size = 32 , transformer = efficient_transformer)

#initiate efficient model 
efficient_model = torchvision.models.efficientnet_b0(weights = efficient_weight)

#show the model architecture
torchinfo.summary(efficient_model,
                  input_size = (1 , 3  ,224 , 224),
                  col_names = ["input_size" , "output_size", "num_params" , "trainable"],
                  col_width = 20 )

#change the model trainable parameters to False and just keep last layers to change
for param in efficient_model.features.parameters():
  param.requires_grad = False

torchinfo.summary(efficient_model,
                  input_size = (1 , 3  ,224 , 224),
                  col_names = ["input_size" , "output_size", "num_params" , "trainable"],
                  col_width = 20 ) #check the trainable parameters again

#change last layer of the model from 1000 to 3 category
classifier = torch.nn.Sequential(
    torch.nn.Dropout(p = 0.2 , inplace = True),
    torch.nn.Linear(in_features = 1280 , out_features = 3 , bias = True)
)

efficient_model.classifier = classifier

torchinfo.summary(efficient_model,
                  input_size = (1 , 3  ,224 , 224),
                  col_names = ["input_size" , "output_size", "num_params" , "trainable"],
                  col_width = 20 ) #check final layer again

#lets create loss and optimzer methods and set device agnostic code for training
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params = efficient_model.parameters() , lr = 0.001)
device = "cuda" if torch.cuda.is_available() else "cpu"

#train
results1 = train.train(efficient_model, epochs = 10 , train_data = train_dataLoader ,
            test_data = test_dataLoader , loss_fn = loss_fn ,
            optimizer = optimizer , device = device)

print("Train Loss:" , np.mean(results1["train_loss"]))
print("Train Accurac:" , np.mean(results1["train_accuracy"]))
print("Test Loss:" , np.mean(results1["test_loss"]))
print("Test Accuracy:" ,np.mean(results1["test_accuracy"]))





#create a method to plot train/test curves in a same range

def plot_accuracy_and_loss_curves(results):
  '''
  plot accuracy and loss curves

  Input:
      results: a dictionary contains trian/test losses and accuracies for each epoch

  output:
      plot train/test losses and accuracies curves
  '''

  #normalize train/test accuracies and losses
  train_accuracies = [a/100 for a in results["train_accuracy"]]
  test_accuracies = [a/100 for a in results["test_accuracy"]]

  train_loss_max, test_loss_max = max(results["train_loss"]) , max(results["test_loss"])

  train_losses = [a/train_loss_max for a in results["train_loss"]]
  test_losses = [a/test_loss_max for a in results["test_loss"]]


  plt.figure(figsize = (15 , 7))

  plt.subplot(1 , 2 , 1)
  plt.plot(train_accuracies , label = "train_accuracy")
  plt.plot(train_losses , label = "train_loss")
  plt.xlabel("Epoch")
  plt.legend()
  plt.title("Train")

  plt.subplot(1 , 2 , 2)
  plt.plot(test_accuracies , label = "test_accuracy")
  plt.plot(test_losses , label = "test_loss")
  plt.xlabel("Epoch")
  plt.title("Test")
  plt.legend()

  plt.show()


plot_accuracy_and_loss_curves(results1)
