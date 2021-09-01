// pages/appointment/admit/admit.js
const app = getApp()

Page({
  data: {
    hidden1: true,
    hidden2: true,
    read: false,
    read_text: '+ 借阅物品应按时取用，及时归还\n\n+ 物品损坏需要按相应价格进行赔偿\n\n+ 不得将所借物品转借他人',

    disable: [], //无法预约的时间段
    occupy: [
      [],
      [],
      [],
      [],
      [],
      [],
      []
    ], //每一天被占用的时间段
    cast: ['08:00-12:00', '13:00-17:00', '18:00-23:00', '08:00-23:59'],

    //物品信息相关
    name: '',
    id: 0,
    attr: 0,
    reason: '',
    md_intro: '',
    rsv_method: 3,
    choose_method: 0,
    item_feature: [],

    //时间选择相关
    selected: false,
    select_st: '',
    select_ed: '',
    final_st: '',
    final_ed: '',
    date_index: 0,

    //画图相关
    ctx: null,
    whole_width: 0, //整体宽度
    now_height: 0,
    each_height: 81, //单格高度

    list: [], //已选择的预约时间
    calendar: [], //固定预约日期表
    flex_calendar: [], //自由预约日期表
    items1: [{
        value: '0',
        name: '上午（08：00-12：00）  '
      },
      {
        value: '1',
        name: '下午（13：00-17：00）  '
      },
      {
        value: '2',
        name: '晚上（18：00-23：00）  '
      }
    ],
    items2: [{
      value: '3',
      name: '周末全天    '
    }]
  },
  onLoad: function (options) {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    this.setData({
      id: parseInt(options.id),
      disable: [
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true]
      ],
      item_feature: app.globalData.item_feature
    })
    wx.setNavigationBarTitle({
      title: '提交申请'
    })
    //计算接下来七天的日期
    let that = this;

    function getThisMonthDays(year, month) {
      return new Date(year, month, 0).getDate();
    }
    // 计算每月第一天是星期几
    function getFirstDayOfWeek(year, month) {
      return new Date(Date.UTC(year, month - 1, 1)).getDay();
    }
    const date = new Date();
    const cur_year = date.getFullYear();
    const cur_month = date.getMonth() + 1;
    const cur_date = date.getDate();
    const weeks_ch = ['日', '一', '二', '三', '四', '五', '六'];
    //利用构造函数创建对象
    function calendar(date, week) {
      var y = cur_year;
      var m = cur_month;
      var d = date;
      if (d > monthLength) {
        if (m == 12) {
          y = y + 1;
          m = 1;
          d = d - 31;
        } else {
          y = y;
          m = m + 1;
          d = d - monthLength;
        }
      }
      this.date = String(y) + ((m < 10) ? '-0' : '-') + String(m) + ((d < 10) ? '-0' : '-') + String(d);
      this.week = '星期' + week;
    }
    //当前月份的天数
    var monthLength = getThisMonthDays(cur_year, cur_month)
    //当前月份的第一天是星期几
    var week = getFirstDayOfWeek(cur_year, cur_month)
    var x = week;
    for (var i = 1; i <= monthLength + 8; i++) {
      if (x > 6) {
        x = 0;
      }
      //利用构造函数创建对象
      that.data.calendar[i] = new calendar(i, [weeks_ch[x]][0])
      x++;
    }
    var t = that.data.calendar[cur_date].week
    var flag = that.data.calendar.slice(cur_date, cur_date + 8)
    for (var i = 0; i < 8; ++i) {
      let item = flag[i]
      item.whole = item.date + '（' + item.week + '）'
    }
    that.setData({
      flex_calendar: flag.slice(0, 7),
      calendar: flag.slice((t == '星期六' ? 2 : (t == '星期日') ? 1 : 0), (t == '星期六' ? 2 : (t == '星期日') ? 1 : 0) + (t == '星期六' ? 5 : 7))
    })
    that.getitem().then(function () {
      that.getrsvs().then(function () {
        wx.hideLoading()
      }).catch(function (res) {
        console.log(res)
        wx.showToast({
          title: '信息读取失败',
          icon: 'error',
          duration: 1500
        })
        setTimeout(function () {
          wx.navigateBack({
            delta: 1
          })
        }, 1500)
      })
    }).catch(function (res) {
      console.log(res)
      wx.showToast({
        title: '信息读取失败',
        icon: 'error',
        duration: 1500
      })
      setTimeout(function () {
        wx.navigateBack({
          delta: 1
        })
      }, 1500)
    })
  },
  onPageScroll: function (e) {
    this.setData({
      now_height: e.scrollTop
    })
  },
  //封装接口
  getitem() { //读取物品信息
    let that = this
    return new Promise(function (resolve, reject) {
      wx.request({
        url: app.globalData.url + '/item/' + that.data.id + '/',
        method: 'GET',
        success: (res) => {
          let those = res.data
          if (those.code == 0) {
            that.setData({
              name: those.item.name,
              md_intro: those.item['md-intro'],
              rsv_method: those.item['rsv-method'],
              attr: those.item.attr
            })
            resolve()
          } else {
            reject(res)
          }
        },
        fail: (res) => {
          reject(res)
        }
      })
    })
  },
  getrsvs() { //读取并处理预约信息
    let that = this
    return new Promise(function (resolve, reject) {
      wx.request({
        url: app.globalData.url + '/item/' + that.data.id + '/reservation/',
        method: 'GET',
        success: (res) => {
          //当前时间获取
          const date = new Date();
          const cur_hour = date.getHours()
          const cur_min = date.getMinutes()
          const cur_time = (cur_hour < 10 ? '0' : '') + cur_hour + ':' + (cur_min < 10 ? '0' : '') + cur_min
          if (res.data.code == 0) {
            var tmp = that.data.disable;
            console.log(res.data.rsvs)
            for (var i = 0; i < res.data.rsvs.length; ++i) {
              let the_rsv = res.data.rsvs[i]; //枚举每一个预约i
              if ((the_rsv.state >> 2) % 2 == 1) {
                continue;
              }
              if (the_rsv.method == 1) //处理固定预约信息
              {
                //固定时间段处理
                for (var j = 0; j < that.data.calendar.length; ++j) {
                  let the_date = that.data.calendar[j]; //枚举日期j
                  for (var k = 0; k < the_rsv.interval.length; ++k) {
                    let the_time = the_rsv.interval[k] //枚举具体的预约时间段k
                    if (the_time.slice(0, -2) == the_date.date) {
                      if (the_date.week == '星期六')
                        tmp[j + 1][the_time.slice(-1) - 1] = false;
                      else
                        tmp[j][the_time.slice(-1) - 1] = false
                    }
                  }
                }
                //自由时间段处理
                for (var j = 0; j < that.data.flex_calendar.length; ++j) {
                  let the_date = that.data.flex_calendar[j]; //枚举日期j
                  for (var k = 0; k < the_rsv.interval.length; ++k) {
                    var the_time = the_rsv.interval[k] //枚举具体的预约时间段k
                    if (the_time.slice(0, -2) == the_date.date) {
                      let the_occupy = that.data.occupy[j]
                      var path = 'occupy[' + j + ']'
                      that.setData({
                        [path]: the_occupy.concat(that.data.cast[the_time.slice(-1) - 1])
                      })
                      if (the_date.week == '星期六') {
                        let the_occupys = that.data.occupy[j + 1]
                        var path = 'occupy[' + (j + 1) + ']'
                        that.setData({
                          [path]: the_occupys.concat(that.data.cast[the_time.slice(-1) - 1])
                        })
                      }
                    }
                  }
                }
              } else { //处理自由预约信息
                //固定时间段处理
                for (var j = 0; j < that.data.calendar.length; ++j) {
                  let the_date = that.data.calendar[j]; //枚举日期j
                  let the_time = the_rsv.interval //具体的预约时间段
                  if (the_time.slice(0, -12) == the_date.date) {
                    if (the_date.week == '星期六') {
                      tmp[j + 1][3] = false;
                    } else if (the_date.week == '星期日') {
                      tmp[j][3] = false;
                    } else {
                      var st = the_time.slice(-11, -6)
                      var ed = the_time.slice(-5)
                      if (st < '12:00') tmp[j][0] = false;
                      if ((st >= '13:00' && st < '17:00') || (ed > '13:00' && ed <= '17:00') || (st < '13:00' && ed > '17:00')) tmp[j][1] = false;
                      if ((st >= '18:00' && st < '23:00') || (ed > '18:00' && ed <= '23:00') || (st < '18:00' && ed > '23:00')) tmp[j][2] = false;
                    }
                  }
                }
                //自由时间段处理
                for (var j = 0; j < that.data.flex_calendar.length; ++j) {
                  let the_date = that.data.flex_calendar[j]; //枚举日期j
                  let the_time = the_rsv.interval //具体的预约时间段
                  if (the_time.slice(0, -12) == the_date.date) {
                    let the_occupy = that.data.occupy[j]
                    var path = 'occupy[' + j + ']'
                    that.setData({
                      [path]: the_occupy.concat(the_time.slice(-11))
                    })
                  }
                }
              }
            }
            //今日特殊处理
            //固定时间预约
            if (cur_hour >= 8) tmp[0][0] = false
            if (cur_hour >= 13) tmp[0][1] = false
            if (cur_hour >= 18) tmp[0][2] = false
            that.setData({
              disable: tmp
            })
            //自由时间预约    
            for (var i = 0; i < that.data.flex_calendar.length; ++i) {
              let t = that.data.occupy[i]
              t.sort()
            }
            var cur_obj = ['08:00-' + cur_time]
            var i = 0
            let sq = that.data.occupy[0]
            console.log(sq)
            for (i = 0; i < sq.length; ++i) {
              if (sq[i].slice(0, 5) <= cur_time) {
                if (sq[i].slice(6) > cur_time) {
                  cur_obj = ['08:00-' + sq[i].slice(6)]
                    ++i
                  break
                }
              } else {
                break
              }
            }
            that.setData({
              ['occupy[0]']: cur_obj.concat(sq.splice(i))
            })
            console.log(that.data.occupy)
            resolve()
          } else {
            reject(res)
          }
        },
        fail: (res) => {
          reject(res)
        }
      })
    })
  },
  //输入预约信息
  inputmethod(e) {
    this.setData({
      choose_method: parseInt(e.detail.value)
    });
    if (e.detail.value == 2) this.drawpic();
  },
  //输入预约原因
  inputwhy(e) {
    this.setData({
      reason: e.detail.value
    });
  },
  //固定时间预约
  checkboxChange(e) {
    console.log('选中时间为：', e.detail.value)
    this.selectedIdxs = e.detail.value
  },
  //自由时间预约
  date_change(e) {
    console.log('选择日期为', e.detail.value)
    this.setData({
      date_index: e.detail.value,
      final_st: '',
      final_ed: ''
    })
    this.drawpic();
  },
  //画图形化预约界面
  drawpic() {
    // 通过 SelectorQuery 获取 Canvas 节点
    wx.createSelectorQuery()
      .select('#canvas')
      .fields({
        node: true,
        size: true,
      })
      .exec(this.init.bind(this))
  },
  init(res) { //初始化处理
    //宽高坐标转换
    const width = res[0].width
    const height = res[0].height
    const h = this.data.each_height
    //获取画图实例
    const canvas = res[0].node
    const ctx = canvas.getContext('2d')
    const dpr = wx.getSystemInfoSync().pixelRatio
    canvas.width = width * dpr
    canvas.height = height * dpr
    ctx.scale(dpr, dpr)
    //留着备用
    this.setData({
      ctx: ctx,
      whole_width: width
    })
    //初始属性定义
    ctx.lineWidth = 2 //线宽
    ctx.strokeStyle = '#dddddd' //描边样式
    ctx.textAlign = 'center' //文字横线
    ctx.textBaseline = 'middle' //文字竖向
    ctx.font = '20px SimSun, Songti SC' //文字样式
    //开始画画！
    ctx.clearRect(0, 0, width, height)
    ctx.beginPath()
    //画竖线
    for (var i = 0; i < 3; ++i) {
      ctx.moveTo(width / 4 * i, 0)
      ctx.lineTo(width / 4 * i, height)
      ctx.stroke()
    }
    ctx.moveTo(width, 0)
    ctx.lineTo(width, height)
    ctx.stroke()
    //画横线
    ctx.moveTo(0, 0)
    ctx.lineTo(width, 0)
    ctx.stroke()
    ctx.moveTo(0, 40)
    ctx.lineTo(width, 40)
    ctx.stroke()
    for (var i = 1; i < 16; ++i) {
      var t = 0
      if (i != 5 && i != 10) t = width / 4
      ctx.moveTo(t, i * h + 40)
      ctx.lineTo(width / 2, i * h + 40)
      ctx.stroke()
    }
    ctx.moveTo(0, height)
    ctx.lineTo(width, height)
    ctx.stroke()
    //画横排文字
    for (var i = 8; i < 24; ++i) ctx.fillText((i < 10 ? '0' : '') + i + ':00', width / 8 * 3, h * (i - 8) + 50) //时间显示
    ctx.fillText('时间', width / 8 * 3, 20)
    ctx.fillText('预约情况', width / 4 * 3, 20)
    //画竖排文字
    ctx.font = '20px SimSun, Songti SC' //文字样式
    ctx.textAlign = 'center' //文字横线
    ctx.textBaseline = 'middle' //文字竖向
    ctx.fillText('上', width / 8, 5 * h / 3 + 40)
    ctx.fillText('午', width / 8, 10 * h / 3 + 40)
    ctx.fillText('下', width / 8, 20 * h / 3 + 40)
    ctx.fillText('午', width / 8, 25 * h / 3 + 40)
    ctx.fillText('晚', width / 8, 12 * h + 40)
    ctx.fillText('上', width / 8, 14 * h + 40)
    //画出已经预约的时间段
    let tmp_data = this.data.occupy[this.data.date_index]
    var begin = '08:00'
    for (var i = 0; i < tmp_data.length; ++i) {
      let tmp_time = tmp_data[i]
      if (tmp_time.slice(0, 5) > begin) this.drawRect(2, this.change_time(begin), this.change_time(tmp_time.slice(0, 5)), false)
      this.drawRect(1, this.change_time(tmp_time.slice(0, 5)), this.change_time(tmp_time.slice(6)), true)
      begin = tmp_time.slice(6)
    }
    if (begin < '24:00') this.drawRect(2, this.change_time(begin), this.change_time('23:59'), false)
  },
  //时间转换二部曲
  change_time(t) { //时间转位置
    return ((parseInt(t.slice(0, 2)) - 8) * 60 + parseInt(t.slice(3))) * (this.data.each_height / 60)
  },
  change_position(x) { //位置转时间
    var tmp = parseInt(x * 60 / this.data.each_height)
    var h = parseInt(tmp / 60) + 8
    var m = tmp % 60
    return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m
  },
  //用户点击监控三部曲
  touch_start(e) {
    let that = this
    wx.createSelectorQuery().select('#cover').boundingClientRect(function (rect) {
      let tmp_data = that.data.occupy[that.data.date_index]
      var op = '08:00'
      var touch_y = that.change_position(e.changedTouches[0].pageY - rect.top - that.data.now_height)
      console.log(e.changedTouches[0].pageY - rect.top - that.data.now_height)
      for (var i = 0; i < tmp_data.length; ++i) {
        var st = tmp_data[i].slice(0, 5)
        var ed = tmp_data[i].slice(6)
        if (touch_y >= op && touch_y < st) { //点到可预约的时间段
          if (that.data.select_st != '') {
            let ctx = that.data.ctx
            let width = that.data.whole_width
            var select_st = that.change_time(that.data.select_st)
            var select_ed = that.change_time(that.data.select_ed)
            ctx.clearRect(width / 2, select_st + 40, width / 2, select_ed - select_st)
            that.drawRect(2, select_st, select_ed, false)
          }
          that.setData({
            selected: true,
            select_st: op,
            select_ed: st,
            final_st: touch_y,
            final_ed: touch_y
          })
          return;
        } else if (touch_y >= st && touch_y < ed) {
          wx.showToast({
            title: '时间段无法预约',
            icon: 'error',
            duration: 1500
          });
          return;
        }
        op = ed
      }
      if (op < '24:00') {
        if (that.data.select_st != '') {
          let ctx = that.data.ctx
          let width = that.data.whole_width
          var select_st = that.change_time(that.data.select_st)
          var select_ed = that.change_time(that.data.select_ed)
          ctx.clearRect(width / 2, select_st + 40, width / 2, select_ed - select_st)
          that.drawRect(2, select_st, select_ed, false)
        }
        that.setData({
          selected: true,
          select_st: op,
          select_ed: '23:59',
          final_st: touch_y,
          final_ed: touch_y
        })
      }
    }).exec()
  },
  touch_move(e) {
    if (this.data.selected) {
      let that = this
      wx.createSelectorQuery().select('#cover').boundingClientRect(function (rect) {
        let ctx = that.data.ctx
        let width = that.data.whole_width
        var touch_y = that.change_position(e.changedTouches[0].pageY - rect.top - that.data.now_height)
        var select_st = that.change_time(that.data.select_st)
        var select_ed = that.change_time(that.data.select_ed)
        var final_st = that.change_time(that.data.final_st)
        if (touch_y > that.data.final_st) {
          if (touch_y >= that.data.select_ed) touch_y = that.data.select_ed
          ctx.clearRect(width / 2, select_st + 40, width / 2, select_ed - select_st)
          that.drawRect(2, select_st, select_ed, false)
          that.drawRect(0, final_st, that.change_time(touch_y), (that.change_time(touch_y) - final_st >= that.data.each_height / 6) ? true : false)
          that.setData({
            final_ed: touch_y
          })
        } else {
          that.setData({
            final_ed: that.data.final_st
          })
          ctx.clearRect(width / 2, select_st + 40, width / 2, select_ed - select_st)
          that.drawRect(2, select_st, select_ed, false)
        }
      }).exec()
    }
  },
  touch_end(e) {
    if (this.data.selected && this.data.final_st != this.data.final_ed) {
      wx.showLoading({
        title: '加载中',
        mask:true
      })
      let that = this
      setTimeout(function () {
        that.setData({
          selected: false,
          hidden2: false
        })
        wx.hideLoading()
      }, 300)
    }
  },
  //横线绘制函数,暂时废弃
  // drawLine(position) {
  //   let ctx = this.data.ctx
  //   let width = this.data.whole_width
  //   ctx.beginPath()
  //   ctx.lineWidth = 3 //线宽
  //   ctx.strokeStyle = 'RGBA(0,0,255)' //描边样式
  //   ctx.fillStyle = 'RGBA(0,0,0)' //填充样式
  //   ctx.moveTo(width / 2, 40 + position)
  //   ctx.lineTo(width, 40 + position)
  //   ctx.stroke()
  // },
  //矩形绘制函数
  drawRect(state, st, ed, pan) {
    let ctx = this.data.ctx
    let width = this.data.whole_width
    if(st=='23:59') st='24：00'
    //填充样式
    if (state == 1)
      ctx.fillStyle = 'RGBA(255,0,0,0.5)'
    else if (state == 2)
      ctx.fillStyle = 'RGBA(0,255,0,0.5)'
    else
      ctx.fillStyle = 'RGBA(0,0,255,0.5)'
    //绘制矩形
    var x = parseInt(width / 2)
    ctx.fillRect(x, 40 + st, x, ed - st)
    if (pan) {
      ctx.fillStyle = 'RGBA(255,255,255)' //填充样式
      ctx.font = '14px SimSun, Songti SC' //文字样式
      ctx.textAlign = 'left' //文字横线
      ctx.textBaseline = 'top' //文字竖向
      ctx.fillText(this.change_position(st), x, 40 + st)
      ctx.textAlign = 'right' //文字横线
      ctx.textBaseline = 'bottom' //文字竖向
      ctx.fillText(this.change_position(ed), 2 * x, 40 + ed)
    }
  },
  //最终选定时间
  st_change(e) {
    this.setData({
      final_st: (e.detail.value>=this.data.select_st?e.detail.value:this.data.select_st),
    })
  },
  ed_change(e) {
    this.setData({
      final_ed: (e.detail.value<=this.data.select_ed?e.detail.value:this.data.select_ed),
    })
  },
  time_confirm() {
    var final_st = this.change_time(this.data.final_st)
    var final_ed = this.change_time(this.data.final_ed)
    if (final_ed - final_st >= this.data.each_height / 6) {
      let ctx = this.data.ctx
      let width = this.data.whole_width
      var select_st = this.change_time(this.data.select_st)
      var select_ed = this.change_time(this.data.select_ed)
      ctx.clearRect(width / 2, select_st + 40, width / 2, select_ed - select_st)
      this.drawRect(2, select_st, select_ed, false)
      this.drawRect(0, final_st, final_ed, true)
      this.setData({
        hidden2: true,
      })
    } else {
      wx.showToast({
        title: '至少预约10分钟',
        icon:'error',
        duration:1000,
        mask:true
      })
    }
  },
  //预约须知相关
  read_confirm() {
    this.setData({
      read: true,
      hidden1: true
    })
    this.appoint()
  },
  read_cancel() {
    this.setData({
      hidden1: true
    })
  },
  //提交预约
  appoint: function () {
    this.setData({
      list: []
    });
    //判断信息输入完整
    if (this.data.choose_method == 0) {
      wx.showToast({
        title: '未选择预约方式',
        icon: 'error'
      })
    } else if (this.data.choose_method == 1 && this.selectedIdxs == null) {
      wx.showToast({
        title: '未选择预约时间',
        icon: 'error'
      })
    } else if (this.data.choose_method == 2 && this.data.final_st == '') {
      wx.showToast({
        title: '未选择预约时间',
        icon: 'error',
      })
    } else if (this.data.reason == '') {
      wx.showToast({
        title: '未填写预约理由',
        icon: 'error'
      })
    } else if (!this.data.read) {
      this.setData({
        hidden1: false
      })
    } else {
      wx.showLoading({
        mask: true,
        title: '提交中',
      })
      if (this.data.choose_method == 1) { //固定时间段预约
        this.selectedIdxs.sort()
        for (var i = 0; i < this.selectedIdxs.length; i++) {
          var d = parseInt(this.selectedIdxs[i] / 10)
          var m = parseInt(this.selectedIdxs[i]) % 10 + 1
          if (this.data.calendar[d].week == '星期日')
            d = this.data.calendar[d - 1].date
          else
            d = this.data.calendar[d].date
          var addone = [d + ' ' + m]
          this.setData({
            list: this.data.list.concat(addone)
          });
        }
      } else { //自由时间段预约
        this.setData({
          list: this.data.flex_calendar[this.data.date_index].date + ' ' + this.data.final_st + '-' + this.data.final_ed,
        })
      }
      //测试备用
      // console.log({
      //   'item-id': this.data.id,
      //     reason: this.data.reason,
      //     method: this.data.choose_method,
      //     interval: this.data.list
      // })
      wx.request({
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        url: app.globalData.url + '/reservation/',
        method: 'POST',
        data: {
          'item-id': this.data.id,
          reason: this.data.reason,
          method: this.data.choose_method,
          interval: this.data.list
        },
        success: function (res) {
          console.log(res)
          if (res.data.code == 0) {
            wx.hideLoading()
            wx.showToast({
              title: '提交成功',
              icon: 'success',
              duration: 1500,
              mask: true
            })
            setTimeout(function () {
              wx.navigateBack({
                delta: 1
              })
            }, 1500)
          } else {
            if (res.data.code == 101) {
              wx.hideLoading();
              wx.showToast({
                title: '预约时间冲突',
                icon: 'error',
                mask: true
              })
            }
            if (res.data.code == 102) {
              wx.hideLoading();
              wx.showToast({
                title: '超出可预约时间',
                icon: 'error',
                mask: true
              })
            } else {
              console.log(res)
              wx.hideLoading();
              wx.showToast({
                title: '提交失败',
                icon: 'error'
              })
            }
          }
        },
        fail: function (res) {
          console.log(res)
          wx.hideLoading();
          wx.showToast({
            title: '网络异常',
            icon: 'error'
          });
        }
      })
    }
  },
})