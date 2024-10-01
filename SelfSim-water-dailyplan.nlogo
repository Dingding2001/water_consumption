__includes
[
  "Setup/setup-agent.nls"
  "Setup/initialization.nls"
  "Population Dynamics/education-model.nls"
  "Population Dynamics/income-model.nls"
  "Population Dynamics/birth-model.nls"
  "Population Dynamics/employ-model.nls"
  "Population Dynamics/marriage-model.nls"
  "Population Dynamics/update-relationship.nls"
  "Population Dynamics/immigration-model.nls"
  "Population Dynamics/Death-model.nls"
  "Land Use/residence-model.nls"
  "Land Use/school-model.nls"
  "Land Use/shop-model.nls"
  "Land Use/firm-model.nls"
  "Population Dynamics/daily-plan.nls"
  "Population Dynamics/network-model.nls"
  "Water Energy Consumption/water-model.nls"
  "Daily Plan/inhome-dailyplan.nls"
  "Daily Plan/inhome-time.nls"
  "Daily Plan/dailyplan-waterconsumption.nls"
  "Output Data/output.nls"
]


extensions [gis py csv profiler array table]

globals
[
  labor-current
  labor-lastyear
  Tpurchase ;threshold of purchasing a residence
  Trent ;threshold of renting a residence
  Year
  Nimm ;Number of people immigrate
  Nemi ;Number of people emigrate
  Nbirth ;Number of people born
  Ndeath ;Number of people dead
  Nmarr ;Number of married couples
  Ndivo;Number of divorced couples
  MeanIncome
  WeekdayShoppingLoc ;On weekdays, the probability that shopping occurs near work, near home, elsewhere [work/study home other]
  WeekendShoppingLoc;On weekends, the probability that shopping occurs near work, near home, elsewhere
  WeekdayLeisureLoc;On weekdays, the probability that leisure occurs near work, near home, elsewhere
  WeekendLeisureLoc;On weekends, the probability that leisure occurs near work, near home, elsewhere
  WeekdayShoppingFre ;Probability of frequency of shopping on weekdays [0 0~5 6~10 11~15]
  WeekendShoppingFre ;Probability of frequency of shopping on weekends [0 0~5 6~10 11~15]
  WeekdayLeisureFre ;Probability of frequency of leisure on weekdays [0 0~5 6~10 11~15]
  WeekendLeisureFre ;Probability of frequency of leisure on weekends [0 0~5 6~10 11~15]

  ;the farest location
  WorkDistance
  WorkDistanceProb

  ;EV market
  transaction-purchase ;annual housing transaction (purchasing)
  transaction-rent ;annual housing transaction (renting)
]

breed [people person]
breed [residences residence]
breed [schools school]
breed [firms firm]
breed [CBs CB] ;commercial building
breed [shops shop]
breed [OBs OB] ;office building
breed [facility-operators facility-operator]
breed [manufacturers manufacturer]

undirected-link-breed [couples couple]
undirected-link-breed [parents parent]
undirected-link-breed [grapas grapa]
undirected-link-breed [friends friend]
undirected-link-breed [cpurchases cpurchase] ;candidate residences to purchase
undirected-link-breed [crents crent] ;candidate residences to rent
undirected-link-breed [rents rent]
undirected-link-breed [purchases purchase]
undirected-link-breed [students student]
undirected-link-breed [employees employee]

;shopping and leisure (daily plan)
undirected-link-breed [shoppings shopping]
undirected-link-breed [leisures leisure]

undirected-link-breed [cfrents cfrent] ;candidate office building to rent
undirected-link-breed [csrents csrent] ;candidate commercial building to rent

undirected-link-breed [c2stations c2station]
undirected-link-breed [s2stations s2station]

