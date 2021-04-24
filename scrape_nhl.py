import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #initialize dictionary for scraped data results
    nhl_scrape = {}







    ### NHL player salary & cap hit data
    #salary_dict = {}
    salary_url = 'https://query.data.world/s/fqj3jtoxu3j6cxluz2umg77haeqcms'
    excel_source_df = pd.read_excel(salary_url)
    salary_df = excel_source_df.rename(columns={'Tm':'Abbr'})
    salary_df = salary_df.replace(to_replace='VEG',value='VGK')







    ### NHL team details
    #Get the team data as a DataFrame
    #teams_dict = {}
    #team_cap_dict = {}
    teams_url = 'https://statsapi.web.nhl.com/api/v1/teams'
    json_source_df = pd.read_json(teams_url)

    #Count the number of rows (i.e. teams)
    team_count = json_source_df['copyright'].count()

    #List of row indices for use later
    counts = list(range(0, team_count))

    #Data presents with nested dictionaries an needs to be cleaned
    #Use a for loop to drill down to teams section of JSON data
    teams_list = []
    for count in counts:
        teams_list.append(json_source_df['teams'][count])

    #Cleaning data of undesirable columns
    teams_df = pd.DataFrame(teams_list)
    teams_df = teams_df.drop(['id','link','venue','officialSiteUrl','franchise','division','conference','shortName'], axis=1)

    #Extract desired elements from nested dictionaries
    venue_list = []
    division_list = []
    conference_list = []
    #Use for loop to construct lists of desired data
    for count in counts:
        venue_list.append(teams_list[count]['venue']['name'])
        division_list.append(teams_list[count]['division']['name'])
        conference_list.append(teams_list[count]['conference']['name'])

    #Zip the desired data to a separate DataFrame
    venue_df = pd.DataFrame(list(zip(venue_list,division_list,conference_list)),columns=['venue','division','conference'])

    #Join the deisred data into clean data frame
    teams_df = teams_df.join(venue_df,how='left')

    #scrub column names
    teams_df = teams_df.rename(columns={'name':'Name','abbreviation':'Abbr','teamName':'Team','locationName':'Location',\
                                        'firstYearOfPlay':'First Year','franchiseId':'Franchise ID','active':'Active',\
                                        'venue':'Arena','division':'Division','conference':'Conference'
                                    })

    #sort as desired (oldest to newest)
    teams_df = teams_df.sort_values(by=['First Year','Franchise ID'])

    #teams_dict = teams_df.to_html(index=False)
    #nhl_scrape['teams'] = teams_dict







    ### NHL team salary cap data
    team_cap_df = salary_df.drop(['Player','Salary'], axis=1)
    team_cap_df = team_cap_df.groupby(['Abbr']).sum()
    team_cap_df = team_cap_df.sort_values(by='Cap Hit', ascending=False)
    top_cap_df = team_cap_df.iloc[:10]
    top_cap_df = top_cap_df.rename(columns={'Cap Hit':'Salary Cap'})







    ### Assemble the details in a presentable structure
    top_cap_df2 = top_cap_df.merge(salary_df.drop_duplicates(['Abbr']), how='left', on='Abbr')
    top_cap_df2 = top_cap_df2.drop(['Cap Hit'],axis=1)
    top_cap_df3 = top_cap_df2.merge(teams_df, how='left', on='Abbr')
    top_cap_df3 = top_cap_df3.drop(columns=['Location','First Year','Franchise ID','Active','Arena',\
                                        'Division','Conference'], axis=1)


    #team_cap_dict = top_cap_df3.to_dict()
    #nhl_scrape['team_cap'] = team_cap_dict




    cap_team_list = []
    cap_slrycp_list = []
    cap_plyr_list = []
    cap_slry_list = []

    for i in range(len(top_cap_df3)):
        cap_team_list.append(top_cap_df3['Name'][i])
        cap_slrycp_list.append(str(top_cap_df3['Salary Cap'][i]))
        cap_plyr_list.append(top_cap_df3['Player'][i])
        cap_slry_list.append(str(top_cap_df3['Salary'][i]))

    nhl_scrape['cap_team_list'] = cap_team_list
    nhl_scrape['cap_slrycp_list'] = cap_slrycp_list
    nhl_scrape['cap_plyr_list'] = cap_plyr_list
    nhl_scrape['cap_slry_list'] = cap_slry_list





    ### Scrape NHL team logos

    #initialize variable
    img_list = []

    #Loop through NHL team websites to scrape logo images
    for i in range(len(top_cap_df3)):
        # Set up Splinter
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        #URL definitions
        base_url = 'https://www.nhl.com/'
        target_url = base_url + top_cap_df3['Team'][i].lower().replace(' ','')
        browser.visit(target_url)
        #time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
        soup1 = soup.find('a', class_='top-nav__club-logo-link')
        scrape = soup1.find_all('img')[0]['src']
        img_link = scrape.replace('https:','')
        img_link = img_link.replace('http:','')
        img_link = img_link.replace('//','')
        img_list.append(img_link)
        browser.quit()

        nhl_scrape['img_list'] = img_list

    print(img_list)
    return nhl_scrape

