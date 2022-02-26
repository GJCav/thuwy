<template>
	<view class="col-container" style="align-items: flex-start; padding-bottom: 50rpx; background-color: #fffff9;">
		<weiyang-background style="opacity: 0.4;" />
		<view class="header">
			<!-- 页眉 -->
			<view class="title">
				<!-- 标题 -->
				{{bubbles[0].title}}
			</view>
			<view class="comment-text">
				<!-- 相关信息 -->
				<text style="font-weight: 600; margin-right: 10rpx;">{{bubbles[0].author}}</text>
				<text>{{timeString(bubbles[0].date)}}</text>
			</view>
			<view style="width: calc(100% - 60rpx); height: 0rpx; border: 1rpx solid #CCCCCC; margin-top: 20rpx;">
			</view>
		</view> <!-- .header -->
		<view class="bubbles-container">
			<!-- 所有气泡的容器 -->
			<view
				:class="{'row-container': (bubble.tags.indexOf('#teacher') > -1), 'row-reverse-container':(bubble.tags.indexOf('#teacher') === -1)}"
				style="justify-content: flex-start; align-items: flex-start;width: 100%; padding-right: 50rpx; margin-top: 20rpx; "
				v-for="bubble in bubbles" :key="bubble.id">
				<!-- 每一个发言 -->
				<image class="avatar" :src="avatarurl" />
				<view style="padding-left: 0rpx; flex-grow: 1;">
					<view class="comment-text" style="margin-left: 30rpx;">
						<!-- header -->
						<text style="color: #333; font-weight: 450;">{{bubble.author}}</text>
						<text style="margin-left: 10rpx;">发布于{{timeString(bubble.date)}}</text>
						<!-- <text style="margin-left: 10rpx;">最后更新于{{timeString(bubble.last_modified_at)}}</text> -->
					</view>
					<view
						:class="{'bubble-teacher': (bubble.tags.indexOf('#teacher') > -1), 'bubble-student': (bubble.tags.indexOf('#teacher') === -1)}">
						<!-- content -->
						<text>{{bubble.content.text}}</text>
						<image 
							v-for="url in bubble.content.urls" :src="url" @click="clickImg(url)"
							style="width: 95%;"
							mode="widthFix"
						></image>
					</view>
				</view>
			</view> <!-- .bubble -->
		</view>
	</view>
</template>

<script>
	const app = getApp();
	export default {
		data() {
			return {
				admin: null,
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
						text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras dapibus justo et tortor iaculis, suscipit luctus magna accumsan. Integer aliquet volutpat tellus sit amet imperdiet. Nunc laoreet sem ac diam lacinia, nec volutpat massa tristique.",
						urls: ["https://dev-static.thuwy.top/image/2022/02/26/1645859133490_YhjbzUBU2W74230284f448f64339ec6ecc24d925972f.jpeg",
							""
						],
					},
				}, ],
			};
		},
		computed: {
			timeString() {
				return (dateInt) => {
					let date = new Date(dateInt);
					return `${date.getFullYear()}年${date.getMonth()}月${date.getDate()}日 ${date.getHours()}:${(Array(2).join(0) + date.getMinutes()).slice(-2)}`;
				}
			},
		},
		methods: {
			clickImg(url) {
				wx.previewImage({
					urls: [url], //需要预览的图片http链接列表，多张的时候，url直接写在后面就行了
					current: '', // 当前显示图片的http链接，默认是第一个
					success: function(res) {},
					fail: function(res) {},
					complete: function(res) {},
				})
			},
		},
		onLoad(e) {
			this.admin = e.admin;
			console.log(e.id)
			// 根据e.id获取详细信息
			uni.request({
				header: {
					'content-type': 'application/json; charset=utf-8',
					'cookie': wx.getStorageSync('cookie'),
				},
				url: app.globalData.url.backend + `/issue/${e.id}/`,
				method: 'GET',
			}).then(res => {
				console.log(res);
				this.bubbles = res.data.issues.slice();
			})
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

		flex-shrink: 0;
	}

	.title {
		width: 100%;
		flex-shrink: 0;
		// margin-top: 40rpx;
		// margin-left: 30rpx;

		font-weight: 350;
		font-size: 50rpx;
	}

	.bubbles-container {
		width: 100%;

		margin-top: 10rpx;
		margin-left: 10rpx;
		padding-left: 10rpx;
	}

	.bubble-teacher {
		position: relative;
		margin-left: 30rpx;
		border-radius: 10rpx;

		background: #00aabb;
		color: #FFF;
		padding: 10rpx 10rpx 10rpx 20rpx;

	}

	.bubble-student {
		position: relative;
		margin-right: 30rpx;
		border-radius: 10rpx;

		background: #e9fffe;
		color: #333;
		padding: 10rpx 10rpx 10rpx 20rpx;

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
		border-left-color: #e9fffe;
		border-right: 0;
		border-bottom: 0;
		margin-top: -10rpx;
		margin-right: -20rpx;
	}
</style>
