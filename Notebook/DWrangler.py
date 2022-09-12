import pandas as pd


class wrangler:

    def __init__(self) -> None:
        pass


    def missing_values(self, data):
        """Function that checks for null values and computes the percentage of null values
        Args:
            data: dataframe - data whose missing value is to be determined
        Return:
            missing_output: dataframe - dataframe of total null values with corresponding percentages
        """

        total = data.isnull().sum().sort_values(ascending=False) 
        percentage = round((total / data.shape[0]) * 100, 2)
        
        missing_output = pd.concat([total, percentage], axis=1, keys=['Total','Percentage'])
        
        return missing_output



    def convert_dtype(self, data, dtype, cols):
        """Function that converts columns to specific data types
        
        Args:
            dtype: data type to be achieved
            cols: list of columns to convert
        Return:
            data: dataframe with converted data types
        """
        
        for col in cols:
            if col in data.columns:
                data[col] = data[col].astype(dtype)
            else:
                pass
        
        return data



    def convert_date(self, data, cols):
        """Function that converts julian dates to datetime columns
        
        Args:
            data: data type to be achieved
            col: column to convert
        Return:
            converted column
        """
        for col in cols:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col], unit='D', origin='julian')
            else:
                pass

        return data 



    def drop_cols(self, data, cols):
        """ Function to drop list of columns 

        Args:
            data: dataframe
            cols: assigned columns to be deleted
        
        Return:
            data: modified dataframe
        """

        data = data.drop(columns = cols)

        return data



    def data_clean(self, data):
        """ Function to cleans wildfire data 

        Args:
            data: dataframe
        
        Return:
            data: cleaned dataframe
        """

        # get missing values
        miss_values = self.missing_values(data)

        # dropping columns with missing values > 60%
        missing_columns = list(miss_values[miss_values['Percentage'] > 59.9].index)
        data = self.drop_cols(data, missing_columns)

        # drop unneeded columns
        cols_drop = ["SOURCE_SYSTEM_TYPE", "SOURCE_SYSTEM", "NWCG_REPORTING_AGENCY", "NWCG_REPORTING_UNIT_ID", 
                    "NWCG_REPORTING_UNIT_NAME", "SOURCE_REPORTING_UNIT", "SOURCE_REPORTING_UNIT_NAME","FIRE_NAME", 
                    "LOCAL_INCIDENT_ID", "FIPS_CODE", "FIPS_NAME", "OWNER_CODE", "OWNER_DESCR", "Shape"]

        # check if columns exist in dataframe
        cols_drop = [cols for cols in cols_drop if cols in data.columns]
        data = self.drop_cols(data, cols_drop)

        # converting julian date
        data = self.convert_date(data, ['DISCOVERY_DATE', 'CONT_DATE'])

        # converting object data types
        obj_cols = data.select_dtypes(include="object").columns.to_list()
        data =  self.convert_dtype(data, 'category', obj_cols)
        
        # creating duration and fire_month column
        data['FIRE_DURATION'] = (data['CONT_DATE'] - data['DISCOVERY_DATE']).dt.days
        data['FIRE_MONTH']  = data['DISCOVERY_DATE'].dt.month_name()

        # drop missing values
        data.dropna(axis=0, inplace=True)
        
        return data



    def get_timeseries(self, data, date_col, period, groupby_col):
        """Funtion that samples data into multiple time series
        Args:
            data: dataframe
            date_col - str: datetime column in the dataset - used for resampling
            period str: resampling period (D - days, W - weeks, M - months)
            grupby_col: column to groupby with aggregation
        Return:
            time_series: final time series data
        """
        
        time_series = pd.DataFrame({'count':data.set_index(date_col).resample(period)[groupby_col].value_counts()}).reset_index()
        
        return time_series