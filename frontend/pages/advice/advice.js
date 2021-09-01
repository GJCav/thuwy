// pages/advice/advice.js
const app = getApp()
Page({
    data: {
        admin:false,
        activeTab: 0,
        p1: 0,
        p2: 0,
        pan1: false,
        pan2: false,
        advice_list: [], //建议列表
        checked_list: [], //已审核建议列表
    },
    onLoad(options) {
        wx.setNavigationBarTitle({
            title: '建议反馈'
        })
        this.setData({
          admin:(options.admin=='1')
        })
        this.refresh()
    },
    //封装建议读取函数
    advice(page) {
        let that = this
        return new Promise(function (resolve, reject) {
            wx.request({
                url: app.globalData.url + '/advice/'+(that.data.admin?'':'me/')+'?state=<state>&p=<page>',
                method: 'GET',
                header: {
                    'content-type': 'application/json; charset=utf-8',
                    'cookie': wx.getStorageSync('cookie')
                },
                data: {
                    state: 1,
                    p: page
                },
                success: (res) => {
                    if (res.data.code == 0) {
                        let advice = res.data.advice
                        that.setData({
                            p1: res.data.page,
                        })
                        if (page > 1 && advice.length == 0) {
                            that.setData({
                                pan1: true
                            })
                        }
                        that.setData({
                            advice_list: that.data.advice_list.concat(advice)
                        })
                        resolve()
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
    checked(page) {
        let that = this
        console.log(app.globalData.url + '/advice/'+(that.data.admin?'':'me/')+'?state=<state>&p=<page>')
        return new Promise(function (resolve, reject) {
            wx.request({
                url: app.globalData.url + '/advice/'+(that.data.admin?'':'me/')+'?state=<state>&p=<page>',
                method: 'GET',
                header: {
                    'content-type': 'application/json; charset=utf-8',
                    'cookie': wx.getStorageSync('cookie')
                },
                data: {
                    state: 2,
                    p: page
                },
                success: (res) => {
                    if (res.data.code == 0) {
                        let advice = res.data.advice
                        that.setData({
                            p2: res.data.page,
                        })
                        if (page > 1 && advice.length == 0) {
                            that.setData({
                                pan2: true
                            })
                        }
                        that.setData({
                            checked_list: that.data.checked_list.concat(advice)
                        })
                        resolve()
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
    onPullDownRefresh() {
        this.refresh();
    },
    refresh() {
        var t = this.data.activeTab
        if (t == 0) {
            this.refresh_advice()
        } else {
            this.refresh_checked()
        }
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
    //刷新待审批建议
    refresh_advice() {
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        this.setData({
            advice_list: [],
        })
        this.advice(1).then(function () { //读取未审阅的建议
            wx.hideLoading()
        }).catch(function (res) {
            console.log(res)
            wx.hideLoading();
            wx.showToast({
                title: '连接失败',
                icon: 'error',
                duration: 1500
            });
        })
    },
    //刷新已审批建议
    refresh_checked() {
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        this.setData({
            checked_list: []
        })
        this.checked(1).then(function () { //读取已审阅的建议
            wx.hideLoading()
        }).catch(function (res) {
            console.log(res)
            wx.hideLoading();
            wx.showToast({
                title: '连接失败',
                icon: 'error',
                duration: 1500
            });
        })
    },
    //触底刷新
    onReachBottom() {
        var t = this.data.activeTab
        if (t == 0) {
            this.load_advice()
        } else {
            this.load_checked()
        }
    },
    //加载更多建议信息
    load_advice() {
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        let that = this
        this.setData({
            pan1: false
        })
        this.advice(this.data.p1 + 1).then(function () {
            wx.hideLoading()
            if (that.data.pan1) {
                wx.showToast({
                    title: '没有更多了',
                    icon: 'none',
                    duration: 1500
                })
            }
        }).catch(function (res) {
            console.log(res)
            wx.hideLoading();
            wx.showToast({
                title: '连接失败',
                icon: 'error',
                duration: 1500
            });
        })
    },
    load_checked() {
        wx.showLoading({
            mask: true,
            title: '加载中',
        })
        let that = this
        this.setData({
            pan2: false
        })
        this.checked(this.data.p2 + 1).then(function () {
            wx.hideLoading()
            if (that.data.pan2) {
                wx.showToast({
                    title: '没有更多了',
                    icon: 'none',
                    duration: 1500
                })
            }
        }).catch(function (res) {
            console.log(res)
            wx.hideLoading();
            wx.showToast({
                title: '连接失败',
                icon: 'error',
                duration: 1500
            });
        })
    },
    //意见反馈
    showadvice(e) {
        var id = e.currentTarget.dataset['id']
        wx.navigateTo({
            url: 'admit/admit?id=' + id+'&admin='+this.data.admin,
        })
    },
    addadvice(){
        wx.navigateTo({
            url: 'admit/admit?id=0&admin='+this.data.admin,
        })
    }
})