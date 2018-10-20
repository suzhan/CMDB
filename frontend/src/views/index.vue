<template>
    <div id="app" class="app">
        <app-header></app-header>
        <app-main></app-main>
    </div>
</template>

<script>
    import AppHeader from '@/components/AppHeader.vue'
    import AppMain from '@/components/AppMain.vue'

    export default {
        name: "index",
        components: {
            AppHeader,
            AppMain
        },
        computed: {

        }
    }
</script>

<style scoped>
	html, body {
		height: 100%;
	}
	body {
		font-family: 'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif;
		font-size: 14px;
	}
	.app {
		height: 100%;
		min-height: 100%;
	}
</style>