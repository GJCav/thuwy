// pages/home/home.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
    data: {
        //记录显示
        ddl: null,
        colst: ["受理中", "未通过", "已通过", "已取消", "已违约"],
        success: [],
        ongoing: [],
        history: [],
        activeTab: 0,
    },
    num: function (x, t) {
        return (x >> t) % 2
    },
    onLoad() {
        wx.setNavigationBarTitle({
            title: '我的信息'
        })
    },
    onTabItemTap() {
        // this.thetime();
        this.refresh();
    },
    onPullDownRefresh: function () {
        // this.thetime();
        this.refresh();
        wx.stopPullDownRefresh();
    },
    //报错函数
    bug(res) {
        wx.hideLoading();
        util.show_error(res)
    },
    //封装读取函数
    waiting() { //获取待审批预约
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        wx.request({
            url: app.globalData.url + '/reservation/me/?state=1',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'Session': wx.getStorageSync('Session')
            },
            success: (res) => {
                let that = this
                if (res.data.code == 0) {
                    that.setData({
                        ongoing: that.data.ongoing.concat(res.data['my-rsv'])
                    })
                    wx.hideLoading()
                } else {
                    this.bug(res);
                }
            },
            fail: (res) => {
                this.bug(res);
            }
        })
    },
    going() { //获取进行中预约
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        wx.request({
            url: app.globalData.url + '/reservation/me/?state=2',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'Session': wx.getStorageSync('Session')
            },
            success: (res) => {
                let that = this
                if (res.data.code == 0) {
                    that.setData({
                        success: that.data.success.concat(res.data['my-rsv'])
                    })
                    wx.hideLoading()
                } else {
                    this.bug(res);
                }
            },
            fail: (res) => {
                this.bug(res);
            }
        })
    },
    history() { //获取历史预约
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        wx.request({
            url: app.globalData.url + '/reservation/me/?state=4',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'Session': wx.getStorageSync('Session')
            },
            success: (res) => {
                let that = this
                if (res.data.code == 0) {
                    that.setData({
                        history: that.data.success.concat(res.data['my-rsv'])
                    })
                    wx.hideLoading()
                } else {
                    this.bug(res);
                }
            },
            fail: (res) => {
                this.bug(res);
            }
        })
    },
    //刷新状态
    refresh: function () {
        var t = this.data.activeTab
        if (app.globalData.login) {
            if (app.globalData.userInfo) {
                this.setData({
                    success: [],
                    ongoing: [],
                    history: [],
                })
                if (t == 0)
                    this.going();
                else if (t == 1)
                    this.waiting();
                else
                    this.history();
            } else {
                wx.showToast({
                    title: '未绑定信息',
                    icon: 'error',
                    duration: 1500,
                    mask: true
                });
            }
        } else {
            wx.showToast({
                title: '未成功登录',
                icon: 'error',
                duration: 1500,
                mask: true
            });
        }
    },
    //更新时间
    thetime() {
        function getThisMonthDays(year, month) {
            return new Date(year, month, 0).getDate();
        }
        const date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        if (day > 8)
            day = day - 8;
        else if (month > 1) {
            month = month - 1;
            var monthLength = getThisMonthDays(year, month);
            day = monthLength - (8 - day);
        } else {
            year = year - 1;
            month = 12;
            var monthLength = getThisMonthDays(year, 11);
            day = monthLength - (8 - day);
        }
        this.setData({
            ddl: year + (month < 10 ? '-0' : '-') + month + (day < 10 ? '-0' : '-') + day
        })
    },
    //转换选择
    switchTab(e) {
        this.setData({
            activeTab: e.detail.index,
        });
        this.refresh()
    },
    //展示细节
    showdetail(e) {
        var rsvid = e.currentTarget.dataset['id'];
        wx.navigateTo({
            url: '../reservation/reservation?rsvid=' + rsvid + '&who=' + (this.data.activeTab % 2),
        })
    },
});