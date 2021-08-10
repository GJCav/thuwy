// pages/admin/admin.js
const app = getApp()
Page({
  data: {
    activeTab: 0
  },
  onLoad: function () {
    wx.setNavigationBarTitle({
      title: '系统管理'
  })
  },
  //处理不同界面的函数
  refresh_rsv:function(){

  },
  refresh_equip:function(){

  },
  refresh_admin:function(){
    
  },
  onPullDownRefresh: function () {
  },
  onReachBottom: function () {
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
      case 2:
        this.setData({
          activeTab: 2
        });
        break;
    }
  },
})