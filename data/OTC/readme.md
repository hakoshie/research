## 手動追加
to kegg with category.csv

- フルニソリド  1329 https://www.plamedplus.co.jp/ing/pdf/gn520.pdf,  
２００６年くらいで医療用では販売中止https://medical.nikkeibp.co.jp/leaf/mem/pub/di/trend/201811/558505.html  


- アミノプロフェン 1149 https://www.plamedplus.co.jp/ing/pdf/gn066.pdf  
2008年に販売中止
https://gooday.nikkei.co.jp/atcl/column/14/091100015/111100002/

- オキシメタゾリン塩酸塩 139 or 1324こっちを採用
https://s3-ap-northeast-1.amazonaws.com/medley-medicine/prescriptionpdf/300089_1324700Q1035_1_05.pdf,  
https://www.mhlw.go.jp/topics/2020/04/dl/tp20201118-01_03.pdf

あと、日本標準商品分類番号の下４桁が薬効分類番号に対応するらしい。

## direct otc

2020,D08738,Rosskastanien extract,  
2014,D10748,Chaste berry extract,

## データの順番

- "approved_ingredients_kegg.csv"
- scrape
- "kegg_with_category.csv" <-ここに追加した
- id_split
- "kegg_w_cate_split.csv"
- id_shorten(ここでmeltしているので重要)
- "ingre_cate_len[234].csv"





