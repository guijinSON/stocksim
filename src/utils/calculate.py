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
            diff = (imap[idx] * logits[idx] * 10000 * time * 0.3) + price_dict[k] * random.uniform(-0.03, 0.03)
            print(k, price_dict[k], diff)
            # NOTE: diff의 감소 폭이 기존 가격보다 큰 경우
            if price_dict[k] <= -diff:
                diff *= 0.5
            if price_dict[k] * 1.2 <= -diff:
                diff *= 0.2
            if price_dict[k] * 1.5 <= -diff:
                diff *= 0.1
            new_price = ((price_dict[k] + diff) // 100) * 100
            new_price_list.append(new_price)
    return new_price_list


def calculate_revenue(old_investment, new_investment):
    return round((new_investment - old_investment) / old_investment * 100, 2)


def format_number_with_commas(number: str):
    return format(number, ",")

# if __name__ == "__main__":
#     calculate_roi([50, 50], [5000, 5000], [5500, 6000])
# if __name__ == "__main__":
#     calculate_new_price(
#         background="삼성전자는 프로메테우스 프로젝트를 통해 AI 분야에서 기술력을 입증했지만 최근 적자폭이 확대되고 있으며, SK하이닉스는 AI 옵티마이저 프로젝트를 통해 AGI 기술 개발에 집중하고 있지만 임금 체불 문제로 인해 생산 효율성이 저하되고 있습니다. 네이버는 하이퍼클로바 X를 개발하여 프로메테우기술에 투자했으나 대형 파트너들의 전략적 파트너십으로 뒤처지기 시작했습니다. 한글과컴퓨터는 프로메테우스 AGI의 부상으로 오피스 소프트웨어 시장에서의 변화에 대응하기 위해 전략을 재조정하고 있습니다.",
#         stock_names=["삼성전자", "SK하이닉스", "네이버", "카카오", "셀바스AI", "한글과컴퓨터"],
#         current_price=[351100, 523000, 302400, 12800, 187100, 82900],
#         time=55,
#     )
