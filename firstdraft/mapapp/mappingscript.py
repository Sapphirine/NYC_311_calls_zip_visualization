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

    import os
    import folium
    from folium import IFrame
    import pandas as pd

    #raw_311_df = pd.read_csv('mapapp/500data.csv')

    from sodapy import Socrata
    import cgi
    # client = Socrata("data.cityofnewyork.us", "iBBb7XdJQQL5zLxWTKQyP8fVN",
                     # username="plm2130@columbia.edu", password="hHfa29h7pWmyR6g7e7")

    LIMIT = 500000
    # client.timeout = 500
    # print("Client is waiting for 311...")
    print("Fetching 311 data")
    '''
    results = client.get("erm2-nwe9", limit=LIMIT)
    print("Connected to 311")
    raw_311_df = pd.DataFrame.from_records(results)
    zip_311_df = raw_311_df.filter(items=['created_date', 'complaint_type', 'incident_zip', 'status'])
    no_nan_df = zip_311_df.dropna()
    no_nan_df.reset_index(drop=True, inplace=True)
    no_nan_df.head(LIMIT)
    '''
    no_nan_df = pd.read_csv('~/Documents/500mil.csv')
    print("File read successfully")
    # form = cgi.FieldStorage()
    # searchterm =  form.getvalue('searchbox')

    testing_for = 'Noise - Residential'

    save_as = 'mapapp/templates/maps/the_map.html'
    geoJson_path = 'mapapp/JSONfiles/NYCgeo.json'
    #data_path = '~/Downloads/erm2-nwe9.csv'

    geoJson = pd.read_json(geoJson_path)

#    for index, row in no_nan_df.iterrows():
#        row[incident_zip]


    data = no_nan_df#[no_nan_df.incident_zip.isnumeric()]
    #data = pd.read_csv(data_path)

    #geoJson['features'][1]['properties']['postalCode']
    #df.loc[df['column_name'] == some_value]
    # appending-- df = df.append({'User_ID': 23, 'UserName': 'Riti', 'Action': 'Login'}, ignore_index=True)
    number_of_zipCodes = len(geoJson['features'])
    zips = {}
    print("Zip processing stuff")
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

    df = pd.DataFrame(columns=['ZipCode', testing_for])
    for call in range(len(data)):
        zipcode = int(data['incident_zip'][call])
        incident = data['complaint_type'][call]

        if zipcode > 0: # This is only true for data with a zipcode
            zipcode = str(zipcode)
            if incident == testing_for:
                try:
                    df.at[df.loc[df["ZipCode"]==zipcode].index[0], testing_for] = df.at[df.loc[df["ZipCode"]==zipcode].index[0], testing_for] + 1
                except:
                    df = df.append({'ZipCode': zipcode, testing_for: 1}, ignore_index=True)
                    #Zip code exists
                pass
            pass
        pass
    center_coord = [40.701412, -74.017116]

    print("Map time")
    m = folium.Map(center_coord, zoom_start=11, attr="attribution")

    #folium.GeoJson(geoJson_path, style_function=lambda feature: {
    #        'fillColor': '#ffff00',
    #        'color': 'black',
    #        'weight': 2,
    #        'dashArray': '.5,5'
    #    }).add_to(m)

    choropleth = folium.Choropleth(
        geo_data=geoJson_path,
        name='choropleth',
        data=df,
        columns=["ZipCode", testing_for],
        key_on= 'feature.properties.postalCode',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name= testing_for + " -- Darkened regions have no incidents"
    ).add_to(m)
    folium.LayerControl().add_to(m)

#    title_html = '''
#             <h3 align="center" style="font-size:20px"><b>Your map title</b></h3>
#             '''
#    m.get_root().html.add_child(folium.Element(title_html))
    m.save(os.path.join(save_as))
