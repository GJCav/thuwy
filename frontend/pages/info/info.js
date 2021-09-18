// pages/info/info.js
const app = getApp()
Page({
    data: {
        md_info: {},
        title: '',
    },
    onLoad: function (options) {
        let pages = getCurrentPages();
        let prevPage = pages[pages.length - 2];
        let result=app.towxml(`# Markdown`,'markdown',{
            base:'https://static.thuwy.top/image/docs/%E6%9C%AA%E5%A4%AE%E8%AE%BE%E5%A4%87%E5%80%9F%E7%94%A8%E7%AE%A1%E7%90%86%E5%8A%9E%E6%B3%95%282021%E7%89%88%29.md',            
        })
        // prevPage.data.md_intro,
        this.setData({
            md_info:result,
            title: options.title
        })
        wx.setNavigationBarTitle({
            title: this.data.title
        })
    },
})