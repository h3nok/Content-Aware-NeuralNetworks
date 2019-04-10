#!/bin/sh

MODEL=inception_v1
DATASET_NAME=cifar100
DATASET="/home/deeplearning/data/cifar/cifar100"
CURRICULUM=True
STEPS=100000

declare -a metrics=("iv" "mi" "min"
                     "l1" "l2" "psnr"
                     "ssim" "cross_entropy"
                     "kl" "je" "ce")

run baseline 
python3 train.py --curriculum False --model_name $MODEL --max_number_of_steps $STEPS --dataset_dir $DATASET --dataset_name $DATASET_NAME

#curriculum leanring 
for i in "${metrics[@]}"
do
    python3 train.py --measure $i --curriculum True --model_name $MODEL --max_number_of_steps $STEPS --dataset_dir $DATASET --dataset_name $DATASET_NAME
done


