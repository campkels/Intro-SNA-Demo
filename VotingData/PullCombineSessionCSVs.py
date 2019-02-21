# ------------------------------------------------------------------------------------------------------------
#  Pull 115th Congress Voting Data
#  Kelsey Campbell - 2/20/2019
# 
#  Voting Record Data is available from https://www.govtrack.us/congress/votes. Using the options to filter
#  to just the 115th (2018) Senate records (https://www.govtrack.us/congress/votes#session=302&chamber[]=1) 
#  shows that there were 274 roll call votes. Following and inspecting the URL's for the results, we see that
#  CSV's for each session are available with the following URL pattern:
#
#                                /congress/votes/115-2018/s1/export/csv
#                                /congress/votes/115-2018/s2/export/csv
#												...
#                                /congress/votes/115-2018/s273/export/csv
#                                /congress/votes/115-2018/s274/export/csv
#
#  This script uses this URL pattern to pull each CSV and save both a single session file and a combined CSV
#  of all 115th congress voting records. 						
# ------------------------------------------------------------------------------------------------------------

# Import Packages
#---------------------------------------------------
import requests
import pandas as pd
import io
import time

# Pull & Combine Data
#---------------------------------------------------

# Initialize loop helper variables
baseurl = 'https://www.govtrack.us/congress/votes/115-2018/'
votesdata = pd.DataFrame()
rowcnt = 0

# Loop and pull vote data for each session (search returns 274 roll call votes for 115th congress)
for x in range(1,275):
	print(x)
	# Construct download CSV URL for session vote
	url = baseurl + 's'+ str(x) + '/export/csv'
	# Download data for session vote
	data = requests.get(url)
	# Convert data to pandas (skip title at top)
	try:
		df = pd.read_csv(io.StringIO(data.text), skiprows=[0]) 
	except:
		data = requests.get(url)
		time.sleep(10)
		df = pd.read_csv(io.StringIO(data.text), skiprows=[0]) 
	# Add column for session vote number
	df['session'] = x
	# Append to master set
	votesdata = votesdata.append(df, ignore_index = True)
	# Save out individual file too
	df.to_csv('SessionCSVs/votes_session{}.csv'.format(x), encoding='utf-8-sig')
	# check row counts
	rows = df.shape[0]
	rowcnt += rows

# Save Data
#---------------------------------------------------
votesdata.to_csv('115Congress_VotesData.csv', encoding='utf-8-sig')
print(votesdata.head())
print(votesdata.shape)
print(rowcnt)