// pages/document/document.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
  data: {
    document: [{
      name: '学生公寓29号楼活动室借用指南',
      url: 'https://static.thuwy.top/image/2021/08/16/1629094147961_nb3lrm247jgpdku37akcs2wx2wwheixv.jpeg'
    }]
  },
  onLoad: function (options) {
    wx.setNavigationBarTitle({
      title: '预约须知'
    })
  },
  download(e) {
   
  }
})