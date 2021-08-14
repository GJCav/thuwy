// pages/home/home.js
const app = getApp()
Page({
    data: {
        //记录显示
        ddl: null,
        st: ["受理中", "已审批", "已取消", "已结束", "已违约"],
        colst: ["待审批", "未通过", "已通过", "未审批"],
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
    onShow() {
        this.thetime();
        this.refresh(0);
    },
    onPullDownRefresh: function () {
        console.log('home 下拉');
        this.thetime();
        this.refresh(this.data.activeTab);
    },
    //刷新状态
    refresh: function (t) {
        if (app.globalData.userInfo) {
            wx.showLoading({
                mask: true,
                title: '加载中',
            })
            var my_rsvs = [];
            var his_rsvs = [];
            //获取七天前的预约
            wx.request({
                url: app.globalData.url + '/reservation/me?ed=' + this.data.ddl,
                method: 'GET',
                header: {
                    'content-type': 'application/json; charset=utf-8',
                    'cookie': wx.getStorageSync('cookie')
                },
                success: (res) => {
                    if (res.data.code == 0) {
                        his_rsvs = res['my-rsv']
                        wx.hideLoading();
                    } else {
                        console.log(res.data.code, res.data.errmsg);
                        wx.hideLoading();
                        wx.showToast({
                            title: '连接错误',
                            icon: 'error',
                            duration: 1500
                        });
                    }
                },
                fail: (res) => {
                    console.log(res.data.code, res.data.errmsg);
                    wx.hideLoading();
                    wx.showToast({
                        title: '连接失败',
                        icon: 'error',
                        duration: 1500
                    });
                }
            })
            //获取近七天的预约
            wx.request({
                url: app.globalData.url + '/reservation/me?st=' + this.data.ddl,
                method: 'GET',
                header: {
                    'content-type': 'application/json; charset=utf-8',
                    'cookie': wx.getStorageSync('cookie')
                },
                success: (res) => {
                    if (res.data.code == 0) {
                        my_rsvs = res['my-rsv']
                        wx.hideLoading();
                    } else {
                        console.log(res.data.code, res.data.errmsg);
                        wx.hideLoading();
                        wx.showToast({
                            title: '连接错误',
                            icon: 'error',
                            duration: 1500
                        });
                    }
                },
                fail: (res) => {
                    console.log(res.data.code, res.data.errmsg);
                    wx.hideLoading();
                    wx.showToast({
                        title: '连接失败',
                        icon: 'error',
                        duration: 1500
                    });
                }
            })
            //读取设备名称
            var util = require('../../utils/util.js')
            var key = 'item-name'
            for (var i = 0; i < my_rsvs.length; ++i) {
                var value = util.the_name(my_rsvs[i]['item-id'])
                my_rsv[i][key] = value
            }
            for (var i = 0; i < his_rsvs.length; ++i) {
                var value = util.the_name(his_rsvs[i]['item-id'])
                his_rsv[i][key] = value
            }
            //处理需要显示的数据
            var tmp = [];
            if (t == 0) {
                for (var i = 0; i < my_rsvs.length; ++i) {
                    if (this.num(my_rsvs[i].state, 1) || this.num(my_rsvs[i].state, 2) && (this.num(my_rsvs[i].state, 4) || this.num(my_rsvs[i].state, 5))) {
                        tmp = tmp.concat(my_rsvs[i])
                    }
                }
                this.setData({
                    success: tmp
                });
            } else if (t == 1) {
                for (var i = 0; i < my_rsvs.length; ++i) {
                    if (this.num(my_rsvs[i].state, 0)) {
                        tmp = tmp.concat(my_rsvs[i])
                    }
                }
                this.setData({
                    ongoing: tmp
                });
            } else {
                for (var i = 0; i < my_rsvs.length; ++i) {
                    if (this.num(my_rsvs[i].state, 2) && this.num(my_rsvs[i].state, 4) != 1) {
                        tmp = tmp.concat(my_rsvs[i])
                    }
                }
                this.setData({
                    history: tmp.concat(his_rsvs)
                });
            }
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
            ddl: year + '-' + month + '-' + day
        })
        console.log(this.data.ddl);
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
        this.refresh(this.data.activeTab)
    },
    //展示细节
    showdetail(e) {
        var rsvid = e.currentTarget.dataset['id'];
        wx.navigateTo({
            url: '../reservation/reservation?rsvid=' + rsvid + '&who=' + this.data.activeTab % 2,
        })
    },
});