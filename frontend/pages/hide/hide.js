// pages/hide/hide.js
const app = getApp()
Page({
    onLoad: function (options) {
        wx.setNavigationBarTitle({
            title: '测试界面'
        })
    },
    be_admin() {
        wx.showLoading({
            title: '加载中',
            mask: true
        })
        wx.request({
            timeout: 5000,
            url: app.globalData.url + '/test/login/?mode=admin',
            method: 'GET',
            success: res => {
                wx.clearStorageSync()
                wx.setStorage({ //将得到的openid存储到缓存里面方便后面调用
                    key: "Session",
                    data: res.header["Session"]
                })
                app.globalData.login = true
                app.globalData.isadmin = true
                app.globalData.userInfo = true
                wx.hideLoading()
                wx.showToast({
                  title: '登录成功',
                  icon: 'success',
                  duration: 1500,
                  mask: true
                })
                setTimeout(function () {
                  wx.navigateBack({
                    delta: 1
                  })
                }, 1500)
            },
            fail: res => {
                console.log(res)
                wx.hideLoading();
                wx.showToast({
                    title: '连接失败',
                    icon: 'error',
                    duration: 1500
                });
            }
        })
    },
    be_user() {
        wx.showLoading({
            title: '加载中',
            mask: true
        })
        wx.request({
            timeout: 5000,
            url: app.globalData.url + '/test/login/?mode=user',
            method: 'GET',
            success: res => {
                wx.clearStorageSync()
                wx.setStorage({ //将得到的openid存储到缓存里面方便后面调用
                    key: "Session",
                    data: res.header["Session"]
                })
                app.globalData.login = true
                app.globalData.isadmin = false
                app.globalData.userInfo = true
                wx.hideLoading()
                wx.showToast({
                  title: '登录成功',
                  icon: 'success',
                  duration: 1500,
                  mask: true
                })
                setTimeout(function () {
                  wx.navigateBack({
                    delta: 1
                  })
                }, 1500)
            },
            fail: res => {
                console.log(res)
                wx.hideLoading();
                wx.showToast({
                    title: '连接失败',
                    icon: 'error',
                    duration: 1500
                });
            }
        })
    }
})