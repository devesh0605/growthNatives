import numpy as np
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from variables.analytics_creds import view_id
from variables.analytics_creds import key_location


def format_summary(response):
    try:
        # create row index
        try:
            row_index_names = response['reports'][0]['columnHeader']['dimensions']
            row_index = [element['dimensions'] for element in response['reports'][0]['data']['rows']]
            row_index_named = pd.MultiIndex.from_arrays(np.transpose(np.array(row_index)),
                                                        names=np.array(row_index_names))
        except:
            row_index_named = None

        # extract column names
        summary_column_names = [item['name'] for item in response['reports'][0]
        ['columnHeader']['metricHeader']['metricHeaderEntries']]

        # extract table values
        summary_values = [element['metrics'][0]['values'] for element in response['reports'][0]['data']['rows']]

        # combine. I used type 'float' because default is object, and as far as I know, all values are numeric
        df = pd.DataFrame(data=np.array(summary_values),
                          index=row_index_named,
                          columns=summary_column_names).astype('float')

    except:
        df = pd.DataFrame()

    return df


def format_pivot(response):
    try:
        # extract table values
        pivot_values = [item['metrics'][0]['pivotValueRegions'][0]['values'] for item in response['reports'][0]
        ['data']['rows']]

        # create column index
        top_header = [item['dimensionValues'] for item in response['reports'][0]
        ['columnHeader']['metricHeader']['pivotHeaders'][0]['pivotHeaderEntries']]
        column_metrics = [item['metric']['name'] for item in response['reports'][0]
        ['columnHeader']['metricHeader']['pivotHeaders'][0]['pivotHeaderEntries']]
        array = np.concatenate((np.array(top_header),
                                np.array(column_metrics).reshape((len(column_metrics), 1))),
                               axis=1)
        column_index = pd.MultiIndex.from_arrays(np.transpose(array))

        # create row index
        try:
            row_index_names = response['reports'][0]['columnHeader']['dimensions']
            row_index = [element['dimensions'] for element in response['reports'][0]['data']['rows']]
            row_index_named = pd.MultiIndex.from_arrays(np.transpose(np.array(row_index)),
                                                        names=np.array(row_index_names))
        except:
            row_index_named = None
        # combine into a dataframe
        df = pd.DataFrame(data=np.array(pivot_values),
                          index=row_index_named,
                          columns=column_index).astype('float')
    except:
        df = pd.DataFrame()
    return df


def format_report(response):
    summary = format_summary(response)
    pivot = format_pivot(response)
    if pivot.columns.nlevels == 2:
        summary.columns = [[''] * len(summary.columns), summary.columns]

    return pd.concat([summary, pivot], axis=1)


def run_report(body, credentials_file):
    # Create service credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_file,
                                                                        scopes=[
                                                                            'https://www.googleapis.com/auth/analytics.readonly'])
    # Create a service object
    service = build('analyticsreporting', 'v4', credentials=credentials)

    # Get GA data
    response = service.reports().batchGet(body=body).execute()

    return format_report(response)


your_view_id = view_id
ga_keys = key_location

body = {'reportRequests': [{'viewId': your_view_id,
                            'dateRanges': [{'startDate': '2021-01-01', 'endDate': '2022-01-19'}],
                            'metrics': [{'expression': 'ga:users'},
                                        {"expression": "ga:bounceRate"}],
                            'dimensions': [{'name': 'ga:yearMonth'}],
                            "pivots": [{"dimensions": [{"name": "ga:channelGrouping"}],
                                        "metrics": [{"expression": "ga:users"},
                                                    {"expression": "ga:bounceRate"}]
                                        }]
                            }]}

summary_body = {'reportRequests': [{'viewId': your_view_id,
                                    'dateRanges': [{'startDate': '2021-01-01', 'endDate': '2021-02-28'}],
                                    'metrics': [{'expression': 'ga:sessions'},
                                                {'expression': 'ga:totalEvents'},
                                                {"expression": "ga:avgSessionDuration"}],
                                    'dimensions': [{'name': 'ga:country'}],
                                    }]}
pivot_body = {'reportRequests': [{'viewId': your_view_id,
                                  'dateRanges': [{'startDate': '2021-01-01', 'endDate': '2021-02-28'}],
                                  'dimensions': [{'name': "ga:channelGrouping"}],
                                  "pivots": [{"dimensions": [{"name": 'ga:yearMonth'}],
                                              "metrics": [{"expression": "ga:users"},
                                                          {"expression": "ga:newUsers"},
                                                          {"expression": "ga:timeOnPage"}]
                                              }]
                                  }]}

short_body = {"reportRequests": [{
    "viewId": your_view_id,
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "yesterday"}],
    "metrics": [{"expression": "ga:users"}]
}]}

untidy_body = {'reportRequests': [{'viewId': your_view_id,
                                   'dateRanges': [{'startDate': '2021-01-01', 'endDate': '2021-02-28'}],
                                   "pivots": [{"dimensions": [{"name": 'ga:yearMonth'}, {"name": "ga:channelGrouping"}],
                                               "metrics": [{"expression": "ga:users"},
                                                           {"expression": "ga:timeOnPage"}]
                                               }]
                                   }]}

ga_report = run_report(body, ga_keys)
print(ga_report)
# ga_report.to_csv('analytics_result.csv')
