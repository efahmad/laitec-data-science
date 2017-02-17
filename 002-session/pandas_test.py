import pandas as pan
import os
import matplotlib.pyplot as plt

data = pan.read_csv(os.path.join(os.path.dirname(__file__), "movie_metadata.csv"))
likes = [
    (name, sum(data['actor_1_facebook_likes'][data['actor_1_name'] == name].values)) for name in
    data['actor_1_name'].unique()
    ]

likes = sorted(likes, key=lambda l: l[1], reverse=True)[:10]

x = [item for item in range(len(likes))]
y = [item[1] for item in likes]

plt.bar(x, y)
plt.xticks(x, [item[0] for item in likes])
# print([item[0] for item in likes])
plt.show()
