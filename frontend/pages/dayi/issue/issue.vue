<template>
	<view class="col-container" style="align-items: flex-start; padding-bottom: 50rpx; background-color: #fffff9;">
		<weiyang-background style="opacity: 0.4" :distance="{bottom: '100rpx'}" />
		<view class="header">
			<view class="title">{{bubbles[0].title}}</view>
			<!-- 发布时间及标签 -->
			<view class="comment-text">
				<text>发布于{{timeString(bubbles[0].date)}}</text>
			</view>
			<view style="width: calc(100% - 60rpx); height: 0rpx; border: 1rpx solid #CCCCCC; margin-top: 20rpx;">
			</view>
		</view>
		<view class="bubbles-container">
			<!-- 所有气泡的容器 -->
			<view v-for="bubble in bubbles" :key="bubble.id"
				:class="bubble.tags.indexOf('#teacher') > -1?'row-container':'row-reverse-container'"
				style="justify-content: flex-start; align-items: flex-start;padding-right: 50rpx; margin-top: 20rpx; ">
				<!-- 每一个发言 -->
				<image class="avatar" :src="avatarurl" />
				<view class="bubble-class">
					<view class="comment-text" style="margin:0 30rpx;">
						{{timeDistance(bubble.date)}}
						<!-- <text style="margin-left: 10rpx;">最后更新于{{timeString(bubble.last_modified_at)}}</text> -->
					</view>
					<view :class="bubble.tags.indexOf('#teacher')>-1?'bubble-teacher':'bubble-student'">
						<!-- content -->
						<text>{{bubble.content.text}}</text>
						<image v-for="(url,index) in bubble.content.urls" :src="url" :key='index' @click="clickImg(url)"
							style="width:100%;margin:3px 0" mode="widthFix"></image>
					</view>
				</view>
			</view>
		</view>
		<!-- 底部按钮栏 -->
		<view style="height:120rpx;"></view>
		<view class="buttonbar" style="justify-content: space-between;">
			<weiyang-button type="blue" @click="setDetail">
				<view style="margin: 10rpx;">设置</view>
			</weiyang-button>
			<weiyang-button type="green" @click="newAnswer">
				<view style="margin: 10rpx;">回复</view>
			</weiyang-button>
		</view>
	</view>
</template>

<script>
	const app = getApp();
	import utils from '../../../common/utils.js'
	export default {
		data() {
			return {
				admin: false,
				avatarurl: '../../../static/main/setting/avatar.png',
				bubbles: [{
					id: 2,
					title: "Lorem ipsum dolor sit amet, consectetur adipiscing elit?",
					author: "000000",
					date: 1645789960264,
					last_modified_at: 0,
					status: "open",
					visibility: "public",
					tags: ["#teacher", "GPA"],
					reply_to: 1,
					root_id: 1,
					content: {
						text: "Lorem ipsum sxsxs sdedad ddwdsad sd sasdad d",
						urls: ["https://dev-static.thuwy.top/image/2022/02/26/1645859133490_YhjbzUBU2W74230284f448f64339ec6ecc24d925972f.jpeg"],
					},
				}, ],
			};
		},
		computed: {
			timeString() {
				return (dateInt) => {
					let date = new Date(dateInt);
					return `${date.getFullYear()}年${date.getMonth()}月${date.getDate()}日 ${('0' + date.getHours()).slice(-2)}:${('0' + date.getMinutes()).slice(-2)}`;
				}
			},
		},
		methods: {
			// 查看图片详情
			clickImg(url) {
				uni.previewImage({
					urls: [url],
				})
			},
			// 时间距离
			timeDistance(stamp) {
				return utils.changeTime(stamp)
			},
			// 回复消息
			newAnswer() {
				
			}
		},
		onLoad(e) {
			uni.request({
				header: {
					'content-type': 'application/json; charset=utf-8',
					'cookie': wx.getStorageSync('cookie'),
				},
				url: app.globalData.url.backend + `/issue/${e.id}/`,
				method: 'GET',
			}).then(res => {
				console.log(res);
				if (res.data.code == 0) {
					this.bubbles = res.data.issues.slice();
				} else {
					throw res
				}
			}).catch(err => {
				utils.errInfo(err, '网络加载失败')
			})
			this.admin = e.admin;
		},
	}
</script>

<style lang="scss">
	/* 头像框 */
	.avatar {
		width: 100rpx;
		height: 100rpx;
		border: 5rpx solid #660874;
		border-radius: 50%;
		box-sizing: border-box;

		flex-shrink: 0;
	}

	.header {
		width: 100%;
		padding-left: 30rpx;
		padding-top: 20rpx;
	}

	.comment-text {
		margin-top: 10rpx;
		font-size: 25rpx;
		font-weight: 400;
		color: #777777;
	}

	.title {
		width: 100%;
		flex-shrink: 0;
		// margin-top: 40rpx;
		// margin-left: 30rpx;

		font-weight: 600;
		font-size: 50rpx;
	}

	.bubbles-container {
		width: 100%;

		margin-top: 10rpx;
		margin-left: 10rpx;
		padding-left: 10rpx;
	}
	.bubble-class{
		max-width:75%;
		align-items: inherit;
		justify-content:inherit;
	}
	.bubble-teacher {
		position: relative;
		margin-left: 30rpx;
		border-radius: 15rpx;

		background: #112C9A;
		color: #FFF;
		padding: 10rpx 20rpx;

	}

	.bubble-student {
		position: relative;
		margin-right: 30rpx;
		border-radius: 15rpx;

		background: #CEE0EF;
		color: #333;
		padding: 10rpx 20rpx;

	}

	.bubble-teacher:after {
		content: '';
		position: absolute;
		left: 0;
		top: 20rpx;
		width: 0;
		height: 0;
		border: 20rpx solid transparent;
		border-right-color: #112C9A;
		border-left: 0;
		border-bottom: 0;
		margin-top: -10rpx;
		margin-left: -20rpx;
	}

	.bubble-student:after {
		content: '';
		position: absolute;
		right: 0;
		top: 20rpx;
		width: 0;
		height: 0;
		border: 20rpx solid transparent;
		border-left-color: #CEE0EF;
		border-right: 0;
		border-bottom: 0;
		margin-top: -10rpx;
		margin-right: -20rpx;
	}
</style>
