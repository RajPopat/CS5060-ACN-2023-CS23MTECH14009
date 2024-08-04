import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import re
import datetime
warnings.filterwarnings("ignore")

################## Utility functions for plotting graphs ##################
def show_user_browsing_activities():
    print('########### Showing user statistics ############')
    df = pd.read_csv('client_activity.csv', parse_dates=['TimeStamp'])
    df['Day'] = df['TimeStamp'].dt.day
    df['Week'] = df['TimeStamp'].dt.isocalendar().week
    df['Month'] = df['TimeStamp'].dt.month
    df['Year'] = df['TimeStamp'].dt.year
    parsed_url_list = []

    for url in df['URL']:
        #match = re.search(r"(?:https?://)?(www\.[\w.-]+|[\w.-]+)",str(url))
        match = re.search(r"(?:https?://)?(?:www\.)?([\w.-]+)", str(url))
        parsed_url_list.append(match.group(1))

    df['Domain'] = parsed_url_list

    # 1. Daily statistics
    current_day = datetime.datetime.now().day
    current_week = datetime.datetime.now().isocalendar().week
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    df_for_today = df[(df['Day'] == current_day) & (df['Week'] == current_week) & (df['Month'] == current_month) & (df['Year'] == current_year)]

    # 2. Weekly statistics
    current_week = datetime.datetime.now().isocalendar().week
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    df_for_current_week = df[(df['Week'] == current_week) & (df['Month'] == current_month) & (df['Year'] == current_year)]

    # 3. Monthly statistics
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    df_for_current_month = df[(df['Month'] == current_month) & (df['Year'] == current_year)]

    ############################ Bar charts ###############################
    # Today
    df_for_today_blocked = df_for_today[df_for_today['IsUrlBlocked']==True]
    df_for_today_unblocked = df_for_today[df_for_today['IsUrlBlocked']==False]

    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(12, 10))
    ax1.bar(x=df_for_today_blocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), height=df_for_today_blocked['Domain'].value_counts().sort_values(ascending=False)[:5], color = 'teal')
    ax1.set_title('Top 5 blocked websites accessed today')
    ax1.set_xlabel('Websites')
    ax1.set_ylabel('Counts of requests')
    ax1.set_xticklabels(labels=df_for_today_blocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), rotation=30)

    ax2.bar(x=df_for_today_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), height=df_for_today_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5], color = "#4CAF50")
    ax2.set_title('Top 5 unblocked websites accessed today')
    ax2.set_xlabel('Websites')
    ax2.set_ylabel('Counts of requests')
    #ax2.set_yticks(np.arange(max(df_for_today_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5]), step=1))
    ax2.set_xticklabels(labels=df_for_today_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), rotation=30)

    plt.savefig('today.png')
    plt.tight_layout()
    plt.show()

    # Weekly stats

    week_counts = df['Week'].value_counts().sort_index()
    all_weeks_counts = pd.Series(0, index=range(1, 54))
    all_weeks_counts.update(week_counts)
    ax = all_weeks_counts.plot(kind='bar', figsize=(18, 8), color='green')

    plt.xlabel('Week No.')
    plt.ylabel('Number of requests hit')
    plt.title('Number of requests hit per Week')
    plt.xticks(rotation=0)
    plt.savefig('weekly1.png')
    plt.show()

    df_for_current_week_blocked = df_for_current_week[df_for_current_week['IsUrlBlocked']==True]
    df_for_current_week_unblocked = df_for_current_week[df_for_current_week['IsUrlBlocked']==False]

    fig, ((ax3, ax4)) = plt.subplots(1, 2, figsize=(12, 10))
    ax3.bar(x=df_for_current_week_blocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), height=df_for_current_week_blocked['Domain'].value_counts().sort_values(ascending=False)[:5])
    ax3.set_title('Top 5 blocked websites accessed in current week')
    ax3.set_xlabel('Websites')
    ax3.set_ylabel('Counts of requests')
    ax3.set_xticklabels(labels=df_for_current_week_blocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), rotation=30)

    ax4.bar(x=df_for_current_week_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), height=df_for_current_week_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5], color = "coral")
    ax4.set_title('Top 5 unblocked websites accessed in current week')
    ax4.set_xlabel('Websites')
    ax4.set_ylabel('Counts of requests')
    ax4.set_xticklabels(labels=df_for_current_week_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), rotation=30)

    plt.savefig('weekly2.png')
    plt.tight_layout()
    plt.show()
    
    # Monthly
    
    month_counts = df['Month'].value_counts().sort_index()
    all_months_counts = pd.Series(0, index=range(1, 13))
    all_months_counts.update(month_counts)
    ax = all_months_counts.plot(kind='bar', figsize=(18, 8), color='yellowgreen')

    plt.xlabel('Month No.')
    plt.ylabel('Number of requests hit')
    plt.title('Number of requests hit per Month')
    plt.xticks(rotation=0)
    plt.savefig('monthly1.png')
    plt.show()

    df_for_current_month_blocked = df_for_current_month[df_for_current_month['IsUrlBlocked']==True]
    df_for_current_month_unblocked = df_for_current_month[df_for_current_month['IsUrlBlocked']==False]

    fig, ((ax5, ax6)) = plt.subplots(1, 2, figsize=(10, 10))
    ax5.bar(x=df_for_current_month_blocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), height=df_for_current_month_blocked['Domain'].value_counts().sort_values(ascending=False)[:5], color = "skyblue")
    ax5.set_title('Top 5 blocked websites accessed in current month')
    ax5.set_xlabel('Websites')
    ax5.set_ylabel('Counts of requests')
    ax5.set_xticklabels(labels=df_for_current_month_blocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), rotation=30)

    ax6.bar(x=df_for_current_month_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), height=df_for_current_month_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5], color = "lightgreen")
    ax6.set_title('Top 5 unblocked websites accessed in current month')
    ax6.set_xlabel('Websites')
    ax6.set_ylabel('Counts of requests')
    ax6.set_xticklabels(labels=df_for_current_month_unblocked['Domain'].value_counts().sort_values(ascending=False)[:5].keys(), rotation=30)

    plt.savefig('monthly2.png')
    plt.tight_layout()
    plt.show()
    ###########################################################################

    ############################### Pie charts #############################
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    ######### Daily Pie Chart  #########
    if df_for_today_blocked.shape[0] != 0 or df_for_today_unblocked.shape[0] != 0: 
        ax1.pie([df_for_today_blocked.shape[0], df_for_today_unblocked.shape[0]], labels=['Blocked Urls','UnBlocked Urls'], autopct='%1.1f%%', colors=['red','springgreen'])
        ax1.set_title('Percentage of urls blocked/unblocked today')
    else:
        fig.delaxes(ax1)
    ######### Weekly Pie Chart  #########
    if df_for_current_week_blocked.shape[0] != 0 or df_for_current_week_unblocked.shape[0] != 0:
        ax2.pie([df_for_current_week_blocked.shape[0], df_for_current_week_unblocked.shape[0]], labels=['Blocked Urls','UnBlocked Urls'], autopct='%1.1f%%', colors=['red','springgreen'])
        ax2.set_title('Percentage of urls blocked/unblocked in current week')
    else:
        fig.delaxes(ax2)
    ######### Monthly Pie Chart  #########
    if df_for_current_month_blocked.shape[0] != 0 or df_for_current_month_unblocked.shape[0] != 0:
            ax3.pie([df_for_current_month_blocked.shape[0], df_for_current_month_unblocked.shape[0]], labels=['Blocked Urls','UnBlocked Urls'], autopct='%1.1f%%',colors=['red','springgreen'])
            ax3.set_title('Percentage of urls blocked/unblocked in current month')
    else:
        fig.delaxes(ax3)
    fig.delaxes(ax4)
    plt.tight_layout()
    plt.savefig('piechart.png')
    plt.show()
    ###########################################################################

def main():
    try:
        show_user_browsing_activities()
    except Exception as e:
        print('Error occurred while showing statistics:',str(e))

if __name__ == '__main__':
    main()
