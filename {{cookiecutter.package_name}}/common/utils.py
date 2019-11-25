import importlib
from decimal import Decimal
import pickle
import pandas as pd
from enum import Enum
import json
from common.mixins import DictMixin
from common.errors import DataRetrievalFailureException

# is_dump = True
is_dump = False


def custom_round(number, round_type='integer'):
    if round_type == 'integer':
        return float(Decimal(number).quantize(Decimal('0')))
    elif round_type == 'percentage':
        return float(Decimal(number).quantize(Decimal('0.00')))
    elif round_type == 'ultra_percentage':
        return float(Decimal(number).quantize(Decimal('0.0000')))


def dump_pickle(data, file_path):
    if is_dump:
        with open(file_path, "wb") as f:
            pickle.dump(data, f)


def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data


def get_instance_of_attr(path):
    module, function = path.rsplit('.', maxsplit=1)
    module_instance = importlib.import_module(module)
    if hasattr(module_instance, function):
        return getattr(module_instance, function)
    else:
        raise AttributeError


class RiskType(Enum):
    CUSTOMIZE = 0  # 自定义
    CONSERVATIVE = 1  # 保守
    STEADY = 2  # 稳健
    RADICAL = 3  # 激进


class CashType(Enum):
    MONETARY_FUND = 1  # 货币基金
    MATURE_FINANCIAL = 2  # 到期理财
    OTHER_INCOME = 3  # 其他收入
    INVESTMENT_EXPENSES = 4  # 投资支出
    OTHER_EXPENSES = 5  # 其他支出


class PaymentType(Enum):
    PRINCIPAL_INTEREST = 1  # 等额本息
    AVERAGE_CAPITAL = 2  # 等额本金
    DEBT_SERVICE = 3  # 到期一次还本付息


class FrequenceType(Enum):
    MONTH = 1
    SEASON = 3
    YEAR = 12


class ProductType(Enum):
    LOAN = 1
    STRUCTURED = 2
    REGULAR_FINANCIAL = 3
    MONETARY_FUND = 4
    OPEN_FUND = 5


class Utils(object):
    """
    convert recordscollection to dataframe
    """

    @staticmethod
    def get_dataframe(res):
        df = pd.DataFrame([DictMixin.to_dict(i.as_dict()) for i in res])
        return df

    """
    convert pandas dataframe to python list
    """

    @staticmethod
    def to_pylist(dataframe):
        columns = dataframe.columns.values.tolist()
        data_source = []
        for index, row in dataframe.iterrows():
            dic = {}
            for column in columns:
                dic[column] = row[column]
            data_source.append(dic)
        return data_source

    @staticmethod
    def dataframe2json(df):
        return json.loads(df.to_json(orient='records'))

    @staticmethod
    def json2dataframe(json_data):
        return pd.read_json(json.dumps(json_data), orient='records')

    @staticmethod
    def fill_df_nan(dataframe):
        # fill the nan value with none for json
        dataframe = dataframe.where(pd.notnull(dataframe), None)
