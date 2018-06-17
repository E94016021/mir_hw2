# mir_hw2
*所有的code可以詳見https://github.com/E94016021/mir-hw2，相關之輸出在該檔同名之txt檔中*

## Q1 (20%): Evaluate your tempo estimation algorithm on the Ballroom dataset using the Fourier tempogram.

使用的方法：

    先做出tempogram之後再依每個時間取peak的點，將其所對應之tempo與其value存入累加之後，以累計的數量由大排到小，再利用自製的click聲（即最純淨的tempo音)，得出累計value最大所對應的tempo T1與次大的Tempo T2，再利用實驗結果調整參數，可得完全符合之tempo，在預測click之tempo時可以完美cover。
![eg.此為 bpm=60 之 click 的 tempogram 圖：](https://d2mxuefqeaa7sj.cloudfront.net/s_FD26B236708BC906E918F324198967E509AD4D9E241641A5DAF1BCD35C89A9C0_1528816292413_60.png)

    BPM/value_of_tempo_we_get = const ?
    60/31.23999255259728 = 1.9206150545324514
    78/41.21020294172407 = 1.892735158579561
    120/63.809346490411464 = 1.8806022408963587
    134/71.12083410910445 = 1.8841173852718658
    160/84.4144479612735 = 1.8954101325569601
    171/90.39657419474958 = 1.8916646070192784
    mean = 1.8941907631427457 
  由上述實驗得到參數 1.8941907631427457  
  所以我們所輸出的
    tempo = idx數*單位idx的tempo數*1.8941907631427457 
  在結果上我們可以看這張圖表
            Cha Cha : avg.P-score = 0.0194 , avg.ALOTC = 0.06306306306306306
               Jive : avg.P-score = 0.8908 , avg.ALOTC = 0.9166666666666666
          Quickstep : avg.P-score = 0.7948 , avg.ALOTC = 0.8048780487804879
              Rumba : avg.P-score = 0.0318 , avg.ALOTC = 0.05102040816326531
              Samba : avg.P-score = 0.0690 , avg.ALOTC = 0.1744186046511628
              Tango : avg.P-score = 0.3569 , avg.ALOTC = 0.4883720930232558
     Viennese Waltz : avg.P-score = 0.4996 , avg.ALOTC = 0.5076923076923077
         Slow Waltz : avg.P-score = 0.1538 , avg.ALOTC = 0.2818181818181818
  可以看得出來在 Jive和Quickstep有較高的P-score與ALOTC
  
## Q2 (20%):Comparing T1/T2，T1/G，T2/G for the genres：
  一樣也是參考圖表
            Cha Cha : avg.t2/t1 = 1.4537 , avg.t1/gt = 1.7842 , avg.t2/gt = 2.0464
               Jive : avg.t2/t1 = 1.1017 , avg.t1/gt = 1.0095 , avg.t2/gt = 1.0723
          Quickstep : avg.t2/t1 = 1.3960 , avg.t1/gt = 0.8201 , avg.t2/gt = 0.9590
              Rumba : avg.t2/t1 = 1.4777 , avg.t1/gt = 1.5919 , avg.t2/gt = 1.8927
              Samba : avg.t2/t1 = 1.7279 , avg.t1/gt = 2.5271 , avg.t2/gt = 3.3165
              Tango : avg.t2/t1 = 1.6480 , avg.t1/gt = 0.9703 , avg.t2/gt = 1.3311
     Viennese Waltz : avg.t2/t1 = 1.5206 , avg.t1/gt = 0.5402 , avg.t2/gt = 0.7107
         Slow Waltz : avg.t2/t1 = 1.3978 , avg.t1/gt = 0.8671 , avg.t2/gt = 1.1524
  其實這個很有趣，可以發現一些有趣的現象，比如說cha cha cha會產生
    t2/t1 = 1.4537，t1/gt = 1.7842，t2/gt = 2.0464
  這組數字，而在每一個genre都會出先一個pattern，不斷地出現(可詳見q2.txt)
  eg. Jive
    avg.t2/t1 = 1.1017 , avg.t1/gt = 1.0095 , avg.t2/gt = 1.0723
  便可觀察出通常是某節奏是某節奏的一倍、兩倍、三倍等等
## Q3 (10%): try to use[𝑇 /2,𝑇 /2], [𝑇 /3,𝑇 /3], and [𝑇 /4,𝑇 /4].
  在除2除3除4的狀況下觀察到一些現象：
  基本上當出狀況很糟的genre似乎很容易會在除與某數的時候分數突然地升高，這也代表當初在預測的tempo可能是正確值之倍數，Cha Cha就是個明顯的例子，在初始的預測他的tempo很多都來到257，但實際值為127，所以再除以二之後的表現非常優異，之後的例子族繁不及備載。
  但再除以3與4時，大部分的分數都掉到近乎零分，也就代表已經超過太多倍了。


    T/2
            Cha Cha : avg.P-score = 0.9116 , avg.ALOTC = 0.990990990990991
               Jive : avg.P-score = 0.0495 , avg.ALOTC = 0.05
          Quickstep : avg.P-score = 0.0000 , avg.ALOTC = 0.0
              Rumba : avg.P-score = 0.7235 , avg.ALOTC = 0.8163265306122449
              Samba : avg.P-score = 0.1654 , avg.ALOTC = 0.313953488372093
              Tango : avg.P-score = 0.3175 , avg.ALOTC = 0.37209302325581395
     Viennese Waltz : avg.P-score = 0.0000 , avg.ALOTC = 0.0
         Slow Waltz : avg.P-score = 0.1533 , avg.ALOTC = 0.2


    T/3
            Cha Cha : avg.P-score = 0.0000 , avg.ALOTC = 0.0
               Jive : avg.P-score = 0.0000 , avg.ALOTC = 0.0
          Quickstep : avg.P-score = 0.0000 , avg.ALOTC = 0.0
              Rumba : avg.P-score = 0.0000 , avg.ALOTC = 0.0
              Samba : avg.P-score = 0.0000 , avg.ALOTC = 0.0
              Tango : avg.P-score = 0.0000 , avg.ALOTC = 0.0
     Viennese Waltz : avg.P-score = 0.0000 , avg.ALOTC = 0.0
         Slow Waltz : avg.P-score = 0.0091 , avg.ALOTC = 0.00909090909090909


    T/4
            Cha Cha : avg.P-score = 0.0000 , avg.ALOTC = 0.0
               Jive : avg.P-score = 0.0000 , avg.ALOTC = 0.0
          Quickstep : avg.P-score = 0.0000 , avg.ALOTC = 0.0
              Rumba : avg.P-score = 0.0062 , avg.ALOTC = 0.01020408163265306
              Samba : avg.P-score = 0.5407 , avg.ALOTC = 0.6744186046511628
              Tango : avg.P-score = 0.0000 , avg.ALOTC = 0.0
     Viennese Waltz : avg.P-score = 0.0000 , avg.ALOTC = 0.0
         Slow Waltz : avg.P-score = 0.0045 , avg.ALOTC = 0.00909090909090909


## Q4 (20%): Using the ACF tempogram and repeat Q1 and Q2. What do you see? Compare the result with Q1 and Q2.
  有經過ＡＣＦ處理過後，明顯各種score都高很多，除了Waltz系列的，且Viennese Waltz還反而降低
            Cha Cha : avg.P-score = 0.9910 , avg.ALOTC = 0.4463 
                      avg.t2/t1 = 1.5547 avg.t1/gt = 0.9212 avg.t2/gt = 1.4249
               Jive : avg.P-score = 0.8333 , avg.ALOTC = 0.7694 
                      avg.t2/t1 = 1.7219 avg.t1/gt = 0.5766 avg.t2/gt = 0.9550
          Quickstep : avg.P-score = 0.0854 , avg.ALOTC = 0.0814 
                      avg.t2/t1 = 1.1772 avg.t1/gt = 0.4999 avg.t2/gt = 0.5893
              Rumba : avg.P-score = 0.8673 , avg.ALOTC = 0.3679 
                      avg.t2/t1 = 1.4911 avg.t1/gt = 1.0397 avg.t2/gt = 1.5225
              Samba : avg.P-score = 0.8721 , avg.ALOTC = 0.1670 
                      avg.t2/t1 = 1.3423 avg.t1/gt = 1.0168 avg.t2/gt = 1.3572
              Tango : avg.P-score = 1.0000 , avg.ALOTC = 0.8883 
                      avg.t2/t1 = 1.1545 avg.t1/gt = 0.9187 avg.t2/gt = 1.0389
     Viennese Waltz : avg.P-score = 0.4154 , avg.ALOTC = 0.3782 
                      avg.t2/t1 = 1.3613 avg.t1/gt = 0.6078 avg.t2/gt = 0.8079
         Slow Waltz : avg.P-score = 0.3000 , avg.ALOTC = 0.1185 
                      avg.t2/t1 = 1.2522 avg.t1/gt = 1.3324 avg.t2/gt = 1.6236
    


## Q5 (10%): Instead of using your estimated [𝑇 , 𝑇 ] in evaluation, try to use [𝑇 /2,𝑇 /2], [𝑇 /3,𝑇 /3], and [𝑇 /4,𝑇 /4]. Or, try to use [2𝑇 ,2𝑇 ], [3𝑇 ,3𝑇 ], and [4𝑇 , 4𝑇 ]. What are the resulting P-scores? Discuss the result. 

基本上使用ACF之後已經非常準確，只有在tempo算成1/2倍與2倍比較有機會產生，也就是所謂除與2和乘與2之後還剩下一點點的P-score

    
    diff = 2                               mul = 2
            Cha Cha : avg.P-score = 0.4054         Cha Cha : avg.P-score = 0.0631 
               Jive : avg.P-score = 0.0167            Jive : avg.P-score = 0.8000 
          Quickstep : avg.P-score = 0.0000       Quickstep : avg.P-score = 0.9512 
              Rumba : avg.P-score = 0.4286           Rumba : avg.P-score = 0.0102 
              Samba : avg.P-score = 0.1163           Samba : avg.P-score = 0.0000 
              Tango : avg.P-score = 0.0116           Tango : avg.P-score = 0.0116 
     Viennese Waltz : avg.P-score = 0.0000  Viennese Waltz : avg.P-score = 0.4923 
         Slow Waltz : avg.P-score = 0.3273      Slow Waltz : avg.P-score = 0.0000 
    diff = 3                               mul = 3
            Cha Cha : avg.P-score = 0.0000         Cha Cha : avg.P-score = 0.0000 
               Jive : avg.P-score = 0.0000            Jive : avg.P-score = 0.0000 
          Quickstep : avg.P-score = 0.0000       Quickstep : avg.P-score = 0.0122 
              Rumba : avg.P-score = 0.0000           Rumba : avg.P-score = 0.0000 
              Samba : avg.P-score = 0.0000           Samba : avg.P-score = 0.0000 
              Tango : avg.P-score = 0.0000           Tango : avg.P-score = 0.0000 
     Viennese Waltz : avg.P-score = 0.0000  Viennese Waltz : avg.P-score = 0.0000 
         Slow Waltz : avg.P-score = 0.0000      Slow Waltz : avg.P-score = 0.0000 
    diff = 4                               mul = 4
            Cha Cha : avg.P-score = 0.0000         Cha Cha : avg.P-score = 0.0000 
               Jive : avg.P-score = 0.0000            Jive : avg.P-score = 0.0000 
          Quickstep : avg.P-score = 0.0000       Quickstep : avg.P-score = 0.0000 
              Rumba : avg.P-score = 0.0000           Rumba : avg.P-score = 0.0000 
              Samba : avg.P-score = 0.0000           Samba : avg.P-score = 0.0000 
              Tango : avg.P-score = 0.0000           Tango : avg.P-score = 0.0000 
     Viennese Waltz : avg.P-score = 0.0000  Viennese Waltz : avg.P-score = 0.0000 
         Slow Waltz : avg.P-score = 0.0000      Slow Waltz : avg.P-score = 0.0000 
    
    


## Q6 (10%): From the above discussion, do you have any idea in improving the current algorithms using either the Fourier tempogram (Q1) or the ACF tempogram (Q4)? Please propose one tempo estimation algorithm that outperforms the current ones. (Hint: you may modify the definition of the weighting factor 𝑆1, or find some ways in combining the Fourier tempogram and the ACF tempogram.)
  經過acf的研究可以發現他所找到的tempi似乎有一定的出現規律與比重，也許可以丟入深度學習的模型試試看。
## Q7 (20%): Evaluate a beat tracking algorithm on the Ballroom dataset …
## … please compute the average F-scores of Cha Cha and Slow Waltz in the Ballroom dataset.
    ChaCha       P: 0.2435 R: 0.2701 F: 0.2561
    Slow Waltz   P: 0.2179 R: 0.3003 F: 0.2343

