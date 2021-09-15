// pages/advice/admit/admit.js
const app = getApp()
const util = require('../../../utils/util.js') 
Page({
    data: {
        id: 0,
        title: '',
        text: '',
        answer: '',
        admin: false,
        advice_detail: {},
    },
    onLoad: function (options) {
        this.setData({
            id: options.id,
            admin: (options.admin == 'true')
        })
        wx.setNavigationBarTitle({
            title: '建议反馈'
        })
        if (this.data.id != 0) {
            wx.showLoading({
                mask: true,
                title: '加载中',
            })
            wx.request({
                url: app.globalData.url + '/advice/' + this.data.id + '/',
                method: 'GET',
                header: {
                    'content-type': 'application/json; charset=utf-8',
                    'cookie': wx.getStorageSync('cookie')
                },
                success: (res) => {
                    if (res.data.code == 0) {
                        this.setData({
                            advice_detail: res.data.advice
                        })
                        wx.hideLoading()
                    } else {
                        wx.hideLoading()
                        util.show_error(res)
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
        }
    },
    //获取内容
    inputitle(e) {
        this.setData({
            title: e.detail.value
        });
    },
    inputanswer(e) {
        this.setData({
            answer: e.detail.value
        })
    },
    inputext(e) {
        this.setData({
            text: e.detail.value
        });
    },
    //提交建议
    addadvice() {
        if (this.data.id == 0) {
            if (this.data.title == '' || this.data.text == '') {
                wx.showToast({
                    title: '信息未填写完整',
                    icon: 'error',
                    duration: 1500
                });
            } else {
                wx.showLoading({
                    mask: true,
                    title: '提交中',
                })
                wx.request({
                    url: app.globalData.url + '/advice/',
                    method: "POST",
                    header: {
                        'content-type': 'application/json; charset=utf-8',
                        'cookie': wx.getStorageSync('cookie')
                    },
                    data: {
                        title: this.data.title,
                        content: this.data.text
                    },
                    success: (res) => {
                        if (res.data.code == 0) {
                            wx.hideLoading();
                            wx.showToast({
                                mask: true,
                                title: '提交成功',
                                icon: 'success',
                                duration: 1500
                            });
                            setTimeout(function () {
                                wx.navigateBack({
                                    delta: 1
                                })
                                let pages = getCurrentPages();
                                let prevPage = pages[pages.length - 2];
                                prevPage.refresh()
                            }, 1500)
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
                        wx.hideLoading();
                        wx.showToast({
                            title: '连接失败',
                            icon: 'error',
                            duration: 1500
                        });
                    }
                })
            }
        } else {
            if (this.data.answer == '') {
                wx.showToast({
                    title: '未填写回复',
                    icon: 'error',
                    duration: 1500
                });
            } else {
                wx.request({
                    url: app.globalData.url + '/advice/' + this.data.id + '/',
                    method: "POST",
                    header: {
                        'content-type': 'application/json; charset=utf-8',
                        'cookie': wx.getStorageSync('cookie')
                    },
                    data: {
                        response: this.data.answer
                    },
                    success: (res) => {
                        if (res.data.code == 0) {
                            wx.hideLoading();
                            wx.showToast({
                                mask: true,
                                title: '审阅成功',
                                icon: 'success',
                                duration: 1500
                            });
                            setTimeout(function () {
                                wx.navigateBack({
                                    delta: 1
                                })
                                let pages = getCurrentPages();
                                let prevPage = pages[pages.length - 2];
                                prevPage.refresh()
                            }, 1500)
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
                        wx.hideLoading();
                        wx.showToast({
                            title: '连接失败',
                            icon: 'error',
                            duration: 1500
                        });
                    }
                })
            }
        }

    }
})