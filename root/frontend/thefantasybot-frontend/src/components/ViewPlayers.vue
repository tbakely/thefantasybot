<template>
    <li>
        <h2>{{ player }}</h2>
        <ul>
            <li><strong>ID:</strong> {{ id }}</li>
            <li><strong>Player:</strong> {{ player }}</li>
            <li><strong>Position:</strong> {{ position }}</li>
            <li><strong>Value Score:</strong> {{ valueScore }}</li>
            <li><strong>ADP:</strong> {{ adp }}</li>
            <li><strong>Sleeper Score:</strong> {{ sleeperScore }}</li>
        </ul>
    </li>
</template>
  
<script>
export default {
    props: {
        id: {
            type: Number,
            required: true,
        },
        player: {
            type: String,
            required: true,
        },
        position: {
            type: String,
            required: true,
        },
        valueScore: {
            type: Number,
            required: true,
        },
        adp: {
            type: Number,
            required: true,
        },
        sleeperScore: {
            type: Number,
            required: true
        },
    },
    emits: ['toggle-favorite', 'delete'],
    //   emits: {
    //     'toggle-favorite': function(id) {
    //         if (id) {
    //             return true;
    //         } else {
    //             console.warn('Id is missing!')
    //             return false;
    //         }
    //     },
    //   },
    data() {
        return {
            detailsAreVisible: false,
        };
    },
    methods: {
        toggleDetails() {
            this.detailsAreVisible = !this.detailsAreVisible;
        },
        toggleFavorite() {
            this.$emit('toggle-favorite', this.id);
        },
    },
};
</script>
  