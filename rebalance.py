import sympy
import web3
import json

w3 = web3.Web3(web3.HTTPProvider("http://localhost:8545"))

f = open("abi.json")
f2 = open("delta_neutral_abi.json")
abi = json.load(f)
delta_neutral_abi = json.load(f2)

Xglp, Xsbtc, Xseth, Pglp, Psbtc, Pseth, Lglpbtc, Aglpbtc, Lglpeth, Aglpeth, Lsbtc, Asbtc, Lseth, Aseth, t = sympy.symbols("Xglp Xsbtc Xseth Pglp Psbtc Pseth Lglpbtc Aglpbtc Lglpeth Aglpeth Lsbtc Asbtc Lseth Aseth t")

glp_btc_equation = sympy.Eq(0.96 * Xglp * 1 * 0.18, 0.57 * Xsbtc * 3 * 1)
btc_equation = sympy.Eq(0.96 * Xglp * 1 * 0.34, 0.16 * Xseth * 3 * 1)
eth_equation = sympy.Eq(0.96 * Xglp + 0.57 * Xsbtc + 0.16 * Xseth, 1000)

def f(eq_lst):
    """
    Solves equations in eq_lst for x, substitutes values from values_dct, 
    and returns value of x.

    :param x: Sympy symbol
    :param values_dct: Dict with sympy symbols as keys, and numbers as values.
    """

    try:
        return list(sympy.linsolve(eq_lst, Xglp, Xsbtc, Xseth))[0]
    except IndexError:
        print('This equation has no solutions.')



from flask import Flask

app = Flask(__name__)

delta_neutral_rebalancer = w3.eth.contract(address="0x4826533B4897376654Bb4d4AD88B7faFD0C98528", abi=delta_neutral_abi)

@app.route("/rebalance")
def rebalance():
    r = f(eq_lst=[glp_btc_equation, btc_equation, eth_equation])
    position_managers = [
        (w3.eth.contract(address="0x8f86403A4DE0BB5791fa46B8e795C547942fE4Cf", abi=abi), int(r[0])),
        (w3.eth.contract(address="0x99bbA657f2BbC93c02D617f8bA121cB8Fc104Acf", abi=abi), int(r[1])),
        (w3.eth.contract(address="0x0E801D84Fa97b50751Dbf25036d067dCf18858bF", abi=abi), int(r[2]))
    ]
    
    rebalance_queue = []

    for position_manager, usdcAmount in position_managers:
        rebalance_action = position_manager.functions.getRebalanceAction(usdcAmount).call() 

        rebalance_queue.append((
            {
                "positionManager": position_manager,
                "usdcAmountToHave": usdcAmount
            }, rebalance_action))

    rebalance_queue.sort(key=lambda q: q[1], reverse=True)

    rebalance_queue_data = list(map(get_rebalance_queue_data, rebalance_queue))
    print(rebalance_queue_data)

    delta_neutral_rebalancer.functions.rebalance(rebalance_queue_data).transact();
    
    return str(r)

def get_rebalance_queue_data(d):
    position_manager = d[0]["positionManager"]
    return {
        "positionManager": position_manager.address,
        "usdcAmountToHave": int(d[0]["usdcAmountToHave"] * (position_manager.functions.price().call() / (1*10**6)))
    };
    