---
title: "LLM Training"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/AI/AI-llm-architecture/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Basic Information

You should start by reading this post for some basic concepts you should know about:

## 1. Tokenization

The goal of this phase is to **divide the input into tokens and map them to token IDs**.

## 2. Data Sampling

The goal of this phase is to prepare training sequences of a chosen context length together with their shifted prediction targets.

## 3. Token Embeddings

The goal of this third phase is very simple: **Assign each of the previous tokens in the vocabulary a vector of the desired dimensions to train the model.** Each word in the vocabulary will a point in a space of X dimensions.

Note that initially the position of each word in the space is just initialised “randomly” and these positions are trainable parameters (will be improved during the training).

Moreover, during token embedding, **another embedding layer is created** that represents (in this case) the **absolute position of the word in the training sentence**. This way, a word in different positions in the sentence has a different representation.

## 4. Attention Mechanisms

The goal of this fourth phase is very simple: **Apply some attetion mechanisms**. These are going to be a lot of **repeated layers** that are going to **capture the relation of a word in the vocabulary with its neighbours in the current sentence being used to train the LLM**.

A lot of layers are used for this, so a lot of trainable parameters are going to be capturing this information.

## 5. LLM Architecture

The goal of this fifth phase is very simple: **Develop the architecture of the full LLM**. Put everything together, apply all the layers and create all the functions to generate text or transform text to IDs and backwards.

This architecture will be used for both, training and predicting text after it was trained.

## 6. Pre-training & Loading models

The goal of this sixth phase is very simple: **Train the model from scratch**. For this the previous LLM architecture will be used with some loops going over the data sets using the defined loss functions and optimizer to train all the parameters of the model.

[6. Pre-training & Loading models](6.-pre-training-and-loading-models.html)

## 7.0. LoRA Improvements in fine-tuning

LoRA substantially reduces the number of trainable parameters and optimizer state needed to fine-tune a pretrained model.

[7.0. LoRA Improvements in fine-tuning](7.0.-lora-improvements-in-fine-tuning.html)

## 7.1. Fine-Tuning for Classification

The goal of this section is to show how to fine-tune an already pre-trained model so instead of generating new text the LLM will select give the **probabilities of the given text being categorized in each of the given categories** (like if a text is spam or not).

[7.1. Fine-Tuning for Classification](7.1.-fine-tuning-for-classification.html)

## 7.2. Fine-Tuning to follow instructions

The goal of this section is to show how to **fine-tune an already pre-trained model to follow instructions** rather than just generating text, for example, responding to tasks as a chat bot.

[7.2. Fine-Tuning to follow instructions](7.2.-fine-tuning-to-follow-instructions.html)

## References
