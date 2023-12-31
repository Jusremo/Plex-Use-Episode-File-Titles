# Use Episode File Names For Plex Titles

Example Files
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://i.imgur.com/CynOU9O.png">
 <source media="(prefers-color-scheme: light)" srcset="https://i.imgur.com/CynOU9O.png">
 <img alt="YOUR-ALT-TEXT" src="https://i.imgur.com/CynOU9O.png">
</picture>

Before and After
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://i.imgur.com/hoygJLU.png">
 <source media="(prefers-color-scheme: light)" srcset="https://i.imgur.com/hoygJLU.png">
 <img alt="YOUR-ALT-TEXT" src="https://i.imgur.com/hoygJLU.png">
</picture>


<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://i.imgur.com/okmRzQG.png">
 <source media="(prefers-color-scheme: light)" srcset="https://i.imgur.com/okmRzQG.png">
 <img alt="YOUR-ALT-TEXT" src="https://i.imgur.com/okmRzQG.png">
</picture>

### How does it work?

It takes a series and attempt to format the episode file names into acceptable titles on Plex, by searching the file names for 'E#' and taking the text after, will attempt alternative methods if 'E#' not found.

Mainly meant to be used for unmatched series.

### Requirements

* python-plexapi 4.15.7+ (installed by requirements.txt)

### How to Use
* pip install -r requirements.txt </summary></details>
* Create config.ini matching config.ini.example with your desired settings </summary></details>
* python plex-use-episode-file-titles.py </summary>



| Config Setting         | How it Works |
|-----------------------:|-----------|
| Dry Run | Test script to view output without committing title changes to Plex|
| Try Alt Title if No Episode Indicator | Try finding title base start from a "-" or "\\" if S0xE0x isn't found in the file name    |
| Series Year | Not required, use if there's multiple shows of the same name you need to narrow down    |

