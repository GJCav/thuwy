// pages/home/home.js
const app = getApp()
Page({
    data: {
        ddl: null,
        st: ["受理中", "已审批", "已取消", "已结束"],
        colst: ["待审批", "未通过", "已通过", "未审批"],
        my_rsvs: [{
            id: 236237236,
            item_id: 1001,
            state: 2
        }, {
            id: 328392832,
            item_id: 1002,
            state: 4
        }, {
            id: 20200148394,
            item_id: 1003,
            state: 6
        }, {
            id: 20200148394,
            item_id: 1004,
            state: 8
        }, {
            id: 20200148394,
            item_id: 1005,
            state: 10
        }, {
            id: 20200148394,
            item_id: 1007,
            state: 14
        }],
        his_rsvs: [{
            id: 20200148394,
            item_id: 1006,
            state: 4
        }, ],
        activeTab: 0,
        kind: 'success',
        refresh: ''
    },
    onLoad() {
        wx.setNavigationBarTitle({
            title: '我的信息'
        })
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
            if (t == 2) {
                this.refresh();
                //获取七天外的预约
                wx.request({
                    url: app.globalData.url + '/querymyrsv?ed=' + this.data.ddl,
                    method: 'GET',
                    data: {
                        code: wx.getStorageSync('openid')
                    },
                    success: res => {
                        if (res.code == 0) {
                            this.setData({
                                his_rsvs: res.my_rsv
                            })
                        } else {
                            console.log(res.code, res.errmsg);
                            wx.showToast({
                                title: '获取信息失败',
                                icon: 'error',
                                duration: 1500
                            });
                        }
                    }
                })
            } else {
                wx.request({
                    url: app.globalData.url + '/querymyrsv?st=' + this.data.ddl,
                    method: 'GET',
                    data: {
                        code: wx.getStorageSync('openid')
                    },
                    success: res => {
                        if (res.code == 0) {
                            this.setData({
                                my_rsvs: res.my_rsv
                            })
                        } else {
                            console.log(res.code, res.errmsg);
                            wx.showToast({
                                title: '获取信息失败',
                                icon: 'error',
                                duration: 1500
                            });
                        }
                    }
                })
            }
        } else {
            wx.showToast({
                title: '未绑定信息',
                icon: 'error',
                duration: 1500
            });
        }
    },
    thetime() {
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
    switchTab(e) {
        switch (e.detail.index) {
            case 0:
                this.setData({
                    kind: 'success',
                    activeTab: 0,
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
        this.refresh(this.data.activeTab)
    }
});