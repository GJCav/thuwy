// appointment.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    sum: 0,
    page: 1,
    items: [],

    userInfo: {},
    hasUserInfo: false,
    canIUseGetUserProfile: false,
    canIUseOpenData: false,

    servers: '',
    loading: true,
    imgUrls: [
      'https://zos.alipayobjects.com/rmsportal/AiyWuByWklrrUDlFignR.png',
      'https://zos.alipayobjects.com/rmsportal/TekJlZRVCjLFexlOCuWn.png',
      'https://zos.alipayobjects.com/rmsportal/IJOtIlfsYdTyaDTRVrLI.png',
    ],
  },

  great() {
    app.globalData.userInfo = true
  },
  bad() {
    app.globalData.userInfo = false
  },
  better() {
    app.globalData.login = true
  },
  worse() {
    app.globalData.login = false
  },
  onReachBottom() {
    if (this.data.page * 20 < this.data.sum) {
      wx.request({
        url: app.globalData.url + '/item?p=<page>/',
        data: {
          p: this.data.page
        },
        method: 'GET',
        success: (res) => {
          console.log('获取成功');
          if (res.data.code == 0) {
            this.setData({
              page: this.data.page + 1,
              sum: res.data['item-count'],
              items: this.data.items.concat(res.data.items)
            })
          } else {
            console.log('读取物品：', res.data.code, res.data.errmsg)
            wx.showToast({
              title: '连接错误',
              icon: 'error',
              duration: 1500
            })
          }
        },
        fail: (res) => {
          console.log(res.data.code, res.data.errmsg)
          wx.showToast({
            title: '连接失败',
            icon: 'error',
            duration: 1500
          });
          stop = true;
        }
      });
    } else {
      wx.showToast({
        title: '没有更多了',
        icon: 'none',
        duration: 1500
      });
    }

  },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
    wx.setNavigationBarTitle({
      title: '预约设备'
    })
    wx.request({
      url: app.globalData.url + '/item?p=<page>/',
      data: {
        p: this.data.page
      },
      method: 'GET',
      success: (res) => {
        console.log('获取成功');
        if (res.data.code == 0) {
          this.setData({
            page: this.data.page + 1,
            sum: res.data['item-count'],
            items: this.data.items.concat(res.data.items)
          })
        } else {
          console.log('读取物品：', res.data.code, res.data.errmsg)
          wx.showToast({
            title: '连接错误',
            icon: 'error',
            duration: 1500
          })
        }
      },
      fail: (res) => {
        console.log(res.data.code, res.data.errmsg)
        wx.showToast({
          title: '连接失败',
          icon: 'error',
          duration: 1500
        });
      }
    });
  },
  chooseMe(e) {
    let value = e.currentTarget.dataset.value
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1000
      });
    } else if (app.globalData.userInfo) {
      wx.navigateTo({
        url: 'admit/admit?id=' + this.data.items[value].id + '&name=' + this.data.items[value].name
      })
    } else {
      wx.showToast({
        title: '未绑定信息',
        icon: 'error',
        duration: 1000
      });
      setTimeout(function () {
        wx.navigateTo({
          url: '../bind/bind'
        })
      }, 1000)
    }
  }
})