<template>
	<view>
		<uni-nav-bar :fixed="true" color="#333333" leftWidth="50rpx" rightWidth="50rpx" background-color="#F0F0F0">
			<block slot="left">
				<!-- <uni-data-picker v-model="category" :localdata="category_option" placeholder="选择分类"></uni-data-picker> -->
			</block>
			<view class="input-view">
				<uni-icons class="input-uni-icon" type="search" size="18" color="#999" />
				<input confirm-type="search" v-model="key" class="nav-bar-input" type="text"
					placeholder="输入搜索关键词 , 以空格隔开" @confirm="searchRes" />
			</view>
		</uni-nav-bar>
		<view class="col-container" style="margin-bottom:10px;">
			<weiyang-card v-for="item in whole_data" :key="item.id" :text="item.detail" :pattern="item.pattern"
				:url="issue_url+item.id">
			</weiyang-card>
		</view>
		<uni-fab v-if="admin" :popMenu="false" :pattern="{buttonColor:'#112C9A'}" @fabClick="addNew()"></uni-fab>
		<uni-load-more v-if="whole_data.length>0" :status="load_more"></uni-load-more>
	</view>
</template>

<script>
	const app = getApp()
	import utils from '../../../common/utils.js'
	export default {
		data() {
			return {
				admin: false,
				page: 1,
				key: '',
				load_more: 'more',
				whole_data: []
				// category:'',
				// category_option:[{
				// 	text: "全部答疑",
				// 	value: "全部答疑"
				// }, {
				// 	text: "我的答疑",
				// 	value: "我的答疑"
				// }, {
				// 	text: "精选答疑",
				// 	value: "精选答疑"
				// }, {
				// 	text: "教务发布",
				// 	value: "教务答疑"
				// }]
			}
		},
		computed: {
			issue_url() {
				return '../issue/issue?admin=' + this.admin + '&id='
			},
		},
		onLoad(e) {
			this.admin = e.admin
		},
		onShow() {
			this.refreshDate(1, this.key)
		},
		onPullDownRefresh() {
			this.refreshDate(1, this.key)
		},
		onReachBottom() {
			if (this.load_more != 'noMore') {
				this.load_more = 'loading'
				this.refreshDate(++this.page, this.key)
			}
		},
		methods: {
			// 获取数据
			refreshDate(page, key) {
				uni.showLoading({
					title: '加载中',
					mask: true
				})
				if (page == 1) {
					this.page = 1
					this.whole_data = []
				}
				uni.request({
					header: {
						'content-type': 'application/json; charset=utf-8',
						'cookie': wx.getStorageSync('cookie')
					},
					url: app.globalData.url.backend + '/issue/',
					method: 'GET',
					data: {
						page_num: page,
						keywords: key || ''
					}
				}).then(res => {
					console.log(res)
					if (res.data.code == 0) {
						let raw_data = res.data.issues
						let whole = []
						for (let i = 0, len = raw_data.length; i < len; i++) {
							let item = raw_data[i]
							whole.push({
								id: item.id,
								pattern: item.tags.indexOf('#closed') == -1 ? 21 : 22,
								detail: {
									title: '有关' + item.tags[0] + '的问题',
									theme: '',
									content: item.title,
									info: utils.changeTime(item.date),
									tag: item.tags.indexOf('#closed') == -1 ? '待解决' : '已解决'
								}
							})
						}
						if (whole.length > 0) {
							this.whole_data = this.whole_data.concat(whole)
							this.load_more = 'more'
						} else {
							this.load_more = 'noMore'
						}
						uni.hideLoading()
					} else {
						throw res
					}
				}).catch(err => {
					utils.errInfo(err, '网络加载失败')
				})
			},
			// 进行搜索
			searchRes(e) {
				console.log(this.key)
				this.refreshDate(1, this.key)
			},
			// 转到创建页面
			addNew() {
				uni.navigateTo({
					url: '../info/info?admin=' + this.admin
				})
			}
		}
	}
</script>

<style>
	.input-view {
		display: flex;
		flex-direction: row;
		background-color: #fdfdfd;
		height: 30px;
		border-radius: 15px;
		padding: 0 15px;
		margin: 7px 0;
		line-height: 30px;
	}

	.input-uni-icon {
		line-height: 30px;
	}

	.nav-bar-input {
		height: 30px;
		line-height: 30px;
		width: 430rpx;
		padding: 0 5px;
		font-size: 14px;
		background-color: #fdfdfd;
	}
</style>
