// pages/administrator/administrator.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
    data: {
        activeTab: 0,
        be_list: [], //管理员申请列表
        admin_list: [], //管理员列表
        user_list: [], //用户列表

        user_clazz: [
            ["行政", "2020级", "2021级"],
            ["未央教务"]
        ],
        grade: [
            ["行政", "2020级", "2021级"]
        ],
        class: [
            ["未央教务"],
            ["未央-建环01", "未央-水木01", "未央-水木02", "未央-环01", "未央-能动01", "未央-能动02", "未央-机械01", "未央-精01", "未央-工01", "未央-电01", "未央-微01", "未央-软件01", "未央-工物01", "未央-材01"],
            ["未央-建环11", "未央-水木11", "未央-水木12", "未央-环11", "未央-能动11", "未央-能动12", "未央-机械11", "未央-精11", "未央-工11", "未央-电11", "未央-微11", "未央-软件11", "未央-工物11", "未央-材11", "未央-材12", "未央-材13"],
        ],
        index: [0, 0]
    },
    onLoad: function (options) {
        wx.setNavigationBarTitle({
            title: '权限管理'
        })
        this.refresh()
    },
    switchTab(e) {
        this.setData({
            activeTab: e.detail.index,
        });
        this.refresh()
    },
    onPullDownRefresh() {
        this.refresh();
        wx.stopPullDownRefresh();
    },
    refresh() {
        var t = this.data.activeTab
        if (t == 0) {
            this.refresh_admin()
        } else if (t == 1) {
            this.refresh_list()
        } else {
            this.refresh_user()
        }
    },
    //刷新用户列表
    refresh_user() {
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        let data = this.data
        console.log(data.class[data.index[0]][data.index[1]])
        wx.request({
            url: app.globalData.url + '/user/?clazz=' + data.class[data.index[0]][data.index[1]],
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
            },
            success: (res) => {
                if (res.data.code == 0) {
                    this.setData({
                        user_list: res.data.profiles
                    });
                    wx.hideLoading()
                } else {
                    wx.hideLoading()
                    util.show_error(res)
                }
            },
            fail: (res) => {
                wx.hideLoading()
                util.show_error(res)
            }
        })
    },
    //刷新管理员列表
    refresh_list() {
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        wx.request({
            url: app.globalData.url + '/admin/',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
            },
            success: (res) => {
                if (res.data.code == 0) {
                    this.setData({
                        admin_list: res.data.profiles
                    });
                    wx.hideLoading()
                } else {
                    wx.hideLoading()
                    util.show_error(res)
                }
            },
            fail: (res) => {
                wx.hideLoading()
                util.show_error(res)
            }
        })
    },
    //刷新管理员申请
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
                    wx.hideLoading()
                    util.show_error(res)
                }
            },
            fail: (res) => {
                wx.hideLoading()
                util.show_error(res)
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
                        duration: 1500,
                        mask: true
                    })
                    this.refresh_admin();
                } else {
                    wx.hideLoading();
                    util.show_error(res)
                }
            },
            fail: (res) => {
                wx.hideLoading();
                util.show_error(res)
            }
        })
    },
    //拒绝请求
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
    //同意请求
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
    //解除权限
    fired(e) {
        let that = this
        let id = e.currentTarget.dataset.value
        wx.showModal({
            title: '提示',
            content: '确认要解除管理员权限?',
            success: (res) => {
                if (res.confirm) {
                    wx.showLoading({
                        mask: true,
                        title: '提交中',
                    })
                    console.log('用户点击确定')
                    //解除权限
                    wx.request({
                        url: app.globalData.url + '/admin/' + id + '/',
                        method: 'DELETE',
                        header: {
                            'content-type': 'application/json; charset=utf-8',
                            'cookie': wx.getStorageSync('cookie')
                        },
                        success: (res) => {
                            if (res.data.code == 0) {
                                wx.hideLoading();
                                wx.showToast({
                                    title: '解除权限成功',
                                    icon: 'success',
                                    duration: 1500,
                                    mask: true
                                })
                                setTimeout(function () {
                                    that.refresh()
                                }, 1500)
                            } else {
                                wx.hideLoading();
                                util.show_error(res)
                            }
                        },
                        fail: (res) => {
                            wx.hideLoading();
                            util.show_error(res)
                        }
                    })
                } else if (res.cancel) {
                    console.log('用户点击取消')
                }
            }
        })
    },
    //选择班级
    choose_clazz(e) {
        console.log('选择班级为', e.detail.value)
        this.setData({
            index: e.detail.value
        })
        this.refresh()
    },
    //改变选择列
    change_column(e) {
        console.log('修改的列为', e.detail.column, '，值为', e.detail.value);
        if (e.detail.column == 0) {
            this.setData({
                'user_clazz[1]': this.data.class[e.detail.value]
            })
        }
    },
    //解除绑定
    unlock(e) {
        let that = this
        let id = e.currentTarget.dataset.value
        wx.showModal({
            title: '提示',
            content: '确认要解绑用户信息?',
            success: (res) => {
                if (res.confirm) {
                    wx.showLoading({
                        mask: true,
                        title: '提交中',
                    })
                    console.log('用户点击确定')
                    //解除权限
                    wx.request({
                        url: app.globalData.url + '/user/' + id + '/',
                        method: 'DELETE',
                        header: {
                            'content-type': 'application/json; charset=utf-8',
                            'cookie': wx.getStorageSync('cookie')
                        },
                        success: (res) => {
                            if (res.data.code == 0) {
                                wx.hideLoading();
                                wx.showToast({
                                    title: '解除权限成功',
                                    icon: 'success',
                                    duration: 1500,
                                    mask: true
                                })
                                setTimeout(function () {
                                    that.refresh()
                                }, 1500)
                            } else {
                                wx.hideLoading();
                                util.show_error(res)
                            }
                        },
                        fail: (res) => {
                            wx.hideLoading();
                            util.show_error(res)
                        }
                    })
                } else if (res.cancel) {
                    console.log('用户点击取消')
                }
            }
        })
    }
})