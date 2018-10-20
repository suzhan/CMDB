<template>
	<div class="app-container">
		<div class="app-view">
			<div class="app-main">
				<router-view></router-view>
			</div>
		</div>
	</div>
</template>


<script>

	export default {
		name: 'AppMain',
		data () {
			return {

			}
		},
		computed: {

		},
		methods: {

		},
		mounted() {

		}
	}
</script>


<style lang="scss" scoped>
	.app-container {
		min-height: 100%;
		/*background: #1C2B36;*/

		.app-view {
			padding: 70px 0 50px 0;
		}

		.app-main {
			min-width: 1024px;
			max-width: 1280px;
			/*min-height: 600px;*/
			min-height: 100%;
			margin: 0 auto;
			background: #fff;
			border-radius: 5px;
			background-image: url("../assets/light-main-bg.png");
		}
	}
</style>