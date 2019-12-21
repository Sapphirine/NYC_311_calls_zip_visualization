def map_maker():
#    import socket
#
#    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#    PORT = 9000        # Port to listen on (non-privileged ports are > 1023)
#
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#        s.bind((HOST, PORT))
#        s.listen()
#        conn, addr = s.accept()
#        with conn:
#            print('Connected by', addr)
#            while True:
#                servdata = conn.recv(1024)
#                if not data:
#                    break
#                conn.sendall(servdata)
    #print(servdata)   
#    from flask import Flask, render_template, request
#
#    app = Flask(__name__)
#
#    @app.route('/', methods=['GET', 'POST'])
#    def form():
#        return render_template('form.html')
#
#    @app.route('/hello', methods=['GET', 'POST'])
#    def hello():
#        return render_template('greeting.html', say=request.form['say'], to=request.form['to'])
#    app.run()
    import time
    start_all = time.time()
    start_imports = time.time()
    import os
    import folium
    from folium import IFrame
    import pandas as pd

    #raw_311_df = pd.read_csv('mapapp/500data.csv')

    from sodapy import Socrata
    end_imports = time.time()
    print(end_imports-start_imports)
    start_client = time.time()
    client = Socrata("data.cityofnewyork.us", "iBBb7XdJQQL5zLxWTKQyP8fVN",
                     username="plm2130@columbia.edu", password="hHfa29h7pWmyR6g7e7")

    testing_for1 = 'Noise - House of Worship'
    testing_for2 = 'Noise'
    testing_for3 = 'Noise - Residential'

    LIMIT = 10000000
    client.timeout = 500
#    print("Client is waiting for 311...")
    results = client.get("erm2-nwe9", limit=LIMIT, select='incident_zip, complaint_type WHERE complaint_type="'+testing_for1+'" OR complaint_type="'+testing_for2+'" OR complaint_type="'+testing_for3+'"')
    end_client = time.time()
    #print("Connected to 311")
    print(end_client - start_client)
    start_midprocess = time.time()
    raw_311_df = pd.DataFrame.from_records(results)
    #zip_311_df = raw_311_df.filter(items=['created_date', 'complaint_type', 'incident_zip', 'status'])
    no_nan_df = raw_311_df.dropna()
    no_nan_df.reset_index(drop=True, inplace=True)

    save_as = 'mapapp/templates/maps/the_map.html'
    geoJson_path = 'mapapp/JSONfiles/NYCgeo.json'
    #data_path = '~/Downloads/erm2-nwe9.csv'

    geoJson = pd.read_json(geoJson_path)

    #    for index, row in no_nan_df.iterrows():
    #        row[incident_zip]


    data = no_nan_df
    df = data#[no_nan_df.incident_zip.isnumeric()]
    #data = pd.read_csv(data_path)

    #geoJson['features'][1]['properties']['postalCode']  
    #df.loc[df['column_name'] == some_value]
    # appending-- df = df.append({'User_ID': 23, 'UserName': 'Riti', 'Action': 'Login'}, ignore_index=True)
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

    end_midprocess = time.time()
    print(end_midprocess - start_midprocess)
    start_livability = time.time()
    livability = {}
    
    #print("before the for loop")
    # This for loop is the bottleneck in speed - we need to figure out a better way, maybe some kind of mapping thing
    for key in zips:
        # for each zipcode (key), I want to assign (value) another KV list for each complaint type and its frequency.
        # To select a row from a df where some column column_name is some_value df.loc[df['column_name'] == some_value]
        livability[key] = df.loc[df['incident_zip'] == key].loc[df['complaint_type'] == testing_for1].shape[0] + df.loc[df['incident_zip'] == key].loc[df['complaint_type'] == testing_for2].shape[0] + df.loc[df['incident_zip'] == key].loc[df['complaint_type'] == testing_for3].shape[0]
    #        zips[key][testing_for2] = df.loc[df['incident_zip'] == key].loc[df['complaint_type'] == testing_for2].shape[0]
    #        zips[key][testing_for3] = df.loc[df['incident_zip'] == key].loc[df['complaint_type'] == testing_for3].shape[0]
    #print("after the for loop")
    end_livability = time.time()
    print(end_livability - start_livability)
    
    start_norm = time.time()
    df2 = pd.DataFrame(columns=[])
    for key in livability:   
        df2 = df2.append({'ZipCode': key, 'livability': livability[key]}, ignore_index=True)

    maximum = df2.livability.max()
    minimum = df2.livability.min()

    delta = maximum - minimum

    df2['livability']*=-1
    df2['livability']+=maximum
    df2['livability']*=1/delta
    end_norm = time.time()
    print(end_norm - start_norm)
#    for call in range(len(data)):
#        zipcode = int(data['incident_zip'][call])
#        incident = data['complaint_type'][call]
#
#        if zipcode > 0: # This is only true for data with a zipcode
#            zipcode = str(zipcode)
#            if incident == testing_for1 or incident == testing_for2 or incident == testing_for3:
#                try: 
#                    df.at[df.loc[df["ZipCode"]==zipcode].index[0], incident] = df.at[df.loc[df["ZipCode"]==zipcode].index[0], incident] + 1
#                except:
#                    df = df.append({'ZipCode': zipcode, incident: 1}, ignore_index=True)
#                    #Zip code exists
#                pass
#            pass
#        pass
    start_folium = time.time()
    center_coord = [40.701412, -74.017116]

    m = folium.Map(center_coord, zoom_start=11, attr="attribution")

    #folium.GeoJson(geoJson_path, style_function=lambda feature: {
    #        'fillColor': '#ffff00',
    #        'color': 'black',
    #        'weight': 2,
    #        'dashArray': '.5,5'
    #    }).add_to(m)

    choropleth1 = folium.Choropleth(
        geo_data=geoJson_path,
        name='choropleth',
        data=df2,
        columns=["ZipCode", 'livability'],
        key_on= 'feature.properties.postalCode',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name= 'Livability Index'
    ).add_to(m)
    
#    choropleth2 = folium.Choropleth(
#        geo_data=geoJson_path,
#        name='choropleth',
#        data=df,
#        columns=["ZipCode", testing_for2],
#        key_on= 'feature.properties.postalCode',
#        fill_color='YlGn',
#        fill_opacity=0.7,
#        line_opacity=0.2,
#        legend_name= testing_for1
#    ).add_to(m)
#    
#    choropleth3 = folium.Choropleth(
#        geo_data=geoJson_path,
#        name='choropleth',
#        data=df,
#        columns=["ZipCode", testing_for3],
#        key_on= 'feature.properties.postalCode',
#        fill_color='YlGn',
#        fill_opacity=0.7,
#        line_opacity=0.2,
#        legend_name= testing_for3
#    ).add_to(m)
    folium.LayerControl().add_to(m)
    
#    title_html = '''
#             <h3 align="center" style="font-size:20px"><b>Your map title</b></h3>
#             '''
#    m.get_root().html.add_child(folium.Element(title_html))
    m.save(os.path.join(save_as))
    end_folium = time.time()
    end_all = time.time()
    print(end_folium - start_folium)
    print(end_all-start_all)
    print("Done")