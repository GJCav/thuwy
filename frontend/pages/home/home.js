// pages/home/home.js
const app = getApp()
const util = require('../../utils/util.js')
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
        this.refresh(this.data.activeTab);
    },
    onPullDownRefresh: function () {
        console.log('home 下拉');
        this.thetime();
        this.refresh(this.data.activeTab);
    },
    //封装读取函数
    before(ddl) { //获取七天前的预约
        return new Promise(function (resolve, reject) {
            wx.showLoading({
                mask: true,
                title: '加载中',
            })
            var his_rsvs = [];
            wx.request({
                url: app.globalData.url + '/reservation/me?ed=' + ddl,
                method: 'GET',
                header: {
                    'content-type': 'application/json; charset=utf-8',
                    'cookie': wx.getStorageSync('cookie')
                },
                success: (res) => {
                    if (res.data.code == 0) {
                        his_rsvs = res.data['my-rsv']
                        //读取设备名称       
                        for (let i in his_rsvs) {
                            let item = his_rsvs[i]
                            util.the_name(item['item-id']).then(function (value) {
                                item.name = value                            
                            }).catch(function (res) {
                                reject(res)
                            })
                        }
                        resolve(his_rsvs)
                    } else {
                        reject(res)
                    }
                },
                fail: (res) => {
                    reject(res)
                }
            })
        })
    },
    after(ddl) { //获取近七天的预约
        return new Promise(function (resolve, reject) {
            wx.showLoading({
                mask: true,
                title: '加载中',
            })
            var my_rsvs = [];
            wx.request({
                url: app.globalData.url + '/reservation/me?st=' + ddl,
                method: 'GET',
                header: {
                    'content-type': 'application/json; charset=utf-8',
                    'cookie': wx.getStorageSync('cookie')
                },
                success: (res) => {
                    if (res.data.code == 0) {
                        my_rsvs = res.data['my-rsv']
                        //读取设备名称
                        for (let i in my_rsvs) {
                            let item = my_rsvs[i]
                            util.the_name(item['item-id']).then(function (value) {
                                item.name = value
                            }).catch(function (res) {
                                reject(res)
                            })
                        }
                        resolve(my_rsvs)
                    } else {
                        console.log(res.data.code, res.data.errmsg);
                        reject()
                    }
                },
                fail: (res) => {
                    reject(res)
                }
            })
        })
    },
    //刷新状态
    refresh: function (t) {
        if (app.globalData.userInfo) {
            wx.showLoading({
                title: '加载中',
                mask: true
            })
            var my_rsvs = [];
            var his_rsvs = [];
            let that = this
            that.before(that.data.ddl).then(function (res1) {
                his_rsvs = res1
                that.after(that.data.ddl).then(function (res2) {
                    my_rsvs = res2;
                    //处理需要显示的数据
                    var tmp = [];
                    if (t == 0) {
                        for (let i in my_rsvs) {
                            if (that.num(my_rsvs[i].state, 1) || that.num(my_rsvs[i].state, 2) && (that.num(my_rsvs[i].state, 4) || that.num(my_rsvs[i].state, 5))) {
                                tmp = tmp.concat(my_rsvs[i])
                            }
                        }
                        that.setData({
                            success: tmp
                        });
                    } else if (t == 1) {
                        for (let i in my_rsvs) {
                            if (that.num(my_rsvs[i].state, 0)) {
                                tmp = tmp.concat(my_rsvs[i])
                            }
                        }
                        that.setData({
                            ongoing: tmp
                        });
                    } else {
                        for (let i in my_rsvs) {
                            if (that.num(my_rsvs[i].state, 2) && that.num(my_rsvs[i].state, 4) != 1) {
                                tmp = tmp.concat(my_rsvs[i])
                            }
                        }
                        that.setData({
                            history: tmp.concat(his_rsvs)
                        });
                    }
                    wx.hideLoading()
                }).catch(function (res) {
                    console.log(res.code,res.errmsg)
                    wx.hideLoading();
                    wx.showToast({
                        title: '连接失败',
                        icon: 'error',
                        duration: 1500
                    });
                })
            }).catch(function (res) {
                console.log(res.code,res.errmsg)
                wx.hideLoading();
                wx.showToast({
                    title: '连接失败',
                    icon: 'error',
                    duration: 1500
                });
            })
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
            ddl: year + (month<10?'-0':'-') + month +(day<10?'-0':'-') + day
        })
        console.log(this.data.ddl); //七日前的日期
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
        var name=e.currentTarget.dataset['name']
        wx.navigateTo({
            url: '../reservation/reservation?rsvid=' + rsvid + '&who=' + (this.data.activeTab % 2)+'&name='+name,
        })
    },
});