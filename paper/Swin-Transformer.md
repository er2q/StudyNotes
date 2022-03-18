[Swin Transformer](https://links.jianshu.com/go?to=https%3A%2F%2Farxiv.org%2Fabs%2F2103.14030)

### **摘要**：

本文提出了一种新型的视觉变换器，即`Swin`变换器，它可作为计算机视觉的通用骨干。将`Transformer`从`NLP`转移到`CV`上，由于两个领域的差异而存在着挑战，例如视觉实体的尺度变化较大，以及图像相对于句子是个很长的序列。为了解决这些差异，我们提出了一种分层变换器，它的表示是用==移位窗口==来计算的。==移位窗口将自注意力的计算限制在**非重叠的局部窗口**上，同时考虑了跨窗口连接，提高了效率==。该层次结构具有在不同尺度下建模的灵活性，并且具有与图像大小相关的**线性计算复杂度**。`Swin`变换器的这些特性使其与广泛的视觉任务兼容，包括图像分类（ImageNet-1K上的86.4 top-1精度）和目标检测（COCO测试开发上的58.7boxAP和51.1maskAP）和语义分割（ADE20K val上的53.5 mIoU）等密集预测任务。其性能超过了以往的最新水平，COCO上的+2.7boxAP和+2.6maskAP和ADE20K上的+3.2MIou的大幅度提升，显示了变换型作为视觉主干的潜力。代码和模型在[https://github.com/microsoft/Swin-Transformer](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fmicrosoft%2FSwin-Transformer)

### **1. 引言**

卷积神经网络（CNNs）一直是计算机视觉建模的主流。从AlexNet[38]及其在ImageNet图像分类挑战中的革命性表现开始，CNN架构通过更大的规模[29，73]、更广泛的连接[33]和更复杂的卷积形式[67，17，81]而变得越来越强大。由于CNNs作为各种视觉任务的骨干网络，这些体系结构的进步导致了性能的提高，从而广泛提升了整个领域。

另一方面，自然语言处理（NLP）中网络体系结构的演变走了一条不同的道路，今天流行的体系结构取而代之的是Transformer[61]。Transformer是为序列建模和转换任务而设计的，因为它关注数据中的长期依赖性建模。它在语言领域的巨大成功促使研究人员研究它对计算机视觉的适应性，最近它在某些任务上显示了有希望的结果，特别是图像分类[19]和联合视觉语言建模[46]。

在本文中，我们试图扩展Transformer的适用性，使它可以像NLP和CNNs一样作为计算机视觉的通用主干。我们观察到，将其在语言领域的高性能转移到视觉领域的重大挑战可以解释为两种模式之间的差异。**其中一个差异涉及尺度(scale)**。与作为语言Transformer中处理的基本元素的单词标记不同，视觉元素在尺度上可能有很大的差异，这是一个在目标检测等任务中受到关注的问题[41，52，53]。在现有的基于Transformer的模型中[61，19]，tokens都是固定尺度的，这种属性不适合视觉应用；另一个区别是图像中像素数比文本段落中的单词数多得多。存在许多视觉任务，如语义分割，需要在像素级进行密集的预测，这对于高分辨率图像上的Transformer来说是很困难的，因为它自身注意力的计算复杂度是图像大小的二次方。为了克服这些问题，我们提出了一种通用的变换器主干，称为Swin-Transformer，它**构造了层次化的特征映射**，并且计算复杂度与图像大小成线性关系。如图1(a)所示，Swin-Transformer通过从小尺寸（编者注：小尺寸应该是相对于ViT中的14x14或16x16而言）的图块（用灰色表示）开始，并在更深的Transformer层中，逐渐合并相邻图块来构造层次表示。有了这些分层特征映射，Swin-Transformer模型可以方便地利用高级技术进行密集预测，如特征金字塔网络（FPN）[41]或U-Net[50]。线性计算复杂度是通过在分割图像的非重叠窗口（红色轮廓）内局部计算自注意来实现的。每个窗口中的图块数是固定的，因此复杂度与图像大小成线性关系。这些优点使得Swin-Transformer适合作为各种视觉任务的通用主干，与以前基于Transformer的体系结构形成对比[19]，后者产生单一分辨率的特征图，并且具有二次复杂性。

<img src="https:////upload-images.jianshu.io/upload_images/13727053-fac9042b671b1727.png" alt="img"  />

图1.(a) 所提出的Swin Transformer通过在更深的层中合并图像块（以灰色显示）来构建分层特征图，并且由于仅在每个局部窗口（以红色显示）内计算自注意，因此对于输入图像大小具有线性计算复杂度。因此，它可以作为图像分类和密集识别任务的通用主干。(b) 相比之下，以前的ViT[19]产生单一低分辨率的特征图，并且由于全局计算自我注意，相对于输入图像大小具有二次计算复杂性

Swin Transformer的一个关键设计元素是**它在连续的自注意层之间的窗口分区的移动**(`its shift of the window partition between consecutive self-attention layers`)，如图2所示。移动的窗口桥接了前一层的窗口(`The shifted windows bridge the windows of the preceding layer`)，提供了它们之间的连接，显著增强了建模能力（见表4）。这种策略对于真实世界场景的延迟也是有效的：一个窗口中的所有查询图块都共享相同的键图块集(all query patches within a window share the same key set)(注释：查询和键是自注意层中的投影向量)，这有助于硬件中的内存访问。相比之下，早期的基于滑动窗口的自注意方法[32，49]由于不同查询像素的键集不同，在一般硬件上的延迟较低（注释2：虽然有一些高效的方法可以在通用硬件上实现基于滑动窗口的卷积层，但这是因为卷积层在整个特征映射中共享内核权重。而基于滑动窗口的自注意层在实践中很难实现高效的内存访问）。我们的实验表明，所提出的移位窗口方法比滑动窗口方法具有更低的延迟，但在建模能力方面相似（见表5和表6）。

![img](https:////upload-images.jianshu.io/upload_images/13727053-5ef7bd298a4c9c3e.png?imageMogr2/auto-orient/strip|imageView2/2/w/625/format/webp)

图2.在所提的Swin Transformer架构中，用于计算自注意的移位窗口方法的图示。在$l$层（左），采用规则的窗口划分方案，并在每个窗口内计算自注意。在下一层$l+1$(右)中，窗口分区被移动，从而产生新的窗口。新窗口中的自注意计算跨越层$l$中先前窗口的边界，提供它们之间的连接。

所提出的Swin变换器在图像分类、目标检测和语义分割等识别任务上取得了很好的效果。它在这三项任务显著优于ViT/DeiT[19,60]和ResNe(X)t模型[29,67]而具有相似的延迟。COCO test-dev上的58.7box-AP和51.1mask-AP超过了先前的最新结果，分别是+2.7box-AP（Copy-paste[25]，无外部数据）和+2.6mask-AP（DetectoRS[45]）。在ADE20K语义分割上，它在val集合上获得了53.5 mIoU，比以前的最新技术（SETR[78]）提高了+3.2 mIoU。在ImageNet-1K图像分类中，该算法的分类精度达到了86.4%。

我们相信，一个跨计算机视觉和自然语言处理的统一体系结构可以使这两个领域都受益，因为它将促进视觉和文本信号的联合建模，并且来自这两个领域的建模知识可以更深入地共享。我们希望swin transformer在各种视觉问题上的出色表现能够推动社区加深这种信念，并鼓励视觉和语言信号的统一建模。

### **2.相关工作**

**CNN及其变体**  CNNs作为计算机视觉的标准网络模型。虽然CNN已经存在了几十年[39]，但直到AlexNet的引入[38]，CNN才开始发展并成为主流。从那时起，人们提出了更深入、更有效的卷积神经结构，以进一步推动计算机视觉中的深度学习浪潮，如VGG[51]、GoogleNet[56]、ResNet[29]、DenseNet[33]、HRNet[62]和EfficientNet[57]。除了这些架构上的进步，还有许多工作在改进各个卷积层，例如深度卷积[67]和可变形卷积[17,81]。虽然CNN及其变体仍然是计算机视觉应用的主要骨干架构，我们强调了在视觉和语言之间进行统一建模的 transformer式体系结构的强大潜力。我们的工作在一些基本的视觉识别任务上取得了很好的效果，我们希望这将有助于模型的转变。

**基于自注意力的主干体系结构**  同样受到自然语言处理领域中自注意层和transformer结构的成功启发，一些作品使用自注意层来代替流行ResNet中的部分或全部空间卷积层[32，49，77]。在这些工作中，在每个像素的局部窗口内计算自注意以加速优化[32]，并且它们实现了比对应的ResNet架构稍好的精度/FLOPs权衡。然而，它们昂贵的内存访问导致它们的实际延迟明显大于卷积网络的延迟[32]。我们不使用滑动窗口，而是建议在连续层之间切换窗口，这样可以在一般硬件中实现更高效的实现。

**自注意/ transformer补充CNN**  另一项工作是用自注意层或 transformer来增强标准的CNN架构。自注意层可以补充主干网[64，6，68，22，71，54]或头部网络[31，26]，通过提供编码远程依赖或异构交互的能力。最近，Transformer中的编解码器设计已经应用于目标检测和实例分割任务[7，12，82，55]。我们的工作探索了transformer用于基本视觉特征的提取，是对这些工作的补充。

**基于transformer的视觉主干**  与我们的工作最相关的是视觉变压器（ViT）[19]及其后续工作[60、69、14、27、63]。ViT的开创性工作是在不重叠的中等尺寸图像块上直接应用一种变换器结构进行图像分类。与卷积网络相比，它在图像分类上实现了令人印象深刻的速度-精度折中。虽然ViT需要大规模的训练数据集（即JFT-300M）才能很好地执行，但DeiT[60]引入了几种训练策略，使ViT也能有效地使用较小的ImageNet-1K数据集。ViT在图像分类方面的结果是令人鼓舞的，但由于其低分辨率的特征映射和复杂度随图像大小的二次增加，其结构不适合作为密集视觉任务或输入图像分辨率较高时的通用骨干网络。将ViT模型应用于直接上采样或反卷积的目标检测和语义分割等稠密视觉任务中的工作很少，但性能相对较低[2,78]。与我们的工作同时进行的还有一些改进ViT体系结构[69，14，27]，以获得更好的图像分类。根据经验，我们发现我们的Swin-Transformer架构在这些图像分类方法中实现了最佳的速度精度折中，尽管我们的工作重点是通用性能，而不是专门针对分类。另一项并行工作[63，PVTv1]探索了一种类似的思路，即在变压器上构建多分辨率特征图。它的复杂度仍然是图像大小的二次方，而我们的算法是线性的，并且在局部操作，这在视觉信号的高相关性建模中被证明是有益的[35，24，40]。我们的方法既高效又有效，在COCO目标检测和ADE20K语义分割方面都达到了最先进的精度。

### **3.方法**

#### **3.1. 总体架构**

图3给出了Swin-Transformer体系结构的概述，它演示了微型版本（tiny version，SwinT）。它首先通过像ViT一样的分块模块将输入的RGB图像分成不重叠的图块。每个图块被视为一个token，其特征被设置为原始像素RGB值的拼接。在我们的实现中，我们使用的块大小为4×4， 因此每个图块的特征维数为4×4×3=48。在该原始值特征上应用线性嵌入层，将其投影到任意维（表示为$C$）。

![img](https:////upload-images.jianshu.io/upload_images/13727053-76fc048ce2b8aac6.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

图3.(a)Swin变压器（Swin-T）的结构；(b) 两个连续的SWN变压器组（符号为式（3））。W-MSA和SW-MSA分别是具有规则和移位窗口配置的多头自注意模块。

在这些patch tokens上计算自注意力修改版本的一些transformer块（Swin Transformer blocks）。这些transformer块不改变tokens的数量![(\frac{H}{4} \times \frac{W}{4} )](https://math.jianshu.com/math?formula=(%5Cfrac%7BH%7D%7B4%7D%20%5Ctimes%20%5Cfrac%7BW%7D%7B4%7D%20))，与线性嵌入层一起，被称为“阶段1”。

为了产生一个层次化的表示，tokens的数量会随着网络渐深，在patch merging layer层中被减少。第一个patch merging layer**拼接**每组2×2个相邻图块的特征，并在拼接得到的![4C](https://math.jianshu.com/math?formula=4C)维的特征上应用线性层。这将使tokens的数量减少2×2=4倍(分辨率2×下采样），输出维度设置为![2C](https://math.jianshu.com/math?formula=2C)。然后应用Swin Transformer块进行特征变换，分辨率保持在![\frac{H}{8} \times \frac{W}{8} ](https://math.jianshu.com/math?formula=%5Cfrac%7BH%7D%7B8%7D%20%5Ctimes%20%5Cfrac%7BW%7D%7B8%7D%20)。patch merging和特征变换的第一个块被称为阶段2。这个过程被重复2次，分别是阶段3和阶段4，输出分辨率分辨是![\frac{H}{16} \times \frac{W}{16} ](https://math.jianshu.com/math?formula=%5Cfrac%7BH%7D%7B16%7D%20%5Ctimes%20%5Cfrac%7BW%7D%7B16%7D%20)和![\frac{H}{32} \times \frac{W}{32} ](https://math.jianshu.com/math?formula=%5Cfrac%7BH%7D%7B32%7D%20%5Ctimes%20%5Cfrac%7BW%7D%7B32%7D%20)。这些阶段共同产生一个层次表示，具有与典型卷积网络相同的特征图分辨率，例如VGG[51]和ResNet[29]。因此，所提出的架构可以方便地取代现有方法中的主干网来执行各种视觉任务。

**Swin Transformer block**  Swin-Transformer是通过将Transformer块中的标准多头自注意（MSA）模块替换为基于移位窗口的模块（如第3.2节所述）构建的，其他层保持不变。如图3（b）所示，Swin Transformer block由一个基于移位窗口的MSA模块组成，接着是两层MLP，两层MLP之间是GELU非线性。在每个MSA模块和每个MLP之前应用LayerNorm（LN）层，在每个模块之后应用残差连接。

#### **3.2. 基于移位窗口的自注意**

标准Transformer体系结构[61]及其对图像分类的适应[19]都进行全局自注意力，其中计算了一个token和所有其他tokens之间的关系。全局计算导致相对于token数量的二次复杂度，这使得它不适用于许多需要大量token进行密集预测或表示高分辨率图像的视觉问题。

**非重叠窗口中的自注意**  为了高效地建模，我们建议在局部窗口内计算自注意。窗口被布置成以不重叠的方式均匀地分割图像。假设每个窗口包含M× M个patches，对于一张包含![h\times w](https://math.jianshu.com/math?formula=h%5Ctimes%20w)个patches的图像，全局自注意力(MSA)与基于窗口的自注意力的计算复杂度为：

![\Omega (\mathrm{MSA})=4hwC^2+2(hw)^2C](https://math.jianshu.com/math?formula=%5COmega%20(%5Cmathrm%7BMSA%7D)%3D4hwC%5E2%2B2(hw)%5E2C)  ![(1)](https://math.jianshu.com/math?formula=(1))

![\Omega (\mathrm{W-MSA})=4hwC^2+2M^2hwC](https://math.jianshu.com/math?formula=%5COmega%20(%5Cmathrm%7BW-MSA%7D)%3D4hwC%5E2%2B2M%5E2hwC)  ![(2)](https://math.jianshu.com/math?formula=(2))

注释3：在分析复杂度时，我们省略掉softmax的计算。

其中，前者是patches![hw](https://math.jianshu.com/math?formula=hw)的二次方，后者当![M](https://math.jianshu.com/math?formula=M)为固定时（默认设置为7）是线性的。当![hw](https://math.jianshu.com/math?formula=hw)很大时，全局自注意力计算通常是难以承受的，而基于窗口的自注意力是可扩展的。

##### **连续块的移位窗口划分**

基于窗口的自我注意力模块缺乏跨窗口的连接，这限制了它的建模能力。为了在保持非重叠窗口计算效率的同时引入跨窗口连接，我们提出了一种移位窗口划分方法，该方法在连续的Swin Transformer blocks中交替使用两种划分配置。

如图2所示，第一个模块使用一个常规的窗口分区策略，从左上角的像素开始，8×8的特征映射被平均划分为2×2窗口，每个窗口的尺寸是是4×4（M=4）。下一个模块采用的窗口配置与前一层不同，其相比规则划分窗口，将窗口移位![(⌊\frac{M}{2} ⌋,⌊\frac{M}{2} ⌋)](https://math.jianshu.com/math?formula=(%E2%8C%8A%5Cfrac%7BM%7D%7B2%7D%20%E2%8C%8B%2C%E2%8C%8A%5Cfrac%7BM%7D%7B2%7D%20%E2%8C%8B))个像素。(Then, the next module adopts a windowing configuration that is shifted from that of the preceding layer, by displacing the windows by (⌊M/2⌋,⌊M/2⌋) pixels from the regularly partitioned windows.)

利用移位窗口划分方法，连续的swn变换块被计算为：

![img](https:////upload-images.jianshu.io/upload_images/13727053-69737dffbfc7f45e.png?imageMogr2/auto-orient/strip|imageView2/2/w/390/format/webp)

其中![{\hat{\mathrm{z}} }^l](https://math.jianshu.com/math?formula=%7B%5Chat%7B%5Cmathrm%7Bz%7D%7D%20%7D%5El)和![{\mathrm{z} }^l](https://math.jianshu.com/math?formula=%7B%5Cmathrm%7Bz%7D%20%7D%5El)分别表示块![l](https://math.jianshu.com/math?formula=l)的(S)W-MSA模块和MLP模块的输出特征；W-MSA和SW-MSA分别表示使用规则和移位窗口划分配置的基于窗口的多头部自注意。

移位窗口分割方法引入了前一层中相邻非重叠窗口之间的连接，在图像分类、目标检测和语义分割方面都是有效的，如表4所示。

##### **移位的高效批量计算**  

移位窗口分区的一个问题是，它将导致更多的窗口，从![(⌈\frac{h}{M}  ⌉)\times (⌈\frac{w}{M}  ⌉ )](https://math.jianshu.com/math?formula=(%E2%8C%88%5Cfrac%7Bh%7D%7BM%7D%20%20%E2%8C%89)%5Ctimes%20(%E2%8C%88%5Cfrac%7Bw%7D%7BM%7D%20%20%E2%8C%89%20))变为![(⌈\frac{h}{M}  ⌉+1)\times (⌈\frac{w}{M}  ⌉+1)](https://math.jianshu.com/math?formula=(%E2%8C%88%5Cfrac%7Bh%7D%7BM%7D%20%20%E2%8C%89%2B1)%5Ctimes%20(%E2%8C%88%5Cfrac%7Bw%7D%7BM%7D%20%20%E2%8C%89%2B1))，并且一些窗口将小于![M× M](https://math.jianshu.com/math?formula=M%C3%97%20M)（注释4：为了使窗口大小(M,M)可以被特征映射(h,w)整除，需要的话在特征映射上使用右边和底部的padding）。一个简单的解决方案是将较小的窗口填充到M×M大小，计算注意力时，将填充的值屏蔽掉。当常规分区中的窗口数较少时，例如2× 2，用这种朴素解增加的计算量是相当可观的（2×2.→ 3×3，大2.25倍)。在这里，我们提出了一种更高效的批量计算方法，通过循环向左上方向移动，如图4所示。在这个移动之后，一个批量窗口可能由几个在特征图中不相邻的子窗口组成，因此，采用掩蔽机制将自注意计算限制在每个子窗口内。通过循环移位，批量处理窗口的数量与常规窗口分区的数量相同，因此也是高效的。这种方法的低延迟如表5所示。

![img](https:////upload-images.jianshu.io/upload_images/13727053-691fa6b5fbd846ad.png?imageMogr2/auto-orient/strip|imageView2/2/w/625/format/webp)

图4.移位窗口划分中用于自注意的高效批处理计算方法的图示。

##### **相对位置偏置**  

在计算自注意力时，我们遵循[48,1,31,32]，在每个头计算相似性时，包含一个相对位置偏置![B\in R^{M^2 \times M^2 } ](https://math.jianshu.com/math?formula=B%5Cin%20R%5E%7BM%5E2%20%5Ctimes%20M%5E2%20%7D%20)：

![\mathrm{Attention}(Q,K,V)=\mathrm{SoftMax}(QK^T/\sqrt{d} +B )V](https://math.jianshu.com/math?formula=%5Cmathrm%7BAttention%7D(Q%2CK%2CV)%3D%5Cmathrm%7BSoftMax%7D(QK%5ET%2F%5Csqrt%7Bd%7D%20%2BB%20)V)，  ![(4)](https://math.jianshu.com/math?formula=(4))

其中![Q,K,V\in R^{M^2\times d } ](https://math.jianshu.com/math?formula=Q%2CK%2CV%5Cin%20R%5E%7BM%5E2%5Ctimes%20d%20%7D%20)是查询、键、值项矩阵，其中![d](https://math.jianshu.com/math?formula=d)是查询和键的维度，![M^2](https://math.jianshu.com/math?formula=M%5E2)是一个窗口内的图块数。由于沿每个轴的相对位置位于范围[−M+1；M−1]内，我们参数化一个较小尺寸的偏置矩阵![\hat{ B }  \in R^{(2M-1)\times (2M-1)} ](https://math.jianshu.com/math?formula=%5Chat%7B%20B%20%7D%20%20%5Cin%20R%5E%7B(2M-1)%5Ctimes%20(2M-1)%7D%20)，![B](https://math.jianshu.com/math?formula=B)中的值取自![\hat{B} ](https://math.jianshu.com/math?formula=%5Chat%7BB%7D%20)。

如表4所示，我们观察到，相比不使用偏置项或使用绝对位置嵌入，使用该项可以带来显著改进。如[19]所示，进一步向输入中添加绝对位置嵌入会略微降低性能，因此在我们的实现中没有采用。

预训练中学习到的相对位置偏差也可用于初始化模型，当在下游任务的窗口大小不同时，使用bi-cubic插值[19, 60]。

#### **3.3. 体系结构变体**

我们建立了我们的基础模型Swin-B，它的模型大小和计算复杂度与ViTB/DeiT-B相似。我们还介绍了Swin-T、Swin-S和Swin-L，它们的模型大小和计算复杂度大约是0.25×、0.5×和2×。

请注意，**Swin-T**和Swin-S的复杂度分别与**ResNet-50**(DeiT-S)和ResNet-101相似。默认情况下，窗口大小设置为M=7。所有实验中，每个头部的查询维度为d=32，每个MLP的扩展层为α = 4。这些模型变体的体系结构参数包括：

•  Swin-T:  C=96，层数={2，2，6，2}

•  Swin-S:  C=96，层数={2，2，18，2}

•  Swin-B:  C=128，层数={2，2，18，2}

•  Swin-L:  C=192，层数={2，2，18，2}

其中**C是第一阶段中隐藏层的通道数**。模型大小、理论计算复杂度（FLOPs）和ImageNet图像分类吞吐量如表1所示。

### **4.实验**

我们在ImageNet-1K图像分类[18]、COCO目标检测[42]和ADE20K语义分割[80]上进行了实验。在下面，我们首先将所提出的Swin变压器架构与之前在这三项任务上的最新技术进行比较。然后，分析了Swin变压器的重要设计要素。

#### **4.1. 基于ImageNet-1K的图像分类**

**设置**  对于图像分类，我们在ImageNet-1K[18]上对所提出的Swin变换器进行了测试，其中包含1.28M个训练图像和来自1000个类的50K个验证图像。报告了单个裁剪的最高精度。我们考虑两种训练设置：

•  常规ImageNet-1K训练。此设置主要遵循[60]（编者注：在arxiv不同版本中，引用索引号会发生变化，这里指的是DeiT）。我们使用了一个AdamW[36]优化器，用于300个阶段，使用余弦衰减学习率调度器和**20**个阶段的线性预热。批量大小为1024，初始学习率为0.001，权重衰减为0.05。我们将[60]中的大部分增强和正则化策略都包括在训练中，除了repeated augmentation [30]和EMA[44]，它们不能提高性能。请注意，这与[60]相反，在[60]中，repeated augmentation 对于稳定ViT训练至关重要。

•  ImageNet-22K预训练和ImageNet-1K微调。我们还对较大的ImageNet-22K数据集进行了预训练，该数据集包含1420万张图像和22K个类。我们采用一个AdamW优化器，使用线性衰减学习率调度器训练60个epoch，使用5个epoch的线性预热。批量大小为4096，初始学习率为0.001，权重衰减为0.01。在ImageNet-1K微调中，我们训练了30个阶段的模型，批大小为1024，恒定学习率为10e−5，重量衰减10e−8。

**常规ImageNet-1K训练的结果**  表1(a) 给出了与其它主干网络的比较（包括基于Transformer和基于卷积网络的），使用常规ImageNet-1K训练。

与之前最先进的基于Transformer的架构（即DeiT[60]）相比，Swin Transformers明显超过了具有类似复杂度的对应DeiT架构：使用224×224输入时，Swin-T（81.3%）比DeiT-S（79.8%）高出1.5%，使用224×224/384×384输入时，Swin-B（83.3%/84.2%）比DeiT-B（81.8%/83.1%）分别高出1.5%/1%。

与最先进的卷积网络（即RegNet[47]和EfficientNet[57]）相比，Swin Transformers实现了稍微好一点的速度精度折衷。注意到，虽然RegNet[47]和EfficientNet[57]是通过彻底的架构搜索获得的，所提出的Swin Transformer是从标准Transformer适配而来的，具有很强的进一步改进潜力。

**ImageNet-22K预训练结果**  我们还在ImageNet22K上预训练了更大容量的Swin-B和Swin-L。在ImageNet-1K图像分类上微调的结果如表1(b)所示。对于Swin-B，ImageNet22K预训练相比在ImageNet-1K从头训练，能带来大约1.8%到1.9%的提升。与之前ImageNet-22K预训练的最佳结果相比，我们的模型实现了显著更好的速度-精度折衷：Swin-B获得86.0%的top-1精度，比ViT高2.0%，具有相似的推理吞吐量（84.7 vs.85.9图像/秒）和略低的FLOPs（47.0G vs.55.4G）。更大的Swin-L模型达到86.4%的top-1精度，略好于Swin-B模型。

![img](https:////upload-images.jianshu.io/upload_images/13727053-76fb173eb8461ba9.png?imageMogr2/auto-orient/strip|imageView2/2/w/578/format/webp)

![img](https:////upload-images.jianshu.io/upload_images/13727053-11c956597208e6f8.png?imageMogr2/auto-orient/strip|imageView2/2/w/571/format/webp)

表1.ImageNet-1K分类中不同主干的比较。吞吐量是使用[[65\]](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Frwightman%2Fpytorch-image-models)的GitHub repository和V100 GPU来测量的，following [60]。

#### **4.2. COCO的目标检测**

设置对象检测和实例分割实验在COCO2017上进行，包括118K训练、5K验证和20K test-dev图像。使用验证集进行消融研究，并在test-dev上报告系统级比较。对于消融研究，我们考虑了四种典型的目标检测框架：mmdetection [9]中的Cascade Mask R-CNN[28,5]、ATSS[76]、RepPoints v2[11]和Sparse RCNN[55]。对于这四个框架，我们使用了相同的设置：多尺度训练[7,55]（调整输入大小，使短边在480到800之间，而长边最多为1333），AdamW[43]优化器（初始学习率为0.0001，权重衰减为0.05，批大小为16），以及3倍计划（36个周期）。对于系统级比较，我们采用改进的HTC[8]（表示为HTC++），使用instaboost[21]，更强的多尺度训练[6]，6×调度也即72个epoch，软NMS[4]，以及ImageNet-22K预训练模型作为初始化。

我们将我们的Swin变压器与标准卷积网络（也即ResNe(X)t）和之前的Transformer网络（DeiT）进行比较。比较是通过在其他设置不变的情况下仅更改主干来进行的。请注意，尽管Swin-Transformer和ResNe(X)t由于其层次化特征映射而直接适用于上述所有框架，但DeiT只产生单一分辨率的特征映射，不能直接应用。为了公平比较，我们按照[78]的方法，使用反卷积层构造DeiT的层次特征映射。

**与ResNe(X)t的比较**  表2(a)列出了Swin-T和ResNet-50在四种目标检测框架上的结果。我们的Swin-T架构相比ResNet-50带来了一致的提升，+3.4∼4.2box-AP，模型大小、FLOPs和延迟也略微大些。

表2(b)使用Cascade Mask R-CNN比较了不同模型容量下的Swin Transformer和ResNe(X)t。Swin-Transformer实现了51.9box-AP和45.0mask-AP的高检测精度，与ResNeXt101-64x4d相比，有+3.6box-AP和+3.3mask-AP的显著增益，模型大小、FLOPs和延迟相似。在使用改进的HTC框架的52.3 box AP和46.0 mask AP的更高基线上，Swin Transformer的增益也较高，分别为+4.1 boxAP和+3.1 mask AP（见表2(c)）。关于推理速度，虽然ResNe(X)t是由高度优化的Cudnn函数构建的，而我们的体系结构是由内置的PyTorch函数实现的，这些函数并没有得到很好的优化。彻底的核优化超出了本文的范围。

**与DeiT比较**  使用Cascade Mask R-CNN框架的DeiT-S的性能如表2(b)所示。Swin-T的结果是+2.5box-AP和+2.3mask-AP，高于DeiT-S，模型尺寸相似（86M对80M），推理速度显著提高（15.3fps对10.4fps）。DeiT的推理速度较低的主要原因是其对输入图像大小的二次复杂度。

**与以前最先进技术的比较**  表2(c)将我们的最佳结果与以前最先进的模型进行了比较。我们的最佳模型在COCO test dev上实现了58.7 box AP和51.1 mask AP，超过了之前的最佳结果+2.7 box AP（Copy-paste[25]，无外部数据）和+2.6 mask AP（DetectoRS[45]）。

![img](https:////upload-images.jianshu.io/upload_images/13727053-df98aa9ba677c596.png?imageMogr2/auto-orient/strip|imageView2/2/w/507/format/webp)

![img](https:////upload-images.jianshu.io/upload_images/13727053-a949218ac9ae0d49.png?imageMogr2/auto-orient/strip|imageView2/2/w/500/format/webp)

表2.COCO对象检测和实例分割结果。†表示额外的反卷积层用于生成层次特征图。*表示多尺度测试

#### **4.3. 基于ADE20K的语义分割**

**设置**  ADE20K[80]是一个应用广泛的语义切分数据集，涵盖了150个语义类别。它总共有25K个图像，其中20K用于训练，2K用于验证，另外3K用于测试。我们利用mmseg[15]中的UperNet[66]作为我们的基础框架，因为它很高效。更多细节见附录。

**结果**  表3列出了不同方法/主干对的mIoU、模型大小（#param）、FLOPs和FPS。从这些结果可以看出，在计算量相似的情况下，Swin-S比DeiT-S高出5.3 mIoU（49.3比44.0）。它也比ResNet-101高出+4.4 mIoU比ResNeSt-101高出+2.4 mIoU[75]。我们的带有ImageNet-22K预训练的Swin-L模型在val集上实现了53.5 mIoU，超过了之前的最佳模型+3.2 mIoU（SETR[78]提供了50.3 mIoU，其模型更大）。

![img](https:////upload-images.jianshu.io/upload_images/13727053-9b4beb8cb20924e6.png?imageMogr2/auto-orient/strip|imageView2/2/w/585/format/webp)

表3.ADE20K val和测试集的语义分割结果。†表示额外的反卷积层用于生成层次特征图。‡表示模型已在ImageNet-22K上预训练

#### **4.4. 烧蚀研究**

在本节中，我们使用ImageNet-1K图像分类、COCO目标检测的Cascade Mask R-CNN和ADE20K语义分割的UperNet来烧蚀所提出的Swin Transformer中的重要设计元素。

**移位窗口**  移位窗口的消融在这三项任务中如表4所示。在每个阶段移位窗口划分的Swin-T的性能都优于基于单个窗口划分的Swin-T，在ImageNet-1K上的精度为+1.1%，在COCO上的精度为+2.8 boxAP/+2.2 maskAP，在ADE20K上的精度为+2.8 mIoU。结果表明，使用移动窗口在前一层窗口之间建立连接是有效的。移位窗口的延迟开销也很小，如表5所示。

**相对位置偏置**  表4显示了不同位置嵌入方法的比较。相对位置偏差的Swin-T在ImageNet-1K上的准确率为+1.2%/+0.8%，在COCO上的准确率为+1.3/+1.5，在mask上的准确率为+1.1/+1.3，在ADE20K上的准确率为+2.3/+2.9miou，这表明相对位置偏差的有效性。另外请注意，虽然包含绝对位置嵌入提高了图像分类精度（+0.4%），但它损害了目标检测和语义分割（COCO上为-0.2 box/mask AP，ADE20K上为-0.6 mIoU）。

虽然最近的ViT/DeiT模型放弃了图像分类中的平移不变性，尽管它长期以来被证明对视觉建模至关重要，但我们发现，鼓励某些平移不变性的归纳偏置对于通用视觉建模仍然是可取的，特别是对于密集预测任务的目标检测和语义分割。

![img](https:////upload-images.jianshu.io/upload_images/13727053-8c6d137ae3f3ec81.png?imageMogr2/auto-orient/strip|imageView2/2/w/547/format/webp)

表4.使用Swin-T体系结构对三个基准上的移位窗口方法和不同位置嵌入方法进行的消融研究。w/o shifting: 所有自注意模块采用规则窗口划分，不移位；abs. pos.: ViT的绝对位置嵌入项；rel. pos.: 带有附加相对位置偏置项的默认设置，见等式(4)；app.: 等式(4)中的第一个缩放点积项。

**不同的自注意方法**  表5比较了不同的自注意计算方法和实现的实际速度。我们的循环实现比单纯填充(naive padding)更具硬件效率，特别是对于更深层的阶段。总的来说，它对Swin-T，Swin-S和Swin-B分别带来了13%，18%和18%的加速。

在网络的4个阶段，使用我们提出的基于移位窗口的自注意力，要比那些基于滑动窗口的naive/kernel implementations，要分别更高效40.8×/2.5×, 20.2×/2.5×, 9.3×/2.1×, 和7.6×/1.8×。总的来说，构建在移动窗口上的Swin-Transformer架构分别比构建在滑动窗口上的Swin-T、Swin-S和Swin-B快4.1/1.5、4.0/1.5和3.6/1.5倍。表6比较了他们在这三项任务上的准确度，表明他们在视觉建模上的准确度相似。

与Performer[13]相比，Performer[13]是速度最快的Transformer体系结构之一（见[59]），基于移位窗口的自注意计算和整体Swin-Transformer体系结构稍快（见表5），同时与使用Swin-T的ImageNet-1K上的Performer相比，实现了+2.3%的top-1精度（见表6）。

![img](https:////upload-images.jianshu.io/upload_images/13727053-7b2c2f81852cd06a.png?imageMogr2/auto-orient/strip|imageView2/2/w/577/format/webp)

### **5.结论**

本文提出了一种新的视觉变换器Swin-Transformer，它产生了一种层次化的特征表示，其计算复杂度与输入图像的大小成线性关系。Swin-Transformer在COCO目标检测和ADE20K语义分割方面达到了最先进的性能，大大超过了以前最好的方法。我们希望Swin-Transformer在各种视觉问题上的强大性能将促进视觉和语言信号的统一建模。

作为Swin-Transformer的一个关键元素，基于移位窗口的自注意被证明是解决视觉问题的有效方法，我们也期待着研究它在自然语言处理中的应用。

### **A1  详细的体系结构**

详细的架构规范如表7所示，其中所有架构的输入图像大小都假定为224×224。”Concat n×n”表示在1个patch中n×n个相邻特征的拼接。此操作导致特征图下采样n倍。96-d表示输出为96维的线性层。win.sz.7×7表示窗口大小为7×7的多头自注意力。

![img](https:////upload-images.jianshu.io/upload_images/13727053-e56c88a3b0403f2a.png?imageMogr2/auto-orient/strip|imageView2/2/w/1183/format/webp)

### A2  详细的实验设置

#### **A2.1  基于ImageNet-1K的图像分类**

在最后一阶段的输出特征图上应用全局平均池化层，然后使用线性分类器进行图像分类。我们发现这种策略与使用ViT[19]和DeiT[60]中的额外类标记(class token )一样精确。在评估中，报告了使用单个裁剪的top-1精度。

**常规ImageNet-1K培训**  培训设置主要遵循[60]。对于所有型号的变体，我们采用默认的输入图像分辨率224×224。对于384×384这样的其他分辨率，我们对在224×224下训练的模型进行微调，而不是从头开始训练，以减少GPU的消耗。

当使用224×224输入从头开始训练时，我们使用一个AdamW[36]优化器，用于300个epoch，使用一个具有20个线性预热历元的余弦衰减学习率调度器。批大小为1024，初始学习率为0.001，权重衰减为0.05，使用最大范数为1的梯度剪裁。我们在训练中包括了[60]中的大部分增强和正则化策略，包括RandAugment[16]、Mixup[74]、Cutmix[72]、随机擦除[79]和随机深度[34]，但没有重复增强[30]和指数移动平均（EMA）[44]，它们不能提高性能。请注意，这与[60]相反，在[60]中，反复增强对于稳定ViT训练至关重要。对于更大的模型，随机深度增加的程度越来越大，即Swin-T、Swin-S和Swin-B分别为0.2、0.3和0.5。

为了以更高的分辨率对输入进行微调，我们采用了一个adamW[36]优化器，用于30个周期，恒定的学习率为10−5，重量衰减10−8，除将随机深度比设置为0.1外，数据增强和正则化与第一阶段相同。

**ImageNet-22K预训练**    我们还对较大的ImageNet-22K数据集进行了预训练，该数据集包含1420万张图像和22K个类。训练分两个阶段进行。对于输入为224×224的第一阶段，我们使用一个线性衰减学习率调度器和一个5历元线性预热，使用一个60历元的AdamW优化器。批量大小为4096，初始学习率为0.001，权重衰减为0.01。在ImageNet-1K精调的第二阶段，输入224×224/384×384，我们训练了30个时期的模型，批量大小为1024，恒定学习率为10−5，重量衰减10−8。

#### **A2.2  COCO的目标检测**

对于消融研究，我们考虑四个典型的对象检测框架：Cascade Mask R-CNN〔28, 5〕、ATSS〔76〕、RepPoints v2〔11〕和Sparse RCNN〔55〕。对于这四个框架，我们使用相同的设置：多尺度训练[7,55]（调整输入大小，使短边在480到800之间，而长边最多为1333），AdamW[43]优化器（初始学习率为0.0001，权重衰减为0.05，批大小为16），3倍的时间表（36个时期，学习率下降10%× 在第27和33时代）。

对于系统级比较，我们采用改进的HTC[8]（表示为HTC++）和instaboost[21]，更强的多尺度训练[6]（调整输入大小，使短边在400到1400之间，而长边最多为1600），6x时间表（72个时段，学习率在63和69个时段衰减系数为0.1），SoftNMS[4]，并在最后阶段的输出中附加一个额外的全局自关注层，ImageNet-22K预训练模型作为初始化。所有Swin变压器模型均采用0.2的随机深度比。

#### **A2.3  基于ADE20K的语义分割**

ADE20K[80]是一个应用广泛的语义切分数据集，涵盖了150个语义类别。它总共有25K个图像，其中20K用于训练，2K用于验证，另外3K用于测试。我们利用mmsegmentation[15]中的UperNet[66]作为其高效性的基础框架。

在培训中，我们采用了AdamW[43]优化器，初始学习率为6× 10e−5，权重衰减为0.01，调度器使用线性学习率衰减，线性预热为1500次迭代。模型在8个GPU上训练，每个GPU 2个图像，迭代160K次。对于增强，我们采用mmsegmentation中的默认设置：随机水平翻转、比率范围[0.5，2.0]内的随机重缩放和随机光度失真。所有Swin变压器模型均采用了比值为0.2的随机深度。Swin-T、Swin-S与前面的方法一样接受标准设置方面的训练，输入值为512×512.带‡的Swin-B和Swin-L表示这两个模型是在ImageNet-22K上预先训练的，输入640×640。

在推理中，使用分辨率为[0.5，0.75，1.0，1.25，1.5，1.75]× 的多尺度测试，这个缩放比例的一部分是在训练中被使用的。在报告测试分数时，训练图像和验证图像都用于训练，遵循常规做法[68]。

### **A3  更多的实验**

#### **A3.1  不同输入大小的图像分类**

表8列出了在224×224到384×384之间具有不同输入图像大小的Swin变压器的性能。一般来说，输入分辨率越大，top-1的精度越好，但推理速度越慢。

![img](https:////upload-images.jianshu.io/upload_images/13727053-81ddc754bbe0382f.png?imageMogr2/auto-orient/strip|imageView2/2/w/500/format/webp)

#### **A3.2  COCO上ResNe(X)t的不同优化器**

表9比较了ResNe(X)t主干网的AdamW和SGD优化器对COCO目标检测的影响。比较中使用了Cascade Mask R-CNN框架。虽然SGD被用作级Cascade Mask R-CNN框架的默认优化器，但我们通常通过用AdamW优化器替换它来提高精度，特别是对于较小的主干网。因此，我们将AdamW用于ResNe(X)t主干网，与所提出的Swin变压器结构进行比较。

![img](https:////upload-images.jianshu.io/upload_images/13727053-f143323a9905a934.png?imageMogr2/auto-orient/strip|imageView2/2/w/505/format/webp)



作者：Vinteuil
链接：https://www.jianshu.com/p/95fbb8a1328d
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。