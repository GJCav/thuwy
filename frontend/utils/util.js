const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return `${[year, month, day].map(formatNumber).join('/')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : `0${n}`
}

//获取设备名称
function the_name(item_id){
   wx.showLoading({
    mask: true,
    title: '加载中',
  })
  wx.request({
    url: app.globalData.url + '/item/' + item_id,
    method: 'GET',
    success: (res) => {
      let those = res.data
      if (those.code == 0) {
          return those.item.name,
        wx.hideLoading()
      } else {
        console.log(res.data.code, res.data.errmsg)
        wx.hideLoading()
        wx.showToast({
          mask: true,
          title: '连接错误',
          icon: 'error',
          duration: 1500
        })
        return '未知物品'
      }
    },
    fail: (res) => {
      console.log(res.data.code, res.data.errmsg)
      wx.hideLoading()
      wx.showToast({
        mask: true,
        title: '连接失败',
        icon: 'error',
        duration: 1500
      })
      return '未知物品'
    }
  })
}

module.exports = {
  the_name:the_name
}