patches-own
[
  random-n
  centroid
  ID
  Pdistrict ;district
  dem-res ;demand-residences demand of residential building in this patch (the higher the demand, the more likely to develop a new residential building
  dem-cb ;demand-residences demand of commercia in this patch (the higher the demand, the more likely to develop a new residential building
  dem-ob;demand-residences demand of commercia in this patch (the higher the demand, the more likely to develop a new residential building
]

people-own
[
  pid ;person ID
  hhd ;household ID
  relationship ;1 housholder 2 spouse of householder 3 son/daughter of householder 4 parents of householder 5 parents of spouse 6 Grandchildren of householder 7 grandparents of housholder 8 maternal grandparents of householder 9 spouse's grandparents 10 maternal grandparents of spouse 11 siblings of householder 12 other 13Daughter-in-law Son-in-law
  age
  age-group ;1-below; 2-18~24 years old; 3- years old; 4- years old; 5- years old; 6-55~64 years old; 7- above 65 years old
  gender ;0-female; 1-male gender1:2-female 1-male
  income
  income-group ;1- less than 3000; 2- 3000~4500; 3- 4500~6000; 4- 6000~8000; 5- 8000~10000; 6- 10000~15000; 7- more than 15000

  ;education related attributes
  education ;0-preschoolers 1-kindergarten 2-primary school 3-middle school 4-polytechnic school 5-high school 6-college degree7- Bachelor degree 8-from college to bachelor 9-master degree 10-PHD
  education-level ;1- high school or below; 2 college； 3 bachelor； 4 master or PHD
  edu-year ;Years of study at the current school
  edu-year-required ;Years required    preschoolers-3 years; kindergarten-3 years; primary school-6 years; middle school-3 years; high school-3 years; polytechnic school-3 years; college-3 years; from college to bachelor-2 years; master-3 years; PHD-4 years

  status ;1-students or preschoolers 2-employees 3-unemployees 4-retirees 5-wait to be allocated a school

  number ;number of family members
  hhd-income ;household income per year
  hhd-income-group ;1-less than 100000; 2- 100000~200000; 3- 200000~300000; 4- 300000~500000; 5- 500000~700000; 6- 700000~1000000; 7-more than 1000000
  license ;1-having a driving license； 0- not having a driving license
  ;traffic ;traffic expense


  ;social network attributes
  max-friend ; maximum number of friends will have
  min-friend ; minimum number of friends will have
  my-score ; a score to another person, which used to represent the extent to which the two persons will become friends

  ;residence/work and study/shopping/leisure attributes
  district ;district
  livelong ;longitude of residential location
  livelat  ;latitude of residentia
  wslong  ;longitude of work or study place
  wslat ;latitude of work or study place

  ;only for householder (people with relationship equal to 1), others' these variables equal to 0
  flexible ;number of accumulated flexible triggers
  mandatory ;mandatory trigger 0- have no mandatory trigger; 1- have mandatory trigger
  residence-size ;current residence size
  residence-cost ;current residence cost
  current-accessibility ; accessibility of current residence
  move ;determine whether move house this year


  ;distance between current/candidate residence and work/study location
  candidate-ws-dis
  current-ws-dis

  ;daily plan (leisure and shopping)
  ;frequency of shopping/leisure activities
  weekday-shopping
  weekday-leisure
  weekend-shopping
  weekend-leisure

  distance-max  ;Acceptable commuting distance

  ;inhome daily plan
  weekday-deptime ;工作日离家时间
  weekday-endtime ;工作日回家时间
  weekend-deptime ;非工作日离家时间
  weekend-endtime ;非工作日回家时间

  ;inhome activity
  weekday-inhome-activity ;1-firstbath 2-secondbath 3-breakfast 4-lunch 5-dinner 6-washclothes 7-clean 8-footbath
  weekend-inhome-activity
  firstbath-1 ;weekday [happen time | period | finish time]
  secondbath-1
  breakfast-1
  lunch-1
  dinner-1
  washclothes-1
  clean-1
  footbath-1
  firstbath-2 ;weekend [happen time | period | finish time]
  secondbath-2
  breakfast-2
  lunch-2
  dinner-2
  washclothes-2
  clean-2
  footbath-2
  dailyplan-water

  ;water consumption model
  housemover ;1代表今年搬家了，需要重新预测对每个appliance的需求

  ;infrastructures
  drinkingwater       ;小区直饮水 0没有 1有
  hotwater            ;小区集中热水  0没有 1有
  piped-natural-gas   ;管道天然气  0没有 1有
  winterheat          ;冬季市政集中供暖  0没有 1有
  summercool          ;夏季集中供冷  0没有 1有

  ;bathing-appliances
  Electric-Footbath  ;电动足浴盆  0没有 1有
  Water-heater   ;热水器型号 1即热燃气热水器 2即热电热水器 3储水热水器 4太阳能热水器 5空气能热泵 6没有 7其他  [型号 | 使用年限 | 已经使用了多少年]
  showerhead     ;淋浴喷头 1手持花洒 2头顶花洒 3侧喷花洒
  thermostatic   ;淋浴喷头是否有恒温功能 1是 2否
  Faucet         ;水龙头出水类型 1普通水龙头 2加气节水水龙头 3感应水龙头

  ;cleaning-appliances
  Dishwasher    ;洗碗机 0没有 1有  [使用年限 | 已经使用了多少年]
  sterilizer    ;消毒柜 0没有 1有
  sweeping-robot   ;吸尘器或扫地机器人 0没有 1有
  Electric-mop      ;电动拖把或蒸汽拖把 0没有 1有
  Intelligent-Toilet    ;智能马桶 0没有 1有
  Washing-machine    ;洗衣机类型 1滚筒洗衣机 2波轮洗衣机 3双缸洗衣机 4没有洗衣机
  Dry-or-sterilize    ;洗衣机是否有烘干或者消毒功能 1有烘干功能 2有消毒功能 3两种功能都有 4两种均无

  ;cooking-appliances
  pressure    ;高压力锅或电压力锅 0没有 1有
  microwave-oven    ;电磁炉或微波炉 0没有 1有
  soymilk    ;电炖锅或豆浆机或电饼铛 0没有 1有
  Ele-oven    ;电烤箱或面包机或咖啡机 0没有 1有
  Terminal-water    ;终端净水器 0没有 1有
  Kitchen-water-heat    ;厨房用热水器 0没有 1有

  ;HVAC-appliances
  radiator-bag    ;电暖水袋、暖水袋 0没有 1有

  ;bathing-behavior
  bath-style    ;洗澡方式
  Bath-fre-winter    ;冬季平均几天洗一次澡
  Bath-fre-spring    ;春秋平均几天洗一次澡
  Bath-fre-summer    ;夏季平均几天洗一次澡
  Bath-time-winter    ;冬季平均洗澡时间
  Bath-time-spring    ;春秋平均洗澡时间
  Bath-time-summer    ;夏季平均洗澡时间
  Adj-temp            ;洗澡前调整到合适水温的时间
  Water-insulation    ;热水器是否 24 小时处于保温或加热状态
  footbath-fre-winter    ;冬季平均多长时间用木盆洗脚或用电动足浴盆泡脚
  footbath-fre-spring    ;春秋平均多长时间用木盆洗脚或用电动足浴盆泡脚
  footbath-fre-summer   ;夏季平均多长时间用木盆洗脚或用电动足浴盆泡脚

  ;cooking-behavior
  cook-fire-fre    ;开火做饭的频次
  Soup-fre    ;煲汤或炖肉的频次
  Cook-Energy    ;做饭主要使用的能源类型
  Gasstove-time     ;每次做午饭或晚饭时使用燃气灶的累计时间
  bread-machine-fre     ;面包机使用情况
  ele-oven-fre     ;电烤箱使用情况
  soymilk-fre    ;豆浆机使用情况
  ele-stewpot-fre     ;电炖锅使用情况
  induction-fre    ;电磁炉使用情况
  gasstove-fre     ;燃气灶使用情况
  pressure-fre     ;电压力锅使用情况
  rice-fre     ;电饭煲使用情况
  ele-pan-fre     ;电饼铛使用情况
  sterilizer-fre    ;消毒柜使用情况
  dishes-num    ;午饭或晚饭平均几道菜

  ;cleaning-behavior
  washes-avenum    ;每种食材在开始烹饪前的平均洗涤次数
  wash-dish-method    ;洗涤餐具或锅具的方式
  Wash-hotwater       ;洗餐具或厨具时是否使用热水
  wash-time    ;洗完锅碗时间
  wash-cycle   ;洗碗遍数

  Clean-method    ;打扫方式
  Sweep-fre    ;平均扫地的频次
  Mop-fre     ;平均拖地的频次

  wash-method    ;洗衣方式
  handwash-fre-winter    ;冬季手洗衣服频次
  handwash-fre-spring    ;春秋手洗衣服频次
  handwash-fre-summer    ;夏季手洗衣服频次
  washmachine-fre-winter    ;冬季使用洗衣机频次
  washmachine-fre-spring    ;春秋使用洗衣机频次
  washmachine-fre-summer    ;夏季使用洗衣机频次
  Rinse-method   ;漂洗衣服的方式
  laundry-time  ;流水洗衣服平均需用多长时间
  Num-clothes-rinsed   ;手洗衣服会漂洗多少遍
  hotwater-laundry    ;洗衣服时是否使用热水
  Dry-sterilize    ;对衣物进行烘干消毒

  ;HVAC-behavior
  time-heatequipment-winter      ;冬季采暖设备平均每天累计使用时间

  ;水费相关的属性
  winter-consume
  spring-consume
  summer-consume
  year-consume

  family-water-winter
  family-water-spring
  family-water-summer
  family-water-year

  winter-fee;冬天每个月水费
  spring-fee;春秋每个月水费
  summer-fee;夏季每个月水费
  year-fee ;年水费

  family-winter-fee
  family-spring-fee
  family-summer-fee
  family-year-fee
]

to setup
  clear-all
  setup-python
  print "python finished"

  set year 2020

  setup-agent
  print "agent finished"
  initialization
  print "initialization finished"

  if social-network
  [
    generate-network
    print "network finished"
  ]

  generate-daily-plan
  print "daily plan finished"

  generate-appliance-needed
  print "generate water appliance finished"

  ask links [hide-link]

  export-world (word year ".csv")
  print "setup finished"

  reset-ticks
end

to setup-python
  py:setup py:python
  (py:run
    ; dbscan python packages
    "from sklearn.cluster import DBSCAN"
    "from sklearn.datasets import make_blobs"
    ; p-median python packages
    "from itertools import product"
;    "from gurobipy import *"
;    "from pulp import *"
    "import numpy as np"
    "from math import sqrt"
    "import random"
    "import matplotlib.pyplot as plt"
    "from scipy.optimize import curve_fit"
    "random.seed(0)"
    "import os"
    "from scipy.stats import gamma"
    "import pandas as pd"
    "from sklearn.ensemble import RandomForestRegressor"
    "from sklearn.ensemble import RandomForestClassifier"
    "from sklearn.multioutput import MultiOutputClassifier"
    "import subprocess"
  )
end

to go
  set labor-lastyear count people with [status = 2 or status = 3]
  set transaction-rent 0 set transaction-purchase 0
  set year year + 1
  immigration-model
  show count people with [count people with [relationship = 1 and hhd = [hhd] of myself] = 0]
  emigration-model
  ask people [set age age + 1]
  ask firms [set age age + 1]
  education-model
  employ-model
  income-model
  marriage-model
  divorce-model
  birth-model
  death-model
  if social-network [update-friend]
  residence-model
  update-inhome-time ;搬家之后要进行这一步
  firm-model
  school-model
  shop-model
  water-consumption-model
  inhome-dailyplan-model
  predict-dailyplan-water-consumption
  ask links [hide-link]
  output-data

  export-world (word year ".csv")
  tick

  print (word "Year " year " has ended.")
end

to profile
  profiler:start                                 ;; start profiling
  repeat 1 [ go ]                               ;; run something you want to measure
  profiler:stop                                  ;; stop profiling
  csv:to-file "profiler_data.csv" profiler:data  ;; save the results
  profiler:reset                                 ;; clear the data
end
@#$#@#$#@
GRAPHICS-WINDOW
525
21
1133
330
-1
-1
1.4963
1
10
1
1
1
0
0
0
1
-200
200
-100
100
1
1
1
ticks
30.0

BUTTON
77
21
143
54
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
174
21
237
54
NIL
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
23
102
212
147
Number of Schools
count schools
17
1
11

MONITOR
1190
208
1305
253
Number of firms
count firms
17
1
11

MONITOR
1166
45
1290
90
Number of people
count people
17
1
11

MONITOR
22
239
206
284
Number of residences
count residences
17
1
11

SLIDER
238
110
426
143
T-school-birth
T-school-birth
0
1
0.75
0.05
1
NIL
HORIZONTAL

SLIDER
19
165
207
198
T-school-increase
T-school-increase
0
1
0.7
0.05
1
NIL
HORIZONTAL

SLIDER
239
164
428
197
T-school-decrease
T-school-decrease
0
1
0.5
0.05
1
NIL
HORIZONTAL

SLIDER
18
478
212
511
T-rent-afford
T-rent-afford
0
1
0.6
0.01
1
NIL
HORIZONTAL

SLIDER
254
479
443
512
T-purchase-afford
T-purchase-afford
0
1
0.6
0.01
1
NIL
HORIZONTAL

MONITOR
1043
32
1100
77
Year
Year
17
1
11

SLIDER
18
538
211
571
Rent-prospect
Rent-prospect
-1000
1000
0.0
1
1
NIL
HORIZONTAL

SLIDER
254
538
444
571
Purchase-prospect
Purchase-prospect
-10
10
0.007
0.01
1
NIL
HORIZONTAL

SLIDER
1158
277
1330
310
T-firm-move
T-firm-move
0
10
2.0
1
1
NIL
HORIZONTAL

SLIDER
1376
277
1548
310
W-Move-rent
W-Move-rent
0
1
0.5
0.1
1
NIL
HORIZONTAL

SLIDER
1157
331
1329
364
W-Move-acc
W-Move-acc
-1
0
-1.0
0.1
1
NIL
HORIZONTAL

MONITOR
511
360
614
405
Number of CBs
count CBs
17
1
11

MONITOR
656
360
773
405
Number of shops
count shops
17
1
11

SLIDER
920
487
1092
520
T-shop-closure
T-shop-closure
0
100
0.0
1
1
NIL
HORIZONTAL

SLIDER
507
486
681
519
T-CB-increase
T-CB-increase
0
100
9.8
0.1
1
NIL
HORIZONTAL

SLIDER
716
486
888
519
T-CB-decrease
T-CB-decrease
0
100
2.0
1
1
NIL
HORIZONTAL

MONITOR
1329
45
1460
90
Number of couples
count couples
17
1
11

MONITOR
1494
46
1632
91
Number of students
count people with [status = 1]
17
1
11

MONITOR
1166
113
1324
158
Number of Unemployees
Count people with [status = 3]
17
1
11

MONITOR
1345
111
1489
156
Number of employees
count people with [status = 2]
17
1
11

MONITOR
1511
112
1649
157
Number of retirees
count people with [status = 4]
17
1
11

TEXTBOX
60
77
486
103
---------------------School Model-------------------------
12
0.0
1

TEXTBOX
55
215
450
233
---------------------Residence Model-------------------------
12
0.0
1

TEXTBOX
591
336
1068
355
----------------------Commercial Building and Shop----------------------
12
0.0
1

TEXTBOX
1159
179
1625
197
----------------------Office Building and Firm----------------------
12
0.0
1

MONITOR
1410
207
1513
252
Number of OBs
count OBs
17
1
11

TEXTBOX
56
598
427
650
---------------------Social Network--------------------
12
0.0
1

SLIDER
248
675
448
708
W-age
W-age
0
1
0.41
0.01
1
NIL
HORIZONTAL

SLIDER
20
674
216
707
W-gender
W-gender
0
1
0.1
0.01
1
NIL
HORIZONTAL

SLIDER
21
619
215
652
W-education
W-education
0
1
0.2
0.01
1
NIL
HORIZONTAL

SLIDER
248
619
449
652
W-income
W-income
0
1
0.24
0.01
1
NIL
HORIZONTAL

SLIDER
507
426
679
459
W-shop-rent
W-shop-rent
0
1
0.25
0.01
1
NIL
HORIZONTAL

SLIDER
716
425
888
458
W-shop-agg
W-shop-agg
0
1
0.22
0.01
1
NIL
HORIZONTAL

SLIDER
919
425
1091
458
W-shop-traffic
W-shop-traffic
0
1
0.19
0.01
1
NIL
HORIZONTAL

SLIDER
507
544
682
577
Max-CB-rent
Max-CB-rent
0
2
0.84
0.01
1
NIL
HORIZONTAL

SLIDER
715
545
887
578
Min-CB-rent
Min-CB-rent
-1
0
-0.5
0.01
1
NIL
HORIZONTAL

SLIDER
17
361
209
394
W-res-purchase-acc
W-res-purchase-acc
0
1
0.4
0.01
1
NIL
HORIZONTAL

SLIDER
251
364
439
397
W-res-purchase-price
W-res-purchase-price
0
1
0.64
0.01
1
NIL
HORIZONTAL

SLIDER
20
723
215
756
T-friend-break
T-friend-break
0
1
0.5
0.01
1
NIL
HORIZONTAL

SLIDER
1382
498
1554
531
T-OB-increase
T-OB-increase
1
5
1.97
0.01
1
NIL
HORIZONTAL

SLIDER
1159
498
1331
531
T-OB-decrease
T-OB-decrease
0
01
0.5
0.01
1
NIL
HORIZONTAL

SLIDER
1378
331
1550
364
W-move-space
W-move-space
0
1
0.55
0.01
1
NIL
HORIZONTAL

SLIDER
1158
384
1330
417
W-move-agg
W-move-agg
-1
0
-0.09
0.01
1
NIL
HORIZONTAL

SLIDER
1378
386
1550
419
W-firm-loc-agg
W-firm-loc-agg
-1
1
0.7
0.01
1
NIL
HORIZONTAL

SLIDER
1159
440
1331
473
W-firm-loc-acc
W-firm-loc-acc
0
1
0.5
0.01
1
NIL
HORIZONTAL

SLIDER
1380
442
1552
475
W-firm-loc-rent
W-firm-loc-rent
-1
0
-0.5
0.01
1
NIL
HORIZONTAL

SLIDER
1159
564
1331
597
W-growth-size
W-growth-size
-1
1
0.2
0.01
1
NIL
HORIZONTAL

SLIDER
1381
561
1553
594
W-growth-sizesq
W-growth-sizesq
-1
1
-0.05
0.01
1
NIL
HORIZONTAL

SLIDER
1159
624
1331
657
W-growth-acc
W-growth-acc
-1
0
-0.05
0.01
1
NIL
HORIZONTAL

SLIDER
1383
625
1555
658
W-growth-age
W-growth-age
-1
1
0.2
0.01
1
NIL
HORIZONTAL

SLIDER
1161
678
1333
711
T-growth-upper
T-growth-upper
0
1
0.5
0.01
1
NIL
HORIZONTAL

SLIDER
1385
681
1557
714
T-growth-lower
T-growth-lower
-1
1
-0.15
0.01
1
NIL
HORIZONTAL

SLIDER
1163
740
1335
773
T-closure
T-closure
1
2
1.2
0.01
1
NIL
HORIZONTAL

SWITCH
247
724
402
757
Social-Network
Social-Network
1
1
-1000

MONITOR
1364
733
1467
778
mean capacity
mean [capacity] of firms
17
1
11

MONITOR
1492
732
1574
777
mean staff
mean [count in-employee-neighbors] of firms
17
1
11

BUTTON
288
22
402
55
NIL
setup-python
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

PLOT
485
595
1099
890
Social Demographic Attributes
year
NIL
0.0
11.0
0.0
11.0
true
true
"" ""
PENS
"Male" 1.0 0 -16777216 true "" "plot count people with [gender = 1]"
"Female" 1.0 0 -7500403 true "" "plot count people with [gender = 0]"
"Students" 1.0 0 -2674135 true "" "plot count people with [status = 1 and age >= 3]"
"Employee" 1.0 0 -955883 true "" "plot count people with [status = 2]"
"Retiree" 1.0 0 -6459832 true "" "plot count people with [status = 4]"
"Education-HighSchool or Below" 1.0 0 -13840069 true "" "plot count people with [education <= 5]"
"Education-College" 1.0 0 -14835848 true "" "plot count people with [education = 6]"
"Education-Bachelor" 1.0 0 -11221820 true "" "plot count people with [education = 7 or education = 8]"
"Education-Master or PHD" 1.0 0 -13791810 true "" "plot count people with [education >= 9]"
"People" 1.0 0 -13345367 true "" "plot count people"
"Unemployee" 1.0 0 -8630108 true "" "plot count people with [status = 3]"
"IndividualMonthlyIncome-0~5k" 1.0 0 -1184463 true "" "plot count people with [status = 2 and income <= 5000]"
"IndividualMonthlyIncome-5~10k" 1.0 0 -10899396 true "" "plot count people with [status = 2 and income > 5000 and income <= 10000]"
"IndividualMonthlyIncome-10~15k" 1.0 0 -5825686 true "" "plot count people with [status = 2 and income > 10000 and income <= 15000]"
"IndividualMonthlyIncome-15~20k" 1.0 0 -2064490 true "" "plot count people with [status = 2 and income > 15000 and income <= 20000]"
"IndividualMonthlyIncome-Above20k" 1.0 0 -16777216 true "" "plot count people with [status = 2 and income > 20000]"
"HouseholdIncome" 1.0 0 -16777216 true "" "plot mean [hhd-income] of people with [relationship = 1]"

SLIDER
16
419
210
452
W-res-rent-acc
W-res-rent-acc
0
1
0.7
0.01
1
NIL
HORIZONTAL

SLIDER
253
420
442
453
W-res-rent-price
W-res-rent-price
0
1
0.3
0.01
1
NIL
HORIZONTAL

SLIDER
18
307
209
340
T-flexible-purchase
T-flexible-purchase
0
10
7.0
1
1
NIL
HORIZONTAL

INPUTBOX
237
235
314
295
Max-num-residences
7.0
1
0
Number

INPUTBOX
330
236
413
296
Loss
1.2
1
0
Number

SLIDER
251
308
423
341
T-flexible-rent
T-flexible-rent
0
100
1.0
1
1
NIL
HORIZONTAL

MONITOR
435
243
552
288
NIL
count purchases
17
1
11

TEXTBOX
47
780
403
798
------------------Water Consumption Model------------------
12
0.0
1

PLOT
22
800
460
1096
Water Consumption Fee
year
NIL
0.0
11.0
0.0
10.0
true
true
"" ""
PENS
"Average Water Fee" 1.0 0 -7500403 true "" "plot mean [year-fee] of people"
"Average Winter Water Fee" 1.0 0 -2674135 true "" "plot mean [winter-fee] of people"
"Average Spring or Autumn Water Fee" 1.0 0 -955883 true "" "plot mean [spring-fee] of people"
"Average Summer Water Fee" 1.0 0 -6459832 true "" "plot mean [summer-fee] of people"
"Average Family Water Fee" 1.0 0 -1184463 true "" "plot mean [family-year-fee] of people"
"Average Family Winter Water Fee" 1.0 0 -10899396 true "" "plot mean [family-winter-fee] of people"
"Average Family Spring or Autumn Water Fee" 1.0 0 -13840069 true "" "plot mean [family-spring-fee] of people"
"Average Family Summer Water Fee" 1.0 0 -14835848 true "" "plot mean [family-summer-fee] of people"

PLOT
21
1108
460
1393
Bathing Appliances
year
NIL
0.0
11.0
0.0
10.0
true
true
"" ""
PENS
"electric footbath" 1.0 0 -16777216 true "" "plot count people with [length Electric-Footbath > 0]"
"water heater-1" 1.0 0 -7500403 true "" "plot count people with [length water-heater > 0 and item 0 Water-heater = 1]"
"water heater-2" 1.0 0 -2674135 true "" "plot count people with [length water-heater > 0 and item 0 Water-heater = 2]"
"water heater-3" 1.0 0 -955883 true "" "plot count people with [length water-heater > 0 and item 0 Water-heater = 3]"
"water heater-4" 1.0 0 -6459832 true "" "plot count people with [length water-heater > 0 and item 0 Water-heater = 4]"
"water heater-5" 1.0 0 -1184463 true "" "plot count people with [length water-heater > 0 and item 0 Water-heater = 5]"
"water heater" 1.0 0 -10899396 true "" "plot count people with [length Water-heater > 0]"
"shower head-1" 1.0 0 -13840069 true "" "plot count people with [item 0 showerhead = 1]"
"shower head-2" 1.0 0 -14835848 true "" "plot count people with [item 0 showerhead = 2]"
"shower head-3" 1.0 0 -11221820 true "" "plot count people with [item 0 showerhead = 3]"
"thermostatic" 1.0 0 -13791810 true "" "plot count people with [thermostatic = 1]"
"faucet-1" 1.0 0 -13345367 true "" "plot count people with [item 0 Faucet = 1]"
"faucet-2" 1.0 0 -8630108 true "" "plot count people with [item 0 Faucet = 2]"
"faucet-3" 1.0 0 -5825686 true "" "plot count people with [item 0 Faucet = 3]"

PLOT
483
902
1099
1181
cleaning appliances
year
NIL
0.0
11.0
0.0
10.0
true
true
"" ""
PENS
"dishwasher" 1.0 0 -16777216 true "" "plot count people with [length Dishwasher > 0]\n"
"sterilizer" 1.0 0 -7500403 true "" "plot count people with [length sterilizer > 0]"
"sweeping-robot" 1.0 0 -2674135 true "" "plot count people with [length sweeping-robot > 0]"
"ele-mop" 1.0 0 -955883 true "" "plot count people with [length Electric-mop > 0]"
"intelligent-toilet" 1.0 0 -6459832 true "" "plot count people with [length intelligent-toilet > 0]"
"washmachine-1" 1.0 0 -1184463 true "" "plot count people with [length washing-machine > 0 and item 0 Washing-machine = 1]\n"
"washmachine-2" 1.0 0 -10899396 true "" "plot count people with [length washing-machine > 0 and item 0 Washing-machine = 2]"
"dry" 1.0 0 -13840069 true "" "plot count people with [Dry-or-sterilize = 1]"
"sterilize" 1.0 0 -14835848 true "" "plot count people with [Dry-or-sterilize = 2]"
"dry and sterilize" 1.0 0 -11221820 true "" "plot count people with [Dry-or-sterilize = 3]"

PLOT
485
1190
858
1393
Cooking Appliances
year
NIL
0.0
11.0
0.0
10.0
true
true
"" ""
PENS
"pressure" 1.0 0 -16777216 true "" "plot count people with [length pressure > 0]"
"microwave-oven" 1.0 0 -7500403 true "" "plot count people with [length microwave-oven > 0]"
"soymilk" 1.0 0 -2674135 true "" "plot count people with [length soymilk > 0]"
"Ele-oven" 1.0 0 -955883 true "" "plot count people with [length Ele-oven > 0]"
"Terminal-water" 1.0 0 -6459832 true "" "plot count people with [length Terminal-water > 0]"
"Kitchen-water-heat" 1.0 0 -1184463 true "" "plot count people with [length Kitchen-water-heat > 0]"

PLOT
865
1190
1102
1393
HVAV Appliances
NIL
NIL
0.0
11.0
0.0
10.0
true
true
"" ""
PENS
"radiator-bag" 1.0 0 -16777216 true "" "plot count people with [length radiator-bag > 0] "

PLOT
1126
902
1576
1182
Water Consumption
year
NIL
0.0
11.0
0.0
10.0
true
true
"" ""
PENS
"Average Winter Consume" 1.0 0 -16777216 true "" "plot mean [winter-consume] of people "
"Average Spring Consume" 1.0 0 -7500403 true "" "plot mean [spring-consume] of people "
"Average Summer Consume" 1.0 0 -2674135 true "" "plot mean [summer-consume] of people "
"Average Year Consume" 1.0 0 -955883 true "" "plot mean [year-consume] of people "
"Average Family Water Winter" 1.0 0 -6459832 true "" "plot mean [family-water-winter] of people"
"Average Family Water Spring" 1.0 0 -1184463 true "" "plot mean [family-water-spring] of people"
"Average Family Water Summer" 1.0 0 -10899396 true "" "plot mean [family-water-summer] of people"
"Average Family Water Year" 1.0 0 -13840069 true "" "plot mean [family-water-year] of people"

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
