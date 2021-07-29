// pages/home/home.js
const app = getApp()
Page({
    data: {
        activeTab: 0,
        kind: 'success',
        refresh: ''
    },
    onLoad() {
        wx.setNavigationBarTitle({
            title: '我的信息'
        })
        if (app.globalData.userInfo) {
            wx.request({
                url: app.globalData.url + '/querymyrsv?st=<start-time>&ed=<end-time>&state=<state>',
                method: 'GET',
                data: {
                    code: res.code
                },
                success: res => {

                }
            })
        } else {
            wx.showToast({
                title: '未绑定信息',
                icon: 'error',
                duration: 1000
            });
        }
    },
    onPullDownRefresh: function () {
        console.log('home 下拉');
        this.setData({
            refresh: Date.now()
        })
    },

    switchTab(e) {
        switch (e.detail.index) {
            case 0:
                this.setData({
                    kind: 'success',
                    activeTab: 0
                });
                break;
            case 1:
                this.setData({
                    kind: 'ongoing',
                    activeTab: 1
                });
                break;
            case 2:
                this.setData({
                    kind: 'history',
                    activeTab: 2
                });
                break;
        }
    }
});