// pages/document/document.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
  data: {
    document: [{
      name: '学生公寓29号楼活动室借用指南',
      type: '29号楼'
    },{
      name:'未央设备借用管理办法(2021版)',
      type:'未央设备'
    }]
  },
  onLoad: function (options) {
    wx.setNavigationBarTitle({
      title: '预约须知'
    })
  },
  read_it(e) {
    wx.navigateTo({
      url: '../info/info?title=预约须知&type='+e.currentTarget.dataset.type,
    })
  }
})