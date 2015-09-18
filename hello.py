from flask import Flask, make_response, request, render_template
import urllib3
import json

app = Flask(__name__)

keyword_global = 'food'
radius_global = '1000'
location_global = '-33.8665433,151.1956316'
results_list_global = ""

@app.route('/' , methods=['GET', 'POST'])
def hello_world():
	#print("test")
	if request.method == 'POST':
		radius_global = request.form['radius']
		keyword_global = request.form['keyword']
		location_global = request.form['location']
		results_list_global = do_search(request.form['radius'], request.form['keyword'], request.form['location'])
		if(not type(results_list_global) is NoneType):
			place_list = [place['name'] for place in results_list_global]
			loc_list = [place['geometry']['location'] for place in results_list_global]
		else:
			place_list = [""]
			loc_list = [""]
		#print(results_list_global)
		return render_template('placesSearch.html', places = place_list, radius = radius_global, location = location_global, keyword = keyword_global, resultLocations = loc_list, fullJson = results_list_global)
	return render_template('placesSearch.html')

def do_search(radius, keyword, location):
	# Set the Places API key for your application
	AUTH_KEY = 'AIzaSyAvjW1rnzYBpdyeaTtEybrNJ91Mcwq4LwA'
	# Define the location coordinates
	LOCATION = location
	# Define the radius (in meters) for the search
	RADIUS = radius
	#Keywords to search for
	KEYWORD = keyword

	# Compose a URL to query a predefined location with a radius of 5000 meters
	url = ('https://maps.googleapis.com/maps/api/place/search/json?location=%s'
	         '&radius=%s&keyword=%s&key=%s') % (LOCATION, RADIUS, KEYWORD, AUTH_KEY)

	# Send the GET request to the Place details service (using url from above)
	http = urllib3.PoolManager()
	response = http.request("GET", url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read().decode(encoding='UTF-8')
	json_data = json.loads(json_raw)

	# Iterate through the results and print them to the console
	return_list = []
	key_list = ['name', 'geometry', 'types']
	if json_data['status'] == 'OK':
		for place in json_data['results']:
			new_dict = {key:place[key] for key in key_list}
			return_list.append(new_dict)

		return return_list
		#for place in json_data['results']:
			#print(place['name'])
		#return [place['name'] for place in json_data['results']]


@app.route("/download", methods = ['GET', 'POST'])
def download():
	text = request.form['fullJson']
	print(text)
	response = make_response(text)
	response.headers["Content-Disposition"] = "attachment; filename=text.txt"
	return response

if __name__ == '__main__':
	app.debug = True
	app.run()