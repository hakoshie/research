## changed name 
000711129.xlsx to 000560108.xlsx

## filenames
上から
内服　外来（院内）　性年齢別薬効分類別数量  
内服　外来（院内）　都道府県別薬効分類別数量  
内服　外来（院外）　性年齢別薬効分類別数量  
内服　外来（院外）都道府県別薬効分類別数量  
外用　性年齢別薬効分類別数量  
外用　都道府県別薬効分類別数量  

## 項目
薬価は円？
総計は処方数量に対してとられている  
https://www.mhlw.go.jp/file/06-Seisakujouhou-12400000-Hokenkyoku/0000141549.pdf

# merged files
merged_ndb just merged all time and types  
- merged_ndb  
- ndb\_kegg\_merge  
- _output_: len4\_ndb merged merged_ndb and kegg with LEFT JOIN (some duplicated rows)    
- dummy\_agg\_[blp|ndb|in\_oral\_ndb]  
- _output_: len4\_ndb\_[agg|sum] aggregated kegg data (No duplicates)    
- _output_: len4\_ndb\_blp calculated shares and so on (dropped duplicates)    
- impute_blp_len[3,4] impute lagged value for blp instruments, lagged  mean price and quantity.
\hat lagged mean price and quantity=OLS(year+C(id)) this overwrites len[3,4]\_blp  
- impute_generic_len[3,4] mainly for yakuji event, extrapolate generic_it, as for ndb event no extrapolation is performed
\hat generic_share_[r|q]\_it=Logit(year,generic_per,C(id))
only id, year, generic\_share_[r,q] is remained (release year and elasped is irrelevant).  
The output is independent from any data.
The usage is len3 for yakuji events and len4 for ndb events.

## time series  
- len[3,4]_ndb_blp_DN (blp) calculates generic_it for 8 years  
- impute_generic_len[3,4] extrapolate for 13 years and isolate the columns  
- len[3,4]_ndb_DN (event), and yakuji events  

## share of each types
calculated in dummy agg in oral ndb ipynb

## そもそも
初回2014は上位30位だったけど2回目以降は上位100位らしい

# 流れ
 (../yakuji) dummy_agg-> (../OTC) calc_otc_price -> (../ndb) dummy_agg_blp_len3 -> (../yakka) yakka firm -> (../hot) hot -> (../yakka)consolidate
 len3_ship_DN -> len3_ship_DN_blp -> len3_ndb_blp_DN -> firm -> firm_filled -> firm_FC