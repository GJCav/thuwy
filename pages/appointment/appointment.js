// appointment.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    sum: 0,
    items: [{
      name: '英伟达GTX3080',
      id: 1001,
      brief_intro: '￥29999',
      thumbnail: 'https://zos.alipayobjects.com/rmsportal/AiyWuByWklrrUDlFignR.png'
    }],

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
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
    wx.setNavigationBarTitle({
      title: '预约设备'
    })
    var page=1;
    wx.request({
      url: app.globalData.url + '/itemlist?p='+page,
      method: 'GET',
      success: (res)=> {
        console.log('获取成功');
        if (res.code == 0) {
          this.setData({
            sum: res.item_count,
            items: res.items
          })
        } else {
          console.log(res.code, res.errmsg)
          wx.showToast({
            title: '连接错误',
            icon: 'error',
            duration:1500
          })
        }
      },
      fail:(res)=>{
        wx.showToast({
          title: '连接失败',
          icon:'error',
          duration:1500
        })
      }
    })
  },
  chooseMe(e) {
    let value = e.currentTarget.dataset.value
    if (app.globalData.userInfo) {
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