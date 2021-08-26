// pages/home/home.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
    data: {
        //记录显示
        ddl: null,
        colst: ["受理中", "未通过", "已通过", "已取消","已违约"],
        success: [],
        ongoing: [],
        history: [],
        activeTab: 0,
    },
    num: function (x, t) {
        return parseInt(x / Math.pow(2, t)) % 2
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
    },
    //报错函数
    bug(res) {
        console.log(res.data.code, res.data.errmsg)
        wx.hideLoading();
        wx.showToast({
            title: '连接失败',
            icon: 'error',
            duration: 1500
        });
    },
    //封装读取函数
    waiting() { //获取待审批预约
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        var rsvs = [];
        var flag = false;
        var msg = null;
        wx.request({
            url: app.globalData.url + '/reservation/me?state=1',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
            },
            success: (res) => {
                let that = this
                if (res.data.code == 0) {
                    rsvs = res.data['my-rsv']
                    //读取设备名称       
                    for (var i = rsvs.length - 1; i >= 0; --i) {
                        let item = rsvs[i]
                        util.the_name(item['item-id']).then(function (value) {
                            item.name = value
                            that.setData({
                                ongoing: that.data.ongoing.concat(item)
                            })
                        }).catch(function (res) {
                            flag = true
                            msg = res
                        })
                    }
                    if (flag) {
                        this.bug(msg)
                    } else {
                        wx.hideLoading()
                    }
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
        var rsvs = [];
        var flag = false;
        var msg = null;
        wx.request({
            url: app.globalData.url + '/reservation/me?state=2',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
            },
            success: (res) => {
                let that = this
                if (res.data.code == 0) {
                    rsvs = res.data['my-rsv']
                    //读取设备名称
                    for (var i = rsvs.length - 1; i >= 0; --i) {
                        let item = rsvs[i]
                        util.the_name(item['item-id']).then(function (value) {
                            item.name = value
                            that.setData({
                                success: that.data.success.concat(item)
                            })
                        }).catch(function (res) {
                            flag = true
                            msg = res
                        })
                    }
                    if (flag) {
                        this.bug(msg)
                    } else {
                        wx.hideLoading()
                    }
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
        var rsvs = [];
        var flag = false;
        var msg = null;
        wx.request({
            url: app.globalData.url + '/reservation/me?state=4',
            method: 'GET',
            header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
            },
            success: (res) => {
                let that = this
                if (res.data.code == 0) {
                    rsvs = res.data['my-rsv']
                    //读取设备名称
                    for (var i = rsvs.length - 1; i >= 0; --i) {
                        let item = rsvs[i]
                        util.the_name(item['item-id']).then(function (value) {
                            item.name = value
                            that.setData({
                                history: that.data.history.concat(item)
                            })
                        }).catch(function (res) {
                            flag = true
                            msg = res
                        })
                    }
                    if (flag) {
                        this.bug(msg)
                    } else {
                        wx.hideLoading()
                    }
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
                duration: 1500
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
            case 2:
                this.setData({
                    activeTab: 2
                });
                break;
        }
        this.refresh()
    },
    //展示细节
    showdetail(e) {
        var rsvid = e.currentTarget.dataset['id'];
        var name = e.currentTarget.dataset['name']
        wx.navigateTo({
            url: '../reservation/reservation?rsvid=' + rsvid + '&who=' + (this.data.activeTab % 2) + '&name=' + name,
        })
    },
});