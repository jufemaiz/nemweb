#pylint: disable=line-too-long
"""Module for downloading data different 'CURRENT' nemweb dataset
(selected data sets from files from http://www.nemweb.com.au/Reports/CURRENT)

Module includes one main superclass for handling generic nemweb current files. A
series of namedtuples (strored in global constant DATASETS) contains the
relevant data for specfic datasets.

Datasets included from 'CURRENT' index page:

- [Dispatch_SCADA](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_SCADA/)
- [DispatchIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/DispatchIS_Reports/)
- [Next_Day_Actual_Gen](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Actual_Gen/) (METER_DATA_GEN_DUID)
- [Next_Day_Dispatch](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Dispatch) (DISPATCH_UNIT_SOLUTION)
- [ROOFTOP_PV/ACTUAL](https://www.nemweb.com.au/REPORTS/CURRENT/ROOFTOP_PV/ACTUAL/)
- [TradingIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/TradingIS_Reports/)

TODO:
- [Adjusted_Prices_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Adjusted_Prices_Reports/)
- [Alt_Limits](https://www.nemweb.com.au/REPORTS/CURRENT/Alt_Limits/)
- [Ancillary_Services_Payments](https://www.nemweb.com.au/REPORTS/CURRENT/Ancillary_Services_Payments/)
- [Auction_Units_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Auction_Units_Reports/)
- [Bidmove_Complete](https://www.nemweb.com.au/REPORTS/CURRENT/Bidmove_Complete/)
- [Bidmove_Summary](https://www.nemweb.com.au/REPORTS/CURRENT/Bidmove_Summary/)
- [Billing](https://www.nemweb.com.au/REPORTS/CURRENT/Billing/)
- [Causer_Pays](https://www.nemweb.com.au/REPORTS/CURRENT/Causer_Pays/)
- [Causer_Pays_Rslcpf](https://www.nemweb.com.au/REPORTS/CURRENT/Causer_Pays_Rslcpf/)
- [CDEII](https://www.nemweb.com.au/REPORTS/CURRENT/CDEII/)
- [CSC_CSP_ConstraintList](https://www.nemweb.com.au/REPORTS/CURRENT/CSC_CSP_ConstraintList/)
- [CSC_CSP_Settlements](https://www.nemweb.com.au/REPORTS/CURRENT/CSC_CSP_Settlements/)
- [Daily_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Daily_Reports/)
- [DAILYOCD](https://www.nemweb.com.au/REPORTS/CURRENT/DAILYOCD/)
- [Directions_Reconciliation](https://www.nemweb.com.au/REPORTS/CURRENT/Directions_Reconciliation/)
- [Dispatch_IRSR](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_IRSR/)
- [DISPATCH_NEGATIVE_RESIDUE](https://www.nemweb.com.au/REPORTS/CURRENT/DISPATCH_NEGATIVE_RESIDUE/)
- [Dispatch_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_Reports/)
- [Dispatchprices_PRE_AP](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatchprices_PRE_AP/)
- [DWGM](https://www.nemweb.com.au/REPORTS/CURRENT/DWGM/)
- [Gas_Supply_Guarantee](https://www.nemweb.com.au/REPORTS/CURRENT/Gas_Supply_Guarantee/)
- [GSH](https://www.nemweb.com.au/REPORTS/CURRENT/GSH/)
- [HighImpactOutages](https://www.nemweb.com.au/REPORTS/CURRENT/HighImpactOutages/)
- [HistDemand](https://www.nemweb.com.au/REPORTS/CURRENT/HistDemand/)
- [IBEI](https://www.nemweb.com.au/REPORTS/CURRENT/IBEI/)
- [Marginal_Loss_Factors](https://www.nemweb.com.au/REPORTS/CURRENT/Marginal_Loss_Factors/)
- [Market_Notice](https://www.nemweb.com.au/REPORTS/CURRENT/Market_Notice/)
- [MCCDispatch](https://www.nemweb.com.au/REPORTS/CURRENT/MCCDispatch/)
- [Medium_Term_PASA_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Medium_Term_PASA_Reports/)
- [Mktsusp_Pricing](https://www.nemweb.com.au/REPORTS/CURRENT/Mktsusp_Pricing/)
- [MTPASA_RegionAvailability](https://www.nemweb.com.au/REPORTS/CURRENT/MTPASA_RegionAvailability/)
- [Network](https://www.nemweb.com.au/REPORTS/CURRENT/Network/)
- [NEXT_DAY_MCCDISPATCH](https://www.nemweb.com.au/REPORTS/CURRENT/NEXT_DAY_MCCDISPATCH/)
- [Next_Day_Offer_Energy](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Offer_Energy/)
- [Next_Day_Offer_FCAS](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Offer_FCAS/)
- [Next_Day_PreDispatch](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_PreDispatch/)
- [Next_Day_PreDispatchD](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_PreDispatchD/)
- [Next_Day_Trading](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Trading/)
- [Operational_Demand](https://www.nemweb.com.au/REPORTS/CURRENT/Operational_Demand/)
- [P5_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/P5_Reports/)
- [PasaSnap](https://www.nemweb.com.au/REPORTS/CURRENT/PasaSnap/)
- [PD7Day](https://www.nemweb.com.au/REPORTS/CURRENT/PD7Day/)
- [PDPASA](https://www.nemweb.com.au/REPORTS/CURRENT/PDPASA/)
- [Predispatch_IRSR](https://www.nemweb.com.au/REPORTS/CURRENT/Predispatch_IRSR/)
- [Predispatch_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Predispatch_Reports/)
- [Predispatch_Sensitivities](https://www.nemweb.com.au/REPORTS/CURRENT/Predispatch_Sensitivities/)
- [PredispatchIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/PredispatchIS_Reports/)
- [Public_Prices](https://www.nemweb.com.au/REPORTS/CURRENT/Public_Prices/)
- [PublishedModelDataAccess](https://www.nemweb.com.au/REPORTS/CURRENT/PublishedModelDataAccess/)
- [Regional_Summary_Report](https://www.nemweb.com.au/REPORTS/CURRENT/Regional_Summary_Report/)
- [Reserve_Contract_Recovery](https://www.nemweb.com.au/REPORTS/CURRENT/Reserve_Contract_Recovery/)
- [ROOFTOP_PV/FORECAST](https://www.nemweb.com.au/REPORTS/CURRENT/ROOFTOP_PV/FORECAST/)
- [Settlements](https://www.nemweb.com.au/REPORTS/CURRENT/Settlements/)
- [SEVENDAYOUTLOOK_FULL](https://www.nemweb.com.au/REPORTS/CURRENT/SEVENDAYOUTLOOK_FULL/)
- [SEVENDAYOUTLOOK_PEAK](https://www.nemweb.com.au/REPORTS/CURRENT/SEVENDAYOUTLOOK_PEAK/)
- [Short_Term_PASA_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Short_Term_PASA_Reports/)
- [SRA_Bids](https://www.nemweb.com.au/REPORTS/CURRENT/SRA_Bids/)
- [SRA_NSR_RECONCILIATION](https://www.nemweb.com.au/REPORTS/CURRENT/SRA_NSR_RECONCILIATION/)
- [SRA_Results](https://www.nemweb.com.au/REPORTS/CURRENT/SRA_Results/)
- [STTM](https://www.nemweb.com.au/REPORTS/CURRENT/STTM/)
- [SupplyDemand](https://www.nemweb.com.au/REPORTS/CURRENT/SupplyDemand/)
- [Trading_Cumulative_Price](https://www.nemweb.com.au/REPORTS/CURRENT/Trading_Cumulative_Price/)
- [Trading_IRSR](https://www.nemweb.com.au/REPORTS/CURRENT/Trading_IRSR/)
- [VicGas](https://www.nemweb.com.au/REPORTS/CURRENT/VicGas/)
- [Vwa_Fcas_Prices](https://www.nemweb.com.au/REPORTS/CURRENT/Vwa_Fcas_Prices/)
- [Weekly_Bulletin](https://www.nemweb.com.au/REPORTS/CURRENT/Weekly_Bulletin/)
- [Weekly_Constraint_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Weekly_Constraint_Reports/)
- [Yesterdays_Bids_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Yesterdays_Bids_Reports/)
- [Yesterdays_MNSPBids_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Yesterdays_MNSPBids_Reports/)
"""
#pylint: enable=line-too-long

