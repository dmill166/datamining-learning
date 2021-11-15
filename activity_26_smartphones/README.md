# Activity 26

## Smartphones Cluster Analysis

The goal of this activity is to perform a data analysis aiming to group together smartphones that have similar specs.

## Dataset 

The dataset for this report was created from information available [https://www.productchart.com/smartphones/](https://www.productchart.com/smartphones/). For each smartphone, the referred website maintains the following specs (among others):  

* screen size (in inches)
* screen resolution (in pixels x pixels) 
* storage (in GB)
* ram (in GB) 
* clock speed (in GHz)
* number of cores
* weight (in ounces)
* rear camera resolution (in MP)
* front camera resolution (in MP)
* battery (in mah)
* price (in US$)

## Instructions

Create a jupyter notebook with the following sections. 

* Preamble
* Introduction 
* Dataset
* Pre-processing (remove data records that have missing values or smartphones where it is not clear how many cores their cpus have; perform basic transformations, like string to float/int, column splitting, data extraction, and normalization)
* Cluster Analysis (apply k-means to identify 4 cluster of smartphones from the crafted dataset)

After the pre-processing, the dataset should have the following fields:

* price (float)
* screen_size (float)
* storage (float)
* ram (float)
* weight (float)
* screen_width (int)
* screen_height (int)
* rear_camera (float)
* front_camera (float)
* battery (float)
* cores (int)

After you have finished running k-means, identify the dataframe indices per cluster. For example: 

```
0: [ 1 4 6 9 10 14 17 18 21 25 28 35 36 38 40 42 43 44 53 54 55 56 60 62 63 65 66 68 69 78 80 85 87 88 92 93 95 96 97 112 113 114 116 119 120 121 127 130 134 138 141 143 148 152 156 166 167 170 177 178 184 194 200 218 224 229 240 253 257 262 ]
1: [ 3 7 15 24 31 32 39 45 46 51 58 61 64 70 76 77 81 90 99 100 109 115 124 125 131 140 155 158 162 163 168 173 174 176 183 186 191 198 201 204 206 212 215 216 217 227 231 237 238 243 246 255 ]
2: [ 0 2 11 12 13 20 27 29 30 33 37 48 50 72 73 74 79 102 103 111 135 139 142 153 195 219 230 236 245 251 252 254 ]
3: [ 5 8 16 19 22 23 26 34 41 47 49 52 57 59 67 71 75 82 83 84 86 89 91 94 98 101 104 105 106 107 108 110 117 118 122 123 126 128 129 132 133 136 137 144 145 146 147 149 150 151 154 157 159 160 161 164 165 169 171 172 175 179 180 181 182 185 187 188 189 190 192 193 196 197 199 202 203 205 207 208 209 210 211 213 214 220 221 222 223 225 226 228 232 233 234 235 239 241 242 244 247 248 249 250 256 258 259 260 261 ]
```

In your conclusions, try to identify what do phones in each cluster have in common. Drawing boxplot of features per cluster might be helpful. 

