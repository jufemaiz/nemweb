# nemweb

[![Build Status](https://media.readthedocs.org/static/projects/badges/passing-flat.svg)](https://nemweb.readthedocs.io/en/latest/nemweb.html)

## Introduction

This is a python3 package to directly download and process AEMO files from
http://www.nemweb.com.au/. Main module within the package dowloads the nemweb
files and inserts the tables into a local sqlite database.

This forms part of the backend of the
[OpenNEM](https://opennem.org.au/#/all-regions) platform. The openNEM backend
utilises a normalised mysql database (with foreign key and unique constraints).
At present, this package only includes a simple sqlite interface without this
support of capability. Further modules and interfaces for mysql, postgresql and
more may eventually be added.

## Quick start

### nemweb

[nemweb](https://github.com/opennem/nemweb) is a python library enabling access
to AEMO's [nemweb archives](https://www.nemweb.com.au). The tool provides for
programmatic exposure of the datasets that other services can make use of.

nemweb can be installed through `pip`:

```bash
pip install nemweb
```

### opennem data server

nemweb can be installed through `pip` with the opennem service:

```bash
pip install opennem
```

Or by running:

```bash
python3 setup.py install
```

From the package directory. If installing by `setup.py`, a post-install script
will prompt you input a directory for the sqlite database to live in. For
example:

```bash
'Enter directory (abs path) to store for sqlite db:' /home/dylan/Data
```

This value will live in a configuration file in your root directory
(`$HOME/.nemweb_config.ini`).

**IMPORTANT** If you install via `pip` you must manually enter the sqlite
directory in a file named `.nemweb_config.ini` in your home directly
post-install (...couldn't figure out how to make post-install scripts to work
with `pip`).

## Quick example

```python
from nemweb import nemweb_current

nemweb_current.update_datasets([dispatch_scada])
DISPATCH_UNIT_SCADA doesn't exists. Enter start date [YYYYMMDD]: 20180624
```

The first time you add a new dataset to you sqlite db, it will prompt you for a
date to start donwloading from. From then on, it will only download data beyond
what you already have locally.

You can chose to print progress to screen, if desired. For example (and for a
table that has already been initialised):

```python
from nemweb import nemweb_current

nemweb_current.update_datasets([dispatch_scada],
                               print_progress=True)

> 'Dispatch_SCADA 2018-06-24 13:40:00'
> 'Dispatch_SCADA 2018-06-24 13:45:00'
> 'Dispatch_SCADA 2018-06-24 13:50:00'
> 'Dispatch_SCADA 2018-06-24 13:55:00'
> '...'
```

Currently, the following dataset are built in to the package, and can be added
and downloaded automatically from the
[`Current` index of nemweb](http://www.nemweb.com.au/Reports/Current/)

- `next_day_actual_gen`
- `rooftopPV_actual`
- `trading_is`
- `dispatch_scada`
- `next_day_dispatch`
- `dispatch_is`

Other datasets can be add by using using the class factory function for
containing data for 'Current' datasets (`CurrentDataset`) found in the
`nemweb_current` module.  The namedtuple from this can then be used with
`CurrentFileHandler` class to download and process that dataset.

## Documentation

Further information available with
[the online documentation at ReadTheDocs](https://nemweb.readthedocs.io/en/latest/nemweb.html).

## TODO

In no particular order:

- Add more datasets from `Current` index
- Add module to procee archived data (from `Archive` index:
  http://www.nemweb.com.au/Reports/ARCHIVE/)
- Add more sophisticate support for sqlite database (e.g. selectively inserting
  fields, tables from dataset)
- Add module for interfacing with mysql database

### `CURRENT` Index Support

- ✅[Dispatch_SCADA](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_SCADA/)
- ✅[DispatchIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/DispatchIS_Reports/)
- ✅[Next_Day_Actual_Gen](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Actual_Gen/)
  (METER_DATA_GEN_DUID)
- ✅[Next_Day_Dispatch](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Dispatch)
  (DISPATCH_UNIT_SOLUTION)
- ✅[ROOFTOP_PV/ACTUAL](https://www.nemweb.com.au/REPORTS/CURRENT/ROOFTOP_PV/ACTUAL/)
- ✅[TradingIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/TradingIS_Reports/)
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

### `ARCHIVE` Index Support

- [Adjusted_Prices_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Adjusted_Prices_Reports/)
- [Bidmove_Complete](https://www.nemweb.com.au/REPORTS/CURRENT/Bidmove_Complete/)
- [Bidmove_Summary](https://www.nemweb.com.au/REPORTS/CURRENT/Bidmove_Summary/)
- [Billing](https://www.nemweb.com.au/REPORTS/CURRENT/Billing/)
- [CDEII](https://www.nemweb.com.au/REPORTS/CURRENT/CDEII/)
- [Daily_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Daily_Reports/)
- [DAILYOCD](https://www.nemweb.com.au/REPORTS/CURRENT/DAILYOCD/)
- [Dispatch_IRSR](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_IRSR/)
- [Dispatch_Negative_Residue](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_Negative_Residue/)
- [Dispatch_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_Reports/)
- [Dispatch_SCADA](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_SCADA/)
- [DispatchIS_FCAS_Fix](https://www.nemweb.com.au/REPORTS/CURRENT/DispatchIS_FCAS_Fix/)
- [DispatchIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/DispatchIS_Reports/)
- [Dispatchprices_PRE_AP](https://www.nemweb.com.au/REPORTS/CURRENT/Dispatchprices_PRE_AP/)
- [HistDemand](https://www.nemweb.com.au/REPORTS/CURRENT/HistDemand/)
- [Market_Notice](https://www.nemweb.com.au/REPORTS/CURRENT/Market_Notice/)
- [MCCDispatch](https://www.nemweb.com.au/REPORTS/CURRENT/MCCDispatch/)
- [Medium_Term_PASA_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Medium_Term_PASA_Reports/)
- [MTPASA_RegionAvailability](https://www.nemweb.com.au/REPORTS/CURRENT/MTPASA_RegionAvailability/)
- [Network](https://www.nemweb.com.au/REPORTS/CURRENT/Network/)
- [Next_Day_Actual_Gen](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Actual_Gen/)
- [Next_Day_Dispatch](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Dispatch/)
- [NEXT_DAY_MCCDISPATCH](https://www.nemweb.com.au/REPORTS/CURRENT/NEXT_DAY_MCCDISPATCH/)
- [Next_Day_Offer_Energy](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Offer_Energy/)
- [Next_Day_Offer_FCAS](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Offer_FCAS/)
- [Next_Day_PreDispatch](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_PreDispatch/)
- [Next_Day_PreDispatchD](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_PreDispatchD/)
- [Next_Day_Trading](https://www.nemweb.com.au/REPORTS/CURRENT/Next_Day_Trading/)
- [Operational_Demand](https://www.nemweb.com.au/REPORTS/CURRENT/Operational_Demand/)
- [P5_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/P5_Reports/)
- [PDPASA](https://www.nemweb.com.au/REPORTS/CURRENT/PDPASA/)
- [Predispatch_IRSR](https://www.nemweb.com.au/REPORTS/CURRENT/Predispatch_IRSR/)
- [Predispatch_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Predispatch_Reports/)
- [Predispatch_Sensitivities](https://www.nemweb.com.au/REPORTS/CURRENT/Predispatch_Sensitivities/)
- [PredispatchIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/PredispatchIS_Reports/)
- [Public_Prices](https://www.nemweb.com.au/REPORTS/CURRENT/Public_Prices/)
- [ROOFTOP_PV/ACTUAL](https://www.nemweb.com.au/REPORTS/CURRENT/ROOFTOP_PV/ACTUAL/)
- [ROOFTOP_PV/FORECAST](https://www.nemweb.com.au/REPORTS/CURRENT/ROOFTOP_PV/FORECAST/)
- [Settlements](https://www.nemweb.com.au/REPORTS/CURRENT/Settlements/)
- [SEVENDAYOUTLOOK_FULL](https://www.nemweb.com.au/REPORTS/CURRENT/SEVENDAYOUTLOOK_FULL/)
- [SEVENDAYOUTLOOK_PEAK](https://www.nemweb.com.au/REPORTS/CURRENT/SEVENDAYOUTLOOK_PEAK/)
- [Short_Term_PASA_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Short_Term_PASA_Reports/)
- [Trading_Cumulative_Price](https://www.nemweb.com.au/REPORTS/CURRENT/Trading_Cumulative_Price/)
- [Trading_IRSR](https://www.nemweb.com.au/REPORTS/CURRENT/Trading_IRSR/)
- [TradingIS_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/TradingIS_Reports/)
- [Weekly_Bulletin](https://www.nemweb.com.au/REPORTS/CURRENT/Weekly_Bulletin/)
- [Yesterdays_Bids_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Yesterdays_Bids_Reports/)
- [Yesterdays_MNSPBids_Reports](https://www.nemweb.com.au/REPORTS/CURRENT/Yesterdays_MNSPBids_Reports/)
