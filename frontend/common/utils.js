const login(that){
	uni.getUserProfile({ // 获取用户微信信息
		desc: '展示用户信息'
	}).then(res => { // 登录微信账号
		console.log(res)
		that.globalData.wxprofile=res.userInfo
		return uni.login()
	}).then(res => { // 获取openID
		return uni.request({ // 发送 res.code 到后台换取 openId, sessionKey, unionId
			url: that.globalData.url.backend + '/login/',
			method: 'POST',
			data: {
				code: res.code
			}
		})
	}).then(res => { // 储存openID并请求用户信息
		if (res.data.code == 0) {
			uni.setStorage({ // 将得到的openid存储到缓存里面方便后面调用
				key: "cookie",
				data: res.cookies[0]
			})
			console.log(res.cookies)
			return uni.request({
				url: that.globalData.url.backend + '/profile/',
				method: 'GET',
				header: {
					'content-type': 'application/json; charset=utf-8',
					'cookie': res.cookies[0]
				},
			})
		} else {
			throw res
		}
	}).then(res => { // 储存用户信息
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
	}).catch(err => {
		console.log(err)
	})
}
module.exports = {
	login: login,
}