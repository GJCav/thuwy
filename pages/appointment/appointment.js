// appointment.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    

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
  // 事件处理函数
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
    wx.setNavigationBarTitle({
        title: '预约设备'
    })
  },
  chooseMe(e) {
    wx.navigateTo({
        url:'admit/admit'
    })
}
})
