## prodのcolumn
輸入x:主成分(国内<海外)  
輸入star:ほぼ完全輸入
[rx|otc]_agg: 国内＋輸入x+輸入star
[rx|otc]_pro_agg:国内+輸入x
[rx|otc]_pro_dom:国内

## dummy_agg
merge imputed generic_share_it from NDB and generic_per_t from government office pdf
and calculates elapsed times

## 流れ
whole -> yakuji_kegg_merge -> len[3,4]_[ship|prod]  -> dummy_agg (merge ndb_impute_generic)-> drop_never

## for production data
merged with ship data in the kegg merge program