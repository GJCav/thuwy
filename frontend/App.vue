<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
			let that = this

			// 正式代码
			// uni.login().then(res => { // 获取openID
			// 	return uni.request({ // 发送 res.code 到后台换取 openId, sessionKey, unionId
			// 		url: that.globalData.url.backend + '/login/',
			// 		method: 'POST',
			// 		data: {
			// 			code: res.code
			// 		}
			// 	})
			// }).then(res => { // 储存openID并请求用户信息
			// 	if (res.data.code == 0) {
			// 		uni.setStorage({ // 将得到的openid存储到缓存里面方便后面调用
			// 			key: "cookie",
			// 			data: res.cookies[0]
			// 		})
			// 		console.log(res.cookies)
			// 		return uni.request({
			// 			url: that.globalData.url.backend + '/profile/',
			// 			method: 'GET',
			// 			header: {
			// 				'content-type': 'application/json; charset=utf-8',
			// 				'cookie': res.cookies[0]
			// 			},
			// 		})
			// 	} else {
			// 		throw res
			// 	}
			// }).then(res => { // 储存用户信息
			// 	if (res.data.code == 0) {
			// 		that.globalData.profile = {
			// 			name: res.data.name,
			// 			class: res.data.clazz,
			// 			id: res.data['school-id'],
			// 			privileges: res.data.privileges
			// 		}
			// 		console.log(that.globalData.profile)
			// 		that.globalData.login = true;
			// 	} else {
			// 		throw res
			// 	}
			// }).catch(err => {
			// 	console.log(err)
			// })
			
			// 开发代码
			uni.request({
				url: that.globalData.url.backend + '/testaccount/super_admin/'
			}).then(res => {
				uni.setStorage({ // 将得到的openid存储到缓存里面方便后面调用
					key: "cookie",
					data: res.cookies[0]
				})
				uni.request({
					url: that.globalData.url.backend + '/profile/',
					method: 'GET',
					header: {
						'content-type': 'application/json; charset=utf-8',
						'cookie': wx.getStorageSync('cookie')
					},
				}).then(res => {
					if (res.data.code == 0) {
						that.globalData.profile = {
							name: res.data.name,
							class: res.data.clazz,
							id: res.data['school-id'],
							privileges: res.data.privileges
						}
						console.log(that.globalData.profile)
						that.globalData.login = true;
					} else {
						throw res
					}
				}).catch(res=>{
					console.log(res)
				})
			})
		},
		globalData: {
			login: false, // 是否完成登录
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
</style>
