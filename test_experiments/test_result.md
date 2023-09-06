## 1 连续任务 使用LLM

> 执行顺序： 烹饪-物流-制造-清洁

![image-20230901163814506](D:\IDE\Typora\Cache\test_result.assets\image-20230901163814506.png)

![](D:\IDE\Typora\Cache\test_result.assets\image-20230830120714019.png)

### (1) 烹饪

Test Count: 1075		(Unambiguous Count: 985	 Ambiguous Count: 90)
Unambiguous Rule Count:  26  ->  210
  Ambiguous Rule Count:  3   ->  46
     Intent Rule Count:  29  ->  256
     Memory Rule Count:  169 ->  517
        All Rule Count:  198 ->  773
    Unambiguous Parse Count: 964		97.86802030456853%
Unambiguous Plausible Count: 773		78.47715736040609%
      Ambiguous Parse Count: 90		100.0%
  Ambiguous Plausible Count: 70		77.77777777777778%
    Total Parse Percent: 98.04651162790698%
Total Plausible Percent: 78.41860465116279%

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826191131686.png" alt="image-20230826191131686" style="zoom: 33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826191143952.png" alt="image-20230826191143952" style="zoom: 33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826191154743.png" alt="image-20230826191154743" style="zoom: 33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826191202710.png" alt="image-20230826191202710" style="zoom: 50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826191220233.png" alt="image-20230826191220233" style="zoom: 50%;" />

### (2) 物流

Test Count: 1103		(Unambiguous Count: 1008	 Ambiguous Count: 95)
Unambiguous Rule Count:  26  -> 201 -> 292
  Ambiguous Rule Count:   3  ->  46 -> 79
     Intent Rule Count:  29  -> 256 -> 371
     Memory Rule Count:  169 ->  517、353 -> 433
        All Rule Count:  198 ->  773、609 -> 804
    Unambiguous Parse Count: 993		98.51190476190477%
Unambiguous Plausible Count: 834		82.73809523809523%
      Ambiguous Parse Count: 94		98.94736842105263%
  Ambiguous Plausible Count: 73		76.84210526315789%
    Total Parse Percent: 98.5494106980961%
Total Plausible Percent: 82.23028105167724%

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826202037062.png" alt="image-20230826202037062" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826202043347.png" alt="image-20230826202043347" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826202052688.png" alt="image-20230826202052688" style="zoom:33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826202102880.png" alt="image-20230826202102880" style="zoom:50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826202109205.png" alt="image-20230826202109205" style="zoom:50%;" />

### (3) 制造

Test Count: 1151		(Unambiguous Count: 1052	 Ambiguous Count: 99)
Unambiguous Rule Count:  26  ->    201    ->   292   ->   346
  Ambiguous Rule Count:   3  ->     46    ->    79   ->   104
     Intent Rule Count:  29  ->    256    ->   371   ->   450
     Memory Rule Count:  169 ->  517、353 -> 433、287 ->   327
        All Rule Count:  198 ->  773、609 -> 804、658 ->   777
    Unambiguous Parse Count: 1032		98.09885931558935%
Unambiguous Plausible Count: 953		90.5893536121673%
      Ambiguous Parse Count: 98		98.98989898989899%
  Ambiguous Plausible Count: 77		77.77777777777778%
    Total Parse Percent: 98.17549956559513%
Total Plausible Percent: 89.4874022589053%

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826224350336.png" alt="image-20230826224350336" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826224355892.png" alt="image-20230826224355892" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826224403061.png" alt="image-20230826224403061" style="zoom:33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826224411019.png" alt="image-20230826224411019" style="zoom:50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230826224416657.png" alt="image-20230826224416657" style="zoom:50%;" />

### (4) 清洁

Test Count: 1192		(Unambiguous Count: 1092	 Ambiguous Count: 100)
Unambiguous Rule Count: 26 -> 201 -> 292 -> 346 -> 404
  Ambiguous Rule Count:  3 ->  46 ->  79 -> 104 -> 108
     Intent Rule Count: 29 -> 256 -> 371 -> 450 -> 512
     Memory Rule Count: 325
        All Rule Count: 837
    Unambiguous Parse Count: 1087		99.54212454212454%
Unambiguous Plausible Count: 962		88.09523809523809%
      Ambiguous Parse Count: 98		98.0%
  Ambiguous Plausible Count: 79		79.0%
    Total Parse Percent: 99.41275167785236%
Total Plausible Percent: 87.33221476510067%

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827003932518.png" alt="image-20230827003932518" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827003941909.png" alt="image-20230827003941909" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827003953022.png" alt="image-20230827003953022" style="zoom:33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827004027200.png" alt="image-20230827004027200" style="zoom:50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827004039828.png" alt="image-20230827004039828" style="zoom:50%;" />

- 连续

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827004548349.png" alt="image-20230827004548349" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827004554051.png" alt="image-20230827004554051" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827004559402.png" alt="image-20230827004559402" style="zoom:33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827004611849.png" alt="image-20230827004611849" style="zoom:50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230827004618090.png" alt="image-20230827004618090" style="zoom:50%;" />

## 2 单独任务 使用LLM 

### (1) 烹饪(同上)

### (2) 物流

Test Count: 1103		(Unambiguous Count: 1008	 Ambiguous Count: 95)
Unambiguous Rule Count: 26 -> 138
  Ambiguous Rule Count: 3  -> 46
     Intent Rule Count: 29 -> 184
     Memory Rule Count: 187-> 280
        All Rule Count: 216-> 464
    Unambiguous Parse Count: 996		98.80952380952381%
