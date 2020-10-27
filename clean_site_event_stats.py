# pylint: disable=C0103,C0413,W0621
"""
Python script "clean_site_event_stats.py"
by Matthew Garcia, Post-doctoral Research Associate
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2020 by Matthew Garcia

PURPOSE:
    combine multi-site VI statistics based on Landsat queries.

USAGE:
    python clean_site_event_stats.py ALL_SITES_EVENTS_VI_stats.csv
"""


import sys
import pandas as pd


sites = ['CHITTY', 'KLOO', 'SILVER', 'SULPHUR']
events = ['1990-1994', '1995-1999', '2002-2006', '2007-2011', '2011-2015']
vi_names = ['NDVI', 'EVI', 'GRVI', 'RSR', 'NDII', 'NBR', 'KTTC_GRN', 'KTTC_WET']


print()
#
if len(sys.argv) < 2:
    print('input error: need file name (full path)')
    sys.exit(1)
else:
    infname = sys.argv[1]
#
print('reading input data file %s' % infname)
stats_df = pd.read_csv(infname, index_col=None)
print('input df has %d rows' % len(stats_df))
#
# filter out duplicate observations between P60R17 and P60R18 on same date
P60R17_df = stats_df[stats_df['footprint'] == 'P60R17']
P60R18_df = stats_df[stats_df['footprint'] == 'P60R18']
to_remove = list()
for site_name in sites:
    P60R17_site_df = P60R17_df[P60R17_df['site_name'] == site_name]
    P60R17_site_dates = list(P60R17_site_df['dyear'])
    P60R18_site_df = P60R18_df[P60R18_df['site_name'] == site_name]
    P60R18_site_dates = list(P60R18_site_df['dyear'])
    for d17 in P60R17_site_dates:
        if d17 in P60R18_site_dates:
            P60R17_site_date_df = P60R17_site_df[P60R17_site_df['dyear'] == d17]
            P60R17_idx = P60R17_site_date_df['npx_frac'].index[0]
            P60R17_npx_frac = list(P60R17_site_date_df['npx_frac'])[0]
            P60R18_site_date_df = P60R18_site_df[P60R18_site_df['dyear'] == d17]
            P60R18_idx = P60R18_site_date_df['npx_frac'].index[0]
            P60R18_npx_frac = list(P60R18_site_date_df['npx_frac'])[0]
            if P60R17_npx_frac >= P60R18_npx_frac:
                to_remove.append(P60R18_idx)
            else:
                to_remove.append(P60R17_idx)
#
stats_df.drop(to_remove, inplace=True)
print('filtered df has %d rows' % len(stats_df))
#
outfname = '%s_cleaned.csv' % infname[:-4]
stats_df.to_csv(outfname, index=False)
print('wrote %d rows to %s' % (len(stats_df), outfname))
print()

# end clean_site_event_stats.py
