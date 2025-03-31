# Music-Sync

Currently a set of scripts to download liked songs from Spotify and find matches for them and save to liked music on YouTube Music.

### Authorizing Spotipy

I used the `spotipy` python package to download my Spotify playlists and liked songs. Authorization of the Spotipy package was pretty straightforward. Steps taken from [here](https://spotipy.readthedocs.io/en/2.25.1/#authorization-code-flow) include:

* Navigating to your [Spotify Dashboard](https://developer.spotify.com/dashboard/applications) to create an app if you haven't already created one
* Create an `app` 
    * Give it a friendly name
    * Provide a quick description
    * Provide a redirect URL, I used `http://127.0.0.1:fill_port_number_here`, with my own port number typically (1024-49151)
    * Select "WebAPI" under which APIs/SDKs you're planning to use
    * Accept terms and "Save"
* Now copy `ClientID` and `ClientSecret` into a `.env` file along with your `redirect url` - you will need these to authorize your spotify connection
* The resulting .env file will look somewhat like this:

```
SPOTIPY_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
SPOTIPY_CLIENT_ID=YOUR_CLIENT_ID_HERE
SPOTIPY_REDIRECT_URI=http://127.0.0.1:fill_port_number_here
```


### Authorizing YouTube Music

I used the method described on this [page](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html) of the YTMusic python package. In Summary:

* Open YTMusic in your browser and inspect the page, they suggest using the Firefox browser.
* While the inspect tab is open, navigate to the `network` tab and click on a POST action on the page e.g. like a song.
* You will see a new `POST` row in the network tab with a status code of 200 - click on that row.
* Scroll down to the `request headers` and click on the "raw" toggle.
* Copy all the text in that section into a new file called `browser.json` in your project - remember to format your file correctly to be `json` compliant.
* This will be used to authenticate your sessions when loaded as described here: [link](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#using-the-headers-in-your-project)
* The resulting `browser.json` will look somewhat like this:

```
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "X-Goog-AuthUser": "0",
    "x-origin": "https://music.youtube.com",
    "Authorization": "YOUR_AUTHORIZATION",
    "Cookie": "YOUR_COOKIE"
}
```