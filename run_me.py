import pandas as pd
merged = pd.read_csv("cluster_data/cluster_BTX_2S_comb.csv",index_col = "time",low_memory = False)

import library.agents.distAgentsWIP2, library.simulations2, library.agents.baseAgents, library.market_modelsM


UCBc = 200
n_trades = 100
C = 50
n_hist_data = 64
lr = 0.00005
state_size = 2


params = {
    "terminal" : 1,
    "num_trades" : n_trades,
    "position" : 1,
    "batch_size" : 64,
    "action_values" : [0.99,1,1.01]
}

qrdqn = library.agents.distAgentsWIP2.QRAgent(state_size, params["action_values"], f"100T100 QRDQN3 BTX2 R",C=C, N=200,alternative_target = True,UCB=True,UCBc = UCBc,tree_horizon = n_trades,n_hist_data=n_hist_data,n_hist_inputs=4,orderbook =False)
agent = qrdqn

agent.learning_rate = lr

agent.expected_range = 0.002
agent.expected_mean = 0.99

stock = library.market_modelsM.real_stock(merged,n_steps=n_trades,n_train=30)
market = library.market_modelsM.market(stock,n_hist_data)
market.k = 0.01 / params["position"]
market.b = 0.05

my_simulator = library.simulations2.simulator(market,agent,params,test_name = "MOMD2",orderbook = False)
my_simulator.train(10000,epsilon_decay =0.9999)



