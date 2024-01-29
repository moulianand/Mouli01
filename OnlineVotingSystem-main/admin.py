import pandas as pd
from pathlib import Path
from flask import jsonify
path = Path("E:\online_project\OnlineVotingSystem-main\static\database")

# Admin login authentication
def log_admin(admin_ID,password):

    if(admin_ID=="Admin" and password=="admin"):
        return True
    else:
        return False
    
# get party names
def get_partyNames():
    data = pd.read_csv (path/'cand_list.csv')
    pnames = sorted(data['Party_Name'].unique())
    return pnames

# get canidate names
def get_candNames():
    data = pd.read_csv (path/'cand_list.csv')
    cnames = sorted(data['Cand_Name'].unique())
    return cnames

# get city
def get_city():
    data = pd.read_csv (path/'cand_list.csv')
    cities = sorted(data['City'].unique())
    return cities

# get zone
def get_zone():
    data = pd.read_csv (path/'cand_list.csv')
    zones = sorted(data['Zone'].unique())
    return zones

# register candidate
def taking_data_candidate(pname,cname,gender,city,zone):
    
    df = pd.DataFrame({"Party_Name":[pname],
                "Cand_Name":[cname],
                "Gender":[gender],
                "City":[city],
                "Zone":[zone],
                "VoteCount":[0]},)
    df = df.reset_index()
    df.to_csv(path/'cand_list.csv',mode='a',index=False, header=False)
    return True

# show results
def show_result():
    df=pd.read_csv (path/'cand_list.csv')
    df=df[['Party_Name','Cand_Name','City','Zone','VoteCount']]
    v_cnt = []
    for index, row in df.iterrows():
        rec={}
        rec["Party_Name"]=df['Party_Name'].iloc[index]
        rec["Cand_Name"]=df['Cand_Name'].iloc[index]
        rec["City"]=df['City'].iloc[index]
        rec["Zone"]=df['Zone'].iloc[index]
        rec["VoteCount"]=df['VoteCount'].iloc[index]
        v_cnt.append(rec)
    print(v_cnt)
    return v_cnt

# reset all
def count_reset():
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Zone','City','Number','hasVoted']]
    for index,row in df.iterrows():
        df['hasVoted'].iloc[index]=int(0)
    df.to_csv(path/'voterList.csv')

    df=pd.read_csv(path/'cand_list.csv')
    df=df[['Party_Name','Cand_Name','Gender','City','Zone','VoteCount']]
    for index, row in df.iterrows():
        df['VoteCount'].iloc[index]=int(0)
    df.to_csv(path/'cand_list.csv')
    return True
show_result()