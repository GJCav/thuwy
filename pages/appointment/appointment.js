// appointment.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    sum:0,
    items:null,

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
    indicatorDots: true,
    autoplay: true,
    interval: 5000,
    duration: 1000
  },
  great(){
    app.globalData.userInfo=true
  },
  bad(){
    app.globalData.userInfo=false
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
      url: app.globalData.url+'/itemlist?p=1',
      method:'GET',
      success: function (res) {
        console.log('获取成功');
        if(res.code==0)
        {
          this.setData({
            sum:res.item-count,
            items:res.items
          })
        }
        else{
          console.log(res.code,res.errmsg)
        }
      }
    })

  },
  chooseMe(e) {
    if (app.globalData.userInfo) {
      wx.navigateTo({
        url: 'admit/admit?id=' + this.data.items.id+'&name='+this.data.items.name
      })
    } else {
      wx.showToast({
        title: '未绑定信息！',
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