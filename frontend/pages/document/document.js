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
      title: '下载文件'
    })
  },
  download(e) {
    wx.showLoading({
      title: '下载中',
      mask: true
    })
    console.log(e.currentTarget.dataset.url)
    wx.downloadFile({
      timeout: 15000,
      url: e.currentTarget.dataset.url,
      success(res) {
        if (res.statusCode === 200) {
          wx.hideLoading()
          wx.openDocument({
            filePath: res.tempFilePath,
          })
        } else {
          wx.hideLoading()
          util.show_error(res)
        }
      },
      fail(res) {
        wx.hideLoading()
        util.show_error(res)
      }
    })
  }
})