// 登录函数
function logIn(app) {
	// 正式代码
	// uni.showLoading({
	// 	title: '登陆中',
	// 	mask: true
	// }).then(() => {
	// 	return uni.login()
	// }).then(res => { // 获取openID
	// 	return uni.request({ // 发送 res.code 到后台换取 openId, sessionKey, unionId
	// 		url: app.globalData.url.backend + '/login/',
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
	// 		return uni.request({
	// 			url: app.globalData.url.backend + '/profile/',
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
	// 		app.globalData.profile = {
	// 			name: res.data.name,
	// 			class: res.data.clazz,
	// 			id: res.data['school-id'],
	// 			privileges: res.data.privileges
	// 		}
	// 		console.log(app.globalData.profile)
	// 		app.globalData.login = true;
	// 		app.globalData.bind = (app.globalData.profile.id != null)
	// 		uni.hideLoading()
	// 	} else {
	// 		throw res
	// 	}
	// }).catch(err => {
	// 	console.log(err)
	// 	uni.hideLoading()
	// 	uni.showToast({
	// 		title: '微信登录失败',
	// 		mask: true,
	// 		icon: 'error'
	// 	})
	// })

	// 开发代码
	uni.showLoading({
		title: '登陆中',
		mask: true
	}).then(() => {
		return uni.request({
			url: app.globalData.url.backend + '/testaccount/super_admin/'
		})
	}).then(res => {
		uni.setStorage({ // 将得到的openid存储到缓存里面方便后面调用
			key: "cookie",
			data: res.cookies[0]
		})
		return uni.request({
			url: app.globalData.url.backend + '/profile/',
			method: 'GET',
			header: {
				'content-type': 'application/json; charset=utf-8',
				'cookie': wx.getStorageSync('cookie')
			},
		})
	}).then(res => {
		if (res.data.code == 0) {
			app.globalData.profile = {
				name: res.data.name,
				class: res.data.clazz,
				id: res.data['school-id'],
				privileges: res.data.privileges
			}
			console.log(app.globalData.profile)
			app.globalData.login = true
			app.globalData.bind = (app.globalData.profile.id != null)
			uni.hideLoading()
		} else {
			throw res
		}
	}).catch(err => {
		console.log(err)
		uni.hideLoading()
		uni.showToast({
			title: '微信登录失败',
			mask: true,
			icon: 'error'
		})
	})
}


// 图片上传代码
function uploadPic(name, tmpurl) {
	const app = getApp()
	return new Promise((resolve, reject) => {
		uni.request({ // 获取图片上传地址
			url: app.globalData.url.website + '/uploadurl/' + name,
			method: 'GET',
			header: {
				'content-type': 'text/plain',
			}
		}).then(res => { // 上传图片
			console.log(res)
			if (res.statusCode == 200 & res.data.code == 0) {
				return uni.uploadFile({
					url: app.globalData.url.website + '/upload/' + name,
					filePath: tmpurl,
					name: 'file', // 这里固定为"file"
				})
			} else {
				throw res
			}
		}).then(res => {
			var obj = JSON.parse(res.data)
			if (obj.code == 0) {
				console.log(obj.data)
				resolve(obj.data)
			} else {
				throw res
			}
		}).catch(err => {
			reject(err)
		})
	})
}

// 时间戳转通用时间
function changeTime(stamp) {
	let now = new Date();
	let diff = parseInt((now.getTime() - stamp) / 1000)
	if (diff < 60) {
		return diff + '秒前'
	} else if (diff < 3600) {
		return parseInt(diff / 60) + '分钟前'
	} else if (diff < 86400) {
		return parseInt(diff / 3600) + '小时前'
	} else if (diff < 259200) {
		return parseInt(diff / 86400) + '天前'
	} else if (diff < 378432000) {
		return parseInt(diff / 259200) + '月前'
	} else {
		return parseInt(diff / 378432000) + '年前'
	}
}

// 错误信息显示函数
function errInfo(res, title) {
	console.log(res)
	uni.showToast({
		title: title,
		mask: true,
		icon: 'error'
	})
}
export default {
	logIn,
	errInfo,
	uploadPic,
	changeTime
}
