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

## 発売日
kegg with categoryに追加しよう、linkの行も作るか?
日付不明は15日にするか、後半はだいたいnikkei
古いやつはそのうち外されるのが多いし、そもそも入っていない？

## direct otc

2020,D08738,Rosskastanien extract,  
2014,D10748,Chaste berry extract,

## データの順番

- "approved_ingredients_kegg.csv","kegg_ja.csv"
- scrape
- "kegg_with_category.csv" <-ここに手動追加した
- id_split
- "kegg_w_cate_split.csv"
- id_shorten(ここでmeltしているので重要)
- "ingre_cate_len[234].csv"

# 流れ
# 流れ
 (../yakuji) dummy_agg-> (../OTC) calc_otc_price -> (../ndb) dummy_agg_blp_len3 -> (../yakka) yakka firm -> (../hot) hot -> (../yakka)consolidate
 len3_ship_DN -> len3_ship_DN_blp -> len3_ndb_blp_DN -> firm -> firm_filled -> firm_FC



