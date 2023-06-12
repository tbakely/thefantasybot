<template>
  <section>
    <div id="div-header">
      <header>
        <h1>NFL Fantasy Draft Board - 2023</h1>
        <button @click="togglePlayers">Show Players</button>
        <button @click="toggleSearch">Toggle Search</button>
        <button @click="showDrafted">Show Drafted Players</button>
        <button @click="showMyDrafted">Show My Drafted Players</button>
        <button @click="sendPlayers">Suggest Pick</button>
        <!-- <button @click="toggleDebug">Debug Mode</button> -->
        <p>My Snake Position: {{ snakePosition }}</p>
        <select v-if="debugMode" v-model="snakePosition">
          <option v-for="num in 12">{{ num }}</option>
        </select>
        <p>Current Snake Position: {{ this.playerNumber }}</p>
        <p>Draft Board Scoring System: {{ this.scoring }}</p>
        <p v-if="debugMode">Pick Number: {{ overallPick }}</p>
        <p v-if="debugMode">{{ draftOrder }}</p>
      </header>

      <form v-if="isSearched">
        <label>Filter by Position:</label>
        <select id="search" v-model="filterBy">
          <option>All</option>
          <option>QB</option>
          <option>WR</option>
          <option>RB</option>
          <option>TE</option>
        </select>
        <input type="text" class="input-box" placeholder="Enter Player Name" v-model="searchInput" />
      </form>
    </div>

    <table class="player-data" v-if="draftedTeam">
      <thead>
        <tr>
          <th class="table-header" colspan="8">My Roster</th>
        </tr>
        <tr class="row">
          <th v-for="col in columns"><span class="text">{{ col }}</span><span class="arrow-container"><span
                v-if="sortColumn === col" class="arrow" :class="ascending ? 'arrow-up' : 'arrow-down'"></span></span>
          </th>
          <th>Drafted</th>
        </tr>
      </thead>
      <tbody>
        <view-players v-for="player in userDraftedList" :key="player.id" :id="player.id" :player="player.player"
          :position="player.position" :value-score="player.valueScore" :adp="player.adp"
          :sleeper-score="player.sleeperScore" :tier="player.tier" :drafted="player.drafted"></view-players>
      </tbody>
    </table>

    <table class="player-data" v-if="isActive">
      <thead>
        <tr>
          <th class="table-header" colspan="8">Draft Board</th>
        </tr>
        <tr class="row">
          <th v-for="col in columns"><span class="text">{{ col }}</span><span class="arrow-container"><span
                v-if="sortColumn === col" class="arrow" :class="ascending ? 'arrow-up' : 'arrow-down'"></span></span>
          </th>
          <th>Drafted</th>
        </tr>
      </thead>
      <tbody>
        <view-players v-for="player in playersList" :key="player.id" :id="player.id" :player="player.player"
          :position="player.position" :value-score="player.valueScore" :adp="player.adp"
          :sleeper-score="player.sleeperScore" :tier="player.tier" :drafted="player.drafted"
          @toggle-drafted="toggleDrafted($event)"></view-players>
      </tbody>
    </table>

    <table class="player-data">
      <thead>
        <tr>
          <th class="table-header" colspan="8">Drafted Players</th>
        </tr>
        <tr class="row">
          <th v-for="col in columns"><span class="text">{{ col }}</span><span class="arrow-container"><span
                v-if="sortColumn === col" class="arrow" :class="ascending ? 'arrow-up' : 'arrow-down'"></span></span>
          </th>
          <th>Drafted</th>
        </tr>
      </thead>
      <tbody>
        <view-players v-for="player in draftedList" :key="player.id" :id="player.id" :player="player.player"
          :position="player.position" :value-score="player.valueScore" :adp="player.adp"
          :sleeper-score="player.sleeperScore" :tier="player.tier" :drafted="player.drafted"></view-players>
      </tbody>
    </table>
  </section>
</template>

<script>
import ViewPlayers from './components/ViewPlayers.vue';
import axios from 'axios';

