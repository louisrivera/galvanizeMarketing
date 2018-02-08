import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('new_files/simple_model.pkl')
campus = df.campus.unique()
status = df.wk10_status.unique()

# Test
w = 4
Test = df[(df['campus']==campus[w])&(df['day of course start date c']=='2017-10-23')]
df = df[~df.isin(Test)['campus']]


Tact = np.zeros([7,26])
for p in range(0,26,1):
    for i,s in enumerate(status):
        T1 = Test['wk{}_status'.format(p)].value_counts()
        try:
            Tact[i][p] = T1[s]
        except:
            Tact[i][p] = 0


Matrices = []
for k in range(25,-1,-1):
    for c in campus:
        temp = df[df['campus']==c]
        q = np.zeros([7,7])
        for i,s1 in enumerate(status):
            for j,s2 in enumerate(status):
                q[i][j] = temp[(temp['wk{}_status'.format(k)]==s1) & (temp['wk0_status']==s2)]['campus'].count()
        q = q.T
        q = np.divide(q,q.sum(axis=0),out=np.zeros_like(q), where=q.sum(axis=0)!=0)
        Matrices.append(q)


x = range(0,26,1)
y = np.zeros(len(x))
for i in x:
    y[i] = Matrices[(w+7*i)].dot(Tact[:,-1-i])[2]

x = range(-25,1,1)

fig = plt.figure(figsize=(4,3))
ax = fig.add_subplot(111)
ax.plot(x,y)
ax.set_ylim(0,29)
ax.set_title('Location {} Projected Attendance over Time'.format(w))
ax.set_xlabel('Weeks until Course Start')
ax.set_ylabel('Projected Attendance')
plt.savefig('Test15.png',dpi=400)


if __name__ == '__main__':
    print(df.shape)
