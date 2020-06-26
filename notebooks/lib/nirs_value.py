# NIRS加算平均時系列グラフ
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Lis = [] #条件数zave保存
S = 1  #被験者数
jouken = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']    #条件

N = 1   #被験者開始番号
M = S + 1   #被験者終わり番号+1
u = 0   #Lisインデックス

#
rest_dur = 45   #レスト時間[s]
task_dur = 30   #タスク時間[s]
all_dur = rest_dur + task_dur + rest_dur
T = 0.15    #サンプリングレート [s]
Hz = 1 / T  #[Hz]

# データ読み込み
data_path = 'kozawa_1212.TXT'
NAMES = ['Time(sec)', 'Task', 'Mark', 'Count',
        'oxyHb1', 'deoxyHb1', 'totalHb1',
        'oxyHb2', 'deoxyHb2', 'totalHb2',
        'oxyHb3', 'deoxyHb3', 'totalHb3',
        'oxyHb4', 'deoxyHb4', 'totalHb4',
        'oxyHb5', 'deoxyHb5', 'totalHb5',
        'oxyHb6', 'deoxyHb6', 'totalHb6',
        'oxyHb7', 'deoxyHb7', 'totalHb7',
        'oxyHb8', 'deoxyHb8', 'totalHb8',
        'oxyHb9', 'deoxyHb9', 'totalHb9',
        'oxyHb10', 'deoxyHb10', 'totalHb10',
        'oxyHb11', 'deoxyHb11', 'totalHb11',
        'oxyHb12', 'deoxyHb12', 'totalHb12',
        'oxyHb13', 'deoxyHb13', 'totalHb13',
        'oxyHb14', 'deoxyHb14', 'totalHb14',
        'oxyHb15', 'deoxyHb15', 'totalHb15', 
        'oxyHb16', 'deoxyHb16', 'totalHb16',
        'oxyHb17', 'deoxyHb17', 'totalHb17',
        'oxyHb18', 'deoxyHb18', 'totalHb18',
        'oxyHb19', 'deoxyHb19', 'totalHb19',
        'oxyHb20', 'deoxyHb20', 'totalHb20',
        'oxyHb21', 'deoxyHb21', 'totalHb21',
        'oxyHb22', 'deoxyHb22', 'totalHb22']
df = pd.read_table(data_path, names=NAMES)[36:]
df = df.reset_index(drop=True)  #インデックスのリセット
df = df.astype('float')   #strと数値が混合していたのでfloatに統一

#タスク切り替え位置を探索
task_idx = []
idx = 0
task = df['Count'][0]
for c in df['Count']:
    if c != task:
        task_idx.append(idx)
        task = c
    idx += 1

#'Count'の値
count = []
for i in task_idx:
    count.append(df['Count'][i])

#タスク間のデータ数
length = []
for j in range(len(task_idx)):
    if j==0:
        length.append(task_idx[j])
    else:
        length.append(task_idx[j]-task_idx[j-1])

df_mark = pd.DataFrame({'idx':task_idx, 'Count':count, 'length':length})

# zscoreを計算する関数
def zscore(df, task_idx, rest_dur, task_dur):
    Lis = []
    #numpy配列に変換
    dataT = np.array(df, dtype=np.float32)

    for n in range(len(task_idx)):
        #前レスト中の平均値、標準誤差の計算
        rest = dataT[task_idx[n]:(task_idx[n] + int(rest_dur / T)), 4:]
        ave = np.average(rest, axis=0)  #chごとに平均値を算出
        std = np.std(rest, axis=0)  #chごとに標準偏差を算出

        #タスク中のZscore
        zdataT = (dataT[(task_idx[n] + int(rest_dur / T)):(task_idx[n] + int((rest_dur+task_dur) / T)), 4:] - ave) / std

        Lis.append(zdataT)

    return Lis

df_oxy = df.loc[:,['Time(sec)', 'Task', 'Mark', 'Count',
        'oxyHb1', 'oxyHb2', 'oxyHb3', 'oxyHb4',
        'oxyHb5', 'oxyHb6', 'oxyHb7', 'oxyHb8',
        'oxyHb9', 'oxyHb10', 'oxyHb11', 'oxyHb12',
        'oxyHb13', 'oxyHb14', 'oxyHb15', 'oxyHb16',
        'oxyHb17', 'oxyHb18', 'oxyHb19', 'oxyHb20',
        'oxyHb21', 'oxyHb22']]

# df_deoxy = df.loc[:,['Time(sec)', 'Task', 'Mark', 'Count',
#         'deoxyHb1', 'deoxyHb2', 'deoxyHb3', 'deoxyHb4',
#         'deoxyHb5', 'deoxyHb6', 'deoxyHb7', 'deoxyHb8',
#         'deoxyHb9', 'deoxyHb10', 'deoxyHb11', 'deoxyHb12',
#         'deoxyHb13', 'deoxyHb14', 'deoxyHb15', 'deoxyHb16',
#         'deoxyHb17', 'deoxyHb18', 'deoxyHb19', 'deoxyHb20',
#         'deoxyHb21', 'deoxyHb22']]

# df_total = df.loc[:,['Time(sec)', 'Task', 'Mark', 'Count',
#         'totalHb1', 'totalHb2', 'totalHb3', 'totalHb4',
#         'totalHb5', 'totalHb6', 'totalHb7', 'totalHb8',
#         'totalHb9', 'totalHb10', 'totalHb11', 'totalHb12',
#         'totalHb13', 'totalHb14', 'totalHb15', 'totalHb16',
#         'totalHb17', 'totalHb18', 'totalHb19', 'totalHb20',
#         'totalHb21', 'totalHb22']]

Lis_oxy = zscore(df_oxy, task_idx, rest_dur, task_dur)
# Lis_deoxy = zscore(df_deoxy, task_idx, rest_dur, task_dur)
# Lis_total = zscore(df_total, task_idx, rest_dur, task_dur)

# タスク中の平均値を求める関数
def Zave(task_idx, Lis_oxy, rest_dur, task_dur):
    Zave = pd.DataFrame(np.zeros((len(task_idx), 23)),
                        columns=['task',
                                'ch1', 'ch2', 'ch3', 'ch4', 'ch5',
                                'ch6', 'ch7', 'ch8', 'ch9', 'ch10',
                                'ch11', 'ch12', 'ch13', 'ch14', 'ch15',
                                'ch16', 'ch17', 'ch18', 'ch19', 'ch20',
                                'ch21', 'ch22'])
    for g in range(len(task_idx)):
        Zave.loc[g, ['task']] = g + 1
        for m in range(22):
            Zave.loc[g, ['ch'+str(m+1)]] = np.average(np.array(Lis_oxy[g][:, m]))
            # Zave.loc[g, m+1] = np.average(np.array(Lis_oxy[g][:, m]))

    return Zave

oxyZave = Zave(task_idx, Lis_oxy, rest_dur, task_dur)

# # CSV保存
save_path = "task_oxy.csv"
oxyZave.to_csv(save_path)




# print(oxyZave.head())
