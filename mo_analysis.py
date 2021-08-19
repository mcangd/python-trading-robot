import numpy as np
import pandas as pd

from typing import Any
from typing import Dict

from pyrobot.stock_frame import StockFrame

class mo_analysis():
    
    """ 
    Represents an mo_analysis Object which can be used to caluclate certain linear regression based technical indicators to a StockFrame. 
    """

    def __init__(self, price_data_frame: StockFrame) -> None:
        
        """
        Initializes the mo_analysis client
        
        Arguments: 
        ----
        price_data_frame {pyrobot.StockFrame} -- The price data frame which is used to add indicators to.
            At a minimum this data frame must have the following columns: `['timestamp','close','open','high','low']`.

        Usage:
        ----
            >>> historical_prices_df = trading_robot.grab_historical_prices(
                start=start_date,
                end=end_date,
                bar_size=1,
                bar_type='minute'
            )
            >>> price_data_frame = pd.DataFrame(data=historical_prices)
            >>> mo_analysis_client = mo_analysis(price_data_frame=price_data_frame)
            >>> mo_analysis_client.price_data_frame
        
        """

        self._stock_frame: StockFrame = price_data_frame
        self._price_groups = price_data_frame.symbol_groups
        self._current_mo_analysis = {}
        self._mo_analysis_signals = {}
        self._frame = self._stock_frame.frame

        self._mo_analysis_comp_key = []
        self._mo_analysis_key = []

        if self.is_multi_index :
            True

    def get_mo_analysis_signal(self, indicator: str=None) -> Dict:
                
        """
        Return the raw Pandas Dataframe Object.
        
        Arguments:
        ----
        indicator {Optional[str]} -- The mo_analysis key, for example 'TSF' or 'Cnvl' or 'VWC'

        Returns:
        ----
        {dict} -- Either all of the indicators or the one specified
        """

        if indicator and indicator in self._mo_analysis_signals:
            return self._mo_analysis_signals[indicator]
        else:
            return self._mo_analysis_signals

    def set_mo_analysis_signal(self, indicator: str, buy: float, sell: float, condition_buy: Any, condition_sell: Any, 
                             buy_max: float = None, sell_max: float = None, condition_buy_max: Any = None, condition_sell_max: Any = None) -> None:
        
        """
        Used to set an indicator where one indicator crosses above or below a certian numerical threshold.
        
        Arguments:
        ----
        indicator {str} -- The indicator key, for example `ema` or `sma`.

        buy {float} -- The buy signal threshold for the indicator.
        
        sell {float} -- The sell signal threshold for the indicator.

        condition_buy {str} -- The operator which is used to evaluate the `buy` condition. For example, `">"` would
            represent greater than or from the `operator` module it would represent `operator.gt`.
        
        condition_sell {str} -- The operator which is used to evaluate the `sell` condition. For example, `">"` would
            represent greater than or from the `operator` module it would represent `operator.gt`.

        buy_max {float} -- If the buy threshold has a maximum value that needs to be set, then set the `buy_max` threshold.
            This means if the signal exceeds this amount it WILL NOT PURCHASE THE INSTRUMENT. (defaults to None).
        
        sell_max {float} -- If the sell threshold has a maximum value that needs to be set, then set the `buy_max` threshold.
            This means if the signal exceeds this amount it WILL NOT SELL THE INSTRUMENT. (defaults to None).

        condition_buy_max {str} -- The operator which is used to evaluate the `buy_max` condition. For example, `">"` would
            represent greater than or from the `operator` module it would represent `operator.gt`. (defaults to None).
        
        condition_sell_max {str} -- The operator which is used to evaluate the `sell_max` condition. For example, `">"` would
            represent greater than or from the `operator` module it would represent `operator.gt`. (defaults to None).
        """

        # Add the key if it doesn't exist.
        if indicator not in self._mo_analysis_signals:
            self._mo_analysis_signals[indicator] = {}
            self._mo_analysis_key.append(indicator)

        # Add the signals.
        self._mo_analysis_signals[indicator]['buy'] = buy
        self._mo_analysis_signals[indicator]['sell'] = sell
        self._mo_analysis_signals[indicator]['buy_operator'] = condition_buy
        self._mo_analysis_signals[indicator]['sell_operator'] = condition_sell

        # Add the max signals.
        self._mo_analysis_signals[indicator]['buy_max'] = buy_max
        self._mo_analysis_signals[indicator]['sell_max'] = sell_max
        self._mo_analysis_signals[indicator]['buy_operator_max'] = condition_buy_max
        self._mo_analysis_signals[indicator]['sell_operator_max'] = condition_sell_max

    def set_mo_analysis_signal_compare(self, indicator_1: str, indicator_2: str, condition_buy: Any, condition_sell: Any) -> None:

        """
        Used to set signal where one indicator is compared to another
        
        Overview:
        ----
        The intended trading strategy employed within this object depends on comparing one indicator to another indicator.
        For example, the TSF of one time frame crossing above or below the TSF of another timeframe.


        Arguments:
        ----
        indicator_1 {str} -- The first indicator key, for example `Fast_TSF`.

        indicator_2 {str} -- The second indicator key, this is the indicator we will compare to. For example,
            is the `Fast_TSF` greater than the `VeryFast_TSF`.

        condition_buy {str} -- The operator which is used to evaluate the `buy` condition. For example, `">"` would
            represent greater than or from the `operator` module it would represent `operator.gt`.
        
        condition_sell {str} -- The operator which is used to evaluate the `sell` condition. For example, `">"` would
            represent greater than or from the `operator` module it would represent `operator.gt`.
        """

        # Define the key.
        key = "{ind_1}_comp_{ind_2}".format(
            ind_1=indicator_1,
            ind_2=indicator_2
        )

        # Add the key if it doesn't exist.
        if key not in self._mo_analysis_signals:
            self._mo_analysis_signals[key] = {}
            self._mo_analysis_comp_key.append(key)

        # Grab the dictionary.
        mo_analysis_dict = self._mo_analysis_signals[key]

        mo_analysis_dict['type'] = 'comparison'
        mo_analysis_dict['indicator_1'] = indicator_1
        mo_analysis_dict['indicator_2'] = indicator_2
        mo_analysis_dict['buy_operator'] = condition_buy
        mo_analysis_dict['condition_sell'] = condition_sell

    @property
    def price_data_frame(self) -> pd.DataFrame:

        """
        Return the raw Pandas DataFrame Object.
        
        Returns:
        ----
        {pd.DataFrame} -- A multi-index dataframe
        """

        return self._frame

    @price_data_frame.setter
    def price_data_frame(self, price_data_frame: pd.DataFrame) -> None:

        """
        Sets the price data frame.
        
        Arguments:
        ----
        price_data_frame{pd.DataFrame} -- A multi-index dataframe.
        """

        self._frame = price_data_frame

    @property
    def is_multi_index(self) -> bool:

        """
        Identifies whether the dataframe is a multi-index dataframe.
        
        Returns:
        ----
        {bool} -- 'True' if the dataframe is a 'pd.MultiIndex' object, 'False' otherwise.
        """

        if isinstance(self._frame.index, pd.MultiIndex):
            return True
        else:
            return False

    
    def lr_proj(self, y: float, n: int, column_name: str = 'lr_proj') -> pd.DataFrame:
        
        """
        Returns a linear regression curve using the least-squares method to approximate data for each set of bars defined by the length parameter

        Arguments:
        ----
        y, n, column_name 

        Returns:
        ----
        {pd.DataFrame} -- A dataframe with the lr_proj included.
        """

        locals_data = locals()
        del locals_data['self']

        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]['args'] = locals_data
        self._current_indicators[column_name]['func'] = self.lr_proj



        return self._frame
