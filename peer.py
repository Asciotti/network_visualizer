import requests
import networkx as nx
import matplotlib.pyplot as plt

peers = {}
G = nx.Graph()

origin = '104.25.221.25'

headers = {'API-Version': '1'}

def get_peers(hub):
    '''
    Given hub (aka str containing IP) gets the peers on it's peer list
    and adds to master list
    '''
    url = f'http://{hub}:{4001}/api/peers'
    try:
        raw_list = requests.get(url, headers=headers, timeout=0.25)
    except:
        return
    peer_list = raw_list.json()['peers']
    for peer in peer_list:
            peers.setdefault(hub, [])
            peers[hub].append((peer['ip'], peer['height']))


# Get initial node network
r = requests.get('https://explorer.ark.io:8443/api/peers', headers=headers)
peer_list = r.json()['peers']
for peer in peer_list:
    peers.setdefault(origin, [])
    peers[origin].append((peer['ip'], peer['height']))

print('Making temp list of peers')
temp_peers = []
# Get additonal list of nodes for network
for hub in peers:
    for ip, height in peers[hub]:
        temp_peers.append(ip)

print('Crawl out one step of the network')
# Crawl out another step
num_peers = len(temp_peers)
for idx, peer in enumerate(temp_peers):
    if idx%int(num_peers/10) == 0:
        print(f'Parsed {idx}/{num_peers} of the peers')
    get_peers(peer)

for hub in peers:
    for node in peers[hub]:
        G.add_edge(hub, node[0])


pos = nx.spring_layout(G,k=0.95,iterations=20)
nx.draw_shell(G, with_labels=False)

plt.show()