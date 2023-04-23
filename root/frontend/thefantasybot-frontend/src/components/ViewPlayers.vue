<template>
    <tr>
        <td>{{ id }}</td>
        <td>{{ player }}</td>
        <td>{{ position }}</td>
        <td>{{ valueScore }}</td>
        <td>{{ adp }}</td>
        <td>{{ sleeperScore }}</td>
    </tr>
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
  