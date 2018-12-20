import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import json

# authorize information
CLIENT_ID = '22D5RQ'
CLIENT_SECRET = 'ab10a93e2e4ff7df2a0e743a7592d484'

# authorize ourselves
# Using the ID and Secret, we can obtain the access and refresh tokens that authorize us to get our data
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                             refresh_token=REFRESH_TOKEN)


# store data based on time
def saveData(conf_time):
	# acquire the heart rate data,return dict data,validate from print(type(fit_statsHR))
	fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=conf_time, detail_level='1s')

	# convert dict into json string
	# jdata = json.dumps(fit_statsHR, indent=2)
	# print(type(jdata))
	# print(jdata)

	# reads the dictionary format and iterates through the dictionary values
	# saving the respective time and value values as lists before combining both into a pandas data frame
	time_list = []
	val_list = []
	for i in fit_statsHR['activities-heart-intraday']['dataset']:
		val_list.append(i['value'])
		time_list.append(i['time'])
	heartdf = pd.DataFrame({'Heart Rate': val_list, 'Time': time_list})

	# get desktop path
	import os
	def GetDesktopPath():
		return os.path.join(os.path.expanduser("~"), 'Desktop')

	desktop_dir = GetDesktopPath()
	dir_format = desktop_dir.replace("\r", r"\r")  # do not translate string:\->\\

	# save data as csv format
	# to_csv’s path format:C:\Users\Zheng Cheng\Desktop\something.csv
	heartdf.to_csv(dir_format + '\\' + \
	               conf_time + '.csv', \
	               columns=['Time', 'Heart Rate'], header=True, \
	               index=False)


if __name__ == "__main__":
	saveData("2018-11-25")
# for i in range(1,10):
#     time = str((datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
#     #saveData(time)
