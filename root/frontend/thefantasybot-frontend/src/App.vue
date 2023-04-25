<template>
  <section>
    <header>
      <h1>NFL Fantasy Draft Board - 2022</h1>
      <button @click="togglePlayers">Show Players</button>
      <button @click="toggleSearch">Search Results</button>
    </header>
    <form v-if="isSearched" @submit.prevent="searchPlayer(searchInput)">
      <label>Search by {{ filterBy }}</label>
      <select id="search" v-model="filterBy">
        <option>ID</option>
        <option>Player</option>
        <option>Position</option>
        <option>Value Score</option>
        <option>ADP</option>
        <option>Sleeper Score</option>
      </select>
      <input type="text" class="input-box" v-model="searchInput" />
      <p>Searching for {{ searchInput }}</p>
      <button>Submit</button>
    </form>
    <table id="search-data" v-if="isSearched">
      <thead>
        <tr class="row">
          <th>ID</th>
          <th>Player</th>
          <th>Position</th>
          <th>Value Score</th>
          <th>ADP</th>
          <th>Sleeper Score</th>
          <th>Drafted</th>
        </tr>
      </thead>
      <tbody>
        <view-players v-for="search in searched" :key="search.id" :id="search.id" :player="search.player"
          :position="search.position" :value-score="search.valueScore" :adp="search.adp"
          :sleeper-score="search.sleeperScore" :drafted="search.drafted"></view-players>
      </tbody>
    </table>


    <table class="player-data" v-if="isActive">
      <thead>
        <tr class="row">
          <th>ID</th>
          <th>Player</th>
          <th>Position</th>
          <th>Value Score</th>
          <th>ADP</th>
          <th>Sleeper Score</th>
          <th>Drafted</th>
        </tr>
      </thead>
      <tbody>
        <view-players v-for="player in players" :key="player.id" :id="player.id" :player="player.player"
          :position="player.position" :value-score="player.valueScore" :adp="player.adp"
          :sleeper-score="player.sleeperScore" :drafted="player.drafted"
          @toggle-drafted="toggleDrafted($event)"></view-players>
      </tbody>
    </table>
  </section>
</template>

<script>
import ViewPlayers from './components/ViewPlayers.vue';

export default {
  components: {
    ViewPlayers
  },
  data() {
    return {
      players: [],
      searched: [],
      isActive: false,
      isSearched: false,
      searchInput: '',
      filterBy: ''
    }
  },
  methods: {
    getData() {
      fetch("http://127.0.0.1:8000/players/").then((response) => {
        if (response.ok) {
          return response.json();
        }
      }).then((data) => {
        console.log(data);
        const results = [];
        for (const id in data) {
          results.push({
            id: data[id].id,
            player: data[id].player,
            position: data[id].position,
            valueScore: data[id].value_score,
            adp: data[id].adp,
            sleeperScore: data[id].sleeper_score,
            drafted: data[id].drafted
          });
        }
        this.players = results;
      });
    },
    searchPlayer(player_id) {
      fetch(`http://127.0.0.1:8000/players/${player_id}`).then((response) => {
        if (response.ok) {
          return response.json();
        }
      }).then((data) => {
        console.log(data);
        const results = [];
        for (const id in data) {
          results.push({
            id: data[id].id,
            player: data[id].player,
            position: data[id].position,
            valueScore: data[id].value_score,
            adp: data[id].adp,
            sleeperScore: data[id].sleeper_score
          });
        }
        this.searched = results;
      });
    },
    toggleDrafted(id) {
      this.players[id].drafted = !this.players[id].drafted;
    },
    togglePlayers() {
      this.isActive = !this.isActive;
    },
    toggleSearch() {
      this.isSearched = !this.isSearched;
    }
  },
  beforeMount() {
    this.getData();
  },
}
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300&display=swap');

* {
  box-sizing: border-box;
}

html {
  font-family: 'Quicksand', sans-serif;
  background-color: white;
  font-size: 0.9rem;
}

body {
  margin: 0;
}

header {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 3rem auto;
  border-radius: 10px;
  padding: 1rem;
  background-color: #58004d;
  color: white;
  text-align: center;
  width: 90%;
  max-width: 40rem;
}

form {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 3rem auto;
  border-radius: 10px;
  padding: 1rem;
  background-color: #58004d;
  color: white;
  text-align: center;
  width: 90%;
  max-width: 40rem;
}

.input-box {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 1.1rem auto;
  border-radius: 10px;
  padding: 1rem;
  color: black;
  text-align: center;
  width: 90%;
  max-width: 40rem;
}

table {
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.26);
  margin: 3rem auto;
  border-radius: 10px;
  color: white;
  text-align: center;
  width: 100%;
  max-width: 40rem;
  border-collapse: collapse;
}

tr {
  padding: 8px;
  border: 1px solid rgba(221, 221, 221, 0.193);
  background-color: #58004d;
}

td {
  /* border: 1px solid #ddd; */
  padding: 1rem;
}

th {
  /* border: 1px solid #ddd; */
  padding: 12px;
  background-color: #cbc3ca;
  color: #5f505d;
}

.player-data tr:hover {
  background-color: #940386;
}

tr.checked,
tr.checked:hover {
  background-color: gray;
  /* pointer-events: none; */
}

/* .player-data tr:nth-child(even) {
  background-color: #65225c
} */

#app ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

#app li,
#app form {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 1rem auto;
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
  width: 90%;
  max-width: 40rem;
}

#app h2 {
  font-size: 2rem;
  border-bottom: 4px solid #ccc;
  color: #58004d;
  margin: 0 0 1rem 0;
}

#app button {
  font: inherit;
  cursor: pointer;
  border: 1px solid #ff0077;
  background-color: #ff0077;
  color: white;
  padding: 0.05rem 1rem;
  box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.26);
}

#app button:hover,
#app button:active {
  background-color: #ec3169;
  border-color: #ec3169;
  box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.26);
}

#app input {
  font: inherit;
  padding: 0.15rem;
}

#app label {
  font-weight: bold;
  margin-right: 1rem;
  width: 7rem;
  display: inline-block;
}

#app form div {
  margin: 1rem 0;
}
</style>
