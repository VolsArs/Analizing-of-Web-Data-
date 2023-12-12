import requests
import networkx
import time
import collections
import vk

#51811986

#Z3nqjnfiMzezwilRh27k
#de81917cde81917cde81917c21dd9707eedde81de81917cbbf4effba041da4608780477
# session = vk.session(access_token='Z3nqjnfiMzezwilRh27k')
# session = vk.session
# vk_api = vk.API(session)
# user = vk_api.users.get(user_id=1)
# print(user)

def get_friends_ids(user_id):
    friends_url = 'https://api.vk.com/method/friends.get?user_ids=154037572&fields=bdate&access_token=de81917cde81917cde81917c21dd9707eedde81de81917cbbf4eff&v=5.131 HTTP/1.1'
    # также вы можете добавить access_token в запрос, получив его через OAuth 2.0
    json_response = requests.get(friends_url.format(user_id)).json()
    if json_response.get('error'):
        print( json_response.get('error'))
        return list()
    return json_response[u'response']


graph = {}
friend_ids = get_friends_ids(154037572)  # ваш user id, для которого вы хотите построить граф друзей.
for friend_id in friend_ids:
    print ('Processing id: ', friend_id)
    graph[friend_id] = get_friends_ids(friend_id)

g = networkx.Graph(directed=False)
for i in graph:
    g.add_node(i)
    for j in graph[i]:
        if i != j and i in friend_ids and j in friend_ids:
            g.add_edge(i, j)

pos=networkx.graphviz_layout(g,prog="neato")
networkx.draw(g, pos, node_size=30, with_labels=False, width=0.2)

get_friends_ids(154037572)