// pages/home/home.js
const app = getApp()

Page({
    data: {
        active: 0
    },
    onLoad: function () {
        wx.setNavigationBarTitle({
            title: '微未央小程序'
        })
    },
    pressTab(event) { // 切换导航栏
        this.setData({
            active: event.detail
        });
    }
})