from io import BytesIO
import datetime
import re
from collections import namedtuple
import requests
from nemweb import nemfile_reader, nemweb_sqlite


class CurrentFileHandler:
    """Class for handling `CURRENT` nemweb files from http://www.nemweb.com.au

    Requires a 'CurrentDataset' namedtuple with following fields:

    - nemweb_name: the name of the dataset to be download (e.g. Dispatch_SCADA)
    - filename_pattern: a regex expression to match and a determine datetime from filename
      on nemweb. As example, for files in the Dispatch_SCADA dataset
      (e.g "PUBLIC_DISPATCHSCADA_201806201135_0000000296175732.zip") the regex
      file_patten is PUBLIC_DISPATCHSCADA_([0-9]{12})_[0-9]{16}.zip
    - the format of the string to strip the datetime from. From the above example, the
      match returns '201806201135', so the string is "%Y%m%d%H%M",
    - the list of tables to insert from each dataset. This is derived from the 2nd and
      3rd column in the nemweb dataset. For example, the 2nd column is in Dispatch_SCADA
      is "DISPATCH" and the 3rd is "SCADA_VALUE" and the name is "DISPATCH_UNIT_SCADA".

    Several datasets contain multiple tables. Examples can be found in the DATASETS dict
    (nemfile_reader.DATASETS)

    Attributes:
        base_url (str): the base URL used in HTTP requests, allows for mocking overrides
        path (str): the path to access the datasets
    """

    def __init__(self):
        self.base_url = "https://www.nemweb.com.au"
        self.path = "REPORTS/CURRENT"

    def update_data(
            self,
            dataset,
            print_progress=False,
            start_date=None,
            end_date='30001225',  #  must be a better way
            db_name='nemweb_live.db'  #  maybe this should look at config?
    ):
        """Main method to process nemweb dataset

        - downloads the index page for the dataset
        - determines date to start downloading from
        - matches the start date against files in the index
        - inserts new files into database

        Args:
            dataset (:obj:`CurrentDataset`): the CurrentDataset to use
            print_progress (bool, optional): debug mode printing process of the
                update_data calls. Defaults to False.

        Returns:
            None
        """
        start_date = nemweb_sqlite.start_from(table_name=dataset.tables[0],
                                              timestamp_col=dataset.datetime_column,
                                              start_date=start_date,
                                              db_name=db_name)
        end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
        page = requests.get("{0}/{1}/{2}/".format(self.base_url,
                                                  self.path,
                                                  dataset.dataset_name))
        regex = re.compile("/{0}/{1}/{2}".format(self.path,
                                                 dataset.dataset_name,
                                                 dataset.nemfile_pattern))

        for match in regex.finditer(page.text):
            file_datetime = datetime.datetime.strptime(match.group(1), dataset.datetime_format)
            if end_date > file_datetime > start_date:
                nemfile = self.download(match.group(0))
                if print_progress:
                    print(dataset.dataset_name, file_datetime)
                for table in dataset.tables:
                    dataframe = nemfile[table].drop_duplicates().copy()
                    nemweb_sqlite.insert(dataframe, table, db_name)

    def download(self, link):
        """Dowloads nemweb zipfile from link into memory as a byteIO object.
        nemfile object is returned from the byteIO object

        Args:
            link (str): the URL to request

        Returns:
            dict
        """
        response = requests.get("{0}{1}".format(self.base_url, link))
        zip_bytes = BytesIO(response.content)
        nemfile = nemfile_reader.nemzip_reader(zip_bytes)
        return nemfile


