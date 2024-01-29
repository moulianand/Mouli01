from twilio.rest import Client
import random
import pandas as pd
from pathlib import Path

path = Path("E:\online_project\OnlineVotingSystem-main\static\database")

# voter id verification
def verify(vid):
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','hasVoted']]
    for index, row in df.iterrows():
        # print("verification")
        try:
            if int(df['voter_id'].iloc[index])==int(vid):
                print('verified')
                return True
        except:
            continue
    return False

def isEligible(vid):
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Number','hasVoted']]
    for index, row in df.iterrows():
        # print('eligibility')
        try:
            if int(df['voter_id'].iloc[index])==int(vid) and int(df['hasVoted'].iloc[index])==int(0):
                print('eligible')
                print(int(df['Number'].iloc[index]))
                return True
        except:
            continue
    return False

def log_server(voter_ID):
    if(verify(voter_ID)==True and isEligible(voter_ID)==True):
        message = "valid voter"
        
    elif(verify(voter_ID)==False):
        message = "Invalid Voter"

    elif(isEligible(voter_ID)==False):
        message = "Vote has Already been Cast"  

    else:
        message = "Server Error"
    return message    


# otp verification
def getNum(vid):
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Number','hasVoted']]
    for index, row in df.iterrows():
        if int(df['voter_id'].iloc[index])==int(vid):
            return int(df['Number'].iloc[index])
    return False


def OTP():
    return random.randrange(100000,1000000)

def checkOTP(otpInput,genOtp):
    try:
        if int(otpInput) == int(genOtp):
            message = "Verification Successful"
        else:
            message ="Wrong OTP"
    except:
        message = "Invalid OTP"
    return message

def otpGen(vid):
    genOtp = str(OTP())
    print('otp sent')
    phoneNum=getNum(vid)
    print(phoneNum)
    client = Client("[Credential]", "[AuthToken]")
    client.messages.create(to =("[your_number]"),
                        from_ ="[twilio_number]",
                        body = genOtp)
    return genOtp


# vote cast
def vote_update(st,vid):
    df=pd.read_csv (path/'cand_list.csv')
    df=df[['Party_Name','Cand_Name','Gender','City','Zone','VoteCount']]
    for index, row in df.iterrows():
        if df['Party_Name'].iloc[index]==st:
            df['VoteCount'].iloc[index]+=1
            print('Updated')
    df.to_csv (path/'cand_list.csv')

    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Zone','City','Number','hasVoted']]
    for index, row in df.iterrows():
        if int(df['voter_id'].iloc[index])==int(vid):
            df['hasVoted'].iloc[index]=int(1)
            print('Updated')
    df.to_csv(path/'voterList.csv')
    return True
