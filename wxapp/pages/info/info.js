// pages/info/info.js
///image/docs/%E6%9C%AA%E5%A4%AE%E8%AE%BE%E5%A4%87%E5%80%9F%E7%94%A8%E7%AE%A1%E7%90%86%E5%8A%9E%E6%B3%95%282021%E7%89%88%29.md
const app = getApp()
Page({
    data: {
        md_info: {},
        info:{
            '未央设备':'# 未央设备借用管理办法(2021版)\n\n一、借用人为设备保管第一责任人，负责设备借取、保管、归还。\n\n二、记签字后领取，并在归还截止时间前归还设备于书院管理中心108未央教务老师或学生工作助理老师处。\n\n三、借用人有在设备借用、使用期间确保仪器不被损坏、丢失的义务和责任，如设备在借用期间被损坏或丢失，需按原价进行赔偿。\n\n四、请在归还前自行将所拍摄内容进行保存。\n\n五、超时借用需确保超时时段设备空闲并提前半天进行预约。\n\n六、如设备超时一天以上未归还且未提前报备说明原因，则一月内禁止该负责人再次借用设备。\n\n\n\n　　本办法自发布之日起实行，最终解释权归未央书院所有。',
            '29号楼':'# 学生公寓29号楼公共活动室借用须知\n\n**活动室预约**\n\n一、预约对象：\n　　29 号楼 5 层会议室、1 层活动室。\n\n二、预约规则： \n　　29 号楼 5 层活动室活动室接受未央书院全体老师、辅导员、同学和学生组织 骨干进行集体活动预约。\n　　活动预约时间自行填写，当活动时间产生冲突时，由未央书院团工委书记朱培豪辅导员视活动重要程度进行协调。 \n　　空闲情况下，同学可进入活动室内自习、休息。预约时间开始后，活动室内其他同学需要让出空间。\n\n三、预约方式： \n　　借用活动室，需要通过微信小程序`微未央`进行预约。不得提前超过一周预约活动。 \n　　如有例行会议需要提前超过一周借用的，需要联系辅导员并获得同意。 \n　　进入小程序后，选择具体使用时间，在`预约理由`处填写借用组织、借用人、联系方式等信息。\n\n\n\n**使用管理办法**\n　　使用 29 号楼活动室时需要自觉遵守以下规定：\n\n一、爱护公共设施。不得毁坏公共空间的设备。严禁将各种设施及物品带离，如有损坏照价赔偿。\n\n\n二、保持环境卫生。不得吸烟，随地吐痰。不得乱丢各种废弃物。不得在活动室中用餐。\n\n\n三、使用活动室时请勿大声喧哗，不得影响周边同学休息和学习。\n\n\n四、活动室使用结束后请将桌椅复原，垃圾带出宿舍楼。\n\n\n五、不得在未报备的情况下允许非本楼同学进入活动室（参考学校住宿管理规定)。\n\n六、遵守《清华大学学生公寓住宿管理办法》的其他相关规定。\n\n\n七、如违反学校安全管理规定，将根据学校有关规定予以处理。同时鼓励同学自觉维护公共空间安全和秩序、发现安全隐患（财产、人生安全等）线索，若查实将予以奖励。\n\n\n\n\n\n未央书院团工委\n2021年9月15日',
        }
    },
    onLoad: function (options) {
        wx.setNavigationBarTitle({
            title: options.title
        })
        if (options.type == '0') {
            let pages = getCurrentPages();
            let prevPage = pages[pages.length - 2];
            let result = app.towxml(prevPage.data.md_intro, 'markdown', {
                base: 'https://static.thuwy.top'
            })
            this.setData({
                md_info: result,
            })
        } else {
            let group=options.type
            console.log(String(group),this.data.info[String(group)])
            let result = app.towxml(this.data.info[String(group)], 'markdown', {
                base: 'https://static.thuwy.top'
            })
            this.setData({
                md_info: result,
            })
        }
    },
})