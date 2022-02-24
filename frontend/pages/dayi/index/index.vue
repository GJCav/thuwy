<template>
	<view>
		<uni-nav-bar :fixed="true" color="#333333" leftWidth="50rpx" rightWidth="50rpx" background-color="#F0F0F0">
			<block slot="left">
				<!-- <uni-data-picker v-model="category" :localdata="category_option" placeholder="选择分类"></uni-data-picker> -->
			</block>
			<view class="input-view">
				<uni-icons class="input-uni-icon" type="search" size="18" color="#999" />
				<input confirm-type="search" class="nav-bar-input" type="text" placeholder="输入搜索关键词 , 以空格隔开"
					@confirm="searchRes" />
			</view>
		</uni-nav-bar>
		<view class="col-container">
		<weiyang-card></weiyang-card>	
		</view>
		<uni-fab v-if="admin" :popMenu="false" :pattern="{buttonColor:'#112C9A'}" @fabClick="addNew()"></uni-fab>
	</view>
</template>

<script>
	const app=getApp()
	import utils from '../../../common/utils.js'
	export default {
		data() {
			return {
				admin: false,
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
			brief_data() {
				var res = []
				for (i = 0, len = this.whole_data.length; i < len; i++) {
					let item = this.whole_data[i]
					res.push({
						title: '有关' + item.tags[0] + '的问题',
						theme: '',
						content: item.title,
						info: utils.changeTime(item.date),
						tag: item.status == 'open' ? '待解决' : '已解决'
					})
				}
				return res
			}
		},
		onLoad(e) {
			uni.request({
				header: {
					'content-type': 'application/json; charset=utf-8',
					'cookie': wx.getStorageSync('cookie')
				},
				url: app.globalData.url.backend + '/issue/',
				method: 'GET',
			}).then(res => {
				console.log(res)
				this.whole_data = res.data.issues
			})
			this.admin = e.admin
		},
		methods: {
			searchRes(e) {
				console.log(res)
			},
			addNew() {
				
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
