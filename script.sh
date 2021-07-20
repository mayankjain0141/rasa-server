#!/bin/bash
echo $1
# Making the directory for nlu.yml file
# mkdir data/$1
rasa train nlu --nlu data/$1/ -c ./config.yml --fixed-model-name $1 # Training the model
# rm -r ./data/$1 # Removing the model data directory with nlu.yml