<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<div align="center">
   <h1>Fantasy Football Helper App</h1>

A complete single page application using a REST API for the backend and Vue.js for the frontend. I do not intend for this to be a long-term project, but it has been a valuable way for me to learn web frameworks, REST APIs, HTTP Requests, and advanced Python techniques.
   <br><br>
   <img src="https://s12.gifyu.com/images/Sutcd.gif">
</div>


## Description
This is a free alternative to other paid fantasy subscriptions that help guide you through your fantasy football drafts. The Fantasy Football Helper App pulls in data from fantasypros.com using a web scraping process. The process includes a value based method to rank players using ADP (Average Draft Position) and VOR (Value Over Replacement), as well as a single feature GMM tiering method (Gaussian Mixture Modeling) for position groups. I will push the up to date player data to the repo as needed when I test it this upcoming season.

The Vue.js frontend dev server and FastAPI backend server will need to be launched prior to using the app. The frontend web page will ask for your snake draft position (currently built for 12 teams only but can be adjusted in the code), and then the type of scoring you would like to use (STD for Standard, HALF for Half PPR, and PPR for Full PPR).

Please note that there are bugs and the code isn't completely cleaned or optimized.

### Built With

[![Vue][Vue.js]][Vue-url]
[![FastAPI][FastAPI]][FastAPI-url]

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/tylerbakely/thefantasybot.git
   ```
2. Install NPM packages
   ```sh
   npm install vue-cli
   ```
3. Install python packages
   ```sh
   pip install -r requirements.txt
   ```

### How To Use

1. Run the web scraper for up to date draft data (optional)
   ```sh
   python draft_boards.py
   ```
2. Launch the frontend and backend servers
   ```sh
   npm run dev
   python root/backend/app/main.py
   ```
3. Enter the frontend server domain in your browser if it does not launch automatically e.g. http://localhost:5174/
4. You will have to enter two prompts when the page launches, the first is the snake order position you are drafting (pick 1-12) and then the type of scoring your fantasy league is using (STD, HALF, or PPR).
5. When your fantasy draft starts, use the checkbox under the "Draft Board" table to CAREFULLY select each player that has been drafted before, during, and after your pick all the way to the end of the draft.
6. When it is your time to pick, the browser will alert you and let you use the "Suggest Pick" button. If you try to use "Suggest Pick" when it is not your turn, the browser will alert you.

#### Button Functions

* Show Players
    * Toggle button that hides and shows the Draft Board table
* Toggle Search
    * Hides and shows the player filter and search form
* Show Drafted Players
    * Hides and shows the Drafted Players table (below the Draft Board table)
* Show My Drafted Players
    * Shows and hides the your currently drafted roster
* Suggest Pick
    * Sends a POST request with a list of dictionaries containing the already drafted players to the FastAPI /players/draft-pick node and returns the recommended pick based on your current roster

<!-- BUGS -->
### Current Bugs

- The ascending/descending sorting function in App.vue is currently disabled because it causes the player selection to not work correctly. Low priority
- Cannot undo drafting a player once they've been selected without advancing the overall draft pick number. Be careful when drafting, as misclicking a player will require you to restart the app in order to not mess up the backend algorithm.
- The player filter and search form will be layered on top of the draft board table if the screen is minimized too much. The CSS formatting was not properly planned out in advance since I was learning CSS on the fly. I will make updates eventually but it is low priority
- The recommendation algorithm in players.py is still a work in progress and may not suggest the most optimal player after all starters have been drafted.
- There are a few other bugs that I can't think of at the moment, but they do not affect the main purpose of the app. I will add to this list as I encounter them.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/tylerbakely/thefantasybot.svg?style=for-the-badge
[contributors-url]: https://github.com/tylerbakely/thefantasybot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/tylerbakely/thefantasybot.svg?style=for-the-badge
[forks-url]: https://github.com/tylerbakely/thefantasybot/network/members
[stars-shield]: https://img.shields.io/github/stars/tylerbakely/thefantasybot.svg?style=for-the-badge
[stars-url]: https://github.com/tylerbakely/thefantasybot/stargazers
[issues-shield]: https://img.shields.io/github/issues/tylerbakely/thefantasybot.svg?style=for-the-badge
[issues-url]: https://github.com/tylerbakely/thefantasybot/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/tylerbakely
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/lo/
