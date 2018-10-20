<template>
	<div class="app-header">
		<div class="h-container clearfix">
			<div class="header-company clearfix">
				<div class="h-company-logo"></div>
				<div class="h-appname">{{ AppName }}</div>
			</div>
			<div  class="header-nav">
                <el-menu
                      :default-active="activeIndex"
                      class="app-header-nav"
                      mode="horizontal"
                      @select="handleSelect"
                      background-color="#545c64"
                      text-color="#fff"
                      active-text-color="#ffd04b">
                      <el-menu-item index="1"><router-link to="/node">主机</router-link></el-menu-item>
                      <el-menu-item index="2"><router-link to="/software">软件</router-link></el-menu-item>
                      <el-menu-item index="3"><router-link to="/properties">配置文件</router-link></el-menu-item>
                      <el-menu-item index="4"><router-link to="/person">人员</router-link></el-menu-item>
                    </el-menu>
			</div>
		</div>
	</div>
</template>


<script>
    export default {
        name: 'AppHeader',
        data () {
            return {
                activeIndex: '1',
				AppName: '资源平台'
            }
        },
		methods: {
            handleSelect(key, keyPath) {
                // console.log(key, keyPath);
			}
		}
    }
</script>


<style lang="scss">

    body {
       background-image: url("../assets/furley-bg.png");
    }

    /*A { text-decoration: none}*/
	.app-header {
		position: fixed;
		top: 0;
		left: 0;
		z-index: 1000;
		width: 100%;
		min-height: 60px;
		background: #545c64;
	}
	.h-container {
		max-width: 1280px;
		height: 100%;
		margin: 0 auto;
	}
	.header-company {
		float: left;
		min-width: 250px;
		padding-right: 15px;
		height: 60px;
        line-height: 60px;


		/*.h-company-logo {*/
			/*float: left;*/
			/*width: 40px;*/
			/*height: 40px;*/
			/*padding: 10px;*/

			/*img {*/
				/*display: inline-block;*/
				/*width: 100%;*/
				/*height: 100%;*/
			/*}*/
		/*}*/

		.h-appname {
			float: left;
			width: 80px;
			height: 60px;
			/*padding: 10px;*/
            color: #fff;
            font-size: 20px;

		}

		.h-company-name {
			float: left;
			height: 60px;
			line-height: 60px;
			font-size: 20px;
			color: #363f44;
		}
	}

	.header-nav {
		float: right;
	}

    /*.app-header-nav {*/
        /*font-size: 20px;*/
    /*}*/

	.app-header-nav {
		background: #f8f8f8;
		color: #303133;

		.el-menu-item {
			border-bottom: 0;
			color: #303133;
            font-size: 18px;
            text-decoration: none;

			&:hover {
				background: rgba(255, 255, 255, 0.7);
                text-decoration: none;
			}
			&.is-active {
				color: #303133;
				border-bottom: 0;
				background: rgba(255, 255, 255, 0.7);
                text-decoration: none;
			}
		}
		.el-submenu .el-submenu__title {
			color: #303133;

			&:hover {
				background: rgba(255, 255, 255, 0.7);
                text-decoration: none;
			}
		}
	}

</style>