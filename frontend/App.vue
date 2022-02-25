<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		globalData: {
			login: false, // 是否完成登录
			bind:false, // 是否绑定信息
			profile: null, // 用户账号信息
			url: {
				// backend: 'https://api.thuwy.top', // 后端地址
				// picture: 'https://https://static.thuwy.top', // 图片站地址
				// website: 'https://https://web.thuwy.top/api' // 网页后端地址
				backend: 'https://dev-api.thuwy.top', // 开发后端地址
				picture: 'https://dev-static.thuwy.top', // 开发图片站地址
				website: 'https://dev-web.thuwy.top/api' // 开发网页后端地址
			}
		}
	}
</script>

<!-- 每个页面公共css -->
<style lang="scss">
	/* 弹性容器 */
	@mixin flex-container {
		display: flex;
		align-items: center;
		justify-content: center;
		box-sizing: border-box;
	}


	.col-container {
		width: 100%;
		flex-direction: column;
		@include flex-container;

	}

	.row-container {
		width: 100%;
		flex-direction: row;
		@include flex-container;
	}
	
	.row-reverse-container {
		width: 100%;
		flex-direction: row-reverse;
		@include flex-container;
	}
</style>
