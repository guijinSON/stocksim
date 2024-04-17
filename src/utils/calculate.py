from typing import List


def calculate_roi(portfolio_ratio_list, old_price_list, new_price_list):
    total_portfolio_ratio = 0
    for idx, portfolio_ratio in enumerate(portfolio_ratio_list):
        each_stock_roi = (new_price_list[idx] - old_price_list[idx]) / old_price_list[idx] * 100
        total_portfolio_ratio += each_stock_roi * portfolio_ratio / 100
    return total_portfolio_ratio


def get_stock_price_dict_by_two_list(stock_names, stock_prices):
    ret = {}
    for idx, stock_name in enumerate(stock_names):
        ret[stock_name] = stock_prices[idx]
    return ret


def calculate_new_price(stock_names: List[str], time: int, current_price: List[int], background: str):
    import torch
    import numpy as np
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    import torch.nn.functional as F
    import random

    tokenizer = AutoTokenizer.from_pretrained("amphora/KorFinASC-XLM-RoBERTa")
    model = AutoModelForSequenceClassification.from_pretrained("amphora/KorFinASC-XLM-RoBERTa")
    imap = {0: 1, 1: -1, 2: 0}

    text = "3년이 지난 후, 삼성전자는 프로메테우스를 스마트폰, 스마트 TV 등 소비자 가전 제품에 더욱 발전시켜 사용자 경험을 차별화하고, 스마트 팩토리와 스마트 시티 분야에서도 혁신을 이끌고 있습니다. 이로써 삼성전자는 글로벌 시장에서의 경쟁력을 더욱 강화하고 있습니다. SK하이닉스는 AI 옵티마이저 프로젝트를 통해 AGI 기술 개발에 집중하고 있으며, 프로메테우스의 발전을 지켜보며 상호 협력 가능성을 모색하고 있습니다. 또한, 네이버는 하이퍼클로바 X를 개발하여 사용자 경험을 혁신하고 B2B 시장 공략을 가속화하며 글로벌 시장에 진출하기 위한 계획을 세우고 있습니다. 카카오는 AI 기술 개발을 강화하기 위해 공격적인 AI 투자와 인수합병을 통해 기술력과 인재 풀을 강화하고 있습니다. 마지막으로, 한글과컴퓨터는 오피스 소프트웨어 시장에서의 변화에 대응하기 위해 전략을 재조정하고, AI 기능을 플러그인으로 개발하여 개방형 플랫폼으로 전환하고자 노력하고 있습니다. 이러한 기업들의 노력으로 AI 기술은 더욱 발전하고 혁신적인 서비스를 제공하며, 글로벌 시장에서의 경쟁력을 강화하고 있습니다. 세계는 더욱 스마트하고 혁신적인 기술로 가득한 새로운 시대로 접어들고 있습니다. 이제는 인류가 더욱 발전된 기술을 통해 더욱 편리하고 혁신적인 삶을 즐길 수 있는 시대가 열릴 것입니다."

    # price = {"삼성전자": 351100, "SK 하이닉스": 523000, "네이버": 302400, "셀바스AI": 12800, "카카오": 187100, "한글과 컴퓨터": 82900}
    price_dict = {}
    for idx, stock in enumerate(stock_names):
        price_dict[stock] = current_price[idx]

    new_price_list = []
    for k, v in price_dict.items():
        input_str = f"{background}</s> {k}"

        with torch.no_grad():
            input = tokenizer(input_str, return_tensors='pt')
            output = model(**input)

            logits = F.softmax(output.logits[0], dim=-1).numpy()
            idx = np.argmax(logits)
            new_price = ((
                                 price_dict[k] + (imap[idx] * logits[idx] * 10000 * time) + price_dict[
                             k] * random.uniform(-0.03, 0.03)
                         ) // 100) * 100
            new_price_list.append(new_price)

    return new_price_list


# if __name__ == "__main__":
#     calculate_roi([50, 50], [5000, 5000], [5500, 6000])