Unambiguous Plausible Count: 853		84.62301587301587%
      Ambiguous Parse Count: 94		98.94736842105263%
  Ambiguous Plausible Count: 43		45.26315789473684%
    Total Parse Percent: 98.82139619220308%
Total Plausible Percent: 81.23300090661832%

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828145308208.png" alt="image-20230828145308208" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828145313736.png" alt="image-20230828145313736" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828145318380.png" alt="image-20230828145318380" style="zoom:33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828145324872.png" alt="image-20230828145324872" style="zoom: 50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828145331965.png" alt="image-20230828145331965" style="zoom: 50%;" />

### (3) 制造

Test Count: 1151		(Unambiguous Count: 1052	 Ambiguous Count: 99)
Unambiguous Rule Count: 26 -> 115
  Ambiguous Rule Count: 4  -> 41 
     Intent Rule Count: 30 -> 156
     Memory Rule Count: 180-> 254
        All Rule Count: 210-> 410
    Unambiguous Parse Count: 1030		97.90874524714829%
Unambiguous Plausible Count: 985		93.63117870722434%
      Ambiguous Parse Count: 99		100.0%
  Ambiguous Plausible Count: 72		72.72727272727273%
    Total Parse Percent: 98.08861859252823%
Total Plausible Percent: 91.83318853171156%

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828140632752.png" alt="image-20230828140632752" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828140639963.png" alt="image-20230828140639963" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828140645460.png" alt="image-20230828140645460" style="zoom:33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828140651046.png" alt="image-20230828140651046" style="zoom:50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828140657241.png" alt="image-20230828140657241" style="zoom:50%;" />

### (4) 清洁

Test Count: 1192		(Unambiguous Count: 1092	 Ambiguous Count: 100)
Unambiguous Rule Count: 26 -> 172
  Ambiguous Rule Count:  3 -> 25
     Intent Rule Count: 29 -> 197
     Memory Rule Count: 170-> 303
        All Rule Count: 199-> 500
    Unambiguous Parse Count: 1090		99.81684981684981%
Unambiguous Plausible Count: 992		90.84249084249085%
      Ambiguous Parse Count: 98		98.0%
  Ambiguous Plausible Count: 50		50.0%
    Total Parse Percent: 99.66442953020133%
Total Plausible Percent: 87.41610738255034%

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828162130506.png" alt="image-20230828162130506" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828162139521.png" alt="image-20230828162139521" style="zoom:33%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828162145103.png" alt="image-20230828162145103" style="zoom:33%;" />

<img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828162154386.png" alt="image-20230828162154386" style="zoom:50%;" /><img src="D:\IDE\Typora\Cache\test_result.assets\image-20230828162215277.png" alt="image-20230828162215277" style="zoom:50%;" />

## 3 Lingua对比

### (1)4次连续任务基础上

#### 1.直接解析veil_500

> 不使用LLM

Test Count: 2040
  Ambiguous Rule Count: 108
     Memory Rule Count: 313
        All Rule Count: 421
      Ambiguous Parse Count: 88		4.313725490196078%

#### 2.学习100条规则

> 使用llm

Test Count: 100
  Ambiguous Rule Count: 173
     Memory Rule Count: 259
        All Rule Count: 432
      Ambiguous Parse Count: 100		100.0%

> 不适用llm 测试剩下2098条数据

Test Count: 2095
      Ambiguous Parse Count: 650		31.026252983293556%

#### 3.学习500条规则

> 使用LLM

Test Count: 400
  Ambiguous Rule Count: 327
     Memory Rule Count: 397
        All Rule Count: 724
      Ambiguous Parse Count: 397		99.25%

> 不使用LLM 测试剩下的1700条

Test Count: 1696
  Ambiguous Rule Count: 327
     Memory Rule Count: 397
        All Rule Count: 724
      Ambiguous Parse Count: 822		48.46698113207547%

#### 4.学习1000条规则

Test Count: 1196
  Ambiguous Rule Count: 475
     Memory Rule Count: 504
        All Rule Count: 979
      Ambiguous Parse Count: 636		53.17725752508361%

#### 5.完全使用LLM

### (2)初始状态

#### 1.学习100条规则

> 使用LLM学习

Test Count: 100
  Ambiguous Rule Count: 68
     Memory Rule Count: 259
        All Rule Count: 327
      Ambiguous Parse Count: 100		100.0%

> 不适用LLM 解析剩下2098条指令

Test Count: 2095
      Ambiguous Parse Count: 639		30.501193317422437%

#### 2.学习500条规则

> 使用LLM

Test Count: 400
  Ambiguous Rule Count: 224
     Memory Rule Count: 401
        All Rule Count: 625
      Ambiguous Parse Count: 398		99.5%

> 不使用LLM 测试剩下的1700条

Test Count: 1696
      Ambiguous Parse Count: 824		48.58490566037736%

#### 3.学习1000条指令后

> 使用LLM

Test Count: 500
  Ambiguous Rule Count: 372
     Memory Rule Count: 505
        All Rule Count: 877
      Ambiguous Parse Count: 499		99.8%

> 不适用LLM 测试剩下的 1200条

Test Count: 1196
      Ambiguous Parse Count: 636		53.17725752508361%

#### 4.完全使用LLM

> 学习了所有指令后

Test Count: 1198
  Ambiguous Rule Count: 769
     Memory Rule Count: 733
        All Rule Count: 1502
      Ambiguous Parse Count: 1196		99.8330550918197%

> 所有指令的解析率

Test Count: 2198
  Ambiguous Rule Count: 769
     Memory Rule Count: 733
        All Rule Count: 1502
      Ambiguous Parse Count: 2195		99.86351228389445%