# Spotify song suggestions
## Synopsis

We will use a data set that has attributes rather than make a direct call to Spotify's API.

Purpose:
* Use machine learning to give a list of suggested songs.
* Create a simple Flask server that can take a list of loved and hated songs and make suggestions from this.
  * The user input should make an API-call that does autocomplete suggestion of known song names from the dataset

Technologies in use:
* Pandas
* Numpy
* Generators
* Flask
* Files
* Machine learning
  * clustering - kmeans

Challenges:
* Machine learning
* RESTapi - making song suggestions for users


### How to use
* Visit frontend on [droplet](http://167.71.50.92:5000/).
* Use the search bar to find songs.
	* Like and/or dislike songs.
* Hit the "Get recommendation" button.
* You'll get a list of your recommendations.
	* Hit the [i] button to learn more about a recommended song.
* Scroll further down to see the graphs displaying a trend found in your selection.