# Class factory function for containing data for 'CURRENT' datasets
CurrentDataset = namedtuple("NemwebCurrentFile",
                            ["dataset_name",
                             "nemfile_pattern",
                             "datetime_format",
                             "datetime_column",
                             "tables"])

DATASETS = {
    "dispatch_scada":CurrentDataset(
        dataset_name="Dispatch_SCADA",
        nemfile_pattern='PUBLIC_DISPATCHSCADA_([0-9]{12})_[0-9]{16}.zip',
        datetime_format="%Y%m%d%H%M",
        datetime_column="SETTLEMENTDATE",
        tables=["DISPATCH_UNIT_SCADA"]),

    "trading_is": CurrentDataset(
        dataset_name="TradingIS_Reports",
        nemfile_pattern="PUBLIC_TRADINGIS_([0-9]{12})_[0-9]{16}.zip",
        datetime_format="%Y%m%d%H%M",
        datetime_column="SETTLEMENTDATE",
        tables=['TRADING_PRICE',
                'TRADING_REGIONSUM',
                'TRADING_INTERCONNECTORRES']),

    "rooftopPV_actual": CurrentDataset(
        dataset_name="ROOFTOP_PV/ACTUAL",
        nemfile_pattern="PUBLIC_ROOFTOP_PV_ACTUAL_([0-9]{14})_[0-9]{16}.zip",
        datetime_format="%Y%m%d%H%M00",
        datetime_column="INTERVAL_DATETIME",
        tables=['ROOFTOP_ACTUAL']),

    "next_day_actual_gen": CurrentDataset(
        dataset_name="Next_Day_Actual_Gen",
        nemfile_pattern="PUBLIC_NEXT_DAY_ACTUAL_GEN_([0-9]{8})_[0-9]{16}.zip",
        datetime_format="%Y%m%d",
        datetime_column="INTERVAL_DATETIME",
        tables=['METER_DATA_GEN_DUID']),

    "dispatch_is": CurrentDataset(
        dataset_name="DispatchIS_Reports",
        nemfile_pattern="PUBLIC_DISPATCHIS_([0-9]{12})_[0-9]{16}.zip",
        datetime_format="%Y%m%d%H%M",
        datetime_column="SETTLEMENTDATE",
        tables=['DISPATCH_PRICE',
                'DISPATCH_REGIONSUM',
                'DISPATCH_INTERCONNECTORRES']),

    "next_day_dispatch": CurrentDataset(
        dataset_name="Next_Day_Dispatch",
        nemfile_pattern="PUBLIC_NEXT_DAY_DISPATCH_([0-9]{8})_[0-9]{16}.zip",
        datetime_format="%Y%m%d",
        datetime_column="SETTLEMENTDATE",
        tables=['DISPATCH_UNIT_SOLUTION'])
}


def update_datasets(datasets, print_progress=False):
    """Updates a subset of datasets (as a list) contained in DATASETS

    Args:
        datasets (list): list of datasets to update
        print_progress (bool, optional): whether or not to print the log
            progress. Defaults to False

    Returns:
        None
    """
    filehandler = CurrentFileHandler()
    for dataset_name in datasets:
        filehandler.update_data(DATASETS[dataset_name],
                                print_progress=print_progress)
