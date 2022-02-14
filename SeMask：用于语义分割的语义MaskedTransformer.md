## SeMask：用于语义分割的语义Masked Transformer

> （SeMask: Semantically Masked Transformers for Semantic Segmentation）个人理解：将语义地Masked Transformer信息用于语义分割。

### 摘要

在图像`transformer`网络的解码部分，对预训练主干结构进行微调一直是语义分割任务的传统方法。然而，**这种方法省略了图像在编码阶段提供的语义上下文信息。**本文论述，将语义信息整合到预训练分层级的`transformer-base`主干上，同时对其进行微调，可以显著提高信息。为了实现这个，我们提出了`SeMask`，一种简单有效的框架，借助于语义注意力操作，将语义信息整合到编码器中。另外，在训练中，我们使用了一个轻量级的语义解码器，在每个阶段对中间语义先验映射进行监督。我们的实验表明，语义先验的加入提高了所建立的层次编码器的性能，增加了少量`FLOPs`。我们通过将`SeMask`集成到每个变体的`Swin-Transformer`中，作为与不同解码器配对的编码器，提供了经验证明。我们的框架在`ADE20K`数据集上达到了`58.22% mIoU`的最新技术水平和在`Cityscapes`数据集上`mIoU`指标的改进超过`3%`。代码和模型公开在：[https://github.com/PicsartAI-Research/SeMask-Segmentation](t https://github.com/PicsartAI-Research/SeMask-Segmentation)。

### 1.介绍

语义分割旨在执行密集预测，以标记图像中的每个像素，该像素对应于改像素所代表的类。基于`transformer`的视觉网络在图像分类任务中的表现优于卷积神经网络。在现代，当转移到语义分割等下游任务时，`transformer`骨干已经显示出令人印象深刻的性能。

视觉'transformer'中的大多数框架设计都以两种方式之一来解决问题：(1)使用现有的预先训练的主干作为编码器，并使用现有的标准解码器(如`Semantic FPN`或`UperNet`)将其传输到下游任务；或者(2)设计一种新的编码器-解码器网络，在`ImageNet`上对编码器进行预处理，完成语义分割任务。正如前面提到的，这两种方法都涉及到对分割任务的编码器骨干进行微调。从大规模数据集进行微调，有助于早期的注意层在`transformer`的较低层合并局部信息。然而，由于数据集相对较小，并且从分类任务到分割任务，语义类的数量和性质发生了变化，因此在精细调优过程中仍然不能利用语义上下文信息。分层视觉`transformer`解决了沿着阶段逐级下下采样特征的问题，尽管它们仍然缺乏图像的语义上下文。

`Liu`等人介绍了`Swin Transformer`，它构建了分层特征图，使其与主要下游视觉任务的通用骨干兼容。建议使用两个注意力：

