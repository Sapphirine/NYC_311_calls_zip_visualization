from sodapy import Socrata
import os
import folium
import pandas as pd
import cgi


def getmap(crit_1):

    client = Socrata("data.cityofnewyork.us", "iBBb7XdJQQL5zLxWTKQyP8fVN",
                        username="plm2130@columbia.edu", password = "hHfa29h7pWmyR6g7e7")

    LIMIT = 50000
    client.timeout = 120
    results = client.get("erm2-nwe9", limit = LIMIT, select = 'incident_zip, complaint_type')
    raw_311_df = pd.DataFrame.from_records(results)
    zip_311_df = raw_311_df
    no_nan_df = zip_311_df.dropna()
    no_nan_df.reset_index(drop = True, inplace = True)

    save_as = './template/result.html'
    geoJson_path = './NYCgeo.json'

    geoJson = pd.read_json(geoJson_path)
    data = no_nan_df

    number_of_zipCodes = len(geoJson['features'])
    zips = {}
    # make a list of the zip codes in the data and see if there are repeats
    for region in range(number_of_zipCodes):
        zipcode = geoJson['features'][region]['properties']['postalCode']
        try:
            #works if there is already this zip in the dict
            zips[zipcode] = zips[zipcode] + 1
        except:
            #works if there isn't this zip in the dict yet
            zips[zipcode] = 1
        pass

    df_1 = pd.DataFrame(columns=['ZipCode', crit_1])
    #df_2 = pd.DataFrame(columns=['ZipCode', crit_2])
    #df_1 = pd.DataFrame(columns=['ZipCode', crit_3])

    for call in range(len(data)):
        zipcode = int(data['incident_zip'][call])
        incident = data['complaint_type'][call]

        if zipcode > 0: # This is only true for data with a zipcode
            zipcode = str(zipcode)
            if incident == crit_1:
                try:
                    df_1.at[df_1.loc[df_1["ZipCode"]==zipcode].index[0], crit_1] = df_1.at[df_1.loc[df_1["ZipCode"]==zipcode].index[0], crit_1] + 1
                    #df_2.at[df_2.loc[df_2["ZipCode"]==zipcode].index[0], crit_2] = df_2.at[df_2.loc[df_2["ZipCode"]==zipcode].index[0], crit_2] + 1
                    #df_3.at[df_3.loc[df_3["ZipCode"]==zipcode].index[0], crit_3] = df_3.at[df_3.loc[df_3["ZipCode"]==zipcode].index[0], crit_3] + 1

                except:
                    df_1 = df_1.append({'ZipCode': zipcode, crit_1: 1}, ignore_index=True)
                    #df_2 = df_2.append({'ZipCode': zipcode, crit_2: 1}, ignore_index=True)
                    #df_3 = df_3.append({'ZipCode': zipcode, crit_3: 1}, ignore_index=True)
                    #Zip code exists
                pass
            pass
        pass

    center_coord = [40.701412, -74.017116]
    m = folium.Map(center_coord, zoom_start=11)

    choropleth_1 = folium.Choropleth(
        geo_data=geoJson_path,
        name='choropleth_1',
        data=df_1,
        columns=["ZipCode", crit_1],
        key_on= 'feature.properties.postalCode',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=crit_1
    ).add_to(m)

    #choropleth_2 = folium.Choropleth(
    #    geo_data=geoJson_path,
#        name='choropleth_2',
#        data=df_2,
#        columns=["ZipCode", crit_2],
#        key_on= 'feature.properties.postalCode',
#        fill_color='YlGn',
#        fill_opacity=0.7,
#        line_opacity=0.2,
#        legend_name=crit_2
#    ).add_to(m)

#    choropleth_3 = folium.Choropleth(
#        geo_data=geoJson_path,
#        columns=["ZipCode", crit_3],
#        key_on= 'feature.properties.postalCode',
#        fill_color='YlGn',
#        fill_opacity=0.7,
#        line_opacity=0.2,
#        legend_name=crit_3
#    ).add_to(m)

    folium.LayerControl().add_to(m)

    m.save(os.path.join(save_as))
