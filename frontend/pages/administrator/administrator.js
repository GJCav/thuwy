// pages/administrator/administrator.js
const app = getApp()
Page({
    data: {
        activeTab: 0,
        be_list: [], //管理员申请列表
        admin_list: [], //管理员列表
    },
    onLoad: function (options) {
        wx.setNavigationBarTitle({
            title: '权限管理'
        })
        this.refresh()
    },
    switchTab(e) {
        switch (e.detail.index) {
            case 0:
                this.setData({
                    activeTab: 0,
                });
                break;
            case 1:
                this.setData({
                    activeTab: 1
                });
                break;
        }
        this.refresh()
    },
    onPullDownRefresh() {
        this.refresh();
    },
    refresh() {
        var t = this.data.activeTab
        if (t == 0) {
            this.refresh_admin()
        } else {

        }
    },
    refresh_admin() {
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        wx.request({
            url: app.globalData.url + '/admin/request/',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
            },
            success: (res) => {
                if (res.data.code == 0) {
                    this.setData({
                        be_list: res.data.list
                    });
                    wx.hideLoading()
                } else {
                    console.log(res)
                    wx.hideLoading()
                    wx.showToast({
                        title: '连接错误',
                        icon: 'error',
                        duration: 1500
                    })
                }
            },
            fail: (res) => {
                console.log(res)
                wx.hideLoading()
                wx.showToast({
                    title: '连接失败',
                    icon: 'error',
                    duration: 1500
                })
            }
        })
    },
    //调整管理员
    req: function (id, p) {
        wx.showLoading({
            mask: true,
            title: '提交中',
        })
        wx.request({
            url: app.globalData.url + '/admin/request/' + id + '/',
            method: 'POST',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
            },
            data: {
                pass: p,
                reason: ""
            },
            success: (res) => {
                if (res.data.code == 0) {
                    wx.hideLoading();
                    wx.showToast({
                        title: '审批成功',
                        icon: 'success',
                        duration: 1500
                    })
                    this.refresh_admin();
                } else {
                    console.log(res)
                    wx.hideLoading();
                    wx.showToast({
                        title: '连接错误',
                        icon: 'error',
                        duration: 1500
                    })
                }
            },
            fail: (res) => {
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
    refuse(e) {
        let value = e.currentTarget.dataset.value
        wx.showModal({
            title: '提示',
            content: '确认要拒绝管理员申请?',
            success: (res) => {
                if (res.confirm) {
                    console.log('用户点击确定')
                    this.req(value, 0)
                } else if (res.cancel) {
                    console.log('用户点击取消')
                }
            }
        })
    },
    approve(e) {
        let value = e.currentTarget.dataset.value
        wx.showModal({
            title: '提示',
            content: '确认要同意管理员申请?',
            success: (res) => {
                if (res.confirm) {
                    console.log('用户点击确定')
                    this.req(value, 1)
                } else if (res.cancel) {
                    console.log('用户点击取消')
                }
            }
        })
    },
    fired(e) {
        wx.showToast({
            title: '功能尚未开通',
            icon: 'error',
            duration: 1500
        });
    }
})