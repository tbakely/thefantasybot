<template>
    <tr :class="{ checked: drafted }">
        <td>{{ id }}</td>
        <td>{{ player }}</td>
        <td>{{ position }}</td>
        <td>{{ valueScore }}</td>
        <td>{{ adp }}</td>
        <td>{{ sleeperScore }}</td>
        <td>{{ tier }}</td>
        <td><input type="checkbox" @click="toggleDrafted" :checked="drafted"></td>
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
        tier: {
            type: Number,
            required: true
        },
        drafted: {
            type: Boolean,
            required: true
        },
    },
    emits: ['toggle-drafted'],
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
            isDrafted: true,
        };
    },
    methods: {
        toggleDetails() {
            this.detailsAreVisible = !this.detailsAreVisible;
        },
        toggleFavorite() {
            this.$emit('toggle-favorite', this.id);
        },
        toggleDrafted() {
            this.$emit('toggle-drafted', this.id);
        }
    },
};
</script>

<style></style>
  