export default {
  components: {
    ViewPlayers
  },
  data() {
    return {
      players: [],
      searched: [],
      draftedPlayers: [],
      columns: ['id', 'player', 'position', 'valueScore', 'adp', 'sleeperScore', 'tier'],
      isActive: true,
      isSearched: true,
      searchInput: '',
      filterBy: 'All',
      ascending: false,
      sortColumn: '',
      arrowVisible: false,
      playerNumber: 1,
      snakeForward: true,
      overallPick: 1,
      notDrafted: false,
      draftOrder: [],
      suggestedPick: '',
      debugMode: false,
      snakePosition: 1,
      draftedTeam: false,
      scoring: "STD",
    }
  },
  methods: {
    getData(scoring = this.scoring) {
      fetch(`http://127.0.0.1:8000/players/?scoring=${scoring}`).then((response) => {
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
            tier: data[id].tier,
            drafted: data[id].drafted
          });
        }
        this.players = results;
      });
    },
    async sendPlayers() {
      if (this.playerNumber != this.snakePosition) {
        alert("It's NOT your turn to pick!")
      }
      else {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.draftOrder)
        };
        const response = await fetch(`http://127.0.0.1:8000/players/draft-pick?scoring=${this.scoring}`, requestOptions);
        const data = await response.json();
        this.suggestedPick = data.the_pick;
        alert(this.suggestedPick);
      }
    },
    toggleDrafted(id) {
      const player = this.players[id]
      this.players[id].drafted = !this.players[id].drafted;
      player.teamNo = this.playerNumber;
      player.overallPick = this.overallPick
      this.draftOrder.push(player);
      this.snakeCount();
      this.overallPick++;
    },
    togglePlayers() {
      this.isActive = !this.isActive;
    },
    toggleSearch() {
      this.isSearched = !this.isSearched;
    },
    clearSearch() {
      this.searched = [];
    },
    sortTable(col) {
      if (this.sortColumn === col) {
        this.ascending = !this.ascending;
      }
      else {
        this.ascending = true;
        this.sortColumn = col;
      }
      var ascending = this.ascending;
      this.arrowVisible = true;

      this.players.sort((a, b) => {
        if (a[col] > b[col]) {
          return ascending ? 1 : -1
        }
        else if (a[col] < b[col]) {
          return ascending ? -1 : 1
        }
        return 0;
      })
    },
    snakeCount() {
      if (this.snakeForward && this.playerNumber < 12) {
        this.playerNumber++;
      }
      else if (this.snakeForward && this.playerNumber === 12) {
        this.snakeForward = false;
      }
      else if (this.snakeForward === false && this.playerNumber === 1) {
        this.snakeForward = true;
      }
      else {
        this.playerNumber--;
      }
    },
    showDrafted() {
      this.notDrafted = !this.notDrafted;
    },
    toggleDebug() {
      this.debugMode = !this.debugMode;
    },
    showMyDrafted() {
      this.draftedTeam = !this.draftedTeam;
    }
  },
  watch: {
    playerNumber(newNumber, oldNumber) {
      if (newNumber == this.snakePosition) {
        alert("It's your turn to pick!");
      }
    }
  },
  computed: {
    playersList() {
      if (this.filterBy != 'All') {
        if (this.searchInput.trim().length > 0) {
          return this.players.filter((player) => player.player.toLowerCase().includes
            (this.searchInput.trim().toLowerCase())).filter((player) => player.position === this.filterBy)
        }
        return this.players.filter((player) => player.position === this.filterBy)
      }
      else if (this.searchInput.trim().length > 0) {
        return this.players.filter((player) => player.player.toLowerCase().includes
          (this.searchInput.trim().toLowerCase()))
      }
      else if (this.notDrafted) {
        return this.players.filter((player) => player.drafted === false)
      }
      return this.players
    },
    draftedList() {
      return this.players.filter((player) => player.drafted)
    },
    userDraftedList() {
      return this.draftOrder.filter((player) => player.teamNo == this.snakePosition)
    }
  },
  beforeMount() {
    const mySnakePosition = prompt("Enter your snake draft position.");
    const myScoring = prompt("Enter the scoring system: STD, HALF, or PPR.");
    this.snakePosition = mySnakePosition;
    this.scoring = myScoring;
    this.getData(this.scoring);
  },
}
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300&display=swap');
@import "./assets/App.css";
</style>
