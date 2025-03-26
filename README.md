# Music-Sync

Currently a set of scripts to download liked songs from Spotify and find matches for them and save to liked music on YouTube Music.

### Authorizing Spotify


### Authorizing YouTube Music

I used the method described on this [page](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html) of the YTMusic python package. In Summary:
* Open YTMusic in your browser and inspect the page.
* While the inspect tab is open, navigate to the `network` tab and click on a POST action on the page e.g. like a song.
* You will see a new `POST` row in the network tab with a status code of 200 - click on that row.
* Scroll down to the `request headers` and click on the "raw" toggle.
* Copy all the text in that section into a new file called `browser.json` in your project - remember to format your file correctly to be `json` compliant.
* This will be used to authenticate your sessions when loaded as described here: [link](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#using-the-headers-in-your-project)
