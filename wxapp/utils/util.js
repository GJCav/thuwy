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

//显示错误信息
function show_error(res){
  console.log(res)
  if(res.data!=undefined){
    wx.showToast({
      title: res.data.errmsg,
      mask:true,
      duration: 1500,
      icon:'error'
    })
  } else{
    wx.showToast({
      title: '网络连接失败',
      icon:'error',
      mask:true,
      duration: 1500
    })
  }
  return
}

//获取设备名称,暂时废弃
// const app = getApp()
// function the_name(item_id) {
//   return new Promise(function (resolve, reject) {
//       wx.request({
//           url: app.globalData.url + '/item/' + item_id,
//           method: 'GET',
//           success: (res) => {
//               if (res.data.code == 0) {                       
//                   resolve(res.data.item.name)  
//               } else {
//                   reject(res.data)               
//               }
//           },
//           fail: (res) => {console.log(1) 
//               reject(res)                   
//           }
//       })
//   })
// }

module.exports = {
  show_error:show_error
}
