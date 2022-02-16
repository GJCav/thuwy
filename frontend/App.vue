<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
			let that = this
			uni.login().then(res => {
					return uni.request({ // 发送 res.code 到后台换取 openId, sessionKey, unionId
						url: that.globalData.url.backend + '/login/',
						method: 'POST',
						data: {
							code: res.code
						}
					})
				},
			).then(res => {
				if (res.data.code == 0) {
					that.globalData.login = true;
					uni.setStorage({ // 将得到的openid存储到缓存里面方便后面调用
						key: "cookie",
						data: res.cookies[0]
					})
				}
				console.log(res.cookies)
			})
		},
		globalData: {
			login: false, // 是否以微信账号登录
			profile: null, // 用户账号信息
			url: {
				// backend: 'https://api.thuwy.top', // 后端地址
				// picture: 'https://https://static.thuwy.top', // 图片站地址
				// website: 'https://https://web.thuwy.top/api' // 网页后端地址
				backend: 'https://dev-api.thuwy.top', // 开发后端地址
				picture: 'https://dev-static.thuwy.top', // 开发图片站地址
				website:'https://dev-web.thuwy.top/api' // 开发网页后端地址
				
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
</style>
