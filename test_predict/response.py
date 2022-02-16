import pandas as pd
import json
from .azureml_endpoint import predict_rent

def create_response(req_body):
    # 駅、地価、地理情報の読み込み
    station_list = pd.read_csv("./test_predict/station.csv")
    landprice = pd.read_csv("./test_predict/landprice.csv")
    location = pd.read_csv("./test_predict/location.csv")
    
    # 指定された電車乗車時間に合致した駅を抽出
    col_name = "traintime"
    traintime = req_body[col_name]
    stations =station_list[station_list[col_name] == traintime]
    
    # リクエストボディをDataframe化し、駅、地価、地理情報と結合
    df = pd.DataFrame.from_dict(req_body, orient='index').T
    df = pd.merge(df,stations,on="traintime")
    df = pd.merge(df,location,on="name")
    df = pd.merge(df,landprice,on="ward")   

    # 予測用のDataframeを作成
    drop_cols = ["ward","name","traintime"]
    pred_df = df.drop(drop_cols,axis=1)
    pred_dict  = pred_df.to_dict(orient='records')
    pred_result  = predict_rent(pred_dict)
    pred_result = pd.DataFrame.from_dict(pred_result, orient='index').T

    # レスポンス用のDataframeを作成
    res_cols = ["area","name"]
    res_df = df[res_cols]
    res_df = pd.concat([res_df,pred_result],axis=1)
    
    res_df["area"] = res_df["area"]*10+5
    res_df["rent"] = res_df["area"]*res_df["Results"].astype(int)
    res_df["subsidy"] = res_df["rent"].apply(lambda x : 25000 if x <= 100000 else 30000)
    
    drop_cols = ["area","Results"]
    res_df.drop(drop_cols,axis=1,inplace=True)
    
    # Dataframe→JSONの変換
    res_df = res_df.reset_index(drop=True)
    # res_json = res_df.to_json(force_ascii=False,orient='records')
    res_json = res_df.to_json(force_ascii=False,orient='index')
    return res_json