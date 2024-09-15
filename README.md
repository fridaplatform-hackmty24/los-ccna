# SOFTTEK HACKMTY 2024

This is the repository for the Softtek HackMTY 2024 team “Los CCNA” made up of

Omar Emiliano Sanchez Villegas

Elliot Denzel Romero Martinez

Andrew Moreira Lee

Sofia Moreno Lopez

## What is it?

A store navigation device for the blind based on natural language processing and computer vision powered CRM

Using Yolov8

## Branch Directory

Main. This is where our last delivery for the hack lives

Ignorant_coco. Various weights trained from scratch

Dominonet. This is the training branch for a YOLOv8n recognizing domino pieces

Denzeel-Patch-1. Text to speech and speech to text model, and natural language  translation into SQL queries

Vino. In this branch we checked the different optimizations we could do for openVINO for benchmarks and comparison
Hugging. In this branch we tested a pre trained traffic sign model found in hugging face.

Coco. In this branch we tested a pre trained coco YOLOv8n model

## About using openVINO

By using openVINO we were able to optimise our models from float32 to int8 and see the difference very clearly in the traffic sign model speed:

### float32

 Median:        333.64 ms
 
[ INFO ]    Average:       350.08 ms

[ INFO ]    Min:           249.05 ms

[ INFO ]    Max:           500.67 ms

[ INFO ] Throughput:   11.32 FPS


### float16 

Median:        323.44 ms

[ INFO ]    Average:       328.12 ms

[ INFO ]    Min:           253.86 ms

[ INFO ]    Max:           432.99 ms

[ INFO ] Throughput:   12.04 FPS


### int8 

[ INFO ]    Median:        99.27 ms

[ INFO ]    Average:       100.29 ms

[ INFO ]    Min:           62.64 ms

[ INFO ]    Max:           162.69 ms

[ INFO ] Throughput:   39.42 FPS





